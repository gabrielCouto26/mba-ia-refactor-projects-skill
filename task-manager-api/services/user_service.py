from flask import current_app
from database import db
from models.user import User
from exceptions import NotFoundError, ConflictError, UnauthorizedError, ForbiddenError
from itsdangerous import URLSafeTimedSerializer

class UserService:
    @staticmethod
    def get_all_users():
        users = User.query.all()
        result = []
        for u in users:
            d = u.to_dict()
            d['task_count'] = len(u.tasks)
            result.append(d)
        return result

    @staticmethod
    def get_user_by_id(user_id: int):
        user = User.query.get(user_id)
        if not user:
            raise NotFoundError('Usuário não encontrado')
        
        data = user.to_dict()
        data['tasks'] = [t.to_dict() for t in user.tasks]
        return data

    @staticmethod
    def create_user(data: dict):
        existing = User.query.filter_by(email=data['email']).first()
        if existing:
            raise ConflictError('Email já cadastrado')

        user = User(
            name=data['name'],
            email=data['email'],
            role=data.get('role', 'user')
        )
        user.set_password(data['password'])

        try:
            db.session.add(user)
            db.session.commit()
            return user.to_dict()
        except Exception as e:
            db.session.rollback()
            raise e

    @staticmethod
    def update_user(user_id: int, data: dict):
        user = User.query.get(user_id)
        if not user:
            raise NotFoundError('Usuário não encontrado')

        if 'email' in data and data['email'] != user.email:
            existing = User.query.filter_by(email=data['email']).first()
            if existing and existing.id != user_id:
                raise ConflictError('Email já cadastrado')
            user.email = data['email']

        if 'name' in data:
            user.name = data['name']
        if 'password' in data:
            user.set_password(data['password'])
        if 'role' in data:
            user.role = data['role']
        if 'active' in data:
            user.active = data['active']

        try:
            db.session.commit()
            return user.to_dict()
        except Exception as e:
            db.session.rollback()
            raise e

    @staticmethod
    def delete_user(user_id: int):
        user = User.query.get(user_id)
        if not user:
            raise NotFoundError('Usuário não encontrado')

        try:
            db.session.delete(user)
            db.session.commit()
            return {'message': 'Usuário deletado com sucesso'}
        except Exception as e:
            db.session.rollback()
            raise e

    @staticmethod
    def authenticate_user(email: str, password: str):
        user = User.query.filter_by(email=email).first()
        if not user or not user.check_password(password):
            raise UnauthorizedError('Credenciais inválidas')

        if not user.active:
            raise ForbiddenError('Usuário inativo')

        serializer = URLSafeTimedSerializer(current_app.config['JWT_SECRET'])
        token = serializer.dumps({'sub': user.id, 'role': user.role})
        return {
            'message': 'Login realizado com sucesso',
            'user': user.to_dict(),
            'token': token
        }
