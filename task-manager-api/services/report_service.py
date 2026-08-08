from database import db
from models.task import Task
from models.user import User
from models.category import Category
from exceptions import NotFoundError, ValidationError
from datetime import datetime, timedelta, timezone

class ReportService:
    """Service layer for generating various reports and managing categories."""

    @staticmethod
    def _is_overdue(task: Task) -> bool:
        return task.due_date and task.due_date < datetime.now(timezone.utc) and task.status not in ('done', 'cancelled')

    @staticmethod
    def summary_report():
        total_tasks = Task.query.count()
        total_users = User.query.count()
        total_categories = Category.query.count()

        pending = Task.query.filter_by(status='pending').count()
        in_progress = Task.query.filter_by(status='in_progress').count()
        done = Task.query.filter_by(status='done').count()
        cancelled = Task.query.filter_by(status='cancelled').count()

        priority_counts = {
            'critical': Task.query.filter_by(priority=1).count(),
            'high': Task.query.filter_by(priority=2).count(),
            'medium': Task.query.filter_by(priority=3).count(),
            'low': Task.query.filter_by(priority=4).count(),
            'minimal': Task.query.filter_by(priority=5).count(),
        }

        # Overdue calculations
        all_tasks = Task.query.all()
        overdue_list = []
        for t in all_tasks:
            if ReportService._is_overdue(t):
                overdue_list.append({
                    'id': t.id,
                    'title': t.title,
                    'due_date': str(t.due_date),
                    'days_overdue': (datetime.now(timezone.utc) - t.due_date).days,
                })
        overdue_count = len(overdue_list)

        # Recent activity (last 7 days)
        seven_days_ago = datetime.now(timezone.utc) - timedelta(days=7)
        recent_tasks = Task.query.filter(Task.created_at >= seven_days_ago).count()
        recent_done = Task.query.filter(
            Task.status == 'done',
            Task.updated_at >= seven_days_ago
        ).count()

        # User productivity stats
        user_stats = []
        users = User.query.all()
        for u in users:
            user_tasks = Task.query.filter_by(user_id=u.id).all()
            total = len(user_tasks)
            completed = sum(1 for t in user_tasks if t.status == 'done')
            user_stats.append({
                'user_id': u.id,
                'user_name': u.name,
                'total_tasks': total,
                'completed_tasks': completed,
                'completion_rate': round((completed / total) * 100, 2) if total > 0 else 0,
            })

        return {
            'generated_at': str(datetime.now(timezone.utc)),
            'overview': {
                'total_tasks': total_tasks,
                'total_users': total_users,
                'total_categories': total_categories,
            },
            'tasks_by_status': {
                'pending': pending,
                'in_progress': in_progress,
                'done': done,
                'cancelled': cancelled,
            },
            'tasks_by_priority': priority_counts,
            'overdue': {
                'count': overdue_count,
                'tasks': overdue_list,
            },
            'recent_activity': {
                'tasks_created_last_7_days': recent_tasks,
                'tasks_completed_last_7_days': recent_done,
            },
            'user_productivity': user_stats,
        }

    @staticmethod
    def user_report(user_id: int):
        user = User.query.get(user_id)
        if not user:
            raise NotFoundError('Usuário não encontrado')
        tasks = Task.query.filter_by(user_id=user_id).all()
        total = len(tasks)
        stats = {'done': 0, 'pending': 0, 'in_progress': 0, 'cancelled': 0, 'overdue': 0, 'high_priority': 0}
        for t in tasks:
            if t.status == 'done':
                stats['done'] += 1
            elif t.status == 'pending':
                stats['pending'] += 1
            elif t.status == 'in_progress':
                stats['in_progress'] += 1
            elif t.status == 'cancelled':
                stats['cancelled'] += 1
            if t.priority <= 2:
                stats['high_priority'] += 1
            if ReportService._is_overdue(t):
                stats['overdue'] += 1
        return {
            'user': {
                'id': user.id,
                'name': user.name,
                'email': user.email,
            },
            'statistics': {
                **stats,
                'total_tasks': total,
                'completion_rate': round((stats['done'] / total) * 100, 2) if total > 0 else 0,
            },
        }

    @staticmethod
    def list_categories():
        categories = Category.query.all()
        result = []
        for c in categories:
            cat_data = c.to_dict()
            cat_data['task_count'] = Task.query.filter_by(category_id=c.id).count()
            result.append(cat_data)
        return result

    @staticmethod
    def create_category(data: dict):
        if not data:
            raise ValidationError('Dados inválidos')
        name = data.get('name')
        if not name:
            raise ValidationError('Nome é obrigatório')
        category = Category()
        category.name = name
        category.description = data.get('description', '')
        category.color = data.get('color', '#000000')
        try:
            db.session.add(category)
            db.session.commit()
            return category.to_dict()
        except Exception as e:
            db.session.rollback()
            raise e

    @staticmethod
    def update_category(cat_id: int, data: dict):
        cat = Category.query.get(cat_id)
        if not cat:
            raise NotFoundError('Categoria não encontrada')
        if 'name' in data:
            cat.name = data['name']
        if 'description' in data:
            cat.description = data['description']
        if 'color' in data:
            cat.color = data['color']
        try:
            db.session.commit()
            return cat.to_dict()
        except Exception as e:
            db.session.rollback()
            raise e

    @staticmethod
    def delete_category(cat_id: int):
        cat = Category.query.get(cat_id)
        if not cat:
            raise NotFoundError('Categoria não encontrada')
        try:
            db.session.delete(cat)
            db.session.commit()
            return {'message': 'Categoria deletada'}
        except Exception as e:
            db.session.rollback()
            raise e
