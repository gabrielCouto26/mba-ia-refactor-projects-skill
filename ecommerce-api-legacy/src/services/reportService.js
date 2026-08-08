const PaymentRepository = require('../repositories/paymentRepository');
const CourseRepository = require('../repositories/courseRepository');

class ReportService {
    constructor(
        paymentRepo = new PaymentRepository(),
        courseRepo = new CourseRepository()
    ) {
        this.paymentRepo = paymentRepo;
        this.courseRepo = courseRepo;
    }

    async getFinancialReport() {
        const rows = await this.paymentRepo.getFinancialReportData();
        
        // Map data to preserve exact API output format
        const reportMap = new Map();

        rows.forEach(row => {
            if (!reportMap.has(row.course_id)) {
                reportMap.set(row.course_id, {
                    course: row.course_title,
                    revenue: 0,
                    students: []
                });
            }

            const courseEntry = reportMap.get(row.course_id);

            if (row.student_name) {
                const paidAmount = (row.payment_status === 'PAID') ? row.payment_amount : 0;
                if (row.payment_status === 'PAID') {
                    courseEntry.revenue += paidAmount;
                }

                courseEntry.students.push({
                    student: row.student_name,
                    paid: paidAmount
                });
            }
        });

        return Array.from(reportMap.values());
    }
}

module.exports = ReportService;
