# reset_and_seed_data.py
from flask import Flask
from core.database import db
from app.models.user import User
from app.models.student import Student
from app.models.teacher import Teacher
from app.models.academic import Khoa, Nganh, Lop, HocPhan
from app.models.grade import Grade
from app.models.prediction import DiemThanhPhan, SinhVienStats

def create_app():
    app = Flask(__name__)
    app.config.from_object('core.config.Config')
    db.init_app(app)
    return app

def clear_all_data():
    """Xóa tất cả dữ liệu trong database"""
    print("🗑️ Xóa tất cả dữ liệu...")
    
    from sqlalchemy import text
    
    # Disable foreign key checks tạm thời
    db.session.execute(text('SET FOREIGN_KEY_CHECKS = 0'))
    
    # Xóa tất cả bảng
    db.session.query(SinhVienStats).delete()
    db.session.query(DiemThanhPhan).delete()
    db.session.query(Grade).delete()
    db.session.query(Student).delete()
    db.session.query(Teacher).delete()
    db.session.query(HocPhan).delete()
    db.session.query(Lop).delete()
    db.session.query(Nganh).delete()
    db.session.query(Khoa).delete()
    db.session.query(User).delete()
    
    # Enable lại foreign key checks
    db.session.execute(text('SET FOREIGN_KEY_CHECKS = 1'))
    
    db.session.commit()
    print("✅ Đã xóa tất cả dữ liệu!")

def create_sample_data():
    """Tạo dữ liệu mẫu cho tất cả các bảng"""
    print("📝 Tạo dữ liệu mẫu...")
    
    # 1. Tạo Users
    print("👤 Tạo Users...")
    # Chỉ tạo teacher và student users vì enum chỉ có 2 giá trị này
    teacher_user = User(username='teacher1', password='teacher123', role='teacher')
    student_user = User(username='student1', password='student123', role='student')
    
    db.session.add_all([teacher_user, student_user])
    db.session.commit()
    
    # 2. Tạo Khoa
    print("🏢 Tạo Khoa...")
    khoa_cntt = Khoa(ma_khoa='CNTT', ten_khoa='Công nghệ thông tin')
    khoa_kt = Khoa(ma_khoa='KT', ten_khoa='Kinh tế')
    khoa_nn = Khoa(ma_khoa='NN', ten_khoa='Ngoại ngữ')
    
    db.session.add_all([khoa_cntt, khoa_kt, khoa_nn])
    db.session.commit()
    
    # 3. Tạo Ngành
    print("🎓 Tạo Ngành...")
    nganh_ktpm = Nganh(ma_nganh='KTPM', ten_nganh='Kỹ thuật phần mềm', ma_khoa='CNTT')
    nganh_httt = Nganh(ma_nganh='HTTT', ten_nganh='Hệ thống thông tin', ma_khoa='CNTT')
    nganh_qtkd = Nganh(ma_nganh='QTKD', ten_nganh='Quản trị kinh doanh', ma_khoa='KT')
    nganh_ta = Nganh(ma_nganh='TA', ten_nganh='Tiếng Anh', ma_khoa='NN')
    
    db.session.add_all([nganh_ktpm, nganh_httt, nganh_qtkd, nganh_ta])
    db.session.commit()
    
    # 4. Tạo Lớp
    print("🏫 Tạo Lớp...")
    lop_data = [
        ('KTPM2021A', 'Kỹ thuật phần mềm 2021A', 'KTPM'),
        ('KTPM2021B', 'Kỹ thuật phần mềm 2021B', 'KTPM'),
        ('HTTT2021A', 'Hệ thống thông tin 2021A', 'HTTT'),
        ('QTKD2021A', 'Quản trị kinh doanh 2021A', 'QTKD'),
        ('TA2021A', 'Tiếng Anh 2021A', 'TA')
    ]
    
    for ma_lop, ten_lop, ma_nganh in lop_data:
        lop = Lop(ma_lop=ma_lop, ten_lop=ten_lop, ma_nganh=ma_nganh)
        db.session.add(lop)
    
    db.session.commit()
    
    # 5. Tạo Giáo viên
    print("👨‍🏫 Tạo Giáo viên...")
    teachers_data = [
        ('GV001', 'Nguyễn Văn A', 'nam', '1980-05-15', '0901234567', 'nguyenvana@university.edu.vn', 'TP.HCM', 'Lập trình'),
        ('GV002', 'Trần Thị B', 'nữ', '1985-08-20', '0907654321', 'tranthib@university.edu.vn', 'Hà Nội', 'Cơ sở dữ liệu'),
        ('GV003', 'Lê Văn C', 'nam', '1978-12-10', '0912345678', 'levanc@university.edu.vn', 'Đà Nẵng', 'Kinh tế'),
        ('GV004', 'Phạm Thị D', 'nữ', '1982-03-25', '0918765432', 'phamthid@university.edu.vn', 'TP.HCM', 'Ngoại ngữ'),
        ('GV005', 'Hoàng Văn E', 'nam', '1975-11-05', '0923456789', 'hoangvane@university.edu.vn', 'Hà Nội', 'Mạng máy tính')
    ]
    
    for ma_gv, ho_ten, gioi_tinh, ngay_sinh, so_dt, email, dia_chi, chuyen_mon in teachers_data:
        teacher = Teacher(
            ma_gv=ma_gv, ho_ten=ho_ten, gioi_tinh=gioi_tinh, 
            ngay_sinh=ngay_sinh, so_dt=so_dt, email=email, 
            dia_chi=dia_chi, chuyen_mon=chuyen_mon
        )
        db.session.add(teacher)
    
    db.session.commit()
    
    # 6. Tạo Học phần
    print("📚 Tạo Học phần...")
    hocphan_data = [
        ('IT001', 'Nhập môn lập trình', 3, 45, 'KTPM'),
        ('IT002', 'Cơ sở dữ liệu', 3, 45, 'KTPM'),
        ('IT003', 'Lập trình web', 4, 60, 'KTPM'),
        ('IT004', 'Mạng máy tính', 3, 45, 'HTTT'),
        ('IT005', 'Phát triển ứng dụng di động', 4, 60, 'HTTT'),
        ('EC001', 'Kinh tế vi mô', 3, 45, 'QTKD'),
        ('EC002', 'Kinh tế vĩ mô', 3, 45, 'QTKD'),
        ('EN001', 'Tiếng Anh cơ bản', 2, 30, 'TA'),
        ('EN002', 'Tiếng Anh nâng cao', 3, 45, 'TA')
    ]
    
    for ma_hp, ten_hp, so_dvht, so_tiet, ma_nganh in hocphan_data:
        hocphan = HocPhan(
            ma_hp=ma_hp, ten_hp=ten_hp, so_dvht=so_dvht,
            ma_nganh=ma_nganh
        )
        db.session.add(hocphan)
    
    db.session.commit()
    
    # 7. Tạo Sinh viên
    print("👨‍🎓 Tạo Sinh viên...")
    students_data = [
        ('SV001', 'Nguyễn Thành Nam', 'nam', '2003-01-15', '0981234567', 'nam.nguyen@student.edu.vn', 'TP.HCM', 'KTPM2021A'),
        ('SV002', 'Trần Thị Hương', 'nữ', '2003-03-20', '0987654321', 'huong.tran@student.edu.vn', 'Hà Nội', 'KTPM2021A'),
        ('SV003', 'Lê Văn Đức', 'nam', '2003-05-10', '0912345678', 'duc.le@student.edu.vn', 'Đà Nẵng', 'KTPM2021B'),
        ('SV004', 'Phạm Thị Mai', 'nữ', '2003-07-25', '0918765432', 'mai.pham@student.edu.vn', 'TP.HCM', 'HTTT2021A'),
        ('SV005', 'Hoàng Văn Tuấn', 'nam', '2003-09-12', '0923456789', 'tuan.hoang@student.edu.vn', 'Hà Nội', 'KTPM2021A'),
        ('SV006', 'Nguyễn Thị Lan', 'nữ', '2003-11-08', '0934567890', 'lan.nguyen@student.edu.vn', 'TP.HCM', 'QTKD2021A'),
        ('SV007', 'Trần Văn Hải', 'nam', '2003-02-14', '0945678901', 'hai.tran@student.edu.vn', 'Hà Nội', 'TA2021A'),
        ('SV008', 'Lê Thị Thu', 'nữ', '2003-04-18', '0956789012', 'thu.le@student.edu.vn', 'Đà Nẵng', 'KTPM2021B'),
        ('SV009', 'Phạm Văn Long', 'nam', '2003-06-22', '0967890123', 'long.pham@student.edu.vn', 'TP.HCM', 'HTTT2021A'),
        ('SV010', 'Hoàng Thị Linh', 'nữ', '2003-08-16', '0978901234', 'linh.hoang@student.edu.vn', 'Hà Nội', 'QTKD2021A')
    ]
    
    for ma_sv, ho_ten, gioi_tinh, ngay_sinh, sdt, email, dia_chi, ma_lop in students_data:
        student = Student(
            ma_sv=ma_sv, ho_ten=ho_ten, gioi_tinh=gioi_tinh,
            ngay_sinh=ngay_sinh, dia_chi=dia_chi, ma_lop=ma_lop
        )
        db.session.add(student)
    
    db.session.commit()
    
    # 8. Tạo Điểm thành phần
    print("📊 Tạo Điểm thành phần...")
    import random
    
    subjects = ['IT001', 'IT002', 'IT003', 'EC001', 'EN001']
    students = ['SV001', 'SV002', 'SV003', 'SV004', 'SV005', 'SV006', 'SV007', 'SV008', 'SV009', 'SV010']
    teachers = ['GV001', 'GV002', 'GV003', 'GV004', 'GV005']
    
    for ma_sv in students:
        for ma_hp in subjects[:3]:  # Mỗi SV có 3 môn
            teacher = random.choice(teachers)
            
            # Random điểm trong khoảng hợp lý
            diem_cc = round(random.uniform(6.0, 10.0), 1)
            diem_bt = round(random.uniform(5.0, 9.5), 1)
            diem_gk = round(random.uniform(4.0, 9.0), 1)
            
            diem_tp = DiemThanhPhan(
                ma_sv=ma_sv, ma_hp=ma_hp, ma_gv=teacher,
                diem_chuyen_can=diem_cc, diem_bai_tap=diem_bt, diem_giua_ky=diem_gk,
                hoc_ky='1', nam_hoc='2024-2025'
            )
            db.session.add(diem_tp)
    
    db.session.commit()
    
    # 9. Tạo Điểm cuối kỳ
    print("🎯 Tạo Điểm cuối kỳ...")
    
    for ma_sv in students:
        for ma_hp in subjects[:3]:  # Mỗi SV có 3 môn
            # Lấy điểm thành phần
            diem_tp_record = db.session.query(DiemThanhPhan).filter_by(ma_sv=ma_sv, ma_hp=ma_hp).first()
            if diem_tp_record:
                diem_tp_avg = (diem_tp_record.diem_chuyen_can + diem_tp_record.diem_bai_tap + diem_tp_record.diem_giua_ky) / 3
                
                # Random điểm cuối kỳ
                diem_ck = round(random.uniform(3.0, 9.5), 1)
                
                # Tính điểm tổng kết (30% TP + 70% CK)
                diem_tk = round(diem_tp_avg * 0.3 + diem_ck * 0.7, 1)
                
                # Xác định điểm chữ
                if diem_tk >= 9.0:
                    diem_chu = 'A'
                elif diem_tk >= 8.5:
                    diem_chu = 'B+'
                elif diem_tk >= 8.0:
                    diem_chu = 'B'
                elif diem_tk >= 7.0:
                    diem_chu = 'C+'
                elif diem_tk >= 6.5:
                    diem_chu = 'C'
                elif diem_tk >= 5.5:
                    diem_chu = 'D+'
                elif diem_tk >= 5.0:
                    diem_chu = 'D'
                else:
                    diem_chu = 'F'
                
                grade = Grade(
                    ma_sv=ma_sv, ma_hp=ma_hp,
                    diem_hp=diem_tk, ma_gv=diem_tp_record.ma_gv
                )
                db.session.add(grade)
    
    db.session.commit()
    
    # 10. Tạo SinhVienStats cho ML
    print("🤖 Tạo SinhVienStats...")
    
    for ma_sv in students:
        # Tính GPA và số môn trượt
        grades = db.session.query(Grade).filter_by(ma_sv=ma_sv).all()
        
        total_points = sum(g.diem_hp for g in grades)
        gpa = round(total_points / len(grades), 2) if grades else 0
        
        failed_subjects = sum(1 for g in grades if g.diem_hp < 5.0)
        
        stats = SinhVienStats(
            ma_sv=ma_sv,
            gpa_hien_tai=gpa,
            so_mon_da_truot=failed_subjects
        )
        db.session.add(stats)
    
    db.session.commit()
    
    print("✅ Hoàn thành tạo dữ liệu mẫu!")
    print(f"📊 Thống kê:")
    print(f"   👤 Users: {db.session.query(User).count()}")
    print(f"   🏢 Khoa: {db.session.query(Khoa).count()}")
    print(f"   🎓 Ngành: {db.session.query(Nganh).count()}")
    print(f"   🏫 Lớp: {db.session.query(Lop).count()}")
    print(f"   👨‍🏫 Giáo viên: {db.session.query(Teacher).count()}")
    print(f"   📚 Học phần: {db.session.query(HocPhan).count()}")
    print(f"   👨‍🎓 Sinh viên: {db.session.query(Student).count()}")
    print(f"   📝 Điểm thành phần: {db.session.query(DiemThanhPhan).count()}")
    print(f"   🎯 Điểm cuối kỳ: {db.session.query(Grade).count()}")
    print(f"   🤖 SinhVienStats: {db.session.query(SinhVienStats).count()}")

def main():
    app = create_app()
    
    with app.app_context():
        print("🚀 Bắt đầu reset và tạo dữ liệu mẫu...")
        
        try:
            # Xóa tất cả dữ liệu cũ
            clear_all_data()
            
            # Tạo dữ liệu mẫu mới
            create_sample_data()
            
            print("🎉 Hoàn thành! Database đã được reset và tạo dữ liệu mẫu mới.")
            
        except Exception as e:
            print(f"❌ Lỗi: {e}")
            db.session.rollback()

if __name__ == '__main__':
    main()
