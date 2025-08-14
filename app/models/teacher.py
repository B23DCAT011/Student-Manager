# app/models/teacher.py
from core.database import db

class Teacher(db.Model):
    """Model cho bảng GIAOVIEN"""
    __tablename__ = 'giaovien'

    ma_gv = db.Column(db.String(10), primary_key=True)
    ho_ten = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100))
    so_dt = db.Column(db.String(15))
    ngay_sinh = db.Column(db.Date)
    gioi_tinh = db.Column(db.String(10))
    dia_chi = db.Column(db.String(200))
    chuyen_mon = db.Column(db.String(200))

    # Relationships
    grades = db.relationship('Grade', backref='teacher', lazy='dynamic')
    user = db.relationship('User', backref='teacher_profile', uselist=False)

    def __repr__(self):
        return f'<Teacher {self.ma_gv}: {self.ho_ten}>'
