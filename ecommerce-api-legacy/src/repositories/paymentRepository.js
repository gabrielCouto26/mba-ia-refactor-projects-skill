const db = require('../config/database');

class PaymentRepository {
    constructor(database = db) {
        this.db = database;
    }

    async create(enrollmentId, amount, status) {
        const result = await this.db.run(
            "INSERT INTO payments (enrollment_id, amount, status) VALUES (?, ?, ?)",
            [enrollmentId, amount, status]
        );
        return result.lastID;
    }

    /**
     * Solves N+1 Problem:
     * Fetches courses, enrollments, users, and payment statuses in a single optimized SQL query.
     */
    async getFinancialReportData() {
        const sql = `
            SELECT 
                c.id AS course_id,
                c.title AS course_title,
                u.name AS student_name,
                p.amount AS payment_amount,
                p.status AS payment_status
            FROM courses c
            LEFT JOIN enrollments e ON e.course_id = c.id
            LEFT JOIN users u ON u.id = e.user_id
            LEFT JOIN payments p ON p.enrollment_id = e.id
            ORDER BY c.id;
        `;
        return await this.db.all(sql);
    }
}

module.exports = PaymentRepository;
