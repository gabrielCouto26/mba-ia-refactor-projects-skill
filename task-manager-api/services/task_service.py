from database import db
from models.task import Task
from models.user import User
from models.category import Category
from exceptions import NotFoundError, ValidationError
from sqlalchemy.orm import joinedload
from datetime import datetime, timezone

class TaskService:
    @staticmethod
    def get_all_tasks():
        # Optimization: Use joinedload to avoid N+1 queries
        tasks = Task.query.options(
            joinedload(Task.user),
            joinedload(Task.category)
        ).all()
        return [t.to_dict() for t in tasks]

    @staticmethod
    def get_task_by_id(task_id: int):
        task = Task.query.options(
            joinedload(Task.user),
            joinedload(Task.category)
        ).filter(Task.id == task_id).first()
        
        if not task:
            raise NotFoundError('Task não encontrada')
        return task.to_dict()

    @staticmethod
    def create_task(data: dict):
        user_id = data.get('user_id')
        if user_id:
            user = User.query.get(user_id)
            if not user:
                raise NotFoundError('Usuário não encontrado')

        category_id = data.get('category_id')
        if category_id:
            category = Category.query.get(category_id)
            if not category:
                raise NotFoundError('Categoria não encontrada')

        task = Task(
            title=data['title'],
            description=data.get('description', ''),
            status=data.get('status', 'pending'),
            priority=data.get('priority', 3),
            user_id=user_id,
            category_id=category_id,
            due_date=data.get('due_date'),
            tags=data.get('tags')
        )

        try:
            db.session.add(task)
            db.session.commit()
            return task.to_dict()
        except Exception as e:
            db.session.rollback()
            raise e

    @staticmethod
    def update_task(task_id: int, data: dict):
        task = Task.query.get(task_id)
        if not task:
            raise NotFoundError('Task não encontrada')

        if 'user_id' in data and data['user_id']:
            if not User.query.get(data['user_id']):
                raise NotFoundError('Usuário não encontrado')
            task.user_id = data['user_id']
        elif 'user_id' in data:
            task.user_id = None

        if 'category_id' in data and data['category_id']:
            if not Category.query.get(data['category_id']):
                raise NotFoundError('Categoria não encontrada')
            task.category_id = data['category_id']
        elif 'category_id' in data:
            task.category_id = None

        if 'title' in data:
            task.title = data['title']
        if 'description' in data:
            task.description = data['description']
        if 'status' in data:
            task.status = data['status']
        if 'priority' in data:
            task.priority = data['priority']
        if 'due_date' in data:
            task.due_date = data['due_date']
        if 'tags' in data:
            task.tags = data['tags']

        task.updated_at = datetime.now(timezone.utc)

        try:
            db.session.commit()
            return task.to_dict()
        except Exception as e:
            db.session.rollback()
            raise e

    @staticmethod
    def delete_task(task_id: int):
        task = Task.query.get(task_id)
        if not task:
            raise NotFoundError('Task não encontrada')

        try:
            db.session.delete(task)
            db.session.commit()
            return {'message': 'Task deletada com sucesso'}
        except Exception as e:
            db.session.rollback()
            raise e

    @staticmethod
    def search_tasks(query: str = '', status: str = '', priority: int = None, user_id: int = None):
        tasks_query = Task.query.options(
            joinedload(Task.user),
            joinedload(Task.category)
        )

        if query:
            tasks_query = tasks_query.filter(
                db.or_(
                    Task.title.like(f'%{query}%'),
                    Task.description.like(f'%{query}%')
                )
            )
        if status:
            tasks_query = tasks_query.filter(Task.status == status)
        if priority is not None:
            tasks_query = tasks_query.filter(Task.priority == priority)
        if user_id is not None:
            tasks_query = tasks_query.filter(Task.user_id == user_id)

        results = tasks_query.all()
        return [t.to_dict() for t in results]

    @staticmethod
    def get_task_stats():
        total = Task.query.count()
        pending = Task.query.filter_by(status='pending').count()
        in_progress = Task.query.filter_by(status='in_progress').count()
        done = Task.query.filter_by(status='done').count()
        cancelled = Task.query.filter_by(status='cancelled').count()

        all_tasks = Task.query.all()
        overdue_count = sum(1 for t in all_tasks if t.is_overdue())

        return {
            'total': total,
            'pending': pending,
            'in_progress': in_progress,
            'done': done,
            'cancelled': cancelled,
            'overdue': overdue_count,
            'completion_rate': round((done / total) * 100, 2) if total > 0 else 0
        }
