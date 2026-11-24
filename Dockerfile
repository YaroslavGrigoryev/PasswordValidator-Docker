FROM eclipse-temurin:17-jdk AS build
WORKDIR /app
COPY src/PasswordValidator.java ./src/
RUN javac --release 17 -encoding UTF-8 -d out src/PasswordValidator.java

FROM eclipse-temurin:17-jre AS runtime
WORKDIR /app
COPY --from=build /app/out ./out
USER 10001:10001
ENTRYPOINT ["java", "-cp", "out", "PasswordValidator"]
