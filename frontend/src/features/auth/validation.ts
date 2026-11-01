export interface Credentials {
    email: string;
    password: string;
}

export interface FieldErrors {
    email?: string;
    password?: string;
}

export const PASSWORD_MIN_LENGTH = 8;
// bcrypt can't handle passwords longer than 72 bytes; the backend enforces the same limit
export const PASSWORD_MAX_BYTES = 72;

const EMAIL_PATTERN = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

function byteLength(value: string): number {
    return new TextEncoder().encode(value).length;
}

function checkEmail(email: string): string | undefined {
    if (!email) return "Enter your email.";
    if (!EMAIL_PATTERN.test(email)) return "Enter a valid email address.";
    return undefined;
}

export function validateSignIn({ email, password }: Credentials): FieldErrors {
    const errors: FieldErrors = {};

    const emailError = checkEmail(email);
    if (emailError) errors.email = emailError;

    if (!password) {
        errors.password = "Enter your password.";
    } else if (byteLength(password) > PASSWORD_MAX_BYTES) {
        errors.password = `Password must be at most ${PASSWORD_MAX_BYTES} bytes long.`;
    }

    return errors;
}

export function validateSignUp({ email, password }: Credentials): FieldErrors {
    const errors: FieldErrors = {};

    const emailError = checkEmail(email);
    if (emailError) errors.email = emailError;

    if (!password) {
        errors.password = "Enter a password.";
    } else if (password.length < PASSWORD_MIN_LENGTH) {
        errors.password = `Password must be at least ${PASSWORD_MIN_LENGTH} characters long.`;
    } else if (byteLength(password) > PASSWORD_MAX_BYTES) {
        errors.password = `Password must be at most ${PASSWORD_MAX_BYTES} bytes long.`;
    }

    return errors;
}