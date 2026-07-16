from app.core.database import SessionLocal
from app.models.course import Course
from app.models.user import User
from passlib.context import CryptContext
from datetime import datetime
from sqlalchemy import func

def seed_database():
    db = SessionLocal()
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    
    print("=" * 50)
    print("🌱 SEEDING DATABASE")
    print("=" * 50)
    
    # 1. Create Admin User
    print("\n👤 Checking admin user...")
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
        print("✅ Admin created: admin@example.com / admin123")
    else:
        print("ℹ️ Admin already exists")
    
    # 2. Delete existing courses
    print("\n🗑️ Deleting existing courses...")
    deleted = db.query(Course).delete()
    db.commit()
    print(f"✅ Deleted {deleted} existing courses")
    
    # 3. Add fresh courses
    print("\n📚 Adding courses...")
    
    courses = [
        {
            "title": "Python Programming for Beginners",
            "description": "Learn Python from scratch with real-world projects.",
            "category": "Programming",
            "difficulty": "BEGINNER",
            "instructor": "Dr. Python",
            "price": 0.00,
            "duration": 10
        },
        {
            "title": "Full Stack Web Development",
            "description": "Master HTML, CSS, JavaScript, React, Node.js, and MongoDB.",
            "category": "Web Development",
            "difficulty": "INTERMEDIATE",
            "instructor": "Web Master",
            "price": 49.99,
            "duration": 25
        },
        {
            "title": "Data Science Masterclass",
            "description": "Complete data science course with Python, Pandas, NumPy, and ML.",
            "category": "Data Science",
            "difficulty": "ADVANCED",
            "instructor": "Data Scientist",
            "price": 99.99,
            "duration": 35
        },
        {
            "title": "JavaScript Complete Guide",
            "description": "Master JavaScript ES6+, DOM manipulation, and modern frameworks.",
            "category": "Programming",
            "difficulty": "BEGINNER",
            "instructor": "JS Ninja",
            "price": 0.00,
            "duration": 15
        },
        {
            "title": "Machine Learning A-Z",
            "description": "Learn all ML algorithms from basics to advanced.",
            "category": "Machine Learning",
            "difficulty": "BEGINNER_TO_ADVANCED",
            "instructor": "AI Expert",
            "price": 149.99,
            "duration": 40
        },
        {
            "title": "React Native Mobile Apps",
            "description": "Build cross-platform mobile apps with React Native.",
            "category": "Mobile Development",
            "difficulty": "INTERMEDIATE",
            "instructor": "Mobile Dev",
            "price": 79.99,
            "duration": 25
        },
        {
            "title": "DevOps with Docker & Kubernetes",
            "description": "Learn containerization, CI/CD, and orchestration.",
            "category": "DevOps",
            "difficulty": "ADVANCED",
            "instructor": "DevOps Engineer",
            "price": 129.99,
            "duration": 35
        },
        {
            "title": "UI/UX Design Fundamentals",
            "description": "Learn design principles, Figma, and prototyping.",
            "category": "Design",
            "difficulty": "BEGINNER",
            "instructor": "Design Expert",
            "price": 39.99,
            "duration": 20
        },
        {
            "title": "Blockchain & Cryptocurrency",
            "description": "Understand blockchain, Bitcoin, Ethereum, and smart contracts.",
            "category": "Blockchain",
            "difficulty": "INTERMEDIATE",
            "instructor": "Blockchain Expert",
            "price": 89.99,
            "duration": 28
        },
        {
            "title": "Artificial Intelligence Basics",
            "description": "Introduction to AI, neural networks, NLP, and computer vision.",
            "category": "AI",
            "difficulty": "BEGINNER_TO_ADVANCED",
            "instructor": "AI Researcher",
            "price": 59.99,
            "duration": 30
        }
    ]
    
    for c in courses:
        course = Course(
            title=c["title"],
            description=c["description"],
            category=c["category"],
            difficulty=c["difficulty"],
            instructor=c["instructor"],
            price=c["price"],
            duration=c["duration"],
            created_at=datetime.now()
        )
        db.add(course)
        print(f"  ✅ Added: {c['title']} ({c['difficulty']})")
    
    db.commit()
    print(f"\n✅ Successfully added {len(courses)} courses!")
    
    # 4. Summary
    print("\n" + "=" * 50)
    print("📊 DATABASE SUMMARY")
    print("=" * 50)
    print(f"👤 Users: {db.query(User).count()}")
    print(f"📚 Courses: {db.query(Course).count()}")
    
    breakdown = db.query(Course.difficulty, func.count()).group_by(Course.difficulty).all()
    print("\n📈 Difficulty Breakdown:")
    for diff, count in breakdown:
        print(f"  - {diff}: {count}")
    
    db.close()
    print("\n🎉 Database seeding complete!")
    print("=" * 50)

if __name__ == "__main__":
    seed_database()