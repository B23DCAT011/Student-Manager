# core/database.py - Database initialization
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

# Initialize extensions
db = SQLAlchemy()
login_manager = LoginManager()

def init_app(app):
    """Initialize database and login manager with Flask app"""

    # Initialize SQLAlchemy
    db.init_app(app)

    # Initialize Flask-Login
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Vui lòng đăng nhập để truy cập trang này.'
    login_manager.login_message_category = 'info'

    # User loader for Flask-Login
    @login_manager.user_loader
    def load_user(user_id):
        from app.models.user import User
        return User.query.get(int(user_id))

    # Import all models to register them with SQLAlchemy
    from app.models.user import User
    from app.models.student import Student
    from app.models.teacher import Teacher
    from app.models.academic import Khoa, Nganh, Lop, HocPhan
    from app.models.grade import Grade
    from app.models.prediction import DiemThanhPhan, SinhVienStats
    from app.models.grade import Grade
    from app.models.academic import Khoa, Nganh, Lop, HocPhan

    print("✅ Database models loaded successfully!")

def create_tables(app):
    """Create all database tables"""
    with app.app_context():
        try:
            db.create_all()
            print("✅ Database tables created successfully!")
        except Exception as e:
            print(f"❌ Error creating tables: {e}")

def drop_tables(app):
    """Drop all database tables (use with caution!)"""
    with app.app_context():
        try:
            db.drop_all()
            print("⚠️ All database tables dropped!")
        except Exception as e:
            print(f"❌ Error dropping tables: {e}")
