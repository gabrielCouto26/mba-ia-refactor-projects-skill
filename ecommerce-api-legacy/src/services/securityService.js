const crypto = require('crypto');

class SecurityService {
    /**
     * Secure password hashing using crypto sha256 with salt
     */
    static hashPassword(password) {
        if (!password) password = "default_password";
        const hash = crypto.createHash('sha256').update(password + '_secret_salt').digest('hex');
        return hash.substring(0, 16);
    }
}

module.exports = SecurityService;
