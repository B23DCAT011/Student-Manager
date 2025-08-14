# app/models/grade.py
from core.database import db

class Grade(db.Model):
    """Model cho bảng DIEMHP"""
    __tablename__ = 'diemhp'

    ma_sv = db.Column(db.String(10), db.ForeignKey('sinhvien.ma_sv'), primary_key=True)
    ma_hp = db.Column(db.String(10), db.ForeignKey('hocphan.ma_hp'), primary_key=True)
    diem_hp = db.Column(db.Float, nullable=False)
    ma_gv = db.Column(db.String(10), db.ForeignKey('giaovien.ma_gv'))
    ngay_nhap = db.Column(db.DateTime, default=db.func.current_timestamp())

    def is_passing(self):
        """Kiểm tra có đậu không (>= 5.0)"""
        return self.diem_hp >= 5.0

    def count_failed_subjects(self):
        """Đếm số môn học bị trượt (điểm < 5.0)"""
        grades = Grade.query.filter_by(ma_sv=self.ma_sv).all()
        return sum(1 for grade in grades if grade.diem_hp < 5.0)

    def average_grade(self):
        """Trả về điểm trung bình của tất cả các môn học"""
        grades = Grade.query.filter_by(ma_sv=self.ma_sv).all()
        if not grades:
            return 0
        total = sum(grade.diem_hp for grade in grades)
        return total / len(grades)

    def __repr__(self):
        return f'<Grade {self.ma_sv}-{self.ma_hp}: {self.diem_hp}>'
