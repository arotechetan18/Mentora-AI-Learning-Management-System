# add_admin.py
from app.core.database import SessionLocal
from app.models.user import User
from passlib.context import CryptContext

def create_admin():
    db = SessionLocal()
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    
    # Check if admin already exists
    admin = db.query(User).filter(User.email == "admin@example.com").first()
    if not admin:
        admin = User(
            email="admin@example.com",
            full_name="Admin User",
            hashed_password=pwd_context.hash("admin123"),
            role="ADMIN",
            is_active=True
        )
        db.add(admin)
        db.commit()
        print("✅ Admin user created!")
        print("Email: admin@example.com")
        print("Password: admin123")
    else:
        print("ℹ️ Admin user already exists.")
    db.close()

if __name__ == "__main__":
    create_admin()