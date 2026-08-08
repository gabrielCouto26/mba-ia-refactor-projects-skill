const sqlite3 = require('sqlite3').verbose();

class Database {
    constructor(dbPath = ':memory:') {
        this.db = new sqlite3.Database(dbPath);
    }

    run(sql, params = []) {
        return new Promise((resolve, reject) => {
            this.db.run(sql, params, function(err) {
                if (err) return reject(err);
                resolve({ lastID: this.lastID, changes: this.changes });
            });
        });
    }

    get(sql, params = []) {
        return new Promise((resolve, reject) => {
            this.db.get(sql, params, (err, row) => {
                if (err) return reject(err);
                resolve(row);
            });
        });
    }

    all(sql, params = []) {
        return new Promise((resolve, reject) => {
            this.db.all(sql, params, (err, rows) => {
                if (err) return reject(err);
                resolve(rows);
            });
        });
    }

    async initDb() {
        await this.run("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, email TEXT, pass TEXT)");
        await this.run("CREATE TABLE IF NOT EXISTS courses (id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT, price REAL, active INTEGER)");
        await this.run("CREATE TABLE IF NOT EXISTS enrollments (id INTEGER PRIMARY KEY AUTOINCREMENT, user_id INTEGER, course_id INTEGER)");
        await this.run("CREATE TABLE IF NOT EXISTS payments (id INTEGER PRIMARY KEY AUTOINCREMENT, enrollment_id INTEGER, amount REAL, status TEXT)");
        await this.run("CREATE TABLE IF NOT EXISTS audit_logs (id INTEGER PRIMARY KEY AUTOINCREMENT, action TEXT, created_at DATETIME)");
        
        // Seed initial data if tables are empty
        const userCount = await this.get("SELECT COUNT(*) as count FROM users");
        if (userCount && userCount.count === 0) {
            await this.run("INSERT INTO users (name, email, pass) VALUES ('Leonan', 'leonan@fullcycle.com.br', '123')");
            await this.run("INSERT INTO courses (title, price, active) VALUES ('Clean Architecture', 997.00, 1), ('Docker', 497.00, 1)");
            await this.run("INSERT INTO enrollments (user_id, course_id) VALUES (1, 1)");
            await this.run("INSERT INTO payments (enrollment_id, amount, status) VALUES (1, 997.00, 'PAID')");
        }
    }
}

const dbInstance = new Database();

module.exports = dbInstance;
