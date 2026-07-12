import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.core.database import SessionLocal
from app.models.course import Course
from app.models.module import Module
from app.models.lesson import Lesson
from app.models.quiz_question import QuizQuestion
from app.models.user import User

def seed_courses():
    db = SessionLocal()
    
    try:
        instructor = db.query(User).filter(User.email == "admin@example.com").first()
        if not instructor:
            print("❌ Admin not found! Run register first.")
            return
        
        # ============================================
        # COURSE 1: BASIC PYTHON
        # ============================================
        python_course = Course(
            title="Basic Python Programming",
            description="Learn Python from scratch with real-world examples",
            category="Programming",
            difficulty="beginner",
            duration=30,
            instructor_id=instructor.id,
            price=1999,
            is_published=True
        )
        db.add(python_course)
        db.commit()
        
        python_modules = [
            {
                "title": "Getting Started with Python",
                "description": "Python basics and setup",
                "order": 1,
                "lessons": [
                    {
                        "title": "What is Python?",
                        "description": "Introduction to Python",
                        "concept": """# What is Python?
Python is a high-level, interpreted programming language.
- Created by Guido van Rossum in 1991
- Easy to learn and read
- Used in: Web, AI, Data Science, Automation

## Key Features:
1. Simple syntax
2. Dynamic typing
3. Large standard library
4. Cross-platform""",
                        "example": """# Hello World in Python
print("Hello, World!")

# Variable examples
name = "Alice"
age = 25
height = 5.6
is_student = True

print(f"Name: {name}, Age: {age}")""",
                        "interview_questions": """1. What is Python and why is it popular?
2. What are the key features of Python?
3. Explain Python's dynamic typing.""",
                        "duration": 20,
                        "order": 1,
                        "quiz": [
                            {
                                "question": "Who created Python?",
                                "options": ["Guido van Rossum", "James Gosling", "Bjarne Stroustrup", "Dennis Ritchie"],
                                "correct_answer": 0,
                                "explanation": "Python was created by Guido van Rossum in 1991."
                            },
                            {
                                "question": "Which of the following is a valid Python variable name?",
                                "options": ["1name", "name-1", "_name", "def"],
                                "correct_answer": 2,
                                "explanation": "_name is valid. Variables can't start with number or contain -."
                            },
                            {
                                "question": "What is the output of print(type(10))?",
                                "options": ["<class 'int'>", "<class 'float'>", "<class 'str'>", "<class 'bool'>"],
                                "correct_answer": 0,
                                "explanation": "10 is an integer, so type is int."
                            }
                        ]
                    }
                ]
            },
            {
                "title": "Python Data Structures",
                "description": "Lists, Tuples, Dictionaries, Sets",
                "order": 2,
                "lessons": [
                    {
                        "title": "Lists in Python",
                        "description": "Working with lists",
                        "concept": """# Lists in Python
A list is a collection of items in a specific order.

## Creating Lists:
fruits = ["apple", "banana", "orange"]
numbers = [1, 2, 3, 4, 5]
mixed = [1, "hello", 3.14, True]

## List Operations:
- Append: fruits.append("grape")
- Insert: fruits.insert(1, "mango")
- Remove: fruits.remove("banana")
- Index: fruits[0]  # apple
- Slice: fruits[1:3]
- Length: len(fruits)""",
                        "example": """# Shopping List Example
shopping_list = ["milk", "bread", "eggs"]

# Add items
shopping_list.append("butter")
shopping_list.insert(1, "cheese")
print(shopping_list)  # ['milk', 'cheese', 'bread', 'eggs', 'butter']

# Remove items
shopping_list.remove("bread")
print(shopping_list)  # ['milk', 'cheese', 'eggs', 'butter']

# Loop through list
for item in shopping_list:
    print(f"Buy: {item}")

# Check if item exists
if "milk" in shopping_list:
    print("Milk is in the list")""",
                        "interview_questions": """1. What is a list in Python?
2. How do you add and remove elements from a list?
3. What is list slicing?""",
                        "duration": 20,
                        "order": 1,
                        "quiz": [
                            {
                                "question": "Which method is used to add an item to the end of a list?",
                                "options": ["insert()", "append()", "add()", "extend()"],
                                "correct_answer": 1,
                                "explanation": "append() adds an item to the end of a list."
                            },
                            {
                                "question": "What is the output of len([1, 2, 3, 4])?",
                                "options": ["3", "4", "5", "6"],
                                "correct_answer": 1,
                                "explanation": "len() returns the number of items in the list."
                            }
                        ]
                    }
                ]
            },
            {
                "title": "Control Flow",
                "description": "If-Else, Loops, Functions",
                "order": 3,
                "lessons": [
                    {
                        "title": "Functions in Python",
                        "description": "Creating and using functions",
                        "concept": """# Functions in Python
A function is a block of reusable code.

## Defining a Function:
def function_name(parameters):
    # code block
    return value

## Example:
def greet(name):
    return f"Hello, {name}!"

# Calling a function
result = greet("Alice")
print(result)  # Hello, Alice!

## Types of Arguments:
1. Positional arguments: greet("Alice")
2. Keyword arguments: greet(name="Alice")
3. Default arguments: def greet(name="Guest")""",
                        "example": """# Calculator using functions
def add(a, b):
    return a + b

def subtract(a, b):
    return a - b

def multiply(a, b):
    return a * b

def divide(a, b):
    if b == 0:
        return "Cannot divide by zero"
    return a / b

# Using the functions
print(add(10, 5))      # 15
print(subtract(10, 5)) # 5
print(multiply(10, 5)) # 50
print(divide(10, 0))   # Cannot divide by zero""",
                        "interview_questions": """1. What is a function in Python?
2. Explain different types of arguments in Python functions.
3. What is the difference between return and print?""",
                        "duration": 20,
                        "order": 1,
                        "quiz": [
                            {
                                "question": "Which keyword is used to define a function in Python?",
                                "options": ["function", "def", "define", "func"],
                                "correct_answer": 1,
                                "explanation": "def is used to define a function in Python."
                            },
                            {
                                "question": "What is the output of def add(a, b): return a + b; print(add(2, 3))?",
                                "options": ["2", "3", "5", "6"],
                                "correct_answer": 2,
                                "explanation": "2 + 3 = 5."
                            }
                        ]
                    }
                ]
            }
        ]
        
        for mod_data in python_modules:
            module = Module(
                course_id=python_course.id,
                title=mod_data["title"],
                description=mod_data["description"],
                order=mod_data["order"]
            )
            db.add(module)
            db.commit()
            
            for lesson_data in mod_data["lessons"]:
                lesson = Lesson(
                    module_id=module.id,
                    title=lesson_data["title"],
                    description=lesson_data["description"],
                    concept=lesson_data["concept"],
                    example=lesson_data["example"],
                    interview_questions=lesson_data["interview_questions"],
                    duration=lesson_data["duration"],
                    order=lesson_data["order"]
                )
                db.add(lesson)
                db.commit()
                
                for quiz_data in lesson_data.get("quiz", []):
                    quiz = QuizQuestion(
                        lesson_id=lesson.id,
                        question=quiz_data["question"],
                        options=quiz_data["options"],
                        correct_answer=quiz_data["correct_answer"],
                        explanation=quiz_data["explanation"]
                    )
                    db.add(quiz)
                db.commit()
        
        print("✅ Python Course seeded successfully!")

        # ============================================
        # COURSE 2: CORE JAVA
        # ============================================
        java_course = Course(
            title="Core Java Programming",
            description="Master Java fundamentals with real-world examples",
            category="Programming",
            difficulty="beginner",
            duration=35,
            instructor_id=instructor.id,
            price=2499,
            is_published=True
        )
        db.add(java_course)
        db.commit()
        
        java_modules = [
            {
                "title": "Getting Started with Java",
                "description": "Java basics and setup",
                "order": 1,
                "lessons": [
                    {
                        "title": "Why Programming?",
                        "description": "Understanding programming importance",
                        "concept": """# Why Programming?
Programming is the process of creating instructions for computers.

## Why Learn Programming?
1. **Automation**: Automate repetitive tasks
2. **Problem Solving**: Develop logical thinking
3. **Innovation**: Build new technology
4. **Career**: High demand in all industries

## Real-world Applications:
- Banking apps
- E-commerce websites
- Healthcare systems
- AI and Machine Learning""",
                        "example": """# Real-world programming examples

## Banking System
- Check balance
- Transfer money
- Pay bills
- Track transactions

## E-Commerce
- Product search
- Cart management
- Payment processing
- Order tracking

## Healthcare
- Patient records
- Appointment scheduling
- Medical equipment control""",
                        "interview_questions": """1. Why is programming important?
2. What are the applications of programming?
3. Which industries use programming?""",
                        "duration": 25,
                        "order": 1,
                        "quiz": [
                            {
                                "question": "What is programming?",
                                "options": ["Creating instructions for computers", "A type of exercise", "A programming language", "A type of computer"],
                                "correct_answer": 0,
                                "explanation": "Programming is creating instructions for computers."
                            },
                            {
                                "question": "Which industry uses programming?",
                                "options": ["Banking", "E-commerce", "Healthcare", "All of the above"],
                                "correct_answer": 3,
                                "explanation": "All industries use programming."
                            }
                        ]
                    },
                    {
                        "title": "What is Java?",
                        "description": "Introduction to Java",
                        "concept": """# What is Java?
Java is a high-level, object-oriented programming language.

## Key Features:
1. Platform Independent (Write Once, Run Anywhere)
2. Object-Oriented
3. Secure
4. Robust
5. Large Community

## Java Versions:
- Java 8 (LTS) - Most popular
- Java 11 (LTS)
- Java 17 (LTS) - Latest LTS
- Java 21 (LTS)

## Java Editions:
- Java SE - Standard Edition
- Java EE - Enterprise Edition
- Java ME - Micro Edition""",
                        "example": """# Hello World in Java
public class HelloWorld {
    public static void main(String[] args) {
        System.out.println("Hello, World!");
    }
}

# Variable examples
public class Variables {
    public static void main(String[] args) {
        String name = "Alice";
        int age = 25;
        double height = 5.6;
        boolean isStudent = true;
        
        System.out.println("Name: " + name);
        System.out.println("Age: " + age);
    }
}""",
                        "interview_questions": """1. What is Java?
2. What are the key features of Java?
3. Explain WORA in Java.""",
                        "duration": 25,
                        "order": 1,
                        "quiz": [
                            {
                                "question": "Who created Java?",
                                "options": ["Guido van Rossum", "James Gosling", "Bjarne Stroustrup", "Dennis Ritchie"],
                                "correct_answer": 1,
                                "explanation": "Java was created by James Gosling at Sun Microsystems."
                            },
                            {
                                "question": "What does JVM stand for?",
                                "options": ["Java Virtual Machine", "Java Variable Machine", "Java View Machine", "Java Version Machine"],
                                "correct_answer": 0,
                                "explanation": "JVM stands for Java Virtual Machine."
                            }
                        ]
                    },
                    {
                        "title": "Variables & Data Types in Java",
                        "description": "Understanding variables and data types",
                        "concept": """# Variables & Data Types in Java
A variable is a container that holds data.

## Primitive Data Types:
1. `int` - whole numbers (10, -5, 100)
2. `double` - decimal numbers (10.5, 3.14)
3. `boolean` - true/false
4. `char` - single character ('A', 'b')
5. `byte`, `short`, `long`, `float`

## Non-Primitive Data Types:
1. `String` - text ("Hello")
2. `Array` - collection of values
3. `Class` - user-defined type

## Variable Declaration:
```java
int age = 25;
double price = 99.99;
boolean isActive = true;
char grade = 'A';
String name = "John";
```""",
                        "example": """# Student Management System
public class Student {
    public static void main(String[] args) {
        // Student data
        int rollNumber = 101;
        String studentName = "Alice";
        double marks = 85.5;
        char grade = 'A';
        boolean isPass = true;
        
        System.out.println("Roll: " + rollNumber);
        System.out.println("Name: " + studentName);
        System.out.println("Marks: " + marks);
        System.out.println("Grade: " + grade);
        System.out.println("Pass: " + isPass);
    }
}

# Banking System
public class BankAccount {
    public static void main(String[] args) {
        int balance = 5000;
        double interestRate = 7.5;
        String accountHolder = "John Doe";
        boolean isActive = true;
        
        System.out.println("Balance: " + balance);
        System.out.println("Interest Rate: " + interestRate);
    }
}""",
                        "interview_questions": """1. What are the different data types in Java?
2. Explain primitive vs non-primitive data types.
3. What is type casting in Java?""",
                        "duration": 30,
                        "order": 1,
                        "quiz": [
                            {
                                "question": "Which data type is used for true/false values in Java?",
                                "options": ["int", "double", "boolean", "char"],
                                "correct_answer": 2,
                                "explanation": "boolean is used for true/false values."
                            },
                            {
                                "question": "Which is a valid integer variable declaration?",
                                "options": ["int x = 10.5;", "int x = 10;", "int x = '10';", "int x = true;"],
                                "correct_answer": 1,
                                "explanation": "int x = 10; is correct."
                            }
                        ]
                    }
                ]
            },
            {
                "title": "Object-Oriented Programming",
                "description": "OOP concepts in Java",
                "order": 2,
                "lessons": [
                    {
                        "title": "Classes & Objects",
                        "description": "Understanding classes and objects",
                        "concept": """# Classes & Objects in Java
A **class** is a blueprint for creating objects.

## Class Structure:
```java
public class Car {
    // Properties (Attributes)
    String brand;
    String model;
    int year;
    
    // Methods (Behavior)
    void start() {
        System.out.println("Car started");
    }
    
    void stop() {
        System.out.println("Car stopped");
    }
} Car myCar = new Car();
myCar.brand = "Toyota";
myCar.model = "Camry";
myCar.year = 2024;
myCar.start();
```""",
                        "example": """# Student Class Example
public class Student {
    // Attributes
    int rollNumber;
    String name;
    double marks;
    
    // Constructor
    Student(int roll, String name, double marks) {
        this.rollNumber = roll;
        this.name = name;
        this.marks = marks;
    }
    
    // Method
    void displayInfo() {
        System.out.println("Roll: " + rollNumber);
        System.out.println("Name: " + name);
        System.out.println("Marks: " + marks);
    }
    
    public static void main(String[] args) {
        Student s1 = new Student(101, "Alice", 85.5);
        Student s2 = new Student(102, "Bob", 78.0);
        
        s1.displayInfo();
        s2.displayInfo();
    }
}""",
                        "interview_questions": """1. What is a class in Java?
2. What is an object in Java?
3. Explain the difference between class and object.""",
                        "duration": 30,
                        "order": 1,
                        "quiz": [
                            {
                                "question": "What is a class in Java?",
                                "options": ["A blueprint for objects", "An instance of an object", "A variable", "A method"],
                                "correct_answer": 0,
                                "explanation": "A class is a blueprint for creating objects."
                            },
                            {
                                "question": "Which keyword is used to create an object in Java?",
                                "options": ["create", "object", "new", "class"],
                                "correct_answer": 2,
                                "explanation": "new keyword is used to create an object."
                            }
                        ]
                    }
                ]
            },
            {
                "title": "Advanced Java",
                "description": "Exception Handling, Packages, Recursion",
                "order": 3,
                "lessons": [
                    {
                        "title": "Exception Handling",
                        "description": "Handling errors in Java",
                        "concept": """# Exception Handling in Java
Exceptions are unexpected events that occur during program execution.

## Types of Exceptions:
1. **Checked Exceptions** - Compile-time (e.g., IOException)
2. **Unchecked Exceptions** - Runtime (e.g., NullPointerException)
3. **Errors** - Serious problems (e.g., OutOfMemoryError)

## Try-Catch Block:
```java
try {
    // Code that may cause exception
    int result = 10 / 0;
} catch (ArithmeticException e) {
    System.out.println("Cannot divide by zero");
} finally {
    System.out.println("This always executes");
}
```""",
                        "example": """# Bank Account Exception Example
public class BankAccount {
    int balance = 5000;
    
    void withdraw(int amount) {
        try {
            if (amount > balance) {
                throw new IllegalArgumentException("Insufficient balance");
            }
            balance -= amount;
            System.out.println("Withdrawal successful. Balance: " + balance);
        } catch (IllegalArgumentException e) {
            System.out.println("Error: " + e.getMessage());
        } finally {
            System.out.println("Transaction completed");
        }
    }
    
    public static void main(String[] args) {
        BankAccount account = new BankAccount();
        account.withdraw(3000);  // Success
        account.withdraw(5000);  // Error
    }
}""",
                        "interview_questions": """1. What is exception handling in Java?
2. Explain checked vs unchecked exceptions.
3. What is the difference between throw and throws?""",
                        "duration": 30,
                        "order": 1,
                        "quiz": [
                            {
                                "question": "Which block is used to handle exceptions in Java?",
                                "options": ["try-catch", "if-else", "switch", "for"],
                                "correct_answer": 0,
                                "explanation": "try-catch block handles exceptions."
                            },
                            {
                                "question": "What is the output of try { int x = 10/0; } catch (ArithmeticException e) { System.out.println('Error'); }",
                                "options": ["10", "0", "Error", "Exception"],
                                "correct_answer": 2,
                                "explanation": "ArithmeticException is caught and 'Error' is printed."
                            }
                        ]
                    }
                ]
            }
        ]
        
        for mod_data in java_modules:
            module = Module(
                course_id=java_course.id,
                title=mod_data["title"],
                description=mod_data["description"],
                order=mod_data["order"]
            )
            db.add(module)
            db.commit()
            
            for lesson_data in mod_data["lessons"]:
                lesson = Lesson(
                    module_id=module.id,
                    title=lesson_data["title"],
                    description=lesson_data["description"],
                    concept=lesson_data["concept"],
                    example=lesson_data["example"],
                    interview_questions=lesson_data["interview_questions"],
                    duration=lesson_data["duration"],
                    order=lesson_data["order"]
                )
                db.add(lesson)
                db.commit()
                
                for quiz_data in lesson_data.get("quiz", []):
                    quiz = QuizQuestion(
                        lesson_id=lesson.id,
                        question=quiz_data["question"],
                        options=quiz_data["options"],
                        correct_answer=quiz_data["correct_answer"],
                        explanation=quiz_data["explanation"]
                    )
                    db.add(quiz)
                db.commit()
        
        print("✅ Java Course seeded successfully!")
        print("=" * 50)
        print("📊 Summary:")
        print(f"   - Python Course: {len(python_course.modules)} modules")
        print(f"   - Java Course: {len(java_course.modules)} modules")
        print("✅ All courses seeded successfully!")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    seed_courses()