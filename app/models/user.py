# app/models/user.py
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from core.database import db

class User(UserMixin, db.Model):
    """Model cho bảng TAIKHOAN"""
    __tablename__ = 'taikhoan'

    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    role = db.Column(db.Enum('student', 'teacher'), nullable=False)
    ma_sv = db.Column(db.String(10), db.ForeignKey('sinhvien.ma_sv'), nullable=True)
    ma_gv = db.Column(db.String(10), db.ForeignKey('giaovien.ma_gv'), nullable=True)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    last_login = db.Column(db.DateTime, nullable=True)

    def set_password(self, password):
        """Hash và lưu password"""
        self.password = generate_password_hash(password)

    def check_password(self, password):
        """Kiểm tra password"""
        return check_password_hash(self.password, password)

    def get_id(self):
        """Required by Flask-Login"""
        return str(self.user_id)
