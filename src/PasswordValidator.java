import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.nio.charset.StandardCharsets;
import java.util.ArrayList;
import java.util.List;

/**
 * Educational ASCII-only password validator.
 * Reads only the first input line and prints OK or validation error codes.
 */
public final class PasswordValidator {
    private static final int MIN_LENGTH = 8;
    private static final int MAX_LENGTH = 16;

    private PasswordValidator() {
        // Utility class: no instances.
    }

    public static void main(String[] args) throws IOException {
        BufferedReader reader = new BufferedReader(
                new InputStreamReader(System.in, StandardCharsets.UTF_8));
        String password = reader.readLine();
        if (password == null) {
            password = "";
        }

        List<String> errors = validate(password);
        if (errors.isEmpty()) {
            System.out.println("OK");
        } else {
            for (String error : errors) {
                System.out.println(error);
            }
        }
    }

    static List<String> validate(String password) {
        boolean hasUppercase = false;
        boolean hasDigit = false;
        boolean validCharacters = true;

        for (int i = 0; i < password.length(); i++) {
            char character = password.charAt(i);
            if (character >= 'A' && character <= 'Z') {
                hasUppercase = true;
            } else if (character >= '0' && character <= '9') {
                hasDigit = true;
            } else if (!(character >= 'a' && character <= 'z')) {
                validCharacters = false;
            }
        }

        List<String> errors = new ArrayList<>();
        if (password.length() < MIN_LENGTH || password.length() > MAX_LENGTH) {
            errors.add("LEN");
        }
        if (!hasUppercase) {
            errors.add("UPPER");
        }
        if (!hasDigit) {
            errors.add("DIGIT");
        }
        if (!validCharacters) {
            errors.add("CHAR");
        }
        return errors;
    }
}
