# app/controllers/grades_controller.py
import datetime
from flask import Blueprint, render_template, request, jsonify, redirect, url_for
from flask_login import login_required, current_user
from app.models.prediction import DiemThanhPhan, SinhVienStats
from app.models.grade import Grade
from app.models.student import Student
from app.models.teacher import Teacher
from app.models.academic import HocPhan, Lop, Nganh
from app.utils.decorators import teacher_required, role_required
from core.database import db
from app.models.prediction import SinhVienStats

grades_bp = Blueprint('grades', __name__)

# =================== DASHBOARD & OVERVIEW ===================

@grades_bp.route('/')
@grades_bp.route('/dashboard')
@teacher_required
def dashboard():
    """
    Dashboard tổng quan về điểm số
    - Thống kê nhanh: số môn, sinh viên đã có điểm
    - Links đến các chức năng chính
    - Cảnh báo sinh viên high-risk
    """
    try:
        # 1. Thống kê tổng quan
        total_students = db.session.query(Student).count()
        print(f"Total students: {total_students}")
        total_subjects = db.session.query(HocPhan).count()

        # 2. Thống kê điểm thành phần (đã nhập)
        thanh_phan_count = db.session.query(DiemThanhPhan).count()
        students_with_thanh_phan = db.session.query(DiemThanhPhan.ma_sv).distinct().count()

        # 3. Thống kê điểm cuối kỳ
        cuoi_ky_count = db.session.query(Grade).count()
        students_with_cuoi_ky = db.session.query(Grade.ma_sv).distinct().count()

        # 4. Tỷ lệ hoàn thành nhập điểm
        thanh_phan_completion = round((students_with_thanh_phan / total_students * 100), 1) if total_students > 0 else 0
        cuoi_ky_completion = round((students_with_cuoi_ky / total_students * 100), 1) if total_students > 0 else 0

        # 5. Cảnh báo sinh viên high-risk (top 10)
        high_risk_students = db.session.query(SinhVienStats).filter(
            SinhVienStats.so_mon_da_truot >= 2  # Ví dụ: trượt >= 2 môn
        ).limit(10).all()

        dashboard_data = {
            'total_students': total_students,
            'total_subjects': total_subjects,
            'thanh_phan_count': thanh_phan_count,
            'cuoi_ky_count': cuoi_ky_count,
            'thanh_phan_completion': thanh_phan_completion,
            'cuoi_ky_completion': cuoi_ky_completion,
            'high_risk_count': len(high_risk_students),
            'high_risk_students': high_risk_students,
        }

        return render_template('grades/dashboard.html', data=dashboard_data)

    except Exception as e:
        # Log error và return empty dashboard
        print(f"Dashboard error: {e}")
        return render_template('grades/dashboard.html', data={})

@grades_bp.route('/high-risk')
@teacher_required
def high_risk_students():
    """
    Trang cảnh báo sinh viên có nguy cơ cao
    - Kết quả từ ML model prediction
    - Danh sách ưu tiên can thiệp
    """
    try:
        # Lấy danh sách sinh viên high-risk
        high_risk_students = db.session.query(SinhVienStats).filter(
            SinhVienStats.so_mon_da_truot>= 2
        ).all()

        data = {
            'high_risk_students': high_risk_students,
            'high_risk_count': len(high_risk_students)
        }
        print(f"High risk students count: {len(high_risk_students)}")

        return render_template('grades/high_risk_students.html', data=data)
    except Exception as e:
        print(f"High risk students error: {e}")
        return render_template('grades/high_risk_students.html', data={})

# =================== ĐIỂM THÀNH PHẦN ROUTES ===================

@grades_bp.route('/thanh-phan')
@teacher_required
def list_thanh_phan():
    """
    Danh sách điểm thành phần
    """
    try:

        lops = db.session.query(Lop).all()
        hocphans = db.session.query(HocPhan).all()
        teachers = db.session.query(Teacher).all()

        # Lấy parameters filter từ request
        hoc_ky = request.args.get('hoc_ky')
        nam_hoc = request.args.get('nam_hoc')
        lop = request.args.get('lop')
        mon_hoc = request.args.get('mon_hoc')
        giao_vien = request.args.get('giao_vien')

        # Base query với join để lấy thông tin liên quan
        query = db.session.query(DiemThanhPhan).join(Student).join(HocPhan)

        # Apply filters nếu có
        if hoc_ky:
            query = query.filter(DiemThanhPhan.hoc_ky == hoc_ky)
        if nam_hoc:
            query = query.filter(DiemThanhPhan.nam_hoc == nam_hoc)
        if lop:
            query = query.filter(Student.ma_lop == lop)
        if mon_hoc:
            query = query.filter(DiemThanhPhan.ma_hp == mon_hoc)
        if giao_vien:
            query = query.filter(DiemThanhPhan.ma_gv == giao_vien)

        # Lấy kết quả
        thanh_phan_records = query.all()

        # Tính thống kê
        total_records = len(thanh_phan_records)

        # Tính điểm trung bình (trung bình của 3 loại điểm thành phần)
        scores = []
        low_scores = 0
        for record in thanh_phan_records:
            avg_score = 0
            count = 0
            if record.diem_chuyen_can is not None:
                avg_score += record.diem_chuyen_can
                count += 1
            if record.diem_bai_tap is not None:
                avg_score += record.diem_bai_tap
                count += 1
            if record.diem_giua_ky is not None:
                avg_score += record.diem_giua_ky
                count += 1

            if count > 0:
                avg_score = avg_score / count
                scores.append(avg_score)
                if avg_score < 5:
                    low_scores += 1

        average_score = sum(scores) / len(scores) if scores else 0

        # Tính số sinh viên chưa có điểm thành phần
        total_students = db.session.query(Student).count()
        students_with_scores = db.session.query(DiemThanhPhan.ma_sv).distinct().count()
        missing_scores = total_students - students_with_scores

        # Lấy data cho dropdowns
        lops = db.session.query(Lop).all()
        hocphans = db.session.query(HocPhan).all()
        teachers = db.session.query(Teacher).all()

        data = {
            'total_records': total_records,
            'average_score': average_score,
            'low_scores': low_scores,
            'missing_scores': missing_scores,
            'thanh_phan_records': thanh_phan_records,
            'lops': lops,
            'hocphans': hocphans,
            'teachers': teachers,
            # Filters hiện tại để giữ state
            'current_filters': {
                'hoc_ky': hoc_ky,
                'nam_hoc': nam_hoc,
                'lop': lop,
                'mon_hoc': mon_hoc,
                'giao_vien': giao_vien
            }
        }

        return render_template('grades/list_thanh_phan.html', data=data)
    except Exception as e:
        print(f"List thanh phan error: {e}")
        return render_template('grades/list_thanh_phan.html', data={})

@grades_bp.route('/thanh-phan/add', methods=['GET', 'POST'])
@teacher_required
def add_thanh_phan():
    """
    Form thêm điểm thành phần
    """
    try:
        if request.method == 'GET':
            students = db.session.query(Student).all()
            subjects = db.session.query(HocPhan).all()
            teachers = db.session.query(Teacher).all()

            data = {
                'students': students,
                'subjects': subjects,
                'teachers': teachers
            }
        if request.method == 'POST':

            data = {
                'ma_sv': request.form.get('ma_sv'),
                'ma_hp': request.form.get('ma_hp'),
                'ma_gv': request.form.get('ma_gv'),
                'diem_chuyen_can': request.form.get('diem_chuyen_can'),
                'diem_bai_tap': request.form.get('diem_bai_tap'),
                'diem_giua_ky': request.form.get('diem_giua_ky'),
                'hoc_ky': request.form.get('hoc_ky'),
                'nam_hoc': request.form.get('nam_hoc'),
                'ngay_tao': datetime.datetime.utcnow(),
                'ngay_cap_nhat': datetime.datetime.utcnow()
            }

            # Validate dữ liệu
            if not data['ma_sv'] or not data['ma_hp'] or not data['ma_gv']:
                return jsonify({
                    'success': False,
                    'error': 'Mã sinh viên, mã học phần và mã giáo viên là bắt buộc'
                }), 400
            # Tạo đối tượng DiemThanhPhan
            new_thanh_phan = DiemThanhPhan(**data)
            db.session.add(new_thanh_phan)
            db.session.commit()
            return jsonify({
                'success': True,
                'message': 'Thêm điểm thành phần thành công',
                'data': {
                    'ma_sv': new_thanh_phan.ma_sv,
                    'ma_hp': new_thanh_phan.ma_hp,
                    'ma_gv': new_thanh_phan.ma_gv,
                    'diem_chuyen_can': new_thanh_phan.diem_chuyen_can,
                    'diem_bai_tap': new_thanh_phan.diem_bai_tap,
                    'diem_giua_ky': new_thanh_phan.diem_giua_ky,
                    'hoc_ky': new_thanh_phan.hoc_ky,
                    'nam_hoc': new_thanh_phan.nam_hoc,
                    'ngay_tao': new_thanh_phan.ngay_tao.isoformat(),
                    'ngay_cap_nhat': new_thanh_phan.ngay_cap_nhat.isoformat()
                }
            })
        return render_template('grades/add_thanh_phan.html', data=data)
    except Exception as e:
        print(f"Add thanh phan error: {e}")
        return render_template('grades/add_thanh_phan.html', data={})

@grades_bp.route('/thanh-phan/edit/<int:id>',methods=['GET', 'POST'])
@teacher_required
def edit_thanh_phan(id):
    """
    Form sửa điểm thành phần
    """
    try:
        if(request.method == 'GET'):
            record = DiemThanhPhan.query.get(id)
            if not record:
                return jsonify({'success': False, 'error': 'Record not found'}), 404

            students = db.session.query(Student).all()
            subjects = db.session.query(HocPhan).all()
            teachers = db.session.query(Teacher).all()

            data = {
                'record': record,
                'students': students,
                'subjects': subjects,
                'teachers': teachers
            }
            return render_template('grades/edit_thanh_phan.html', data=data)
        if(request.method == 'POST'):
            record = DiemThanhPhan.query.get(id)
            if not record:
                return jsonify({'success': False, 'error': 'Record not found'}), 404

            # Chỉ cập nhật những field có trong form (không sửa ma_sv, ma_hp vì là khóa chính)
            record.ma_gv = request.form.get('ma_gv')
            record.diem_chuyen_can = float(request.form.get('diem_chuyen_can')) if request.form.get('diem_chuyen_can') else None
            record.diem_bai_tap = float(request.form.get('diem_bai_tap')) if request.form.get('diem_bai_tap') else None
            record.diem_giua_ky = float(request.form.get('diem_giua_ky')) if request.form.get('diem_giua_ky') else None
            record.hoc_ky = request.form.get('hoc_ky')
            record.nam_hoc = request.form.get('nam_hoc')
            record.ngay_cap_nhat = datetime.datetime.utcnow()

            # Validate dữ liệu
            if not record.ma_gv or not record.hoc_ky or not record.nam_hoc:
                return redirect(url_for('grades.edit_thanh_phan', id=id))

            # Lưu thay đổi
            db.session.commit()
            return redirect(url_for('grades.list_thanh_phan'))
        return render_template('grades/edit_thanh_phan.html', data=data)
    except Exception as e:
        print(f"Edit thanh phan error: {e}")
        return redirect(url_for('grades.list_thanh_phan'))

@grades_bp.route('/thanh-phan/delete/<int:id>', methods=['POST'])
@teacher_required
def delete_thanh_phan(id):
    """
    Xóa điểm thành phần
    """
    try:
        record = DiemThanhPhan.query.get(id)
        if not record:
            return jsonify({'success': False, 'error': 'Record not found'}), 404
        # Xóa record
        db.session.delete(record)
        db.session.commit()
        return jsonify({'success': True, 'message': 'Record deleted successfully'})
    except Exception as e:
        db.session.rollback()
        print(f"Delete thanh phan error: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500
# =================== ĐIỂM CUỐI KỲ ROUTES ===================

@grades_bp.route('/cuoi-ky')
@teacher_required
def list_cuoi_ky():
    """
    Danh sách điểm cuối kỳ
    """
    try:
        lop = db.session.query(Lop).all()
        mon_hoc = db.session.query(HocPhan).all()

        query = db.session.query(Grade).join(Student).join(HocPhan)

        hoc_ky = request.args.get('hoc_ky')
        nam_hoc = request.args.get('nam_hoc')
        lop = request.args.get('lop')
        mon_hoc = request.args.get('mon_hoc')

        # Base query với join để lấy thông tin liên quan
        query = db.session.query(Grade).join(Student).join(HocPhan).join(DiemThanhPhan)

        # Apply filters nếu có
        if hoc_ky:
            query = query.filter(DiemThanhPhan.hoc_ky == hoc_ky)
        if nam_hoc:
            query = query.filter(DiemThanhPhan.nam_hoc == nam_hoc)
        if lop:
            query = query.filter(Student.ma_lop == lop)
        if mon_hoc:
            query = query.filter(Grade.ma_hp == mon_hoc)

        cuoi_ky_records = query.all()


        total_subjects = len(cuoi_ky_records)
        passed_count = sum(1 for record in cuoi_ky_records if record.diem_hp >= 5)
        average_gpa = sum(record.diem_hp for record in cuoi_ky_records) / total_subjects if total_subjects > 0 else 0

        #LAY DATA CHO DROPDOWNS
        lop = db.session.query(Lop).all()
        mon_hoc = db.session.query(HocPhan).all()

        data = {
            'total_subjects': total_subjects,
            'passed_count': passed_count,
            'failed_count': total_subjects - passed_count,
            'average_gpa': average_gpa,
            'cuoi_ky_records': cuoi_ky_records,
            'lops': lop,
            'hocphans': mon_hoc,
            'current_filters': {
                'hoc_ky': hoc_ky,
                'nam_hoc': nam_hoc,
                'lop': lop,
                'mon_hoc': mon_hoc
            }
        }

        return render_template('grades/list_cuoi_ky.html', data=data)
    except Exception as e:
        print(f"List cuoi ky error: {e}")
        return render_template('grades/list_cuoi_ky.html', data={})

@grades_bp.route('/cuoi-ky/add', methods=['GET', 'POST'])
@teacher_required
def add_cuoi_ky():
    """
    Form thêm điểm cuối kỳ
    """
    try:
        if request.method == 'GET':
            # Lấy danh sách cho dropdowns
            students = db.session.query(Student).all()
            subjects = db.session.query(HocPhan).all()
            teachers = db.session.query(Teacher).all()

            data = {
                'students': students,
                'subjects': subjects,
                'teachers': teachers
            }
            return render_template('grades/add_cuoi_ky.html', data=data)

        elif request.method == 'POST':
            # Xử lý submit form
            ma_sv = request.form.get('ma_sv')
            ma_hp = request.form.get('ma_hp')
            ma_gv = request.form.get('ma_gv')
            diem_hp = request.form.get('diem_hp')

            # Validate dữ liệu
            if not all([ma_sv, ma_hp, diem_hp]):
                return redirect(url_for('grades.add_cuoi_ky'))

            # Tạo record mới
            new_grade = Grade(
                ma_sv=ma_sv,
                ma_hp=ma_hp,
                ma_gv=ma_gv,
                diem_hp=float(diem_hp)
            )

            db.session.add(new_grade)
            db.session.commit()

            return redirect(url_for('grades.list_cuoi_ky'))

    except Exception as e:
        print(f"Add cuoi ky error: {e}")
        db.session.rollback()
        return render_template('grades/add_cuoi_ky.html', data={})

@grades_bp.route('/cuoi-ky/edit/<string:ma_sv>/<string:ma_hp>', methods=['GET', 'POST'])
@teacher_required
def edit_cuoi_ky(ma_sv, ma_hp):
    """
    Form sửa điểm cuối kỳ
    """
    try:
        # Lấy record theo composite key
        record = db.session.query(Grade).filter_by(ma_sv=ma_sv, ma_hp=ma_hp).first()
        if not record:
            print(f"Record not found for ma_sv: {ma_sv}, ma_hp: {ma_hp}")
            return redirect(url_for('grades.list_cuoi_ky'))
        if request.method == 'GET':
            # Hiển thị form với dữ liệu hiện tại
            teachers = db.session.query(Teacher).all()

            data = {
                'record': record,
                'teachers': teachers
            }
            print(f"Editing record: {record.ma_sv}, {record.ma_hp}, {record.diem_hp}")
            return render_template('grades/edit_cuoi_ky.html', data=data)

        elif request.method == 'POST':
            # Xử lý cập nhật

            record.diem_hp = float(request.form.get('diem_hp')) if request.form.get('diem_hp') else 0
            record.ngay_nhap = datetime.datetime.utcnow()

            SinhVienStats.query.filter_by(ma_sv=ma_sv).update({
                'gpa_hien_tai': record.average_grade(),
                'so_mon_da_truot': record.count_failed_subjects(),
                'ngay_cap_nhat': datetime.datetime.utcnow()
            })

            # Validate
            if record.diem_hp is None:
                return redirect(url_for('grades.list_cuoi_ky', ma_sv=ma_sv, ma_hp=ma_hp))
            db.session.commit()
            return redirect(url_for('grades.list_cuoi_ky'))

    except Exception as e:
        print(f"Edit cuoi ky error: {e}")
        return redirect(url_for('grades.list_cuoi_ky'))

@grades_bp.route('/cuoi-ky/delete/<string:ma_sv>/<string:ma_hp>', methods=['DELETE'])
@teacher_required
def delete_cuoi_ky(ma_sv, ma_hp):
    """
    Xóa điểm cuối kỳ
    """
    try:
        record = db.session.query(Grade).filter_by(ma_sv=ma_sv, ma_hp=ma_hp).first()
        if not record:
            return jsonify({'success': False, 'error': 'Record not found'}), 404

        # Xóa record
        db.session.delete(record)
        db.session.commit()
        return jsonify({'success': True, 'message': 'Record deleted successfully'})
    except Exception as e:
        db.session.rollback()
        print(f"Delete cuoi ky error: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500
# =================== REPORTS & ANALYTICS ===================
# @grades_bp.route('/reports')
# def reports():
#     """
#     Trang báo cáo và phân tích điểm số
#     - Xuất bảng điểm PDF
#     - Biểu đồ thống kê điểm
#     """
#     try:
#         return render_template('grades/reports.html')
#     except Exception as e:
#         print(f"Reports error: {e}")
#         return render_template('grades/reports.html')

# =================== HELPER FUNCTIONS ===================
