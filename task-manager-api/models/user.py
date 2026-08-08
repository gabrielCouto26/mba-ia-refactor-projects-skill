from database import db
from datetime import datetime, timezone
from werkzeug.security import generate_password_hash, check_password_hash
import hashlib
from constants import UserRole

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(50), default=UserRole.USER.value)
    active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    def to_dict(self, include_sensitive=False):
        data = {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'role': self.role,
            'active': self.active,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
        if include_sensitive:
            data['password'] = self.password
        return data

    def set_password(self, pwd: str):
        self.password = generate_password_hash(pwd)

    def check_password(self, pwd: str) -> bool:
        # Check modern pbkdf2 / scrypt werkzeug hash
        if self.password and (self.password.startswith('pbkdf2:') or self.password.startswith('scrypt:')):
            return check_password_hash(self.password, pwd)
        
        # Legacy fallback for MD5 hash, and auto-upgrade
        md5_hash = hashlib.md5(pwd.encode()).hexdigest()
        if self.password == md5_hash:
            self.set_password(pwd)
            db.session.commit()
            return True
        return False

    def is_admin(self) -> bool:
        return self.role == UserRole.ADMIN.value
