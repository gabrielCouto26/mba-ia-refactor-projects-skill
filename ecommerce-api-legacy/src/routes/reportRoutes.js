const express = require('express');
const ReportController = require('../controllers/reportController');

const router = express.Router();
const reportController = new ReportController();

router.get('/admin/financial-report', reportController.handleFinancialReport);

module.exports = router;
