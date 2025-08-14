from flask import Blueprint, render_template, request, flash, redirect, url_for, session
from app.models.student import Student
from app.models.teacher import Teacher
from app.services.email_service import EmailService
from core.database import db
from flask import jsonify

email_bp = Blueprint('email', __name__)
email_service = EmailService()


@email_bp.route("/contact", methods=['GET', 'POST'])
def email_contact():
    """Gửi email liên hệ từ giáo viên đến sinh viên"""
    if request.method == 'POST':
        student_id = request.form.get('student_id')
        teacher_id = request.form.get('teacher_id')
        subject = request.form.get('subject')
        message = request.form.get('message')

        # Validate input
        if not all([student_id, teacher_id, subject, message]):
            flash('❌ Vui lòng điền đầy đủ thông tin!', 'error')
            return redirect(url_for('email.email_contact'))

        try:
            # Send email
            email_service.send_email(
                to_email=Student.query.filter_by(ma_sv=student_id).first().email,
                subject="Giáo viên: " + Teacher.query.filter_by(ma_gv=teacher_id).first().ho_ten + " - " + subject,
                body=message,
            )
            flash('✅ Đã gửi email liên hệ thành công!', 'success')
            return redirect(url_for('grades.high_risk_students'))
        except Exception as e:
            flash(f'❌ Lỗi gửi email: {str(e)}', 'error')
            return redirect(url_for('email.email_contact'))

    # GET request - hiển thị form với dữ liệu pre-fill
    try:
        # Lấy thông tin từ URL parameters
        student_id = request.args.get('student_id')
        student_name = request.args.get('student_name')
        teacher_id = request.args.get('teacher_id')

        # Nếu không có teacher_id từ URL, lấy từ session
        if not teacher_id and 'user_id' in session:
            teacher_id = session['user_id']

        # Lấy danh sách tất cả giáo viên và sinh viên cho dropdown
        teachers = Teacher.query.all()
        students = Student.query.all()

        # Lấy thông tin chi tiết sinh viên nếu có student_id
        selected_student = None
        if student_id:
            selected_student = Student.query.filter_by(ma_sv=student_id).first()

        # Lấy thông tin chi tiết giáo viên nếu có teacher_id
        selected_teacher = None
        if teacher_id:
            selected_teacher = Teacher.query.filter_by(ma_gv=teacher_id).first()

        return render_template('email/contact_form.html',
                             teachers=teachers,
                             students=students,
                             selected_student=selected_student,
                             selected_teacher=selected_teacher,
                             student_id=student_id,
                             student_name=student_name,
                             teacher_id=teacher_id)

    except Exception as e:
        flash(f'❌ Lỗi tải dữ liệu: {str(e)}', 'error')
        return render_template('email/contact_form.html',
                             teachers=[],
                             students=[])


@email_bp.route("/contact/bulk-warning", methods=['POST'])
def bulk_warning():
    """Gửi cảnh báo hàng loạt đến sinh viên có nguy cơ học tập kém"""
    try:
        data = request.get_json()  # Lấy toàn bộ JSON
        students_list = data.get('students', [])    # List các sinh viên
        total_count = data.get('total_count', 0)    # Tổng số lượng


        print(data.get('students', []))  # Debugging line to check input data

        for student_info in students_list:
            ma_sv = student_info.get('ma_sv')           # 'SV001'
            ho_ten = student_info.get('ho_ten')         # 'Nguyễn Văn A'
            gpa = student_info.get('gpa')               # 1.5
            so_mon_truot = student_info.get('so_mon_truot')
            risk_level = student_info.get('risk_level')

            # Tạo nội dung email
            subject = f"Cảnh báo học tập - {ho_ten}"
            message = f"""
            Chào {ho_ten},

            Chúng tôi nhận thấy rằng bạn đang gặp khó khăn trong học tập với GPA hiện tại là {gpa} và đã trượt {so_mon_truot} môn học. Mức độ rủi ro của bạn được đánh giá là: {risk_level}.

            Chúng tôi khuyến khích bạn liên hệ với giáo viên hướng dẫn để được hỗ trợ kịp thời.

            Trân trọng,
            Hệ thống quản lý sinh viên
            """

            email_service.send_email(
                to_email=Student.query.filter_by(ma_sv=ma_sv).first().email,
                subject=subject,
                body=message,
            )
        return jsonify({
            'success': True,
            'message': 'Cảnh báo đã được gửi thành công',
            'sent_count': len(students_list),
            'total_count': total_count
        }), 200
    except Exception as e:
        flash(f'❌ Lỗi gửi email: {str(e)}', 'error')
        return jsonify({
            'success': False,
            'message': 'Lỗi gửi email',
            'error': str(e)
        }), 500