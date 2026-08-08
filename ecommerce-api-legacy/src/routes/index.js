const express = require('express');
const checkoutRoutes = require('./checkoutRoutes');
const reportRoutes = require('./reportRoutes');
const userRoutes = require('./userRoutes');

const router = express.Router();

router.use('/api', checkoutRoutes);
router.use('/api', reportRoutes);
router.use('/api', userRoutes);

module.exports = router;
