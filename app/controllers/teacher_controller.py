from flask import Blueprint, render_template, request, jsonify, redirect, url_for
from app.models.teacher import Teacher
from core.database import db
from app.utils.decorators import teacher_required

teacher_bp = Blueprint('teacher', __name__)

@teacher_bp.route('/teachers')
@teacher_required
def list_teachers():
    """Hiển thị danh sách giáo viên (JSON API)"""
    try:
        teachers = Teacher.query.all()
        return jsonify({
            'success': True,
            'count': len(teachers),
            'teachers': [
                {
                    'ma_gv': teacher.ma_gv,
                    'ho_ten': teacher.ho_ten,
                    'email': teacher.email,
                    'so_dt': teacher.so_dt,
                    'gioi_tinh': teacher.gioi_tinh,
                    'ngay_sinh': teacher.ngay_sinh.isoformat() if teacher.ngay_sinh else None,
                    'dia_chi': teacher.dia_chi,
                    'chuyen_mon': teacher.chuyen_mon
                } for teacher in teachers
            ]
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@teacher_bp.route('/teachers/list')
@teacher_required
def list_teachers_html():
    """Hiển thị danh sách giáo viên (HTML)"""
    try:
        teachers = Teacher.query.all()
        return render_template('teachers/list.html', teachers=teachers)
    except Exception as e:
        return f"<h2>❌ Lỗi: {str(e)}</h2>"

@teacher_bp.route('/teachers/add', methods=['GET', 'POST'])
@teacher_required
def add_teacher():
    """Thêm giáo viên mới"""
    if request.method == 'POST':
        try:
            # Lấy dữ liệu từ form
            ma_gv = request.form.get('ma_gv')
            ho_ten = request.form.get('ho_ten')
            email = request.form.get('email')
            so_dt = request.form.get('so_dt')
            gioi_tinh = request.form.get('gioi_tinh')
            ngay_sinh = request.form.get('ngay_sinh')
            dia_chi = request.form.get('dia_chi')
            chuyen_mon = request.form.get('chuyen_mon')

            # Validate dữ liệu
            if not ma_gv or not ho_ten:
                return jsonify({
                    'success': False,
                    'error': 'Mã giáo viên và họ tên là bắt buộc'
                }), 400

            # Tạo object Teacher
            new_teacher = Teacher(
                ma_gv=ma_gv,
                ho_ten=ho_ten,
                email=email,
                so_dt=so_dt,
                gioi_tinh=gioi_tinh,
                ngay_sinh=ngay_sinh if ngay_sinh else None,
                dia_chi=dia_chi,
                chuyen_mon=chuyen_mon
            )

            db.session.add(new_teacher)
            db.session.commit()

            return jsonify({
                'success': True,
                'message': 'Thêm giáo viên thành công',
                'teacher': {
                    'ma_gv': new_teacher.ma_gv,
                    'ho_ten': new_teacher.ho_ten,
                    'email': new_teacher.email,
                    'so_dt': new_teacher.so_dt,
                    'gioi_tinh': new_teacher.gioi_tinh,
                    'ngay_sinh': new_teacher.ngay_sinh.isoformat() if new_teacher.ngay_sinh else None,
                    'dia_chi': new_teacher.dia_chi,
                    'chuyen_mon': new_teacher.chuyen_mon
                }
            })
        except Exception as e:
            db.session.rollback()
            return jsonify({
                'success': False,
                'error': str(e)
            }), 500

    return render_template('teachers/add.html')

@teacher_bp.route('/teachers/<ma_gv>/edit', methods=['GET', 'POST'])
@teacher_required
def edit_teacher(ma_gv):
    """Chỉnh sửa thông tin giáo viên"""
    teacher = Teacher.query.filter_by(ma_gv=ma_gv).first()
    if not teacher:
        return jsonify({
            'success': False,
            'error': 'Giáo viên không tồn tại'
        }), 404
    
    if request.method == 'POST':
        try:
            # Lấy dữ liệu từ form
            ho_ten = request.form.get('ho_ten')
            email = request.form.get('email')
            so_dt = request.form.get('so_dt')
            gioi_tinh = request.form.get('gioi_tinh')
            ngay_sinh = request.form.get('ngay_sinh')
            dia_chi = request.form.get('dia_chi')
            chuyen_mon = request.form.get('chuyen_mon')

            # Validate dữ liệu
            if not ho_ten:
                return jsonify({
                    'success': False,
                    'error': 'Họ tên là bắt buộc'
                }), 400

            # Cập nhật thông tin
            teacher.ho_ten = ho_ten
            teacher.email = email
            teacher.so_dt = so_dt
            teacher.gioi_tinh = gioi_tinh
            teacher.ngay_sinh = ngay_sinh if ngay_sinh else None
            teacher.dia_chi = dia_chi
            teacher.chuyen_mon = chuyen_mon

            db.session.commit()

            return jsonify({
                'success': True,
                'message': 'Cập nhật giáo viên thành công',
                'teacher': {
                    'ma_gv': teacher.ma_gv,
                    'ho_ten': teacher.ho_ten,
                    'email': teacher.email,
                    'so_dt': teacher.so_dt,
                    'gioi_tinh': teacher.gioi_tinh,
                    'ngay_sinh': teacher.ngay_sinh.isoformat() if teacher.ngay_sinh else None,
                    'dia_chi': teacher.dia_chi,
                    'chuyen_mon': teacher.chuyen_mon
                }
            })
        except Exception as e:
            db.session.rollback()
            return jsonify({
                'success': False,
                'error': str(e)
            }), 500
    
    # GET - Hiển thị form edit
    return render_template('teachers/edit.html', teacher=teacher)

@teacher_bp.route('/teachers/<ma_gv>/delete', methods=['POST'])
@teacher_required
def delete_teacher(ma_gv):
    """Xóa giáo viên"""
    try:
        teacher = Teacher.query.filter_by(ma_gv=ma_gv).first()
        if not teacher:
            return jsonify({
                'success': False,
                'error': 'Giáo viên không tồn tại'
            }), 404
        
        # Xóa giáo viên
        db.session.delete(teacher)
        db.session.commit()

        return jsonify({
            'success': True,
            'message': 'Xóa giáo viên thành công'
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500
