# app/models/prediction.py - Models cho dữ liệu input ML
from core.database import db
from datetime import datetime

class DiemThanhPhan(db.Model):
    """Model cho bảng điểm thành phần - chỉ chứa input data"""
    __tablename__ = 'diem_thanh_phan'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    ma_sv = db.Column(db.String(10), db.ForeignKey('sinhvien.ma_sv'), nullable=False)
    ma_hp = db.Column(db.String(10), db.ForeignKey('hocphan.ma_hp'), nullable=False)
    ma_gv = db.Column(db.String(10), db.ForeignKey('giaovien.ma_gv'), nullable=False)
    # Dữ liệu input cho ML
    diem_chuyen_can = db.Column(db.Float)  # 0-10
    diem_bai_tap = db.Column(db.Float)     # 0-10
    diem_giua_ky = db.Column(db.Float)     # 0-10
    # Metadata
    hoc_ky = db.Column(db.String(10))
    nam_hoc = db.Column(db.String(10))
    ngay_tao = db.Column(db.DateTime, default=datetime.utcnow)
    ngay_cap_nhat = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    student = db.relationship('Student', backref='diem_thanh_phans')
    hocphan = db.relationship('HocPhan', backref='diem_thanh_phans')
    teacher = db.relationship('Teacher', backref='diem_thanh_phans')

    # Unique constraint
    __table_args__ = (
        db.UniqueConstraint('ma_sv', 'ma_hp', 'hoc_ky', 'nam_hoc', name='unique_student_subject_semester'),
    )

class SinhVienStats(db.Model):
    __tablename__ = 'sinh_vien_stats'

    ma_sv = db.Column(db.String(10), db.ForeignKey('sinhvien.ma_sv'), primary_key=True)
    gpa_hien_tai = db.Column(db.Float)      # Tính từ bảng GRADE
    so_mon_da_truot = db.Column(db.Integer, default=0)  # Đếm từ bảng GRADE
    ngay_cap_nhat = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationship
    student = db.relationship('Student', backref='stats')
