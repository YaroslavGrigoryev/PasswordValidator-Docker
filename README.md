# PasswordValidator — Docker CI/CD

Учебное домашнее задание № 2. Консольное Java 17-приложение проверяет первую строку stdin и выводит OK или коды ошибок LEN, UPPER, DIGIT, CHAR. Используйте только вымышленные пароли.

## Локальная сборка и проверка

```bash
docker build -t password-validator:local .
printf 'Abcdefg1\n' | docker run --rm -i password-validator:local
printf 'abc\n' | docker run --rm -i password-validator:local
```

Ожидается `OK` в первом случае и `LEN`, `UPPER`, `DIGIT` (отдельными строками) во втором.

## CI/CD

Workflow `.github/workflows/ci-cd.yml` запускается при push в main или вручную. Он собирает локальный образ, выполняет smoke-тесты, авторизуется в GHCR через GITHUB_TOKEN, публикует образы для amd64 и arm64, затем скачивает опубликованный образ и проверяет его. Теги: `latest` и `sha-<полный SHA коммита>`. Dockerfile использует JDK для компиляции и JRE для запуска; исходники и компилятор не копируются в runtime.

## Запуск опубликованного образа

Замените OWNER/REPO на имя своего репозитория в нижнем регистре. Для воспроизводимости вместо latest можно указать тег sha-<SHA> из журнала Actions.

```bash
docker pull ghcr.io/OWNER/REPO:latest
printf 'Abcdefg1\n' | docker run --rm -i ghcr.io/OWNER/REPO:latest
```

Для скачивания без авторизации сделайте пакет публичным в настройках GHCR. Публичность репозитория сама по себе не гарантирует публичность пакета.

## Исходные тесты (необязательно)

При наличии JDK 17+ и Python 3: `python3 tests/run_tests.py`.
