const db = require('../config/database');

class UserRepository {
    constructor(database = db) {
        this.db = database;
    }

    async findById(id) {
        return await this.db.get("SELECT * FROM users WHERE id = ?", [id]);
    }

    async findByEmail(email) {
        return await this.db.get("SELECT id, name, email, pass FROM users WHERE email = ?", [email]);
    }

    async create(name, email, passHash) {
        const result = await this.db.run(
            "INSERT INTO users (name, email, pass) VALUES (?, ?, ?)",
            [name, email, passHash]
        );
        return result.lastID;
    }

    async delete(id) {
        const result = await this.db.run("DELETE FROM users WHERE id = ?", [id]);
        return result.changes;
    }
}

module.exports = UserRepository;
