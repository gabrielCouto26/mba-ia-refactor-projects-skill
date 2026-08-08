const ReportService = require('../services/reportService');

class ReportController {
    constructor(reportService = new ReportService()) {
        this.reportService = reportService;
    }

    handleFinancialReport = async (req, res, next) => {
        try {
            const report = await this.reportService.getFinancialReport();
            return res.status(200).json(report);
        } catch (err) {
            next(err);
        }
    };
}

module.exports = ReportController;
