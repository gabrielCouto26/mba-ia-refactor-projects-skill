const UserRepository = require('../repositories/userRepository');
const CourseRepository = require('../repositories/courseRepository');
const EnrollmentRepository = require('../repositories/enrollmentRepository');
const PaymentRepository = require('../repositories/paymentRepository');
const AuditLogRepository = require('../repositories/auditLogRepository');
const SecurityService = require('./securityService');
const cacheService = require('./cacheService');
const config = require('../config/env');
const { PAYMENT_STATUS, CARD_RULES } = require('../constants');

class CheckoutService {
    constructor(
        userRepo = new UserRepository(),
        courseRepo = new CourseRepository(),
        enrollmentRepo = new EnrollmentRepository(),
        paymentRepo = new PaymentRepository(),
        auditRepo = new AuditLogRepository()
    ) {
        this.userRepo = userRepo;
        this.courseRepo = courseRepo;
        this.enrollmentRepo = enrollmentRepo;
        this.paymentRepo = paymentRepo;
        this.auditRepo = auditRepo;
    }

    async processCheckout({ userName, email, password, courseId, cardNumber }) {
        // 1. Verify Course exists and is active
        const course = await this.courseRepo.findActiveById(courseId);
        if (!course) {
            const error = new Error("Curso não encontrado");
            error.statusCode = 404;
            throw error;
        }

        // 2. Find or Create User
        let user = await this.userRepo.findByEmail(email);
        let userId;

        if (!user) {
            const passHash = SecurityService.hashPassword(password);
            userId = await this.userRepo.create(userName, email, passHash);
        } else {
            userId = user.id;
        }

        // 3. Payment Processing Gateway Simulation
        console.log(`Processando cartão ${cardNumber} na chave ${config.paymentGatewayKey}`);
        const paymentStatus = cardNumber.startsWith(CARD_RULES.APPROVED_PREFIX)
            ? PAYMENT_STATUS.PAID
            : PAYMENT_STATUS.DENIED;

        if (paymentStatus === PAYMENT_STATUS.DENIED) {
            const error = new Error("Pagamento recusado");
            error.statusCode = 400;
            throw error;
        }

        // 4. Create Enrollment
        const enrollmentId = await this.enrollmentRepo.create(userId, courseId);

        // 5. Save Payment Record
        await this.paymentRepo.create(enrollmentId, course.price, paymentStatus);

        // 6. Audit Logging
        await this.auditRepo.logAction(`Checkout curso ${courseId} por ${userId}`);

        // 7. Cache Logging
        cacheService.set(`last_checkout_${userId}`, course.title);

        return {
            msg: "Sucesso",
            enrollment_id: enrollmentId
        };
    }
}

module.exports = CheckoutService;
