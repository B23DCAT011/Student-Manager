from flask import Blueprint, render_template, request, jsonify
from app.models.academic import Khoa, Nganh, Lop, HocPhan
from core.database import db
from app.utils.decorators import teacher_required

academic_bp = Blueprint('academic', __name__)

# =================== KHOA ROUTES ===================
@academic_bp.route('/academics/khoa')
@teacher_required
def list_khoa():
    """Danh sách khoa (JSON API)"""
    try:
        khoas = Khoa.query.all()
        return jsonify({
            'success': True,
            'count': len(khoas),
            'khoas': [{'ma_khoa': k.ma_khoa, 'ten_khoa': k.ten_khoa} for k in khoas]
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@academic_bp.route('/academics/khoa/list')
def list_khoa_html():
    """Danh sách khoa (HTML)"""
    try:
        khoas = Khoa.query.all()
        return render_template('academics/khoa_list.html', khoas=khoas)
    except Exception as e:
        return f"<h2>❌ Lỗi: {str(e)}</h2>"

# =================== NGANH ROUTES ===================
@academic_bp.route('/academics/nganh')
@teacher_required
def list_nganh():
    """Danh sách ngành (JSON API)"""
    try:
        nganhs = Nganh.query.all()
        return jsonify({
            'success': True,
            'count': len(nganhs),
            'nganhs': [
                {
                    'ma_nganh': n.ma_nganh,
                    'ten_nganh': n.ten_nganh,
                    'ma_khoa': n.ma_khoa,
                    'ten_khoa': n.khoa.ten_khoa if n.khoa else None
                } for n in nganhs
            ]
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@academic_bp.route('/academics/nganh/list')
@teacher_required
def list_nganh_html():
    """Danh sách ngành (HTML)"""
    try:
        # Lọc theo khoa nếu có
        khoa_filter = request.args.get('khoa')
        if khoa_filter:
            nganhs = Nganh.query.filter_by(ma_khoa=khoa_filter).all()
        else:
            nganhs = Nganh.query.all()

        # Lấy tất cả khoa để làm dropdown
        khoas = Khoa.query.all()

        return render_template('academics/nganh_list.html', nganhs=nganhs, khoas=khoas)
    except Exception as e:
        return f"<h2>❌ Lỗi: {str(e)}</h2>"

# =================== LOP ROUTES ===================
@academic_bp.route('/academics/lop')
@teacher_required
def list_lop():
    """Danh sách lớp (JSON API)"""
    try:
        lops = Lop.query.all()
        return jsonify({
            'success': True,
            'count': len(lops),
            'lops': [
                {
                    'ma_lop': l.ma_lop,
                    'ten_lop': l.ten_lop,
                    'ma_nganh': l.ma_nganh,
                    'ten_nganh': l.nganh.ten_nganh if l.nganh else None,
                    'khoa_hoc': l.khoa_hoc,
                    'he_dt': l.he_dt,
                    'nam_nhap_hoc': l.nam_nhap_hoc
                } for l in lops
            ]
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@academic_bp.route('/academics/lop/list')
@teacher_required
def list_lop_html():
    """Danh sách lớp (HTML)"""
    try:
        lops = Lop.query.all()
        return render_template('academics/lop_list.html', lops=lops)
    except Exception as e:
        return f"<h2>❌ Lỗi: {str(e)}</h2>"

# =================== HOC PHAN ROUTES ===================
@academic_bp.route('/academics/hocphan')
@teacher_required
def list_hocphan():
    """Danh sách học phần (JSON API)"""
    try:
        hocphans = HocPhan.query.all()
        return jsonify({
            'success': True,
            'count': len(hocphans),
            'hocphans': [
                {
                    'ma_hp': h.ma_hp,
                    'ten_hp': h.ten_hp,
                    'so_dvht': h.so_dvht,
                    'ma_nganh': h.ma_nganh,
                    'ten_nganh': h.nganh.ten_nganh if h.nganh else None,
                    'hoc_ky': h.hoc_ky
                } for h in hocphans
            ]
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@academic_bp.route('/academics/hocphan/add', methods=['GET', 'POST'])
@teacher_required
def add_hocphan():
    """Thêm học phần mới"""
    if request.method == 'POST':
        try:
            # Lay data tu form
            ma_hp = request.form.get('ma_hp')
            ten_hp = request.form.get('ten_hp')
            so_dvht = request.form.get('so_dvht')
            ma_nganh = request.form.get('ma_nganh')
            hoc_ky = request.form.get('hoc_ky')
            
            # Validate data
            if not ma_hp or not ten_hp or not ma_nganh:
                return jsonify({
                    'success': False,
                    'error': 'Mã học phần, tên học phần và mã ngành là bắt buộc'
                }), 400
                
            # Tạo đối tượng HocPhan
            new_hocphan = HocPhan(
                ma_hp=ma_hp,
                ten_hp=ten_hp,
                so_dvht=int(so_dvht) if so_dvht else None,
                ma_nganh=ma_nganh,
                hoc_ky=int(hoc_ky) if hoc_ky else None
            )

            db.session.add(new_hocphan)
            db.session.commit()
            return "Thêm học phần thành công", 201
        except Exception as e:
            return jsonify({
                'success': False,
                'error': str(e)
            }), 500
    
    # GET request - hiển thị form
    nganhs = Nganh.query.all()
    return render_template('academics/add_hocphan.html', nganhs=nganhs)

@academic_bp.route('/academics/hocphan/list')
@teacher_required
def list_hocphan_html():
    """Danh sách học phần (HTML)"""
    try:
        # Lọc theo các tiêu chí
        search = request.args.get('search', '').strip()
        dvht_filter = request.args.get('dvht', '').strip()

        # Base query
        query = HocPhan.query

        # Áp dụng filters
        if search:
            query = query.filter(HocPhan.ten_hp.contains(search))
        if dvht_filter:
            query = query.filter(HocPhan.so_dvht == int(dvht_filter))

        hocphans = query.all()
        total_credits = sum(h.so_dvht for h in hocphans if h.so_dvht)

        return render_template('academics/hocphan_list.html',
                             hocphans=hocphans,
                             total_credits=total_credits)
    except Exception as e:
        return f"<h2>❌ Lỗi: {str(e)}</h2>"

@academic_bp.route('/academics/hocphan/<ma_hp>/edit', methods=['GET', 'POST'])
@teacher_required
def edit_hocphan(ma_hp):
    """Sửa thông tin học phần"""
    hocphan = HocPhan.query.get_or_404(ma_hp)
    
    if request.method == 'POST':
        try:
            # Cập nhật thông tin
            hocphan.ten_hp = request.form.get('ten_hp')
            so_dvht = request.form.get('so_dvht')
            hocphan.so_dvht = int(so_dvht) if so_dvht else None
            hocphan.ma_nganh = request.form.get('ma_nganh')
            hoc_ky = request.form.get('hoc_ky')
            hocphan.hoc_ky = int(hoc_ky) if hoc_ky else None
            
            db.session.commit()
            return "Cập nhật học phần thành công", 200
        except Exception as e:
            return f"Lỗi: {str(e)}", 500
    
    # GET request - hiển thị form
    nganhs = Nganh.query.all()
    return render_template('academics/edit_hocphan.html', hocphan=hocphan, nganhs=nganhs)

@academic_bp.route('/academics/hocphan/<ma_hp>/delete', methods=['GET', 'POST'])
@teacher_required
def delete_hocphan(ma_hp):
    """Xóa học phần"""
    try:
        hocphan = HocPhan.query.get_or_404(ma_hp)
        db.session.delete(hocphan)
        db.session.commit()
        return "Xóa học phần thành công", 200
    except Exception as e:
        return f"Lỗi: {str(e)}", 500

# =================== TONG QUAN ROUTE ===================
@academic_bp.route('/academics')
@teacher_required
def academic_overview():
    """Tổng quan Academic (HTML)"""
    try:
        khoa_count = Khoa.query.count()
        nganh_count = Nganh.query.count()
        lop_count = Lop.query.count()
        hocphan_count = HocPhan.query.count()

        return render_template('academics/overview.html',
                             khoa_count=khoa_count,
                             nganh_count=nganh_count,
                             lop_count=lop_count,
                             hocphan_count=hocphan_count)
    except Exception as e:
        return f"<h2>❌ Lỗi: {str(e)}</h2>"
