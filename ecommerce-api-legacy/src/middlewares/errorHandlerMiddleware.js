function errorHandler(err, req, res, next) {
    console.error(`[ERROR] ${err.stack || err.message}`);

    const statusCode = err.statusCode || 500;
    const message = err.message || "Erro interno no servidor";

    return res.status(statusCode).send(message);
}

module.exports = errorHandler;
