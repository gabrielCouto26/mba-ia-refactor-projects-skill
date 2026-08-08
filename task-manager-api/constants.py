from enum import Enum

class UserRole(str, Enum):
    USER = 'user'
    ADMIN = 'admin'
    MANAGER = 'manager'

class TaskStatus(str, Enum):
    PENDING = 'pending'
    IN_PROGRESS = 'in_progress'
    DONE = 'done'
    CANCELLED = 'cancelled'

class TaskPriority(int, Enum):
    CRITICAL = 1
    HIGH = 2
    MEDIUM = 3
    LOW = 4
    MINIMAL = 5

DEFAULT_COLOR = '#000000'
MIN_PASSWORD_LENGTH = 4
MIN_TITLE_LENGTH = 3
MAX_TITLE_LENGTH = 200
