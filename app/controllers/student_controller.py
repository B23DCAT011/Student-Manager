from flask import Blueprint,render_template,request,jsonify,redirect,url_for
from app.models.student import Student
from core.database import db
from app.utils.decorators import teacher_required


student_bp = Blueprint('student',__name__)

@student_bp.route('/students')
@teacher_required
def list_students():
  """Hiển thị danh sách sinh viên (JSON API)"""
  try:
    students = Student.query.all()
    return jsonify({
      'success': True,
      'count': len(students),
      'students':[
        {
          'ma_sv':student.ma_sv,
          'ho_ten':student.ho_ten,
          'gioi_tinh':student.gioi_tinh,
          'ngay_sinh': student.ngay_sinh.isoformat() if student.ngay_sinh else None,
          'dia_chi': student.dia_chi
        } for student in students
      ]
    })
  except Exception as e:
    return jsonify({
      'success': False,
      'error': str(e)
    }),500

@student_bp.route('/students/list')
@teacher_required
def list_students_html():
  """Hiển thị danh sách sinh viên (HTML)"""
  try:
    #!!thêm index cho các cột được truy vấn thường xuyên
    ma_sv = request.args.get('ma_sv', '').strip()
    ho_ten = request.args.get('ho_ten', '').strip()
    ma_lop = request.args.get('ma_lop', '').strip()

    query = Student.query

    if ma_sv:
        query = query.filter(Student.ma_sv.ilike(f'%{ma_sv}%'))
    if ho_ten:
        query = query.filter(Student.ho_ten.ilike(f'%{ho_ten}%'))
    if ma_lop:
        query = query.filter(Student.ma_lop.ilike(f'%{ma_lop}%'))

    students = query.all()
    return render_template('students/list.html', students=students)
  except Exception as e:
    return f"<h2>❌ Lỗi: {str(e)}</h2>"

@student_bp.route('/students/add',methods=['GET','POST'])
@teacher_required
def add_student():
  """thêm sinh viên mới"""
  if request.method == 'POST':
    try:
      # Lấy dữ liệu từ form
      ma_sv = request.form.get('ma_sv')
      ho_ten = request.form.get('ho_ten')
      ma_lop = request.form.get('ma_lop')
      gioi_tinh = request.form.get('gioi_tinh')
      ngay_sinh = request.form.get('ngay_sinh')
      dia_chi = request.form.get('dia_chi')

      #validate dữ liệu
      if not ma_sv or not ho_ten or not ma_lop:
        return jsonify({
          'success': False,
          'error': 'Mã sinh viên, họ tên và mã lớp là bắt buộc'
        }),400
      #Tao Object Student
      new_student = Student(
        ma_sv=ma_sv,
        ho_ten=ho_ten,
        ma_lop=ma_lop,
        gioi_tinh=gioi_tinh,
        ngay_sinh=ngay_sinh,
        dia_chi=dia_chi
      )

      db.session.add(new_student)
      db.session.commit()

      return jsonify({
        'success': True,
        'message': 'Thêm sinh viên thành công',
        'student': {
          'ma_sv': new_student.ma_sv,
          'ho_ten': new_student.ho_ten,
          'ma_lop': new_student.ma_lop,
          'gioi_tinh': new_student.gioi_tinh,
          'ngay_sinh': new_student.ngay_sinh.isoformat() if new_student.ngay_sinh else None,
          'dia_chi': new_student.dia_chi
        }
      })
    except Exception as e:
      db.session.rollback()
      return jsonify({
        'success': False,
        'error': str(e)
      }),500
  return render_template('students/add.html')


@student_bp.route('/students/<ma_sv>/edit', methods=['GET', 'POST'])
@teacher_required
def edit_student(ma_sv):
  """Chỉnh sửa thông tin sinh viên"""
  student = Student.query.filter_by(ma_sv=ma_sv).first()
  if not student:
    return jsonify({
      'success': False,
      'error': 'Sinh viên không tồn tại'
    }),404

  if request.method == 'POST':
    try:
      # Lấy dữ liệu từ form
      ho_ten = request.form.get('ho_ten')
      ma_lop = request.form.get('ma_lop')
      gioi_tinh = request.form.get('gioi_tinh')
      ngay_sinh = request.form.get('ngay_sinh')
      dia_chi = request.form.get('dia_chi')

      # Validate dữ liệu
      if not ho_ten or not ma_lop:
        return jsonify({
          'success': False,
          'error': 'Họ tên và mã lớp là bắt buộc'
        }),400

      # Cập nhật thông tin
      student.ho_ten = ho_ten
      student.ma_lop = ma_lop
      student.gioi_tinh = gioi_tinh
      student.ngay_sinh = ngay_sinh if ngay_sinh else None
      student.dia_chi = dia_chi

      db.session.commit()

      return jsonify({
        'success': True,
        'message': 'Cập nhật sinh viên thành công',
        'student': {
          'ma_sv': student.ma_sv,
          'ho_ten': student.ho_ten,
          'ma_lop': student.ma_lop,
          'gioi_tinh': student.gioi_tinh,
          'ngay_sinh': student.ngay_sinh.isoformat() if student.ngay_sinh else None,
          'dia_chi': student.dia_chi
        }
      })
    except Exception as e:
      db.session.rollback()
      return jsonify({
        'success': False,
        'error': str(e)
      }),500
  # GET - Hiển thị form edit
  return render_template('students/edit.html', student=student)

@student_bp.route('/students/<ma_sv>/delete', methods=['POST'])
@teacher_required
def delete_student(ma_sv):
  """Xoa sinh viên"""
  try:
    student = Student.query.filter_by(ma_sv=ma_sv).first()
    if not student:
      return jsonify({
        'success': False,
        'error': 'Sinh viên không tồn tại'
      }),404
    # Xóa sinh viên
    db.session.delete(student)
    db.session.commit()

    return jsonify({
      'success': True,
      'message': 'Xóa sinh viên thành công'
    })
  except Exception as e:
    db.session.rollback()
    return jsonify({
      'success': False,
      'error': str(e)
    }),500