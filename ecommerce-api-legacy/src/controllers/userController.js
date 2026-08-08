const UserService = require('../services/userService');

class UserController {
    constructor(userService = new UserService()) {
        this.userService = userService;
    }

    handleDeleteUser = async (req, res, next) => {
        try {
            const { id } = req.params;
            const result = await this.userService.deleteUser(id);
            return res.status(200).send(result.message);
        } catch (err) {
            next(err);
        }
    };
}

module.exports = UserController;
