const express = require('express');
const UserController = require('../controllers/userController');
const { validateUserIdParam } = require('../middlewares/validationMiddleware');

const router = express.Router();
const userController = new UserController();

router.delete('/users/:id', validateUserIdParam, userController.handleDeleteUser);

module.exports = router;
