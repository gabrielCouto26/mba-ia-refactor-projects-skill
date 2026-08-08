const db = require('../config/database');

class EnrollmentRepository {
    constructor(database = db) {
        this.db = database;
    }

    async create(userId, courseId) {
        const result = await this.db.run(
            "INSERT INTO enrollments (user_id, course_id) VALUES (?, ?)",
            [userId, courseId]
        );
        return result.lastID;
    }

    async deleteByUserId(userId) {
        return await this.db.run("DELETE FROM enrollments WHERE user_id = ?", [userId]);
    }
}

module.exports = EnrollmentRepository;
