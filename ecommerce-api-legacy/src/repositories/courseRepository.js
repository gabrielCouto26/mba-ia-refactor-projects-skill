const db = require('../config/database');

class CourseRepository {
    constructor(database = db) {
        this.db = database;
    }

    async findActiveById(id) {
        return await this.db.get("SELECT * FROM courses WHERE id = ? AND active = 1", [id]);
    }

    async findAll() {
        return await this.db.all("SELECT * FROM courses");
    }
}

module.exports = CourseRepository;
