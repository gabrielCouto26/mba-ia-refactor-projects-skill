const express = require('express');
const config = require('./config/env');
const db = require('./config/database');
const routes = require('./routes');
const errorHandler = require('./middlewares/errorHandlerMiddleware');

const app = express();

app.use(express.json());
app.use(routes);
app.use(errorHandler);

// Initialize DB schema & seed data, then start server
db.initDb().then(() => {
    app.listen(config.port, () => {
        console.log(`LMS Refactored API rodando na porta ${config.port}...`);
    });
}).catch(err => {
    console.error("Erro ao inicializar o banco de dados:", err);
});

module.exports = app;
