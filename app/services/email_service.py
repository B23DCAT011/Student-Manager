# app/services/email_service.py
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Dict
import logging
from datetime import datetime
from core.config import Config

class EmailService:
    """Service for sending emails using SMTP."""

    def __init__(self):
        self.smtp_server = Config.SMTP_SERVER
        self.smtp_port = Config.SMTP_PORT
        self.email_username = Config.EMAIL_USERNAME
        self.email_password = Config.EMAIL_PASSWORD

    def send_email(self, to_email: str, subject: str, body: str) -> bool:
        """Send an email with the specified subject and body."""
        try:
            msg = MIMEMultipart()
            msg['From'] = self.email_username  # Sử dụng email từ config
            msg['To'] = to_email
            msg['Subject'] = subject

            msg.attach(MIMEText(body, 'plain', 'utf-8'))  # Thêm encoding UTF-8

            # Debug info
            print(f"SMTP Server: {self.smtp_server}")
            print(f"SMTP Port: {self.smtp_port}")
            print(f"Email Username: {self.email_username}")
            print(f"Sending to: {to_email}")
            print(f"Subject: {subject}")

            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.set_debuglevel(1)  # Bật debug mode
                server.starttls()  # Upgrade to secure connection
                server.login(self.email_username, self.email_password)
                text = msg.as_string()
                server.sendmail(self.email_username, [to_email], text)

            logging.info(f"Email sent successfully to {to_email} at {datetime.now()}")
            print(f"✅ Email sent successfully to {to_email}")
            return True
        except Exception as e:
            logging.error(f"Failed to send email: {e}")
            print(f"❌ Failed to send email: {e}")
            return False

    def send_bulk_warning(self, teacher_info: Dict, student_list: list, warning_type: str) -> bool:
        """Send bulk warning emails to students."""
        subject = f"Warning from {teacher_info['ho_ten']}"
        body = f"Dear Student,\n\nYou have received a {warning_type} warning.\n\nBest regards,\n{teacher_info['ho_ten']}"

        for student in student_list:
            if not self.send_email(student['email'], subject, body):
                logging.error(f"Failed to send bulk warning email to {student['email']}")
                return False
        return True
