const CheckoutService = require('../services/checkoutService');

class CheckoutController {
    constructor(checkoutService = new CheckoutService()) {
        this.checkoutService = checkoutService;
    }

    handleCheckout = async (req, res, next) => {
        try {
            // Support legacy payload fields (usr, eml, pwd, c_id, card) and clean payload fields
            const userName = req.body.usr || req.body.userName;
            const email = req.body.eml || req.body.email;
            const password = req.body.pwd || req.body.password;
            const courseId = req.body.c_id || req.body.courseId;
            const cardNumber = req.body.card || req.body.cardNumber;

            const result = await this.checkoutService.processCheckout({
                userName,
                email,
                password,
                courseId,
                cardNumber
            });

            return res.status(200).json(result);
        } catch (err) {
            next(err);
        }
    };
}

module.exports = CheckoutController;
