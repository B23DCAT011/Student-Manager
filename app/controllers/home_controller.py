from flask import Blueprint, render_template
from app.models.student import Student
from app.models.teacher import Teacher
from app.models.grade import Grade
from app.models.academic import HocPhan, Khoa, Nganh, Lop
from app.utils.decorators import teacher_required,role_required

home_bp = Blueprint('home', __name__)

@home_bp.route('/home')
@teacher_required
def index():
    """Trang chủ với thống kê tổng quan"""
    try:
        # Đếm số lượng từng loại
        student_count = Student.query.count()
        teacher_count = Teacher.query.count()
        lop_count = Lop.query.count()
        hocphan_count = HocPhan.query.count()

        return render_template('home.html',
                             student_count=student_count,
                             teacher_count=teacher_count,
                             lop_count=lop_count,
                             hocphan_count=hocphan_count)
    except Exception as e:
        return render_template('home.html',
                             student_count=0,
                             teacher_count=0,
                             lop_count=0,
                             hocphan_count=0)
