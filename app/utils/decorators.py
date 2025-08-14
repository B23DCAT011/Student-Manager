# app/utils/decorators.py
from functools import wraps
from flask import redirect, url_for, flash
from flask_login import current_user

def teacher_required(f):
    """
    Decorator để kiểm tra user có role 'teacher' không
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            flash('Vui lòng đăng nhập để truy cập trang này.', 'warning')
            return redirect(url_for('auth.login'))

        if current_user.role != 'teacher':
            flash('Bạn không có quyền truy cập trang này.', 'error')
            return redirect(url_for('auth.student_portal'))

        return f(*args, **kwargs)
    return decorated_function

def student_required(f):
    """
    Decorator để kiểm tra user có role 'student' không
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            flash('Vui lòng đăng nhập để truy cập trang này.', 'warning')
            return redirect(url_for('auth.login'))

        if current_user.role != 'student':
            flash('Bạn không có quyền truy cập trang này.', 'error')
            return redirect(url_for('home.index'))

        return f(*args, **kwargs)
    return decorated_function

def role_required(*roles):
    """
    Decorator linh hoạt để kiểm tra nhiều role khác nhau
    Usage: @role_required('teacher', 'admin')
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.is_authenticated:
                flash('Vui lòng đăng nhập để truy cập trang này.', 'warning')
                return redirect(url_for('auth.login'))

            if current_user.role not in roles:
                flash('Bạn không có quyền truy cập trang này.', 'error')
                if current_user.role == 'student':
                    return redirect(url_for('auth.student_portal'))
                else:
                    return redirect(url_for('home.index'))

            return f(*args, **kwargs)
        return decorated_function
    return decorator