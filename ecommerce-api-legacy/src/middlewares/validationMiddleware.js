function validateCheckoutPayload(req, res, next) {
    const userName = req.body.usr || req.body.userName;
    const email = req.body.eml || req.body.email;
    const courseId = req.body.c_id || req.body.courseId;
    const cardNumber = req.body.card || req.body.cardNumber;

    if (!userName || !email || !courseId || !cardNumber) {
        return res.status(400).send("Bad Request");
    }

    // Basic email format check
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailRegex.test(email)) {
        return res.status(400).send("Formato de e-mail inválido");
    }

    next();
}

function validateUserIdParam(req, res, next) {
    const { id } = req.params;
    if (!id || isNaN(Number(id))) {
        return res.status(400).send("ID de usuário inválido");
    }
    next();
}

module.exports = {
    validateCheckoutPayload,
    validateUserIdParam
};
