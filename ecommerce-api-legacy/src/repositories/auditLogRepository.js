const db = require('../config/database');

class AuditLogRepository {
    constructor(database = db) {
        this.db = database;
    }

    async logAction(action) {
        return await this.db.run(
            "INSERT INTO audit_logs (action, created_at) VALUES (?, datetime('now'))",
            [action]
        );
    }
}

module.exports = AuditLogRepository;
