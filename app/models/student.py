# app/models/student.py
from core.database import db

class Student(db.Model):
    """Model cho bảng SINHVIEN"""
    __tablename__ = 'sinhvien'

    ma_sv = db.Column(db.String(10), primary_key=True)
    ho_ten = db.Column(db.String(100), nullable=False)
    ma_lop = db.Column(db.String(10), db.ForeignKey('lop.ma_lop'), nullable=False)
    gioi_tinh = db.Column(db.String(10))
    ngay_sinh = db.Column(db.Date)
    dia_chi = db.Column(db.String(200))
    email = db.Column(db.String(100), nullable=True)  # Thêm cột email

    # Relationships
    grades = db.relationship('Grade', backref='student', lazy='dynamic')
    user = db.relationship('User', backref='student_profile', uselist=False)

    def get_average_grade(self):
        """Tính điểm trung bình"""
        grades = self.grades.all()
        if not grades:
            return 0
        return sum(grade.diem_hp for grade in grades) / len(grades)

    def __repr__(self):
        return f'<Student {self.ma_sv}: {self.ho_ten}>'
