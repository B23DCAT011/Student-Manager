from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_user, logout_user, login_required, current_user
from app.models.user import User
from core.database import db
import datetime

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """Trang đăng nhập"""
    # Nếu đã đăng nhập rồi thì redirect
    if current_user.is_authenticated:
        if current_user.role == 'teacher':
            return redirect(url_for('home.index'))
        else:  # student
            return redirect(url_for('auth.student_portal'))

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        # Validate input
        if not username or not password:
            flash('Vui lòng nhập đầy đủ thông tin!', 'error')
            return render_template('auth/login.html')

        # Tìm user
        user = User.query.filter_by(username=username, is_active=True).first()

        if user and user.check_password(password):
            # Đăng nhập thành công
            login_user(user, remember=True)

            # Cập nhật last_login
            user.last_login = datetime.datetime.utcnow()
            db.session.commit()

            flash(f'Đăng nhập thành công! Chào mừng {user.username}', 'success')

            # Redirect theo role
            if user.role == 'teacher':
                return redirect(url_for('home.index'))
            else:  # student
                return redirect(url_for('auth.student_portal'))
        else:
            flash('Tên đăng nhập hoặc mật khẩu không đúng!', 'error')

    return render_template('auth/login.html')

@auth_bp.route('/logout')
@login_required
def logout():
    """Đăng xuất"""
    username = current_user.username
    logout_user()
    flash(f'Đã đăng xuất thành công! Tạm biệt {username}', 'info')
    return redirect(url_for('auth.login'))

@auth_bp.route('/student-portal')
@login_required
def student_portal():
    """Portal dành cho sinh viên - chỉ xem điểm của mình"""
    if current_user.role != 'student':
        flash('Bạn không có quyền truy cập trang này!', 'error')
        return redirect(url_for('grades.dashboard'))

    try:
        # Import models
        from app.models.grade import Grade
        from app.models.prediction import DiemThanhPhan
        from app.models.student import Student

        # Lấy thông tin sinh viên từ ma_sv trong user
        student = Student.query.filter_by(ma_sv=current_user.ma_sv).first()
        if not student:
            flash('Không tìm thấy thông tin sinh viên!', 'error')
            return redirect(url_for('auth.logout'))

        # Lấy điểm cuối kỳ của sinh viên này
        final_grades = Grade.query.filter_by(ma_sv=current_user.ma_sv).all()

        # Lấy điểm thành phần của sinh viên này
        component_grades = DiemThanhPhan.query.filter_by(ma_sv=current_user.ma_sv).all()

        # Tính thống kê cá nhân
        total_subjects = len(final_grades)
        passed_subjects = sum(1 for grade in final_grades if grade.diem_hp >= 5.0)
        failed_subjects = total_subjects - passed_subjects

        # Tính GPA
        if total_subjects > 0:
            gpa = sum(grade.diem_hp for grade in final_grades) / total_subjects
        else:
            gpa = 0.0
        # Xếp loại học lực
        if gpa >= 8.5:
            rank = "Xuất sắc"
            rank_color = "#28a745"
        elif gpa >= 7.0:
            rank = "Giỏi" 
            rank_color = "#28a745"
        elif gpa >= 5.5:
            rank = "Khá"
            rank_color = "#ffc107"
        elif gpa >= 4.0:
            rank = "Trung bình"
            rank_color = "#ffc107"
        else:
            rank = "Yếu"
            rank_color = "#dc3545"

        data = {
            'student': student,
            'final_grades': final_grades,
            'component_grades': component_grades,
            'total_subjects': total_subjects,
            'passed_subjects': passed_subjects,
            'failed_subjects': failed_subjects,
            'gpa': gpa,
            'rank': rank,
            'rank_color': rank_color
        }

        return render_template('auth/student_portal.html', data=data)

    except Exception as e:
        print(1)
        print(f"Student portal error: {e}")
        flash('Có lỗi xảy ra khi tải thông tin!', 'error')
        return "<h2>🎓 Portal Sinh viên</h2><p>Đang phát triển...</p>"
