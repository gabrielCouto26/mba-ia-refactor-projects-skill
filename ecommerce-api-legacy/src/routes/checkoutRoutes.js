const express = require('express');
const CheckoutController = require('../controllers/checkoutController');
const { validateCheckoutPayload } = require('../middlewares/validationMiddleware');

const router = express.Router();
const checkoutController = new CheckoutController();

router.post('/checkout', validateCheckoutPayload, checkoutController.handleCheckout);

module.exports = router;
