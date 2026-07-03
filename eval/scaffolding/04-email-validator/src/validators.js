/**
 * Email validation utility.
 * Returns true if the email matches a basic RFC-like pattern.
 */
export function validateEmail(email) {
  if (typeof email !== 'string' || email.trim().length === 0) {
    return false;
  }
  const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  return re.test(String(email).toLowerCase());
}

/**
 * Password strength validation.
 * Requires: 8+ chars, at least one uppercase, one lowercase, one digit.
 */
export function validatePassword(password) {
  if (typeof password !== 'string') return false;
  return (
    password.length >= 8 &&
    /[A-Z]/.test(password) &&
    /[a-z]/.test(password) &&
    /[0-9]/.test(password)
  );
}

export default { validateEmail, validatePassword };
