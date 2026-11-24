#!/usr/bin/env python3
"""Run reproducible black-box tests against the Java 17-compatible program.

Python is only the test runner; the deliverable program uses Java stdlib only.
"""
import argparse
import datetime as dt
import json
import platform
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def command_output(command, **kwargs):
    return subprocess.run(command, text=True, encoding="utf-8", capture_output=True, **kwargs)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path, default=ROOT / "src" / "PasswordValidator.java")
    parser.add_argument("--log", type=Path, default=ROOT / "evidence" / "final_test_run.txt")
    parser.add_argument("--json", type=Path, default=None)
    args = parser.parse_args()
    source = args.source.resolve()
    workdir = args.log.parent / ("_classes_broken" if "intentional_defect" in str(source) else "_classes_final")
    workdir.mkdir(parents=True, exist_ok=True)
    args.log.parent.mkdir(parents=True, exist_ok=True)
    cases = json.loads((ROOT / "tests" / "cases.json").read_text(encoding="utf-8"))
    compile_cmd = ["javac", "--release", "17", "-encoding", "UTF-8", "-d", str(workdir), str(source)]
    build = command_output(compile_cmd)
    if build.returncode != 0:
        print(build.stdout + build.stderr, file=sys.stderr)
        return 2
    logs = [
        "Timestamp UTC: " + dt.datetime.now(dt.timezone.utc).isoformat(),
        "System: " + platform.platform(),
        "Java: " + command_output(["java", "-version"]).stderr.strip().replace("\n", " | "),
        "Compiler: " + command_output(["javac", "-version"]).stdout.strip(),
        "Compiled with: javac --release 17 -encoding UTF-8 -d <classes> " + str(source),
        "Source: " + str(source),
        "Run command: java -cp <classes> PasswordValidator",
        "----------------------",
    ]
    result_rows = []
    for case in cases:
        proc = command_output(["java", "-cp", str(workdir), "PasswordValidator"], input=case["input"], timeout=10)
        actual = proc.stdout.splitlines()
        expected = case["expected"]
        passed = proc.returncode == 0 and actual == expected and proc.stderr == ""
        result_rows.append({"id": case["id"], "description": case["description"],
                            "expected": expected, "actual": actual, "passed": passed,
                            "returncode": proc.returncode, "stderr": proc.stderr})
        logs.extend([
            f'{case["id"]} {"PASS" if passed else "FAIL"} | {case["description"]}',
            '  input repr: ' + repr(case['input']),
            '  expected: ' + repr(expected),
            '  actual:   ' + repr(actual),
            '  return code: ' + str(proc.returncode),
        ])
    passed_count = sum(x["passed"] for x in result_rows)
    logs.append("----------------------")
    logs.append(f"TOTAL: {passed_count}/{len(cases)} passed, {len(cases) - passed_count} failed")
    args.log.write_text("\n".join(logs) + "\n", encoding="utf-8")
    if args.json:
        args.json.write_text(json.dumps({"passed": passed_count, "total": len(cases),
                                         "source": str(source), "cases": result_rows},
                                        ensure_ascii=False, indent=2), encoding="utf-8")
    print("\n".join(logs))
    return 0 if passed_count == len(cases) else 1


if __name__ == "__main__":
    sys.exit(main())
