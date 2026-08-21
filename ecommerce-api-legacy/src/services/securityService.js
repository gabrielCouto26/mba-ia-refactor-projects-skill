const crypto = require('crypto');

class SecurityService {
    /**
    * Password hashing using a random salt and the native scrypt implementation.
     */
    static hashPassword(password) {
        if (typeof password !== 'string' || password.length < 12) {
            throw new Error("Password must contain at least 12 characters");
        }
        const salt = crypto.randomBytes(16).toString('hex');
        const hash = crypto.scryptSync(password, salt, 64).toString('hex');
        return `scrypt:${salt}:${hash}`;
    }
}

module.exports = SecurityService;
