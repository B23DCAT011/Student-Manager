# app/models/academic.py - Các model hỗ trợ
from core.database import db

class Khoa(db.Model):
    """Model cho bảng KHOA"""
    __tablename__ = 'khoa'

    ma_khoa = db.Column(db.String(10), primary_key=True)
    ten_khoa = db.Column(db.String(100), nullable=False)

    # Relationships
    nganhs = db.relationship('Nganh', backref='khoa', lazy='dynamic')

class Nganh(db.Model):
    """Model cho bảng NGANH"""
    __tablename__ = 'nganh'

    ma_nganh = db.Column(db.String(10), primary_key=True)
    ten_nganh = db.Column(db.String(100), nullable=False)
    ma_khoa = db.Column(db.String(10), db.ForeignKey('khoa.ma_khoa'), nullable=False)

    # Relationships
    lops = db.relationship('Lop', backref='nganh', lazy='dynamic')
    hocphans = db.relationship('HocPhan', backref='nganh', lazy='dynamic')

class Lop(db.Model):
    """Model cho bảng LOP"""
    __tablename__ = 'lop'

    ma_lop = db.Column(db.String(10), primary_key=True)
    ten_lop = db.Column(db.String(100), nullable=False)
    ma_nganh = db.Column(db.String(10), db.ForeignKey('nganh.ma_nganh'), nullable=False)
    khoa_hoc = db.Column(db.String(50))
    he_dt = db.Column(db.String(50))
    nam_nhap_hoc = db.Column(db.Integer)

    # Relationships
    students = db.relationship('Student', backref='lop', lazy='dynamic')

class HocPhan(db.Model):
    """Model cho bảng HOCPHAN"""
    __tablename__ = 'hocphan'

    ma_hp = db.Column(db.String(10), primary_key=True)
    ten_hp = db.Column(db.String(100), nullable=False)
    so_dvht = db.Column(db.Integer)  # Số đơn vị học trình
    ma_nganh = db.Column(db.String(10), db.ForeignKey('nganh.ma_nganh'), nullable=False)
    hoc_ky = db.Column(db.Integer)

    # Relationships
    grades = db.relationship('Grade', backref='hocphan', lazy='dynamic')
