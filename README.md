# Student Manager

Ứng dụng quản lý sinh viên được xây dựng bằng Flask với các tính năng quản lý thông tin sinh viên, điểm số và tích hợp AI.

## Tính năng

- 👥 Quản lý thông tin sinh viên
- 📊 Quản lý điểm số và kết quả học tập
- 🔐 Hệ thống đăng nhập và phân quyền
- 🤖 Tích hợp Gemini AI để hỗ trợ
- 📧 Gửi email thông báo
- 📱 Giao diện responsive

## Công nghệ sử dụng

- **Backend**: Flask, SQLAlchemy
- **Database**: MySQL
- **Authentication**: Flask-Login, bcrypt
- **AI**: Google Generative AI (Gemini)
- **Frontend**: HTML, CSS, JavaScript
- **Email**: SMTP

## Cài đặt

### Yêu cầu hệ thống
- Python 3.8+
- MySQL
- Git

### Bước 1: Clone repository
```bash
git clone <repository-url>
cd Student_Manager
```

### Bước 2: Tạo virtual environment
```bash
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac
```

### Bước 3: Cài đặt dependencies
```bash
pip install -r requirements.txt
```

### Bước 4: Cấu hình environment
1. Copy file `.env.example` thành `.env`
2. Cập nhật các thông tin trong file `.env`:
```env
SECRET_KEY=your-secret-key-here
DATABASE_URL=mysql+pymysql://username:password@localhost:3306/student_manager
GEMINI_API_KEY=your-gemini-api-key
EMAIL_USERNAME=your-email@domain.com
EMAIL_PASSWORD=your-email-password
```

### Bước 5: Tạo database
```bash
# Tạo database trong MySQL
CREATE DATABASE student_manager;
```

### Bước 6: Chạy ứng dụng
```bash
python app.py
```

Ứng dụng sẽ chạy tại: `http://localhost:5000`

## Cấu trúc project

```
Student_Manager/
├── app.py                 # File chính của ứng dụng
├── requirements.txt       # Dependencies
├── .env                  # Environment variables (không commit)
├── .env.example          # Template cho environment variables
├── .gitignore           # Git ignore file
├── static/              # CSS, JS, images
├── templates/           # HTML templates
└── README.md           # File này
```

## Environment Variables

| Variable | Mô tả |
|----------|-------|
| `SECRET_KEY` | Khóa bí mật cho Flask session |
| `DATABASE_URL` | URL kết nối database MySQL |
| `GEMINI_API_KEY` | API key cho Google Gemini AI |
| `SMTP_SERVER` | Server SMTP để gửi email |
| `EMAIL_USERNAME` | Username email |
| `EMAIL_PASSWORD` | Password email |

## Sử dụng

1. Truy cập `http://localhost:5000`
2. Đăng ký tài khoản hoặc đăng nhập
3. Bắt đầu quản lý thông tin sinh viên

## Đóng góp

1. Fork repository
2. Tạo feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Mở Pull Request

## License

Distributed under the MIT License. See `LICENSE` for more information.

## Liên hệ

- Email: luuducanh221203@yandex.com
- Project Link: [https://github.com/username/Student_Manager](https://github.com/username/Student_Manager)
