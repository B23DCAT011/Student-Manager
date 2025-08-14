#!/usr/bin/env python3
"""
Script để hash tất cả passwords plain text trong database
"""
import sys
import os

# Add project root to path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

from app.models.user import User
from core.database import db
from main import app

def hash_existing_passwords():
    """Hash tất cả passwords plain text"""
    with app.app_context():
        try:
            # Lấy tất cả users
            users = User.query.all()
            updated_count = 0

            print("🔍 Checking existing passwords...")

            for user in users:
                # Kiểm tra nếu password chưa được hash
                if not user.password.startswith('$'):
                    print(f"📝 Hashing password for user: {user.username}")

                    # Lưu plain password trước khi hash
                    plain_password = user.password

                    # Hash password
                    user.set_password(plain_password)
                    updated_count += 1

                    print(f"   ✅ {user.username}: {plain_password} → [HASHED]")
                else:
                    print(f"   ⏭️ {user.username}: Already hashed")

            # Commit changes
            if updated_count > 0:
                db.session.commit()
                print(f"\n✅ Successfully hashed {updated_count} passwords!")
            else:
                print(f"\n📌 No passwords needed hashing")

        except Exception as e:
            print(f"❌ Error: {e}")
            db.session.rollback()

if __name__ == '__main__':
    print("🔐 Password Hashing Script")
    print("=" * 30)

    # Confirmation
    confirm = input("⚠️  This will hash all plain text passwords. Continue? (y/N): ")
    if confirm.lower() == 'y':
        hash_existing_passwords()
    else:
        print("❌ Operation cancelled")
