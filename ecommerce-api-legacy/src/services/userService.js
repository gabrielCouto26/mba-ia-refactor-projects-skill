const UserRepository = require('../repositories/userRepository');
const EnrollmentRepository = require('../repositories/enrollmentRepository');

class UserService {
    constructor(
        userRepo = new UserRepository(),
        enrollmentRepo = new EnrollmentRepository()
    ) {
        this.userRepo = userRepo;
        this.enrollmentRepo = enrollmentRepo;
    }

    async deleteUser(id) {
        const user = await this.userRepo.findById(id);
        if (!user) {
            const error = new Error("Usuário não encontrado");
            error.statusCode = 404;
            throw error;
        }

        // Clean up enrollments associated with the user
        await this.enrollmentRepo.deleteByUserId(id);
        await this.userRepo.delete(id);

        return { message: "Usuário e matrículas associadas deletados com sucesso." };
    }
}

module.exports = UserService;
