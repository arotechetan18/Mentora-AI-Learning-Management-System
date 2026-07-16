

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
        # PYTHON COURSE - 20 MODULES
        # ============================================
        print("\n📚 Creating Python Course with 20 Modules...")

        python_course = Course(
            title="Python Programming - Zero to Hero",
            description="Complete Python course with 20 modules - from beginner to advanced",
            category="Programming",
         difficulty="INTERMEDIATE",  
            duration=120,
            instructor_id=instructor.id,
            price=9999,
            is_published=True
        )
        db.add(python_course)
        db.commit()
        db.refresh(python_course)
        print(f"✅ Python Course created (ID: {python_course.id})")

        # ==================== 20 PYTHON MODULES ====================
        python_modules = [
            # ===== MODULE 1 =====
            {
                "title": "Module 1: Getting Started with Python",
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
                                "question": "Which is a valid Python variable name?",
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
                    },
                    {
                        "title": "Python Installation",
                        "description": "Setting up Python",
                        "concept": """# Python Installation
## Step 1: Download Python
- Go to python.org
- Download latest version

## Step 2: Install Python
- Run installer
- Check "Add Python to PATH"
- Verify installation""",
                        "example": """# Check Python version
python --version
# Output: Python 3.11.0

# Verify pip
pip --version""",
                        "interview_questions": """1. How do you install Python?
2. What is PATH in Python?
3. How to verify Python installation?""",
                        "duration": 15,
                        "order": 2,
                        "quiz": [
                            {
                                "question": "Which command checks Python version?",
                                "options": ["python --version", "python -v", "python version", "python --v"],
                                "correct_answer": 0,
                                "explanation": "python --version shows the installed Python version."
                            }
                        ]
                    },
                    {
                        "title": "First Python Program",
                        "description": "Hello World",
                        "concept": """# Your First Python Program
```python
print("Hello, World!")
```

## How it works:
- `print()` is a built-in function
- Text inside quotes is printed
- Run the program""",
                        "example": """# Multiple print statements
print("Hello, World!")
print("Welcome to Python!")
print("Let's learn Python!")""",
                        "interview_questions": """1. What is the print() function?
2. How do you write comments in Python?
3. What is the difference between single and double quotes?""",
                        "duration": 10,
                        "order": 3,
                        "quiz": [
                            {
                                "question": "Which function prints output in Python?",
                                "options": ["print()", "output()", "display()", "show()"],
                                "correct_answer": 0,
                                "explanation": "print() is used to display output."
                            }
                        ]
                    }
                ]
            },
            # ===== MODULE 2 =====
            {
                "title": "Module 2: Variables & Data Types",
                "description": "Variables, numbers, strings, booleans",
                "order": 2,
                "lessons": [
                    {
                        "title": "Variables in Python",
                        "description": "Creating and using variables",
                        "concept": """# Variables in Python
A variable is a container for storing data.

## Rules for Variables:
1. Must start with letter or underscore
2. Can contain letters, numbers, underscore
3. Case-sensitive (age ≠ Age)

## Examples:
```python
name = "Alice"      # String
age = 25            # Integer
height = 5.6        # Float
is_student = True   # Boolean
```""",
                        "example": """# Variable Examples
name = "John"
age = 30
city = "Mumbai"
print(f"Name: {name}, Age: {age}, City: {city}")""",
                        "interview_questions": """1. What is a variable in Python?
2. What are the rules for variable names?
3. How do you assign a value to a variable?
4. What is dynamic typing in Python?""",
                        "duration": 20,
                        "order": 1,
                        "quiz": [
                            {
                                "question": "Which is a valid variable name?",
                                "options": ["1name", "_name", "name-1", "name 1"],
                                "correct_answer": 1,
                                "explanation": "_name is valid. Variables can't start with number."
                            }
                        ]
                    },
                    {
                        "title": "Data Types in Python",
                        "description": "int, float, str, bool",
                        "concept": """# Python Data Types

## 1. int (Integer)
Whole numbers: 10, -5, 100

## 2. float (Float)
Decimal numbers: 10.5, 3.14

## 3. str (String)
Text: "Hello", 'World'

## 4. bool (Boolean)
True / False

## Check Type:
```python
type(10)  # <class 'int'>
type(3.14) # <class 'float'>
type("Hello") # <class 'str'>
type(True) # <class 'bool'>
```""",
                        "example": """# Data Type Examples
age = 25          # int
price = 99.99     # float
name = "Python"   # str
is_valid = True   # bool

print(type(age))   # <class 'int'>
print(type(name))  # <class 'str'>
print(type(is_valid)) # <class 'bool'>""",
                        "interview_questions": """1. What are the basic data types in Python?
2. How do you check the type of a variable?
3. What is the difference between int and float?
4. What is the difference between str and int?""",
                        "duration": 20,
                        "order": 2,
                        "quiz": [
                            {
                                "question": "What is the type of 3.14?",
                                "options": ["int", "float", "str", "bool"],
                                "correct_answer": 1,
                                "explanation": "3.14 is a decimal number, so it's a float."
                            }
                        ]
                    },
                    {
                        "title": "Type Conversion",
                        "description": "Converting between data types",
                        "concept": """# Type Conversion
Converting one data type to another.

## int() - Convert to integer
```python
int("10")    # 10
int(3.14)    # 3
int(True)    # 1
```

## float() - Convert to float
```python
float("10.5") # 10.5
float(10)     # 10.0
float(True)   # 1.0
```

## str() - Convert to string
```python
str(10)      # "10"
str(3.14)    # "3.14"
str(True)    # "True"
```

## bool() - Convert to boolean
```python
bool(1)      # True
bool(0)      # False
bool("")     # False
bool("Hello") # True
```""",
                        "example": """# Type Conversion Examples
num_str = "100"
num_int = int(num_str)  # Convert string to int
num_float = float(num_str)  # Convert string to float

print(num_int)    # 100
print(num_float)  # 100.0

# Convert int to string
num = 50
num_str = str(num)  # "50"
print(type(num_str)) # <class 'str'>

# Convert to boolean
print(bool(0))    # False
print(bool(1))    # True
print(bool(""))   # False""",
                        "interview_questions": """1. What is type conversion in Python?
2. How do you convert a string to an integer?
3. What happens if you try to convert invalid data?
4. What is implicit vs explicit type conversion?""",
                        "duration": 15,
                        "order": 3,
                        "quiz": [
                            {
                                "question": "What is the output of int('10.5')?",
                                "options": ["10.5", "10", "Error", "11"],
                                "correct_answer": 2,
                                "explanation": "int('10.5') will raise an error because '10.5' is not a valid integer string."
                            }
                        ]
                    }
                ]
            },
            # ===== MODULE 3 =====
            {
                "title": "Module 3: Operators in Python",
                "description": "Arithmetic, comparison, logical operators",
                "order": 3,
                "lessons": [
                    {
                        "title": "Arithmetic Operators",
                        "description": "+ - * / % // **",
                        "concept": """# Arithmetic Operators

| Operator | Description | Example |
|----------|-------------|---------|
| + | Addition | 5 + 3 = 8 |
| - | Subtraction | 5 - 3 = 2 |
| * | Multiplication | 5 * 3 = 15 |
| / | Division | 5 / 3 = 1.66 |
| % | Modulus | 5 % 3 = 2 |
| // | Floor Division | 5 // 3 = 1 |
| ** | Exponent | 5 ** 3 = 125 |

## Important Notes:
- `/` always returns a float
- `//` returns an integer (floor division)
- `%` returns the remainder
- `**` is power operator""",
                        "example": """# Arithmetic Examples
a = 10
b = 3

print(a + b)   # 13
print(a - b)   # 7
print(a * b)   # 30
print(a / b)   # 3.33
print(a % b)   # 1
print(a // b)  # 3
print(a ** b)  # 1000

# Operator precedence
print(2 + 3 * 4)    # 14 (multiplication first)
print((2 + 3) * 4)  # 20 (parentheses first)""",
                        "interview_questions": """1. What are arithmetic operators in Python?
2. What is the difference between / and //?
3. What does the % operator do?
4. What is operator precedence?""",
                        "duration": 20,
                        "order": 1,
                        "quiz": [
                            {
                                "question": "What is 10 // 3?",
                                "options": ["3.33", "3", "4", "Error"],
                                "correct_answer": 1,
                                "explanation": "// performs floor division, returning the integer part."
                            }
                        ]
                    },
                    {
                        "title": "Comparison Operators",
                        "description": "== != > < >= <=",
                        "concept": """# Comparison Operators

| Operator | Description | Example |
|----------|-------------|---------|
| == | Equal to | 5 == 5 → True |
| != | Not equal to | 5 != 3 → True |
| > | Greater than | 5 > 3 → True |
| < | Less than | 5 < 3 → False |
| >= | Greater than or equal | 5 >= 5 → True |
| <= | Less than or equal | 5 <= 5 → True |

## Returns: True or False
## Used in: if statements, while loops""",
                        "example": """# Comparison Examples
x = 10
y = 20

print(x == y)  # False
print(x != y)  # True
print(x > y)   # False
print(x < y)   # True
print(x >= 10) # True
print(y <= 20) # True

# Chaining comparisons
print(5 < 10 < 20)  # True
print(5 < 10 > 15)  # False""",
                        "interview_questions": """1. What are comparison operators?
2. What is the difference between = and ==?
3. What do comparison operators return?
4. What is chaining comparisons?""",
                        "duration": 15,
                        "order": 2,
                        "quiz": [
                            {
                                "question": "What is the output of 10 > 5?",
                                "options": ["True", "False", "10", "5"],
                                "correct_answer": 0,
                                "explanation": "10 > 5 is True because 10 is greater than 5."
                            }
                        ]
                    },
                    {
                        "title": "Logical Operators",
                        "description": "and, or, not",
                        "concept": """# Logical Operators

## and: Both conditions True
```python
True and True   # True
True and False  # False
False and False # False
```

## or: At least one True
```python
True or True    # True
True or False   # True
False or False  # False
```

## not: Negate condition
```python
not True        # False
not False       # True
```

## Truth Table:
| A | B | A and B | A or B | not A |
|---|---|---------|--------|-------|
| T | T | T | T | F |
| T | F | F | T | F |
| F | T | F | T | T |
| F | F | F | F | T |""",
                        "example": """# Logical Examples
age = 25
is_student = True

# Check if adult and student
if age >= 18 and is_student:
    print("Adult student")

# Check if age is between 10 and 20
if 10 < age < 20:  # Equivalent to age > 10 and age < 20
    print("Age between 10 and 20")
else:
    print("Age not between 10 and 20")

# Check if not student
if not is_student:
    print("Not a student")
else:
    print("Is a student")""",
                        "interview_questions": """1. What are logical operators in Python?
2. What is the difference between and and or?
3. How does the not operator work?
4. What is short-circuit evaluation?""",
                        "duration": 15,
                        "order": 3,
                        "quiz": [
                            {
                                "question": "What is True and False?",
                                "options": ["True", "False", "1", "0"],
                                "correct_answer": 1,
                                "explanation": "True and False is False because and requires both to be True."
                            }
                        ]
                    }
                ]
            },
            # ===== MODULE 4 =====
#               {
#                 "title": "Module 4: Strings in Python",
#                 "description": "String operations, slicing, methods",
#                 "order": 4,
#                 "lessons": [
#                     {
#                         "title": "String Basics",
#                         "description": "Creating and using strings",
#                         "concept": """# Strings in Python
# A string is a sequence of characters.

# ## Creating Strings:
# ```python
# name = "Python"          # Double quotes
# city = 'Mumbai'          # Single quotes
# message = "Hello World"  # String with space
# multi_line = """This is
# a multi-line
# string"""
# ```

# ## String Operations:
# ```python
# len("Python")  # 6
# "Hello" + "World"  # "HelloWorld"
# "Hi " * 3    # "Hi Hi Hi "
# ```""",
#                         "example": """# String Examples
# name = "Python"
# print(name[0])      # P
# print(name[-1])     # n
# print(len(name))    # 6
# print(name + "!" )   # Python!
# print("Hi" * 3)      # HiHiHi

# # String concatenation
# first_name = "John"
# last_name = "Doe"
# full_name = first_name + " " + last_name
# print(full_name)  # John Doe""",
#                         "interview_questions": """1. What is a string in Python?
# 2. How do you concatenate strings?
# 3. How do you find the length of a string?
# 4. What is the difference between single and double quotes?""",
#                         "duration": 20,
#                         "order": 1,
#                         "quiz": [
#                             {
#                                 "question": "What is len('Python')?",
#                                 "options": ["5", "6", "7", "4"],
#                                 "correct_answer": 1,
#                                 "explanation": "Python has 6 characters."
#                             }
#                         ]
#                     },
#                     {
#                         "title": "String Slicing",
#                         "description": "Extracting parts of strings",
#                         "concept": """# String Slicing
# Extract a portion of a string.

# ## Syntax:
# ```python
# string[start:end:step]
# ```
# - start: Starting index (inclusive)
# - end: Ending index (exclusive)
# - step: Step size (default 1)

# ## Examples:
# ```python
# name = "Python Programming"

# # First 6 characters
# name[:6]    # "Python"

# # Last 10 characters
# name[-10:]  # "ogramming"

# # Every 2nd character
# name[::2]   # "Pto rgamn"

# # Reverse string
# name[::-1]  # "gnimmargorP nohtyP"
# ```""",
#                         "example": """# Slicing Examples
# text = "Hello World"

# print(text[0:5])    # Hello
# print(text[6:])     # World
# print(text[-5:])    # World
# print(text[::-1])   # dlroW olleH (Reverse)

# # More examples
# text2 = "PythonProgramming"
# print(text2[0:6])    # Python
# print(text2[6:])     # Programming
# print(text2[::2])    # Pto rgamn""",
#                         "interview_questions": """1. What is string slicing?
# 2. How do you reverse a string in Python?
# 3. What does text[2:5] do?
# 4. What is the difference between text[:5] and text[0:5]?""",
#                         "duration": 15,
#                         "order": 2,
#                         "quiz": [
#                             {
#                                 "question": "What is the output of 'Python'[::-1]?",
#                                 "options": ["nohtyP", "Python", "nohtyP", "P y t h o n"],
#                                 "correct_answer": 0,
#                                 "explanation": "[::-1] reverses the string."
#                             }
#                         ]
#                     },
#                     {
#                         "title": "String Methods",
#                         "description": "upper, lower, strip, split, join",
#                         "concept": """# String Methods

# ## Common Methods:
# ```python
# text = "  Hello World  "

# text.upper()    # "  HELLO WORLD  "
# text.lower()    # "  hello world  "
# text.strip()    # "Hello World"
# text.lstrip()   # "Hello World  "
# text.rstrip()   # "  Hello World"
# text.split()    # ["Hello", "World"]
# ```

# ## join() - Join strings
# ```python
# ", ".join(["a", "b", "c"])  # "a, b, c"
# ```

# ## Other Methods:
# - `find()` - Find substring
# - `replace()` - Replace substring
# - `startswith()` - Check prefix
# - `endswith()` - Check suffix
# - `count()` - Count occurrences
# - `isalpha()` - Check if all alphabets
# - `isdigit()` - Check if all digits
# - `isalnum()` - Check if alphanumeric""",
#                         "example": """# String Methods Examples
# text = "  Python Programming  "

# print(text.upper())      # "  PYTHON PROGRAMMING  "
# print(text.lower())      # "  python programming  "
# print(text.strip())      # "Python Programming"
# print(text.split())      # ["Python", "Programming"]

# # Replace
# print(text.replace("Python", "Java"))  # "  Java Programming  "

# # Find
# print(text.find("Pro"))  # 9

# # Check
# print("123".isdigit())   # True
# print("abc".isalpha())   # True
# print("abc123".isalnum()) # True

# # Join
# words = ["Hello", "World"]
# print(" ".join(words))   # "Hello World"
# print("-".join(words))   # "Hello-World" """,
#                         "interview_questions": """1. What does strip() do?
# 2. How do you split a string?
# 3. How do you join strings?
# 4. What is the difference between find() and index()?""",
#                         "duration": 15,
#                         "order": 3,
#                         "quiz": [
#                             {
#                                 "question": "What does '  Hello  '.strip() return?",
#                                 "options": ["'Hello'", "'  Hello  '", "'Hello  '", "'  Hello'"],
#                                 "correct_answer": 0,
#                                 "explanation": "strip() removes leading and trailing spaces."
#                             }
#                         ]
#                     }
#                 ]
#             },
            # ===== MODULE 5 =====
            {
                "title": "Module 5: Lists in Python",
                "description": "List operations, methods, comprehension",
                "order": 5,
                "lessons": [
                    {
                        "title": "Lists Basics",
                        "description": "Creating and accessing lists",
                        "concept": """# Lists in Python
A list is a collection of items.

## Creating Lists:
```python
fruits = ["apple", "banana", "orange"]
numbers = [1, 2, 3, 4, 5]
mixed = [1, "hello", 3.14, True]
empty = []
```

## Accessing Elements:
```python
fruits[0]    # "apple"
fruits[-1]   # "orange"
fruits[1:3]  # ["banana", "orange"]
```

## List Properties:
- Mutable (can change)
- Ordered
- Allow duplicates
- Any data type""",
                        "example": """# List Examples
fruits = ["apple", "banana", "orange", "mango"]

print(fruits[0])    # apple
print(fruits[-1])   # mango
print(fruits[1:3])  # ['banana', 'orange']
print(len(fruits))  # 4

# Check if item exists
if "banana" in fruits:
    print("Banana is in the list")

# Iterate through list
for fruit in fruits:
    print(fruit)""",
                        "interview_questions": """1. What is a list in Python?
2. How do you access list elements?
3. What is list indexing?
4. What are the properties of a list?""",
                        "duration": 20,
                        "order": 1,
                        "quiz": [
                            {
                                "question": "What is fruits[-1] if fruits = ['apple', 'banana', 'orange']?",
                                "options": ["apple", "banana", "orange", "Error"],
                                "correct_answer": 2,
                                "explanation": "-1 refers to the last element."
                            }
                        ]
                    },
                    {
                        "title": "List Methods",
                        "description": "append, insert, remove, pop, sort",
                        "concept": """# List Methods

## Adding Elements:
- `append()` - Add at end
- `insert()` - Add at index
- `extend()` - Add multiple items

## Removing Elements:
- `remove()` - Remove first occurrence
- `pop()` - Remove and return last item
- `pop(index)` - Remove and return at index
- `clear()` - Remove all items

## Other Methods:
- `sort()` - Sort list
- `reverse()` - Reverse list
- `index()` - Find index of item
- `count()` - Count occurrences
- `copy()` - Copy list

## Example:
```python
fruits = ["apple", "banana"]
fruits.append("orange")  # Add at end
fruits.insert(1, "mango") # Insert at index
fruits.remove("banana")   # Remove item
fruits.pop()              # Remove last
fruits.sort()             # Sort list
```""",
                        "example": """# List Methods Examples
numbers = [3, 1, 4, 1, 5, 9]

numbers.append(2)    # [3, 1, 4, 1, 5, 9, 2]
numbers.insert(1, 7) # [3, 7, 1, 4, 1, 5, 9, 2]
numbers.remove(1)    # [3, 7, 4, 1, 5, 9, 2]
numbers.sort()       # [1, 2, 3, 4, 5, 7, 9]

last = numbers.pop() # 9, list becomes [1, 2, 3, 4, 5, 7]

# Extend
numbers.extend([10, 11])  # [1, 2, 3, 4, 5, 7, 10, 11]

# Reverse
numbers.reverse()  # [11, 10, 7, 5, 4, 3, 2, 1]

# Count
print(numbers.count(1))  # 1

# Index
print(numbers.index(7))  # 2""",
                        "interview_questions": """1. What does append() do?
2. What is the difference between remove() and pop()?
3. How do you sort a list?
4. What is the difference between extend() and append()?""",
                        "duration": 20,
                        "order": 2,
                        "quiz": [
                            {
                                "question": "What does append() do?",
                                "options": ["Add item at end", "Add item at start", "Remove item", "Sort list"],
                                "correct_answer": 0,
                                "explanation": "append() adds an item to the end of a list."
                            }
                        ]
                    },
                    {
                        "title": "List Comprehension",
                        "description": "Creating lists efficiently",
                        "concept": """# List Comprehension
Create lists in one line.

## Syntax:
```python
[expression for item in iterable]
[expression for item in iterable if condition]
```

## Examples:
```python
# Square numbers
squares = [x**2 for x in range(5)]  # [0, 1, 4, 9, 16]

# Even numbers
evens = [x for x in range(10) if x % 2 == 0]  # [0, 2, 4, 6, 8]

# Nested loop
pairs = [(x, y) for x in [1,2] for y in [3,4]]
# [(1,3), (1,4), (2,3), (2,4)]
```

## Benefits:
- Concise
- Readable
- Faster than loops""",
                        "example": """# List Comprehension Examples
# Square numbers
squares = [x**2 for x in range(1, 6)]
print(squares)  # [1, 4, 9, 16, 25]

# Filter even numbers
numbers = [1, 2, 3, 4, 5, 6]
evens = [x for x in numbers if x % 2 == 0]
print(evens)    # [2, 4, 6]

# String manipulation
names = ["alice", "bob", "charlie"]
caps = [name.capitalize() for name in names]
print(caps)     # ["Alice", "Bob", "Charlie"]

# With if-else
result = [x if x % 2 == 0 else -x for x in range(1, 6)]
print(result)   # [-1, 2, -3, 4, -5]

# Nested comprehension
matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
flat = [num for row in matrix for num in row]
print(flat)  # [1, 2, 3, 4, 5, 6, 7, 8, 9]""",
                        "interview_questions": """1. What is list comprehension?
2. How do you create a list of squares using list comprehension?
3. How do you filter a list using list comprehension?
4. What is the difference between list comprehension and for loop?""",
                        "duration": 15,
                        "order": 3,
                        "quiz": [
                            {
                                "question": "What does [x**2 for x in range(3)] return?",
                                "options": ["[0, 1, 2]", "[0, 1, 4]", "[1, 4, 9]", "[0, 2, 4]"],
                                "correct_answer": 1,
                                "explanation": "0^2=0, 1^2=1, 2^2=4"
                            }
                        ]
                    }
                ]
            },
            # ===== MODULE 6 =====
            {
                "title": "Module 6: Tuples & Sets",
                "description": "Tuples (immutable), Sets (unique)",
                "order": 6,
                "lessons": [
                    {
                        "title": "Tuples in Python",
                        "description": "Creating and using tuples",
                        "concept": """# Tuples in Python
A tuple is an immutable sequence.

## Creating Tuples:
```python
point = (10, 20)
colors = ("red", "green", "blue")
single = (5,)  # Tuple with one item
empty = ()
```

## Tuple Operations:
```python
len(point)    # 2
point[0]      # 10
point[1]      # 20
```

## Tuple Unpacking:
```python
x, y = point
x, y, z = coordinates
```

## Tuple vs List:
- Tuple: Immutable, faster
- List: Mutable, slower

## When to use Tuple:
- When data doesn't change
- For dictionary keys
- For function returns""",
                        "example": """# Tuple Examples
coordinates = (10, 20, 30)

print(coordinates[0])   # 10
print(len(coordinates)) # 3

# Tuple unpacking
x, y, z = coordinates
print(x, y, z)  # 10 20 30

# Nested tuple
nested = (1, (2, 3), 4)
print(nested[1])    # (2, 3)
print(nested[1][0]) # 2

# Tuple as dictionary key
location = {(10, 20): "Point A"}
print(location[(10, 20)])  # Point A""",
                        "interview_questions": """1. What is a tuple in Python?
2. What is the difference between tuple and list?
3. How do you create a tuple with one item?
4. When would you use a tuple instead of a list?""",
                        "duration": 15,
                        "order": 1,
                        "quiz": [
                            {
                                "question": "Which of these is a valid tuple?",
                                "options": ["(1, 2, 3)", "[1, 2, 3]", "{1, 2, 3}", "{'a': 1, 'b': 2}"],
                                "correct_answer": 0,
                                "explanation": "Tuples use parentheses ()."
                            }
                        ]
                    },
                    {
                        "title": "Sets in Python",
                        "description": "Sets (unique, unordered)",
                        "concept": """# Sets in Python
A set is an unordered collection of unique items.

## Creating Sets:
```python
numbers = {1, 2, 3, 4}
letters = {"a", "b", "c"}
empty_set = set()  # Empty set
```

## Set Operations:
```python
set1 = {1, 2, 3}
set2 = {3, 4, 5}

set1.union(set2)       # {1, 2, 3, 4, 5}
set1.intersection(set2) # {3}
set1.difference(set2)  # {1, 2}
set1.symmetric_difference(set2) # {1, 2, 4, 5}
```

## Set Methods:
- `add()` - Add element
- `remove()` - Remove element (error if not found)
- `discard()` - Remove element (no error)
- `pop()` - Remove and return arbitrary
- `clear()` - Remove all
- `copy()` - Copy set""",
                        "example": """# Set Examples
set1 = {1, 2, 3, 4, 5}
set2 = {4, 5, 6, 7, 8}

# Union (all items)
print(set1 | set2)   # {1, 2, 3, 4, 5, 6, 7, 8}

# Intersection (common items)
print(set1 & set2)   # {4, 5}

# Difference (items in set1 not in set2)
print(set1 - set2)   # {1, 2, 3}

# Symmetric difference (not in both)
print(set1 ^ set2)   # {1, 2, 3, 6, 7, 8}

# Check if item exists
if 3 in set1:
    print("3 is in set1")

# Add and remove
set1.add(6)
print(set1)  # {1, 2, 3, 4, 5, 6}
set1.remove(3)
print(set1)  # {1, 2, 4, 5, 6}""",
                        "interview_questions": """1. What is a set in Python?
2. What is the difference between set and list?
3. How do you find the intersection of two sets?
4. What is the difference between remove() and discard()?""",
                        "duration": 15,
                        "order": 2,
                        "quiz": [
                            {
                                "question": "What does {1, 2, 3} & {3, 4, 5} return?",
                                "options": ["{1, 2, 3, 4, 5}", "{3}", "{1, 2}", "{4, 5}"],
                                "correct_answer": 1,
                                "explanation": "& returns the intersection (common elements)."
                            }
                        ]
                    }
                ]
            },
            # ===== MODULE 7 =====
            {
                "title": "Module 7: Dictionaries",
                "description": "Key-value pairs, dictionary methods",
                "order": 7,
                "lessons": [
                    {
                        "title": "Dictionary Basics",
                        "description": "Creating and accessing dictionaries",
                        "concept": """# Dictionaries in Python
A dictionary stores key-value pairs.

## Creating Dictionaries:
```python
student = {
    "name": "Alice",
    "age": 25,
    "grade": "A"
}
empty = {}
```

## Accessing Values:
```python
student["name"]    # "Alice"
student.get("age") # 25
student.get("gender", "Not specified") # "Not specified"
```

## Dictionary Properties:
- Keys must be immutable
- Values can be any type
- Ordered (Python 3.7+)
- No duplicate keys""",
                        "example": """# Dictionary Examples
student = {
    "name": "John",
    "age": 20,
    "course": "Python",
    "marks": [85, 90, 78]
}

print(student["name"])      # John
print(student["marks"][1])  # 90
print(student.get("age"))   # 20
print(student.get("grade", "Not available"))  # Not available

# Check if key exists
if "course" in student:
    print(student["course"])  # Python

# Iterate through dictionary
for key, value in student.items():
    print(f"{key}: {value}")""",
                        "interview_questions": """1. What is a dictionary in Python?
2. How do you access values in a dictionary?
3. What is the difference between dict and list?
4. What are the properties of dictionary keys?""",
                        "duration": 20,
                        "order": 1,
                        "quiz": [
                            {
                                "question": "How do you access the value of 'name' in dict d = {'name': 'Alice', 'age': 25}?",
                                "options": ["d['name']", "d.name", "d.get(name)", "d(name)"],
                                "correct_answer": 0,
                                "explanation": "d['name'] is the correct way to access dictionary values."
                            }
                        ]
                    },
                    {
                        "title": "Dictionary Methods",
                        "description": "keys, values, items, update",
                        "concept": """# Dictionary Methods

## Common Methods:
```python
student = {"name": "Alice", "age": 25}

student.keys()    # dict_keys(['name', 'age'])
student.values()  # dict_values(['Alice', 25])
student.items()   # dict_items([('name', 'Alice'), ('age', 25)])
student.update({"grade": "A"})  # Add/update
student.pop("age")  # Remove and return
student.popitem()  # Remove and return last
```

## Other Methods:
- `clear()` - Remove all
- `copy()` - Copy dictionary
- `fromkeys()` - Create from keys
- `get()` - Get value with default
- `setdefault()` - Get or set default""",
                        "example": """# Dictionary Methods Examples
student = {"name": "Alice", "age": 25}

# Add new key-value pair
student["grade"] = "A"
print(student)  # {'name': 'Alice', 'age': 25, 'grade': 'A'}

# Update multiple values
student.update({"age": 26, "city": "Mumbai"})
print(student)  # {'name': 'Alice', 'age': 26, 'grade': 'A', 'city': 'Mumbai'}

# Get all keys
print(student.keys())   # dict_keys(['name', 'age', 'grade', 'city'])

# Remove item
removed = student.pop("age")
print(removed)  # 26

# Get with default
print(student.get("country", "India"))  # India

# Copy
new_student = student.copy()""",
                        "interview_questions": """1. What are dictionary methods?
2. How do you add a new key-value pair?
3. How do you remove an item from dictionary?
4. What is the difference between get() and setdefault()?""",
                        "duration": 15,
                        "order": 2,
                        "quiz": [
                            {
                                "question": "What does student.keys() return?",
                                "options": ["All keys", "All values", "All items", "None"],
                                "correct_answer": 0,
                                "explanation": "keys() returns all the keys in the dictionary."
                            }
                        ]
                    }
                ]
            },
            # ===== MODULE 8 =====
            {
                "title": "Module 8: Control Flow - If-Else",
                "description": "Conditional statements",
                "order": 8,
                "lessons": [
                    {
                        "title": "If Statement",
                        "description": "Making decisions with if",
                        "concept": """# If Statement in Python
Execute code based on condition.

## Syntax:
```python
if condition:
    # code to execute
```

## Example:
```python
age = 18
if age >= 18:
    print("You are an adult")
```

## Important:
- Indentation is required
- Colon at the end
- Condition returns True/False""",
                        "example": """# If Statement Examples
age = 18

if age >= 18:
    print("You can vote")
    print("You can drive")
    print("You are an adult")

# Check if number is positive
num = 5
if num > 0:
    print(f"{num} is positive")

# Check if string is empty
name = "Alice"
if name:
    print(f"Hello, {name}!")
else:
    print("Name is empty")

# Check if list is empty
items = []
if items:
    print("List has items")
else:
    print("List is empty")""",
                        "interview_questions": """1. What is an if statement?
2. How does Python handle indentation?
3. What happens if the condition is False?
4. What values are considered False in Python?""",
                        "duration": 15,
                        "order": 1,
                        "quiz": [
                            {
                                "question": "What is the output if age = 15 and if age >= 18: print('Adult')?",
                                "options": ["Adult", "No output", "Error", "Child"],
                                "correct_answer": 1,
                                "explanation": "15 < 18, so the condition is False, no output."
                            }
                        ]
                    },
                    {
                        "title": "If-Else and Elif",
                        "description": "Multiple conditions",
                        "concept": """# If-Else Statement
```python
if condition1:
    # code
elif condition2:
    # code
elif condition3:
    # code
else:
    # code
```

## Example:
```python
score = 85
if score >= 90:
    grade = "A"
elif score >= 80:
    grade = "B"
elif score >= 70:
    grade = "C"
else:
    grade = "F"
```

## Key Points:
- Only one block executes
- Order matters
- `elif` is short for "else if"
- `else` is optional""",
                        "example": """# Grade Calculator
marks = 85

if marks >= 90:
    grade = "A+"
elif marks >= 80:
    grade = "A"
elif marks >= 70:
    grade = "B"
elif marks >= 60:
    grade = "C"
else:
    grade = "F"

print(f"Grade: {grade}")

# Number sign checker
num = -5
if num > 0:
    print("Positive")
elif num < 0:
    print("Negative")
else:
    print("Zero")

# Multiple conditions
age = 25
if age < 13:
    print("Child")
elif age < 20:
    print("Teenager")
elif age < 60:
    print("Adult")
else:
    print("Senior")""",
                        "interview_questions": """1. What is if-else statement?
2. What is the difference between if-else and elif?
3. How many elif statements can you have?
4. What is short-circuit evaluation?""",
                        "duration": 15,
                        "order": 2,
                        "quiz": [
                            {
                                "question": "What is grade if marks = 75?",
                                "options": ["A", "B", "C", "F"],
                                "correct_answer": 2,
                                "explanation": "75 >= 70 and < 80, so grade is C."
                            }
                        ]
                    }
                ]
            },
            # ===== MODULE 9 =====
            {
                "title": "Module 9: Loops in Python",
                "description": "For loop, while loop",
                "order": 9,
                "lessons": [
                    {
                        "title": "For Loop",
                        "description": "Iterating over sequences",
                        "concept": """# For Loop in Python
```python
for item in iterable:
    # code to execute
```

## Examples:
```python
fruits = ["apple", "banana", "orange"]
for fruit in fruits:
    print(fruit)

for i in range(5):
    print(i)
```

## range() Function:
- `range(n)` - 0 to n-1
- `range(start, end)` - start to end-1
- `range(start, end, step)` - with step

## Iterating over:
- Lists
- Tuples
- Strings
- Dictionaries
- Sets""",
                        "example": """# For Loop Examples
# List iteration
colors = ["red", "blue", "green"]
for color in colors:
    print(color)

# Range
for i in range(1, 6):
    print(f"Number: {i}")

# String iteration
for char in "Python":
    print(char)

# Dictionary iteration
student = {"name": "Alice", "age": 25, "grade": "A"}
for key, value in student.items():
    print(f"{key}: {value}")

# Enumerate
fruits = ["apple", "banana", "orange"]
for index, fruit in enumerate(fruits):
    print(f"{index}: {fruit}")

# Zip
names = ["Alice", "Bob", "Charlie"]
ages = [25, 30, 35]
for name, age in zip(names, ages):
    print(f"{name} is {age} years old")""",
                        "interview_questions": """1. What is a for loop in Python?
2. How do you use range() with for loop?
3. Can you iterate over strings with for loop?
4. What is the difference between range and enumerate?""",
                        "duration": 20,
                        "order": 1,
                        "quiz": [
                            {
                                "question": "What does for i in range(3): print(i) output?",
                                "options": ["0 1 2", "1 2 3", "0 1 2 3", "1 2"],
                                "correct_answer": 0,
                                "explanation": "range(3) generates 0, 1, 2."
                            }
                        ]
                    },
                    {
                        "title": "While Loop",
                        "description": "Loop until condition is False",
                        "concept": """# While Loop in Python
```python
while condition:
    # code to execute
```

## Example:
```python
count = 1
while count <= 5:
    print(count)
    count += 1
```

## Important:
- Condition checked before each iteration
- Must update condition to avoid infinite loop
- Use `break` to exit early
- Use `continue` to skip iteration

## Common Use Cases:
- User input validation
- Reading files
- Infinite loops with break""",
                        "example": """# While Loop Examples
# Print numbers 1 to 5
num = 1
while num <= 5:
    print(num)
    num += 1

# Sum of numbers
total = 0
num = 1
while num <= 10:
    total += num
    num += 1
print(f"Sum: {total}")

# User input validation
while True:
    user_input = input("Enter a number (or 'quit' to exit): ")
    if user_input.lower() == 'quit':
        break
    try:
        num = int(user_input)
        print(f"You entered: {num}")
    except ValueError:
        print("Please enter a valid number")

# Continue example
num = 0
while num < 10:
    num += 1
    if num % 2 == 0:
        continue
    print(num)  # Prints odd numbers""",
                        "interview_questions": """1. What is a while loop in Python?
2. What is the difference between for and while loop?
3. How do you avoid infinite loops?
4. What is the difference between break and continue?""",
                        "duration": 20,
                        "order": 2,
                        "quiz": [
                            {
                                "question": "What is the output of count = 1; while count <= 3: print(count); count += 1?",
                                "options": ["1 2 3", "1 2", "1 2 3 4", "0 1 2"],
                                "correct_answer": 0,
                                "explanation": "Prints 1, 2, 3 then stops."
                            }
                        ]
                    }
                ]
            },
            # ===== MODULE 10 =====
            {
                "title": "Module 10: Functions",
                "description": "Function definition, arguments, return values",
                "order": 10,
                "lessons": [
                    {
                        "title": "Function Basics",
                        "description": "Defining and calling functions",
                        "concept": """# Functions in Python
A function is a block of reusable code.

## Defining a Function:
```python
def function_name(parameters):
    # code block
    return value
```

## Example:
```python
def greet(name):
    return f"Hello, {name}!"

print(greet("Alice"))  # Hello, Alice!
```

## Function Components:
1. Function name (follows variable rules)
2. Parameters (optional)
3. Body (indented)
4. Return value (optional)

## Docstring:
```python
def add(a, b):
    \"\"\"Add two numbers and return the result.\"\"\"
    return a + b
```""",
                        "example": """# Function Examples
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
print(divide(10, 0))   # Cannot divide by zero

# Function with docstring
def power(base, exponent):
    \"\"\"Calculate base raised to exponent power.\"\"\"
    return base ** exponent

print(power(2, 3))  # 8""",
                        "interview_questions": """1. What is a function in Python?
2. How do you define a function?
3. What is the purpose of return statement?
4. What is a docstring?""",
                        "duration": 20,
                        "order": 1,
                        "quiz": [
                            {
                                "question": "Which keyword is used to define a function?",
                                "options": ["function", "def", "define", "func"],
                                "correct_answer": 1,
                                "explanation": "def is used to define a function in Python."
                            }
                        ]
                    },
                    {
                        "title": "Function Arguments",
                        "description": "Positional, keyword, default",
                        "concept": """# Function Arguments

## Types of Arguments:
1. **Positional** - Order matters
2. **Keyword** - Name matters
3. **Default** - Pre-set values
4. **Variable-length** - *args, **kwargs

## Examples:
```python
# Positional
def greet(name, message):
    print(f"{message}, {name}!")

# Default
def greet(name="Guest"):
    print(f"Hello, {name}!")

# Variable-length
def sum_all(*args):
    return sum(args)
```

## Order:
1. Positional
2. Default
3. *args
4. **kwargs""",
                        "example": """# Arguments Examples
# Positional
def power(base, exponent):
    return base ** exponent

print(power(2, 3))    # 8
print(power(3, 2))    # 9

# Default
def greet(name="Guest", msg="Hello"):
    print(f"{msg}, {name}!")

greet()                 # Hello, Guest!
greet("Alice")          # Hello, Alice!
greet("Bob", "Hi")      # Hi, Bob!

# Keyword
greet(msg="Hey", name="Charlie")  # Hey, Charlie!

# *args (variable positional)
def sum_all(*args):
    return sum(args)

print(sum_all(1, 2, 3, 4))  # 10
print(sum_all(1, 2))        # 3

# **kwargs (variable keyword)
def print_info(**kwargs):
    for key, value in kwargs.items():
        print(f"{key}: {value}")

print_info(name="Alice", age=25, city="Mumbai")
# name: Alice
# age: 25
# city: Mumbai""",
                        "interview_questions": """1. What are different types of function arguments?
2. What is the difference between positional and keyword arguments?
3. How do you use default arguments?
4. What is the purpose of *args and **kwargs?""",
                        "duration": 15,
                        "order": 2,
                        "quiz": [
                            {
                                "question": "What is the output of greet(name='Alice') if greet(name='Guest', msg='Hello')?",
                                "options": ["Hello, Alice!", "Hello, Guest!", "Error", "Alice!"],
                                "correct_answer": 0,
                                "explanation": "Alice overrides the default name."
                            }
                        ]
                    }
                ]
            },
            # ===== MODULE 11 =====
            {
                "title": "Module 11: Scope & Recursion",
                "description": "Variable scope, recursion",
                "order": 11,
                "lessons": [
                    {
                        "title": "Variable Scope",
                        "description": "Global and local variables",
                        "concept": """# Variable Scope

## Local Scope:
Variables defined inside a function

## Global Scope:
Variables defined outside a function

## Example:
```python
x = 10  # Global

def my_func():
    y = 5  # Local
    print(x)  # Access global
    print(y)  # Access local
```

## LEGB Rule:
1. **L**ocal - Inside function
2. **E**nclosing - Outer function
3. **G**lobal - Module level
4. **B**uilt-in - Built-in functions

## Global Keyword:
```python
count = 0
def increment():
    global count
    count += 1
```""",
                        "example": """# Scope Examples
x = 10  # Global

def func():
    y = 5  # Local
    print(f"Inside func: x={x}, y={y}")

func()
print(f"Outside: x={x}")  # y not accessible

# Modifying global variable
count = 0

def increment():
    global count
    count += 1

increment()
increment()
print(count)  # 2

# Enclosing scope
def outer():
    z = 10
    def inner():
        nonlocal z
        z += 5
        print(z)
    inner()
    print(z)

outer()  # 15, 15""",
                        "interview_questions": """1. What is the difference between global and local scope?
2. How do you access a global variable inside a function?
3. What is the 'global' keyword used for?
4. What is the LEGB rule?""",
                        "duration": 15,
                        "order": 1,
                        "quiz": [
                            {
                                "question": "Can a function access a variable defined outside it?",
                                "options": ["Yes", "No", "Only if global", "Only if local"],
                                "correct_answer": 0,
                                "explanation": "Yes, functions can access global variables."
                            }
                        ]
                    },
                    {
                        "title": "Recursion",
                        "description": "Function calling itself",
                        "concept": """# Recursion in Python
A function that calls itself.

## Example: Factorial
```python
def factorial(n):
    if n <= 1:
        return 1
    return n * factorial(n - 1)
```

## Base Case vs Recursive Case:
- Base Case: Stops recursion
- Recursive Case: Function calls itself

## Advantages:
- Elegant solution for recursive problems
- Less code than iteration

## Disadvantages:
- Memory intensive
- Risk of stack overflow
- Slower than iteration""",
                        "example": """# Recursion Examples
# Factorial
def factorial(n):
    if n <= 1:
        return 1
    return n * factorial(n - 1)

print(factorial(5))  # 120

# Fibonacci
def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)

print(fibonacci(6))  # 8

# Sum of numbers
def sum_numbers(n):
    if n <= 0:
        return 0
    return n + sum_numbers(n-1)

print(sum_numbers(5))  # 15

# Power function
def power(base, exp):
    if exp == 0:
        return 1
    return base * power(base, exp - 1)

print(power(2, 3))  # 8

# Tower of Hanoi
def hanoi(n, source, target, auxiliary):
    if n == 1:
        print(f"Move disk 1 from {source} to {target}")
        return
    hanoi(n-1, source, auxiliary, target)
    print(f"Move disk {n} from {source} to {target}")
    hanoi(n-1, auxiliary, target, source)

hanoi(3, 'A', 'C', 'B')""",
                        "interview_questions": """1. What is recursion in Python?
2. What is the base case in recursion?
3. What is the difference between recursion and iteration?
4. What are the advantages and disadvantages of recursion?""",
                        "duration": 20,
                        "order": 2,
                        "quiz": [
                            {
                                "question": "What is factorial(3)?",
                                "options": ["3", "6", "9", "12"],
                                "correct_answer": 1,
                                "explanation": "3! = 3 * 2 * 1 = 6"
                            }
                        ]
                    }
                ]
            },
            # ===== MODULE 12 =====
            {
                "title": "Module 12: File Handling",
                "description": "Read, write, append files",
                "order": 12,
                "lessons": [
                    {
                        "title": "Reading Files",
                        "description": "Reading text files",
                        "concept": """# Reading Files in Python

## Open File:
```python
file = open("filename.txt", "r")
```

## Reading Methods:
```python
# Read entire file
content = file.read()

# Read line by line
for line in file:
    print(line)

# Read all lines into list
lines = file.readlines()
```

## with Statement (Best Practice):
```python
with open("filename.txt", "r") as file:
    content = file.read()
```

## File Modes:
- `'r'` - Read (default)
- `'w'` - Write (overwrites)
- `'a'` - Append
- `'x'` - Create (error if exists)
- `'r+'` - Read and write
- `'t'` - Text (default)
- `'b'` - Binary""",
                        "example": """# Reading File Examples
# Read entire file
with open("data.txt", "r") as file:
    content = file.read()
    print(content)

# Read line by line
with open("data.txt", "r") as file:
    for line in file:
        print(line.strip())

# Read all lines into list
with open("data.txt", "r") as file:
    lines = file.readlines()
    for line in lines:
        print(line)

# Reading specific number of characters
with open("data.txt", "r") as file:
    chunk = file.read(10)  # Read first 10 characters
    print(chunk)""",
                        "interview_questions": """1. How do you read a file in Python?
2. What is the difference between read() and readlines()?
3. Why is 'with' statement used for file operations?
4. What are the different file modes?""",
                        "duration": 20,
                        "order": 1,
                        "quiz": [
                            {
                                "question": "Which mode is used to read a file?",
                                "options": ["'r'", "'w'", "'a'", "'rw'"],
                                "correct_answer": 0,
                                "explanation": "'r' is used for reading files."
                            }
                        ]
                    },
                    {
                        "title": "Writing Files",
                        "description": "Writing to files",
                        "concept": """# Writing Files in Python

## Write Mode:
```python
file = open("filename.txt", "w")
```

## Append Mode:
```python
file = open("filename.txt", "a")
```

## Writing Methods:
```python
# Write string
file.write("Hello")

# Write multiple lines
file.writelines(["Line 1\\n", "Line 2\\n"])
```

## with Statement:
```python
with open("filename.txt", "w") as file:
    file.write("Hello World!")
```

## Modes:
- `'w'` - Write (overwrites)
- `'a'` - Append (adds to end)
- `'x'` - Create (error if exists)""",
                        "example": """# Writing File Examples
# Write to file
with open("output.txt", "w") as file:
    file.write("Hello World!\\n")
    file.write("Python is great!\\n")

# Append to file
with open("output.txt", "a") as file:
    file.write("This line is appended.\\n")

# Write multiple lines
lines = ["Line 1\\n", "Line 2\\n", "Line 3\\n"]
with open("output.txt", "w") as file:
    file.writelines(lines)

# Write numbers
with open("numbers.txt", "w") as file:
    for i in range(1, 11):
        file.write(f"{i}\\n")

# Write with formatting
data = [{"name": "Alice", "age": 25}, {"name": "Bob", "age": 30}]
with open("data.txt", "w") as file:
    for person in data:
        file.write(f"{person['name']},{person['age']}\\n")""",
                        "interview_questions": """1. How do you write to a file in Python?
2. What is the difference between 'w' and 'a' modes?
3. How do you write multiple lines to a file?
4. What happens if the file doesn't exist in write mode?""",
                        "duration": 15,
                        "order": 2,
                        "quiz": [
                            {
                                "question": "What does 'a' mode do in file handling?",
                                "options": ["Read", "Write", "Append", "Read and Write"],
                                "correct_answer": 2,
                                "explanation": "'a' stands for append, adds content to the end."
                            }
                        ]
                    }
                ]
            },
            # ===== MODULE 13 =====
            {
                "title": "Module 13: Exception Handling",
                "description": "Try, except, finally",
                "order": 13,
                "lessons": [
                    {
                        "title": "Exception Handling",
                        "description": "Handling errors gracefully",
                        "concept": """# Exception Handling in Python

## Try-Except Block:
```python
try:
    # code that may raise exception
except:
    # code to handle exception
```

## Example:
```python
try:
    num = int(input("Enter number: "))
    result = 10 / num
except ZeroDivisionError:
    print("Cannot divide by zero")
except ValueError:
    print("Please enter a valid number")
```

## Exception Types:
- `ZeroDivisionError` - Division by zero
- `ValueError` - Invalid value
- `TypeError` - Wrong type
- `IndexError` - List index out of range
- `KeyError` - Dictionary key not found
- `FileNotFoundError` - File doesn't exist

## Finally Block:
```python
try:
    # code
except:
    # handle error
finally:
    # always executes
```""",
                        "example": """# Exception Examples
# Divide by zero
try:
    result = 10 / 0
except ZeroDivisionError:
    print("Cannot divide by zero!")

# Invalid input
try:
    num = int("abc")
except ValueError:
    print("Invalid number format!")

# Multiple exceptions
try:
    num = int(input("Enter number: "))
    result = 10 / num
    print(f"Result: {result}")
except ZeroDivisionError:
    print("Cannot divide by zero!")
except ValueError:
    print("Please enter a valid number!")
except Exception as e:
    print(f"An error occurred: {e}")
finally:
    print("This always executes")

# Raising exceptions
def check_age(age):
    if age < 0:
        raise ValueError("Age cannot be negative")
    print(f"Age is {age}")

try:
    check_age(-5)
except ValueError as e:
    print(f"Error: {e}")

# Custom exception
class CustomError(Exception):
    pass

try:
    raise CustomError("This is a custom error")
except CustomError as e:
    print(f"Custom error: {e}")""",
                        "interview_questions": """1. What is exception handling in Python?
2. What is the difference between try and except?
3. What is the purpose of the finally block?
4. What are the common built-in exceptions?
5. How do you create custom exceptions?""",
                        "duration": 20,
                        "order": 1,
                        "quiz": [
                            {
                                "question": "What is the output of try: 10/0 except ZeroDivisionError: print('Error')?",
                                "options": ["Error", "0", "10", "Exception"],
                                "correct_answer": 0,
                                "explanation": "ZeroDivisionError is caught and 'Error' is printed."
                            }
                        ]
                    }
                ]
            },
            # ===== MODULE 14 =====
            {
                "title": "Module 14: Object-Oriented Programming",
                "description": "Classes, objects, and OOP concepts",
                "order": 14,
                "lessons": [
                    {
                        "title": "Classes & Objects",
                        "description": "Creating classes and objects",
                        "concept": """# Classes & Objects in Python
A class is a blueprint for creating objects.

## Creating a Class:
```python
class Car:
    def __init__(self, brand, model):
        self.brand = brand
        self.model = model
    
    def start(self):
        print(f"{self.brand} {self.model} started!")
```

## Creating Objects:
```python
my_car = Car("Toyota", "Camry")
my_car.start()  # Toyota Camry started!
```

## Key Concepts:
- **Class**: Blueprint
- **Object**: Instance of class
- **Method**: Function inside class
- **Attribute**: Variable inside class
- **Constructor**: __init__ method""",
                        "example": """# Class Examples
class Student:
    def __init__(self, name, age, grade):
        self.name = name
        self.age = age
        self.grade = grade
    
    def display(self):
        print(f"Name: {self.name}")
        print(f"Age: {self.age}")
        print(f"Grade: {self.grade}")
    
    def update_grade(self, new_grade):
        self.grade = new_grade
        print(f"{self.name}'s grade updated to {self.grade}")

# Create objects
s1 = Student("Alice", 20, "A")
s2 = Student("Bob", 22, "B")

s1.display()
s2.display()

s1.update_grade("A+")  # Alice's grade updated to A+

# Class attributes
class Employee:
    company = "Tech Corp"  # Class attribute
    
    def __init__(self, name, salary):
        self.name = name  # Instance attribute
        self.salary = salary

print(Employee.company)  # Tech Corp
e1 = Employee("John", 50000)
print(e1.name, e1.salary)  # John 50000""",
                        "interview_questions": """1. What is a class in Python?
2. What is an object in Python?
3. What is the __init__ method?
4. What is the difference between class and instance attributes?
5. What is the difference between a method and a function?""",
                        "duration": 20,
                        "order": 1,
                        "quiz": [
                            {
                                "question": "What is a class?",
                                "options": ["A blueprint for objects", "An instance of an object", "A variable", "A function"],
                                "correct_answer": 0,
                                "explanation": "A class is a blueprint for creating objects."
                            }
                        ]
                    }
                ]
            },
            # ===== MODULE 15 =====
            {
                "title": "Module 15: Inheritance and Polymorphism",
                "description": "Advanced OOP concepts",
                "order": 15,
                "lessons": [
                    {
                        "title": "Inheritance",
                        "description": "Inheriting from parent class",
                        "concept": """# Inheritance in Python
A class can inherit attributes and methods from another class.

## Syntax:
```python
class ChildClass(ParentClass):
    # additional code
```

## Example:
```python
class Animal:
    def __init__(self, name):
        self.name = name
    
    def speak(self):
        print(f"{self.name} makes a sound")

class Dog(Animal):
    def speak(self):
        print(f"{self.name} barks!")
```

## Types of Inheritance:
1. **Single** - One parent
2. **Multiple** - Multiple parents
3. **Multilevel** - Chain of inheritance
4. **Hierarchical** - Multiple children
5. **Hybrid** - Combination

## super() Function:
```python
class Dog(Animal):
    def __init__(self, name, breed):
        super().__init__(name)
        self.breed = breed
```""",
                        "example": """# Inheritance Examples
class Animal:
    def __init__(self, name):
        self.name = name
    
    def eat(self):
        print(f"{self.name} is eating")
    
    def sleep(self):
        print(f"{self.name} is sleeping")

class Dog(Animal):
    def bark(self):
        print(f"{self.name} barks loudly!")
    
    def eat(self):  # Method overriding
        print(f"{self.name} is eating dog food!")

class Cat(Animal):
    def meow(self):
        print(f"{self.name} meows softly!")

# Single inheritance
dog = Dog("Buddy")
cat = Cat("Whiskers")

dog.eat()   # Buddy is eating dog food!
dog.bark()  # Buddy barks loudly!
cat.eat()   # Whiskers is eating
cat.meow()  # Whiskers meows softly!

# Multiple inheritance
class Flyable:
    def fly(self):
        print("Flying...")

class Swimmable:
    def swim(self):
        print("Swimming...")

class Duck(Animal, Flyable, Swimmable):
    def __init__(self, name):
        super().__init__(name)

duck = Duck("Donald")
duck.eat()   # Donald is eating
duck.fly()   # Flying...
duck.swim()  # Swimming...

# Multilevel inheritance
class Mammal(Animal):
    def feed_milk(self):
        print(f"{self.name} feeds milk")

class Human(Mammal):
    def speak(self):
        print(f"{self.name} speaks")

human = Human("Alice")
human.eat()       # Alice is eating
human.feed_milk() # Alice feeds milk
human.speak()     # Alice speaks""",
                        "interview_questions": """1. What is inheritance in Python?
2. How do you create a child class in Python?
3. What is method overriding?
4. What is the super() function used for?
5. What are the different types of inheritance?""",
                        "duration": 20,
                        "order": 1,
                        "quiz": [
                            {
                                "question": "What is inheritance?",
                                "options": ["Class inheriting from another class", "Function overloading", "Variable assignment", "Looping"],
                                "correct_answer": 0,
                                "explanation": "Inheritance is when a class inherits from another class."
                            }
                        ]
                    }
                ]
            },
            # ===== MODULE 16 =====
            {
                "title": "Module 16: Decorators and Generators",
                "description": "Advanced function concepts",
                "order": 16,
                "lessons": [
                    {
                        "title": "Decorators",
                        "description": "Modifying function behavior",
                        "concept": """# Decorators in Python
A decorator is a function that modifies another function.

## Syntax:
```python
@decorator
def function():
    pass
```

## Example:
```python
def timer(func):
    import time
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(f"{func.__name__} took {end - start:.2f}s")
        return result
    return wrapper

@timer
def slow_function():
    time.sleep(1)
    return "Done"
```

## Common Use Cases:
- Logging
- Timing functions
- Authentication
- Caching
- Permission checking

## Built-in Decorators:
- `@staticmethod`
- `@classmethod`
- `@property`""",
                        "example": """# Decorator Examples
def uppercase(func):
    def wrapper():
        result = func()
        return result.upper()
    return wrapper

@uppercase
def greet():
    return "hello world"

print(greet())  # HELLO WORLD

# Decorator with arguments
def repeat(n):
    def decorator(func):
        def wrapper(*args, **kwargs):
            for _ in range(n):
                func(*args, **kwargs)
        return wrapper
    return decorator

@repeat(3)
def say_hi():
    print("Hi!")

say_hi()  # Prints "Hi!" three times

# Class decorator
def add_method(cls):
    def new_method(self):
        return "New method added!"
    cls.new_method = new_method
    return cls

@add_method
class MyClass:
    def __init__(self):
        self.name = "MyClass"

obj = MyClass()
print(obj.new_method())  # New method added!

# Property decorator
class Person:
    def __init__(self, name):
        self._name = name
    
    @property
    def name(self):
        return self._name
    
    @name.setter
    def name(self, value):
        self._name = value

p = Person("Alice")
print(p.name)  # Alice
p.name = "Bob"
print(p.name)  # Bob""",
                        "interview_questions": """1. What is a decorator in Python?
2. How do you create a custom decorator?
3. What is the @ symbol used for?
4. What are common use cases for decorators?
5. What is the difference between a decorator and a higher-order function?""",
                        "duration": 20,
                        "order": 1,
                        "quiz": [
                            {
                                "question": "What does a decorator do?",
                                "options": ["Modifies function behavior", "Creates a class", "Defines a variable", "Imports a module"],
                                "correct_answer": 0,
                                "explanation": "A decorator modifies the behavior of a function."
                            }
                        ]
                    }
                ]
            },
            # ===== MODULE 17 =====
            {
                "title": "Module 17: Working with Modules and Packages",
                "description": "Organizing and reusing code",
                "order": 17,
                "lessons": [
                    {
                        "title": "Modules and Packages",
                        "description": "Importing and creating modules",
                        "concept": """# Modules and Packages in Python

## Modules:
A module is a Python file (.py) that contains functions, classes, and variables.

## Creating a Module:
```python
# mymodule.py
def greet(name):
    return f"Hello, {name}!"

class Calculator:
    def add(self, a, b):
        return a + b
```

## Importing Modules:
```python
import mymodule
from mymodule import greet
from mymodule import Calculator
from mymodule import *  # Not recommended
```

## Packages:
A package is a directory containing modules and an __init__.py file.

## Standard Library Modules:
- `os` - Operating system interface
- `sys` - System-specific parameters
- `math` - Mathematical functions
- `datetime` - Date and time
- `json` - JSON data handling
- `re` - Regular expressions
- `collections` - Specialized containers
- `random` - Random number generation""",
                        "example": """# Creating and using a math_utils.py module
# math_utils.py
def add(a, b):
    return a + b

def subtract(a, b):
    return a - b

def multiply(a, b):
    return a * b

def divide(a, b):
    if b == 0:
        return None
    return a / b

# Using the module
# main.py
import math_utils as mu

result = mu.add(10, 5)
print(f"Addition: {result}")  # Addition: 15

result = mu.multiply(4, 3)
print(f"Multiplication: {result}")  # Multiplication: 12

# Using standard library
import os
import datetime
import random

print(f"Current directory: {os.getcwd()}")
print(f"Current date: {datetime.datetime.now()}")
print(f"Random number: {random.randint(1, 100)}")

# Creating packages
# mypackage/
#   __init__.py
#   module1.py
#   module2.py

# from mypackage import module1
# module1.some_function()

# Import from package
# from mypackage.module1 import some_function
# some_function()""",
                        "interview_questions": """1. What is the difference between a module and a package?
2. How do you import a module?
3. What is __init__.py for?
4. What are some useful standard library modules?""",
                        "duration": 20,
                        "order": 1,
                        "quiz": [
                            {
                                "question": "What is a module in Python?",
                                "options": ["A Python file", "A Python function", "A Python class", "A Python library"],
                                "correct_answer": 0,
                                "explanation": "A module is a Python file containing Python code."
                            }
                        ]
                    }
                ]
            },
            # ===== MODULE 18 =====
            {
                "title": "Module 18: Working with JSON and APIs",
                "description": "JSON handling and API integration",
                "order": 18,
                "lessons": [
                    {
                        "title": "JSON in Python",
                        "description": "Parsing and generating JSON",
                        "concept": """# JSON in Python
JSON (JavaScript Object Notation) is a lightweight data format.

## JSON Functions:
- `json.dumps()` - Convert Python object to JSON string
- `json.loads()` - Convert JSON string to Python object
- `json.dump()` - Write JSON to file
- `json.load()` - Read JSON from file

## JSON ↔ Python Mapping:
| JSON | Python |
|------|--------|
| object | dict |
| array | list |
| string | str |
| number | int/float |
| boolean | bool |
| null | None |

## API Integration:
- `requests` library for HTTP requests
- GET, POST, PUT, DELETE methods
- Response handling and error checking""",
                        "example": """import json
import requests

# Working with JSON data
data = {
    "name": "Alice",
    "age": 25,
    "city": "New York",
    "hobbies": ["reading", "coding", "traveling"],
    "is_student": True
}

# Convert to JSON string
json_string = json.dumps(data, indent=2)
print(json_string)

# Parse JSON string to Python object
json_data = '{"name": "Bob", "age": 30, "city": "London"}'
parsed_data = json.loads(json_data)
print(f"Name: {parsed_data['name']}")

# Writing JSON to file
with open("data.json", "w") as file:
    json.dump(data, file, indent=2)

# Reading JSON from file
with open("data.json", "r") as file:
    loaded_data = json.load(file)
    print(loaded_data)

# API Integration (example)
try:
    response = requests.get("https://jsonplaceholder.typicode.com/posts/1")
    if response.status_code == 200:
        post_data = response.json()
        print(f"Post title: {post_data['title']}")
    else:
        print(f"Error: {response.status_code}")
except requests.exceptions.RequestException as e:
    print(f"Request failed: {e}")""",
                        "interview_questions": """1. How do you convert between Python objects and JSON?
2. What is the difference between json.dumps() and json.dump()?
3. How do you handle API requests in Python?
4. What are the common HTTP status codes?""",
                        "duration": 20,
                        "order": 1,
                        "quiz": [
                            {
                                "question": "Which method converts a Python object to a JSON string?",
                                "options": ["json.dumps()", "json.loads()", "json.dump()", "json.load()"],
                                "correct_answer": 0,
                                "explanation": "dumps() converts Python object to JSON string."
                            }
                        ]
                    }
                ]
            },
            # ===== MODULE 19 =====
            {
                "title": "Module 19: Regular Expressions",
                "description": "Pattern matching with regex",
                "order": 19,
                "lessons": [
                    {
                        "title": "Regular Expressions",
                        "description": "Pattern matching in Python",
                        "concept": """# Regular Expressions in Python

## Importing:
```python
import re
```

## Common Functions:
- `re.match()` - Match at beginning
- `re.search()` - Search anywhere
- `re.findall()` - Find all matches
- `re.finditer()` - Find all matches (iterator)
- `re.sub()` - Substitute patterns
- `re.split()` - Split by pattern

## Common Patterns:
| Pattern | Description |
|---------|-------------|
| `.` | Any character |
| `^` | Start of string |
| `$` | End of string |
| `*` | 0 or more |
| `+` | 1 or more |
| `?` | 0 or 1 |
| `\\d` | Digit |
| `\\w` | Word character |
| `\\s` | Whitespace |
| `[abc]` | Character set |
| `[^abc]` | Negated set |
| `a|b` | OR operator |
| `()` | Grouping |

## Flags:
- `re.IGNORECASE` - Case insensitive
- `re.DOTALL` - . matches newline
- `re.MULTILINE` - ^$ match line boundaries""",
                        "example": """import re

# Basic examples
text = "Hello, my email is john@example.com and my phone is 123-456-7890"

# Email pattern
email_pattern = r'\\w+@\\w+\\.\\w+'
emails = re.findall(email_pattern, text)
print(f"Email: {emails}")  # ['john@example.com']

# Phone pattern
phone_pattern = r'\\d{3}-\\d{3}-\\d{4}'
phones = re.findall(phone_pattern, text)
print(f"Phone: {phones}")  # ['123-456-7890']

# Validation
def is_valid_email(email):
    pattern = r'^[\\w\\.-]+@[\\w\\.-]+\\.\\w+$'
    return bool(re.match(pattern, email))

print(is_valid_email("test@example.com"))  # True
print(is_valid_email("invalid-email"))     # False

# Replacing patterns
text2 = "Hello, I love Python. Python is great!"
replaced = re.sub(r'Python', 'Java', text2)
print(replaced)  # Hello, I love Java. Java is great!

# Splitting text
text3 = "apple, banana; orange|grape"
split_text = re.split(r'[,;|]', text3)
print(split_text)  # ['apple', ' banana', ' orange', 'grape']

# Groups
phone_pattern = r'(\\d{3})-(\\d{3})-(\\d{4})'
match = re.search(phone_pattern, text)
if match:
    print(f"Area code: {match.group(1)}")  # 123
    print(f"Number: {match.group(2)}-{match.group(3)}")  # 456-7890""",
                        "interview_questions": """1. What are regular expressions and when do you use them?
2. What is the difference between re.match() and re.search()?
3. How do you use groups in regular expressions?
4. What are some common regex patterns?""",
                        "duration": 20,
                        "order": 1,
                        "quiz": [
                            {
                                "question": "Which regex function searches the entire string for a match?",
                                "options": ["re.search()", "re.match()", "re.findall()", "re.finditer()"],
                                "correct_answer": 0,
                                "explanation": "re.search() searches the entire string for a match."
                            }
                        ]
                    }
                ]
            },
            # ===== MODULE 20 =====
            {
                "title": "Module 20: Date and Time",
                "description": "Working with datetime and time",
                "order": 20,
                "lessons": [
                    {
                        "title": "Date and Time",
                        "description": "Handling date and time operations",
                        "concept": """# Date and Time in Python

## Key Modules:
- `datetime` - Basic date/time operations
- `time` - Time-related functions
- `calendar` - Calendar operations

## Datetime Objects:
| Class | Description |
|-------|-------------|
| `datetime.date` | Year, month, day |
| `datetime.time` | Hour, minute, second, microsecond |
| `datetime.datetime` | Date + Time |
| `datetime.timedelta` | Duration |

## Creating Dates:
```python
from datetime import datetime, date, time, timedelta

now = datetime.now()
today = date.today()
specific = datetime(2023, 12, 25, 10, 30, 0)
```

## Formatting:
- `strftime()` - Format datetime to string
- `strptime()` - Parse string to datetime

## Operations:
- Adding/subtracting timedelta
- Comparing dates
- Calculating differences""",
                        "example": """from datetime import datetime, date, time, timedelta
import time as time_module

# Current date and time
now = datetime.now()
print(f"Current: {now}")

# Formatting dates
formatted = now.strftime("%Y-%m-%d %H:%M:%S")
print(f"Formatted: {formatted}")

# Parsing strings
date_string = "2023-12-25 10:30:00"
parsed = datetime.strptime(date_string, "%Y-%m-%d %H:%M:%S")
print(f"Parsed: {parsed}")

# Date arithmetic
today = date.today()
future = today + timedelta(days=30)
print(f"Today: {today}, Future: {future}")
print(f"Days between: {(future - today).days}")

# Time differences
start = datetime.now()
time_module.sleep(2)
end = datetime.now()
difference = end - start
print(f"Elapsed: {difference.total_seconds():.2f} seconds")

# Specific date
christmas = datetime(2023, 12, 25, 0, 0, 0)
print(f"Days until Christmas: {(christmas - now).days}")

# Date comparisons
if today > date(2023, 1, 1):
    print("After 2023")

# Timezone aware (pytz library)
import pytz
utc = pytz.UTC
now_utc = datetime.now(utc)
print(f"UTC time: {now_utc}")""",
                        "interview_questions": """1. How do you work with dates and times in Python?
2. What is the difference between datetime and timedelta?
3. How do you format dates in Python?
4. What is the difference between strftime and strptime?""",
                        "duration": 20,
                        "order": 1,
                        "quiz": [
                            {
                                "question": "Which method gets the current date and time?",
                                "options": ["datetime.now()", "datetime.today()", "datetime.current()", "datetime.get_now()"],
                                "correct_answer": 0,
                                "explanation": "datetime.now() returns the current date and time."
                            }
                        ]
                    }
                ]
            }
        ]

        # Add Python modules to database
        for mod_data in python_modules:
            module = Module(
                course_id=python_course.id,
                title=mod_data["title"],
                description=mod_data["description"],
                order=mod_data["order"]
            )
            db.add(module)
            db.commit()
            db.refresh(module)

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
                db.refresh(lesson)

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

        print(f"✅ Python Course: {len(python_course.modules)} modules created!")

        # ============================================
        # JAVA COURSE - 20 MODULES
        # ============================================
        print("\n📚 Creating Java Course with 20 Modules...")

        java_course = Course(
            title="Core Java - Zero to Hero",
            description="Complete Java course with 20 modules - from basics to advanced",
            category="Programming",
            difficulty="INTERMEDIATE",
            duration=120,
            instructor_id=instructor.id,
            price=9999,
            is_published=True
        )
        db.add(java_course)
        db.commit()
        db.refresh(java_course)
        print(f"✅ Java Course created (ID: {java_course.id})")

        # ==================== 20 JAVA MODULES ====================
        java_modules = [
            # Module 1
            {
                "title": "Module 1: Getting Started with Java",
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
3. Explain WORA in Java.
4. What is the difference between JDK, JRE, and JVM?""",
                        "duration": 25,
                        "order": 2,
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
3. What is type casting in Java?
4. What is the difference between int and Integer?""",
                        "duration": 30,
                        "order": 3,
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
            # Module 2
            {
                "title": "Module 2: OOP Concepts",
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
}

// Creating Objects
Car myCar = new Car();
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
3. Explain the difference between class and object.
4. What is the default constructor?""",
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
            # Module 3
            {
                "title": "Module 3: Advanced Java",
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
```

## Throw vs Throws:
- `throw` - Used to throw an exception explicitly
- `throws` - Declares that a method might throw an exception""",
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
3. What is the difference between throw and throws?
4. What is the purpose of the finally block?""",
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
            },
            # Module 4
            {
                "title": "Module 4: Inheritance & Polymorphism",
                "description": "Inheritance and Polymorphism in Java",
                "order": 4,
                "lessons": [
                    {
                        "title": "Inheritance",
                        "description": "Extending classes",
                        "concept": """# Inheritance in Java
Inheritance allows a class to inherit properties from another class.

## Syntax:
```java
class Parent {
    // Parent class
}

class Child extends Parent {
    // Child class inherits from Parent
}
```

## Key Concepts:
- `extends` keyword
- `super` keyword
- Method overriding
- Inheritance types: Single, Multilevel, Hierarchical

## Types of Inheritance:
1. **Single** - One parent
2. **Multilevel** - Chain of inheritance
3. **Hierarchical** - Multiple children
4. **Multiple** - Not supported in Java (use interfaces)""",
                        "example": """# Inheritance Example
class Animal {
    String name;
    
    Animal(String name) {
        this.name = name;
    }
    
    void eat() {
        System.out.println(name + " is eating");
    }
}

class Dog extends Animal {
    Dog(String name) {
        super(name);
    }
    
    void bark() {
        System.out.println(name + " barks loudly!");
    }
}

class Cat extends Animal {
    Cat(String name) {
        super(name);
    }
    
    void meow() {
        System.out.println(name + " meows softly!");
    }
}

public class Main {
    public static void main(String[] args) {
        Dog dog = new Dog("Buddy");
        Cat cat = new Cat("Whiskers");
        
        dog.eat();   // Buddy is eating
        dog.bark();  // Buddy barks loudly!
        cat.eat();   // Whiskers is eating
        cat.meow();  // Whiskers meows softly!
    }
}""",
                        "interview_questions": """1. What is inheritance in Java?
2. What is the difference between extends and implements?
3. What is method overriding?
4. What is the super keyword used for?
5. Why doesn't Java support multiple inheritance?""",
                        "duration": 30,
                        "order": 1,
                        "quiz": [
                            {
                                "question": "Which keyword is used for inheritance in Java?",
                                "options": ["extends", "implements", "inherit", "super"],
                                "correct_answer": 0,
                                "explanation": "extends is used for inheritance."
                            }
                        ]
                    },
                    {
                        "title": "Polymorphism",
                        "description": "Method overloading and overriding",
                        "concept": """# Polymorphism in Java
Polymorphism means many forms.

## Method Overloading:
Same method name, different parameters.
```java
class Calculator {
    int add(int a, int b) { return a + b; }
    int add(int a, int b, int c) { return a + b + c; }
    double add(double a, double b) { return a + b; }
}
```

## Method Overriding:
Child class provides specific implementation.
```java
class Animal {
    void sound() { System.out.println("Animal sound"); }
}

class Dog extends Animal {
    @Override
    void sound() { System.out.println("Bark"); }
}
```

## Runtime Polymorphism:
```java
Animal animal = new Dog();
animal.sound();  // Bark
```""",
                        "example": """# Polymorphism Examples
class Shape {
    void draw() {
        System.out.println("Drawing shape");
    }
}

class Circle extends Shape {
    @Override
    void draw() {
        System.out.println("Drawing circle");
    }
}

class Rectangle extends Shape {
    @Override
    void draw() {
        System.out.println("Drawing rectangle");
    }
}

class Triangle extends Shape {
    @Override
    void draw() {
        System.out.println("Drawing triangle");
    }
}

public class Main {
    public static void main(String[] args) {
        Shape[] shapes = {
            new Circle(),
            new Rectangle(),
            new Triangle()
        };
        
        for (Shape shape : shapes) {
            shape.draw();  // Runtime polymorphism
        }
        // Drawing circle
        // Drawing rectangle
        // Drawing triangle
    }
}""",
                        "interview_questions": """1. What is polymorphism in Java?
2. What is the difference between method overloading and overriding?
3. What is dynamic method dispatch?
4. What is the @Override annotation used for?
5. What is the difference between compile-time and runtime polymorphism?""",
                        "duration": 30,
                        "order": 2,
                        "quiz": [
                            {
                                "question": "Which is an example of method overloading?",
                                "options": ["Same name, different parameters", "Different name, same parameters", "Same name, same parameters", "None"],
                                "correct_answer": 0,
                                "explanation": "Method overloading is same method name with different parameters."
                            }
                        ]
                    }
                ]
            },
            # Module 5
            {
                "title": "Module 5: Interfaces & Abstract Classes",
                "description": "Abstraction in Java",
                "order": 5,
                "lessons": [
                    {
                        "title": "Abstract Classes",
                        "description": "Abstract classes and methods",
                        "concept": """# Abstract Classes in Java

## Abstract Class:
Cannot be instantiated, may contain abstract methods.

```java
abstract class Vehicle {
    abstract void start();
    
    void stop() {
        System.out.println("Vehicle stopped");
    }
}
```

## Abstract Method:
Declared without implementation.

```java
abstract void start();
```

## Key Points:
- Can have both abstract and concrete methods
- Can have constructors
- Can have instance variables
- Used for code reuse and standardization""",
                        "example": """# Abstract Class Example
abstract class Animal {
    abstract void sound();
    
    void sleep() {
        System.out.println("Sleeping...");
    }
}

class Dog extends Animal {
    @Override
    void sound() {
        System.out.println("Bark");
    }
}

class Cat extends Animal {
    @Override
    void sound() {
        System.out.println("Meow");
    }
}

public class Main {
    public static void main(String[] args) {
        Animal dog = new Dog();
        Animal cat = new Cat();
        
        dog.sound();  // Bark
        dog.sleep();  // Sleeping...
        cat.sound();  // Meow
    }
}""",
                        "interview_questions": """1. What is an abstract class in Java?
2. What is the difference between abstract class and interface?
3. When would you use an abstract class?
4. Can an abstract class have concrete methods?
5. What is an abstract method?""",
                        "duration": 25,
                        "order": 1,
                        "quiz": [
                            {
                                "question": "Which can have both abstract and concrete methods?",
                                "options": ["Abstract class", "Interface", "Both", "None"],
                                "correct_answer": 0,
                                "explanation": "Abstract classes can have both abstract and concrete methods."
                            }
                        ]
                    },
                    {
                        "title": "Interfaces",
                        "description": "Interfaces in Java",
                        "concept": """# Interfaces in Java
Interface is a contract that classes can implement.

## Interface Definition:
```java
interface Driveable {
    void drive();
    void stop();
}
```

## Interface Features:
- All methods are public and abstract by default
- Can have default methods (Java 8+)
- Can have static methods (Java 8+)
- Can have constants (public static final)

## Multiple Interface Implementation:
```java
class Car implements Driveable, Flyable {
    // Implement all methods from both interfaces
}
```""",
                        "example": """# Interface Examples
interface Flyable {
    void fly();
}

interface Swimmable {
    void swim();
}

interface Runnable {
    void run();
}

class Bird implements Flyable, Runnable {
    @Override
    public void fly() {
        System.out.println("Bird is flying");
    }
    
    @Override
    public void run() {
        System.out.println("Bird is running");
    }
}

class Duck implements Flyable, Swimmable, Runnable {
    @Override
    public void fly() {
        System.out.println("Duck is flying");
    }
    
    @Override
    public void swim() {
        System.out.println("Duck is swimming");
    }
    
    @Override
    public void run() {
        System.out.println("Duck is running");
    }
}

public class Main {
    public static void main(String[] args) {
        Bird bird = new Bird();
        Duck duck = new Duck();
        
        bird.fly();   // Bird is flying
        bird.run();   // Bird is running
        duck.fly();   // Duck is flying
        duck.swim();  // Duck is swimming
        duck.run();   // Duck is running
    }
}""",
                        "interview_questions": """1. What is an interface in Java?
2. What is the difference between abstract class and interface?
3. What are default methods in interfaces?
4. Can a class implement multiple interfaces?
5. What are functional interfaces?""",
                        "duration": 25,
                        "order": 2,
                        "quiz": [
                            {
                                "question": "Which keyword is used to implement an interface?",
                                "options": ["implements", "extends", "inherits", "uses"],
                                "correct_answer": 0,
                                "explanation": "implements is used to implement an interface."
                            }
                        ]
                    }
                ]
            },
            # Module 6
            {
                "title": "Module 6: Collections Framework",
                "description": "Java Collections Framework",
                "order": 6,
                "lessons": [
                    {
                        "title": "ArrayList",
                        "description": "Dynamic arrays in Java",
                        "concept": """# ArrayList in Java
ArrayList is a resizable array implementation.

## Creating ArrayList:
```java
ArrayList<String> list = new ArrayList<>();
List<String> list = new ArrayList<>();
```

## Common Methods:
- `add()` - Add element
- `get()` - Get element at index
- `set()` - Set element at index
- `remove()` - Remove element
- `size()` - Get size
- `contains()` - Check if contains
- `clear()` - Remove all

## Features:
- Dynamic sizing
- Ordered
- Allows duplicates
- Random access fast""",
                        "example": """# ArrayList Examples
import java.util.ArrayList;

public class Main {
    public static void main(String[] args) {
        ArrayList<String> fruits = new ArrayList<>();
        
        // Add elements
        fruits.add("Apple");
        fruits.add("Banana");
        fruits.add("Orange");
        
        System.out.println(fruits);  // [Apple, Banana, Orange]
        
        // Get element
        System.out.println(fruits.get(1));  // Banana
        
        // Set element
        fruits.set(1, "Mango");
        System.out.println(fruits);  // [Apple, Mango, Orange]
        
        // Remove element
        fruits.remove(0);
        System.out.println(fruits);  // [Mango, Orange]
        
        // Size
        System.out.println(fruits.size());  // 2
        
        // Check contains
        System.out.println(fruits.contains("Mango"));  // true
        
        // Iterate
        for (String fruit : fruits) {
            System.out.println(fruit);
        }
    }
}""",
                        "interview_questions": """1. What is ArrayList in Java?
2. What is the difference between ArrayList and LinkedList?
3. What is the difference between ArrayList and Array?
4. How does ArrayList dynamically resize?""",
                        "duration": 25,
                        "order": 1,
                        "quiz": [
                            {
                                "question": "Which method adds an element to ArrayList?",
                                "options": ["add()", "append()", "insert()", "push()"],
                                "correct_answer": 0,
                                "explanation": "add() is used to add elements to ArrayList."
                            }
                        ]
                    },
                    {
                        "title": "HashMap",
                        "description": "Key-value pairs in Java",
                        "concept": """# HashMap in Java
HashMap stores key-value pairs.

## Creating HashMap:
```java
HashMap<String, Integer> map = new HashMap<>();
Map<String, Integer> map = new HashMap<>();
```

## Common Methods:
- `put()` - Add key-value pair
- `get()` - Get value by key
- `remove()` - Remove by key
- `containsKey()` - Check key exists
- `containsValue()` - Check value exists
- `keySet()` - Get all keys
- `values()` - Get all values
- `entrySet()` - Get all entries

## Features:
- Key-value pairs
- No duplicate keys
- One null key allowed
- Many null values allowed""",
                        "example": """# HashMap Examples
import java.util.HashMap;

public class Main {
    public static void main(String[] args) {
        HashMap<String, Integer> studentGrades = new HashMap<>();
        
        // Add key-value pairs
        studentGrades.put("Alice", 85);
        studentGrades.put("Bob", 90);
        studentGrades.put("Charlie", 78);
        
        System.out.println(studentGrades);  // {Alice=85, Bob=90, Charlie=78}
        
        // Get value
        System.out.println(studentGrades.get("Alice"));  // 85
        
        // Remove
        studentGrades.remove("Charlie");
        System.out.println(studentGrades);  // {Alice=85, Bob=90}
        
        // Check key
        System.out.println(studentGrades.containsKey("Bob"));  // true
        
        // Iterate
        for (String name : studentGrades.keySet()) {
            System.out.println(name + ": " + studentGrades.get(name));
        }
    }
}""",
                        "interview_questions": """1. What is HashMap in Java?
2. What is the difference between HashMap and Hashtable?
3. What is the difference between HashMap and TreeMap?
4. How does HashMap handle collisions?""",
                        "duration": 25,
                        "order": 2,
                        "quiz": [
                            {
                                "question": "Which method adds a key-value pair to HashMap?",
                                "options": ["put()", "add()", "insert()", "set()"],
                                "correct_answer": 0,
                                "explanation": "put() is used to add key-value pairs to HashMap."
                            }
                        ]
                    }
                ]
            },
            # Module 7
            {
                "title": "Module 7: Multithreading",
                "description": "Threads and concurrency",
                "order": 7,
                "lessons": [
                    {
                        "title": "Thread Basics",
                        "description": "Creating and starting threads",
                        "concept": """# Multithreading in Java
A thread is a lightweight process.

## Creating Threads:
1. Extend Thread class
2. Implement Runnable interface

## Thread Lifecycle:
1. New
2. Runnable
3. Running
4. Blocked/Waiting
5. Terminated

## Common Methods:
- `start()` - Start thread
- `run()` - Thread body
- `sleep()` - Pause thread
- `join()` - Wait for thread
- `yield()` - Yield CPU""",
                        "example": """# Thread Examples
class MyThread extends Thread {
    @Override
    public void run() {
        for (int i = 0; i < 5; i++) {
            System.out.println("Thread: " + i);
            try {
                Thread.sleep(500);
            } catch (InterruptedException e) {
                e.printStackTrace();
            }
        }
    }
}

class MyRunnable implements Runnable {
    @Override
    public void run() {
        for (int i = 0; i < 5; i++) {
            System.out.println("Runnable: " + i);
        }
    }
}

public class Main {
    public static void main(String[] args) {
        // Thread class
        MyThread t1 = new MyThread();
        t1.start();
        
        // Runnable interface
        Thread t2 = new Thread(new MyRunnable());
        t2.start();
        
        // Lambda
        Thread t3 = new Thread(() -> {
            for (int i = 0; i < 5; i++) {
                System.out.println("Lambda: " + i);
            }
        });
        t3.start();
    }
}""",
                        "interview_questions": """1. What is a thread in Java?
2. What is the difference between extending Thread and implementing Runnable?
3. What is the thread lifecycle?
4. What is the difference between start() and run()?""",
                        "duration": 25,
                        "order": 1,
                        "quiz": [
                            {
                                "question": "Which method starts a thread?",
                                "options": ["start()", "run()", "begin()", "execute()"],
                                "correct_answer": 0,
                                "explanation": "start() is used to start a thread."
                            }
                        ]
                    }
                ]
            },
            # Module 8
            {
                "title": "Module 8: File I/O",
                "description": "File operations in Java",
                "order": 8,
                "lessons": [
                    {
                        "title": "File Operations",
                        "description": "Reading and writing files",
                        "concept": """# File I/O in Java

## File Classes:
- `File` - File/directory information
- `FileReader` - Read text files
- `FileWriter` - Write text files
- `BufferedReader` - Efficient reading
- `BufferedWriter` - Efficient writing
- `PrintWriter` - Formatted writing

## Reading Files:
```java
try (FileReader fr = new FileReader("file.txt");
     BufferedReader br = new BufferedReader(fr)) {
    String line;
    while ((line = br.readLine()) != null) {
        System.out.println(line);
    }
} catch (IOException e) {
    e.printStackTrace();
}
```

## Writing Files:
```java
try (FileWriter fw = new FileWriter("file.txt");
     BufferedWriter bw = new BufferedWriter(fw)) {
    bw.write("Hello World!");
    bw.newLine();
} catch (IOException e) {
    e.printStackTrace();
}
```""",
                        "example": """# File I/O Examples
import java.io.*;
import java.util.*;

public class Main {
    public static void main(String[] args) {
        // Writing to file
        try (PrintWriter writer = new PrintWriter("output.txt")) {
            writer.println("Hello World!");
            writer.println("Java is great!");
        } catch (FileNotFoundException e) {
            e.printStackTrace();
        }
        
        // Reading from file
        try (BufferedReader reader = new BufferedReader(new FileReader("output.txt"))) {
            String line;
            while ((line = reader.readLine()) != null) {
                System.out.println(line);
            }
        } catch (IOException e) {
            e.printStackTrace();
        }
        
        // Reading all lines
        try {
            List<String> lines = Files.readAllLines(Paths.get("output.txt"));
            System.out.println("All lines: " + lines);
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
}""",
                        "interview_questions": """1. How do you read a file in Java?
2. What is the difference between FileReader and BufferedReader?
3. What is try-with-resources?
4. How do you handle IOException in Java?""",
                        "duration": 25,
                        "order": 1,
                        "quiz": [
                            {
                                "question": "Which class is used to read text files efficiently?",
                                "options": ["BufferedReader", "FileReader", "FileInputStream", "Scanner"],
                                "correct_answer": 0,
                                "explanation": "BufferedReader is used for efficient reading of text files."
                            }
                        ]
                    }
                ]
            },
            # Module 9
            {
                "title": "Module 9: Lambda Expressions",
                "description": "Functional programming in Java",
                "order": 9,
                "lessons": [
                    {
                        "title": "Lambda Expressions",
                        "description": "Functional programming features",
                        "concept": """# Lambda Expressions in Java
Lambda expressions provide a concise way to implement functional interfaces.

## Syntax:
```java
(parameters) -> expression
(parameters) -> { statements; }
```

## Functional Interfaces:
- `Predicate` - Test condition
- `Function` - Apply function
- `Consumer` - Consume value
- `Supplier` - Supply value

## Examples:
```java
// Without lambda
Runnable r1 = new Runnable() {
    @Override
    public void run() {
        System.out.println("Hello");
    }
};

// With lambda
Runnable r2 = () -> System.out.println("Hello");
```""",
                        "example": """# Lambda Examples
import java.util.*;
import java.util.function.*;

public class Main {
    public static void main(String[] args) {
        List<Integer> numbers = Arrays.asList(1, 2, 3, 4, 5);
        
        // Lambda for each
        numbers.forEach(n -> System.out.println(n));
        
        // Lambda for filter
        numbers.stream()
            .filter(n -> n % 2 == 0)
            .forEach(n -> System.out.println("Even: " + n));
        
        // Predicate
        Predicate<Integer> isEven = n -> n % 2 == 0;
        System.out.println(isEven.test(4));  // true
        
        // Function
        Function<Integer, String> toString = n -> "Number: " + n;
        System.out.println(toString.apply(10));  // Number: 10
        
        // Consumer
        Consumer<String> printer = s -> System.out.println(s);
        printer.accept("Hello Lambda!");
        
        // Supplier
        Supplier<Double> random = () -> Math.random();
        System.out.println(random.get());
    }
}""",
                        "interview_questions": """1. What are lambda expressions in Java?
2. What are functional interfaces?
3. What is the difference between lambda and anonymous class?
4. What are the common functional interfaces?""",
                        "duration": 25,
                        "order": 1,
                        "quiz": [
                            {
                                "question": "Which interface is used for lambda expressions?",
                                "options": ["Functional interface", "Abstract class", "Interface", "Class"],
                                "correct_answer": 0,
                                "explanation": "Lambda expressions are used with functional interfaces."
                            }
                        ]
                    }
                ]
            },
            # Module 10
            {
                "title": "Module 10: Stream API",
                "description": "Stream operations",
                "order": 10,
                "lessons": [
                    {
                        "title": "Stream API",
                        "description": "Processing collections",
                        "concept": """# Stream API in Java
Streams provide a functional way to process collections.

## Creating Streams:
```java
List<Integer> numbers = Arrays.asList(1, 2, 3, 4, 5);
Stream<Integer> stream = numbers.stream();
```

## Intermediate Operations:
- `filter()` - Filter elements
- `map()` - Transform elements
- `sorted()` - Sort elements
- `limit()` - Limit elements

## Terminal Operations:
- `forEach()` - Iterate
- `collect()` - Collect to collection
- `reduce()` - Reduce to single value
- `count()` - Count elements

## Features:
- Lazy evaluation
- Functional operations
- Parallel processing""",
                        "example": """# Stream API Examples
import java.util.*;
import java.util.stream.*;

public class Main {
    public static void main(String[] args) {
        List<Integer> numbers = Arrays.asList(1, 2, 3, 4, 5, 6, 7, 8, 9, 10);
        
        // Filter even numbers
        List<Integer> evens = numbers.stream()
            .filter(n -> n % 2 == 0)
            .collect(Collectors.toList());
        System.out.println("Evens: " + evens);  // [2, 4, 6, 8, 10]
        
        // Map to squares
        List<Integer> squares = numbers.stream()
            .map(n -> n * n)
            .collect(Collectors.toList());
        System.out.println("Squares: " + squares);  // [1, 4, 9, 16, 25, 36, 49, 64, 81, 100]
        
        // Filter and map
        List<String> strings = numbers.stream()
            .filter(n -> n > 5)
            .map(n -> "Number: " + n)
            .collect(Collectors.toList());
        System.out.println("Strings: " + strings);
        
        // Reduce
        int sum = numbers.stream()
            .reduce(0, Integer::sum);
        System.out.println("Sum: " + sum);  // 55
        
        // Count
        long count = numbers.stream()
            .filter(n -> n > 5)
            .count();
        System.out.println("Count > 5: " + count);  // 5
    }
}""",
                        "interview_questions": """1. What is Stream API in Java?
2. What is the difference between intermediate and terminal operations?
3. What is the difference between map() and flatMap()?
4. What is the purpose of reduce()?""",
                        "duration": 25,
                        "order": 1,
                        "quiz": [
                            {
                                "question": "Which operation transforms elements in a stream?",
                                "options": ["map()", "filter()", "forEach()", "collect()"],
                                "correct_answer": 0,
                                "explanation": "map() is used to transform elements in a stream."
                            }
                        ]
                    }
                ]
            },
            # Module 11
            {
                "title": "Module 11: JDBC",
                "description": "Database connectivity",
                "order": 11,
                "lessons": [
                    {
                        "title": "JDBC Basics",
                        "description": "Connecting to databases",
                        "concept": """# JDBC in Java
JDBC provides database connectivity.

## Steps:
1. Load driver
2. Connect to database
3. Create statement
4. Execute query
5. Process results
6. Close connection

## Key Classes:
- `DriverManager` - Manage drivers
- `Connection` - Database connection
- `Statement` - SQL statements
- `PreparedStatement` - Parameterized SQL
- `ResultSet` - Query results

## Connection URL:
```java
String url = "jdbc:postgresql://localhost:5432/db";
String user = "username";
String password = "password";
Connection conn = DriverManager.getConnection(url, user, password);
```""",
                        "example": """# JDBC Examples
import java.sql.*;

public class Main {
    public static void main(String[] args) {
        try {
            // Load driver
            Class.forName("org.postgresql.Driver");
            
            // Connect
            String url = "jdbc:postgresql://localhost:5432/testdb";
            Connection conn = DriverManager.getConnection(url, "user", "pass");
            
            // Create statement
            Statement stmt = conn.createStatement();
            
            // Execute query
            ResultSet rs = stmt.executeQuery("SELECT * FROM users");
            
            // Process results
            while (rs.next()) {
                int id = rs.getInt("id");
                String name = rs.getString("name");
                System.out.println("ID: " + id + ", Name: " + name);
            }
            
            // Close resources
            rs.close();
            stmt.close();
            conn.close();
            
        } catch (ClassNotFoundException e) {
            e.printStackTrace();
        } catch (SQLException e) {
            e.printStackTrace();
        }
    }
}""",
                        "interview_questions": """1. What is JDBC in Java?
2. What is the difference between Statement and PreparedStatement?
3. What is the purpose of ResultSet?
4. How do you handle SQL exceptions?""",
                        "duration": 25,
                        "order": 1,
                        "quiz": [
                            {
                                "question": "Which class is used to create a database connection?",
                                "options": ["DriverManager", "ConnectionManager", "DBManager", "SQLManager"],
                                "correct_answer": 0,
                                "explanation": "DriverManager is used to create database connections."
                            }
                        ]
                    }
                ]
            },
            # Module 12
            {
                "title": "Module 12: Servlet & JSP",
                "description": "Web development with Servlets",
                "order": 12,
                "lessons": [
                    {
                        "title": "Servlet Basics",
                        "description": "Java Web development",
                        "concept": """# Servlets in Java
Servlets are Java programs that run on web servers.

## Servlet Lifecycle:
1. `init()` - Called once
2. `service()` - Called for each request
3. `destroy()` - Called once

## HttpServlet Methods:
- `doGet()` - Handle GET requests
- `doPost()` - Handle POST requests
- `doPut()` - Handle PUT requests
- `doDelete()` - Handle DELETE requests

## Servlet Example:
```java
@WebServlet("/hello")
public class HelloServlet extends HttpServlet {
    protected void doGet(HttpServletRequest request, 
                         HttpServletResponse response) 
                         throws ServletException, IOException {
        response.setContentType("text/html");
        PrintWriter out = response.getWriter();
        out.println("<h1>Hello World!</h1>");
    }
}
```""",
                        "example": """# Servlet Examples
import java.io.*;
import javax.servlet.*;
import javax.servlet.http.*;
import javax.servlet.annotation.*;

@WebServlet("/api/users")
public class UserServlet extends HttpServlet {
    
    @Override
    protected void doGet(HttpServletRequest request, 
                         HttpServletResponse response) 
                         throws ServletException, IOException {
        response.setContentType("application/json");
        PrintWriter out = response.getWriter();
        
        // Get parameter
        String id = request.getParameter("id");
        
        if (id != null) {
            out.println("{\"id\": " + id + ", \"name\": \"User\"}");
        } else {
            out.println("[{\"id\": 1, \"name\": \"User1\"}, {\"id\": 2, \"name\": \"User2\"}]");
        }
    }
    
    @Override
    protected void doPost(HttpServletRequest request, 
                          HttpServletResponse response) 
                          throws ServletException, IOException {
        // Read request body
        BufferedReader reader = request.getReader();
        StringBuilder body = new StringBuilder();
        String line;
        while ((line = reader.readLine()) != null) {
            body.append(line);
        }
        
        // Process data
        response.setContentType("application/json");
        response.getWriter().println("{\"message\": \"User created\"}");
    }
}""",
                        "interview_questions": """1. What is a servlet in Java?
2. What is the servlet lifecycle?
3. What is the difference between doGet() and doPost()?
4. What is the purpose of web.xml?""",
                        "duration": 25,
                        "order": 1,
                        "quiz": [
                            {
                                "question": "Which method handles GET requests in servlets?",
                                "options": ["doGet()", "doPost()", "service()", "handleGet()"],
                                "correct_answer": 0,
                                "explanation": "doGet() is used to handle GET requests."
                            }
                        ]
                    }
                ]
            },
            # Module 13
            {
                "title": "Module 13: Spring Framework",
                "description": "Spring Framework basics",
                "order": 13,
                "lessons": [
                    {
                        "title": "Spring Core",
                        "description": "IOC and Dependency Injection",
                        "concept": """# Spring Framework
Spring provides comprehensive infrastructure for enterprise applications.

## Core Concepts:
1. **IoC** - Inversion of Control
2. **DI** - Dependency Injection
3. **AOP** - Aspect Oriented Programming
4. **MVC** - Model View Controller

## Dependency Injection:
```java
@Component
public class UserService {
    @Autowired
    private UserRepository userRepository;
    
    public User findUser(int id) {
        return userRepository.findById(id);
    }
}
```

## Configuration:
```java
@Configuration
@ComponentScan
public class AppConfig {
    @Bean
    public DataSource dataSource() {
        return DataSourceBuilder.create()
            .url("jdbc:postgresql://localhost:5432/db")
            .build();
    }
}
```""",
                        "example": """# Spring Examples
import org.springframework.stereotype.*;
import org.springframework.beans.factory.annotation.*;
import org.springframework.web.bind.annotation.*;

// Controller
@RestController
@RequestMapping("/api/users")
public class UserController {
    
    @Autowired
    private UserService userService;
    
    @GetMapping("/{id}")
    public User getUser(@PathVariable int id) {
        return userService.getUser(id);
    }
    
    @PostMapping
    public User createUser(@RequestBody User user) {
        return userService.createUser(user);
    }
}

// Service
@Service
public class UserService {
    
    @Autowired
    private UserRepository userRepository;
    
    public User getUser(int id) {
        return userRepository.findById(id).orElse(null);
    }
    
    public User createUser(User user) {
        return userRepository.save(user);
    }
}

// Repository
@Repository
public interface UserRepository extends JpaRepository<User, Integer> {
    // CRUD methods automatically provided
}""",
                        "interview_questions": """1. What is Spring Framework?
2. What is Dependency Injection in Spring?
3. What is the difference between @Component and @Bean?
4. What is the purpose of @Autowired?""",
                        "duration": 30,
                        "order": 1,
                        "quiz": [
                            {
                                "question": "Which annotation is used for dependency injection?",
                                "options": ["@Autowired", "@Inject", "@Component", "@Service"],
                                "correct_answer": 0,
                                "explanation": "@Autowired is used for dependency injection."
                            }
                        ]
                    }
                ]
            },
            # Module 14
            {
                "title": "Module 14: Spring Boot",
                "description": "Spring Boot framework",
                "order": 14,
                "lessons": [
                    {
                        "title": "Spring Boot Basics",
                        "description": "Standalone Spring applications",
                        "concept": """# Spring Boot
Spring Boot simplifies Spring application development.

## Key Features:
1. **Auto-configuration** - Automatic configuration
2. **Embedded Servers** - Tomcat, Jetty, Undertow
3. **Starter Dependencies** - Pre-configured dependencies
4. **Actuator** - Production-ready features
5. **CLI** - Command line interface

## Spring Boot Application:
```java
@SpringBootApplication
public class Application {
    public static void main(String[] args) {
        SpringApplication.run(Application.class, args);
    }
}
```

## Application Properties:
```properties
# application.properties
server.port=8080
spring.datasource.url=jdbc:postgresql://localhost:5432/db
spring.datasource.username=user
spring.datasource.password=pass
```""",
                        "example": """# Spring Boot Examples
import org.springframework.boot.*;
import org.springframework.boot.autoconfigure.*;
import org.springframework.web.bind.annotation.*;

@RestController
@SpringBootApplication
public class Application {
    
    public static void main(String[] args) {
        SpringApplication.run(Application.class, args);
    }
    
    @GetMapping("/hello")
    public String hello() {
        return "Hello, Spring Boot!";
    }
}

// REST API
@RestController
@RequestMapping("/api")
public class UserController {
    
    @GetMapping("/users")
    public List<User> getUsers() {
        return userService.findAll();
    }
    
    @GetMapping("/users/{id}")
    public ResponseEntity<User> getUser(@PathVariable Long id) {
        return userService.findById(id)
            .map(ResponseEntity::ok)
            .orElse(ResponseEntity.notFound().build());
    }
}

// JPA Entity
@Entity
@Table(name = "users")
public class User {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    
    @Column(nullable = false)
    private String name;
    
    @Column(unique = true)
    private String email;
    
    // getters and setters
}""",
                        "interview_questions": """1. What is Spring Boot?
2. What is the advantage of Spring Boot over Spring?
3. What is the @SpringBootApplication annotation?
4. What is the purpose of application.properties?""",
                        "duration": 30,
                        "order": 1,
                        "quiz": [
                            {
                                "question": "Which annotation marks a Spring Boot application?",
                                "options": ["@SpringBootApplication", "@SpringApplication", "@BootApplication", "@SpringApp"],
                                "correct_answer": 0,
                                "explanation": "@SpringBootApplication is the main annotation for Spring Boot applications."
                            }
                        ]
                    }
                ]
            },
            # Module 15
            {
                "title": "Module 15: Spring Data JPA",
                "description": "Spring Data JPA",
                "order": 15,
                "lessons": [
                    {
                        "title": "Spring Data JPA",
                        "description": "Database access with Spring",
                        "concept": """# Spring Data JPA
Spring Data JPA simplifies database access.

## Repository Interface:
```java
@Repository
public interface UserRepository extends JpaRepository<User, Long> {
    // CRUD methods automatically provided
    
    // Custom query methods
    List<User> findByName(String name);
    Optional<User> findByEmail(String email);
    List<User> findByAgeGreaterThan(int age);
    
    // Custom query with JPQL
    @Query("SELECT u FROM User u WHERE u.name LIKE %:name%")
    List<User> searchByName(@Param("name") String name);
}
```

## Query Methods:
- `findBy...` - Find by property
- `findBy...And...` - Multiple conditions
- `findBy...Or...` - OR conditions
- `existsBy...` - Check existence
- `countBy...` - Count results
- `deleteBy...` - Delete by property

## Custom Queries:
- `@Query` - JPQL queries
- `@Query` with nativeQuery - SQL queries
- `@Modifying` - Update/delete queries""",
                        "example": """# Spring Data JPA Examples
import org.springframework.data.jpa.repository.*;
import org.springframework.data.repository.query.Param;
import org.springframework.stereotype.Repository;
import java.util.*;

@Repository
public interface UserRepository extends JpaRepository<User, Long> {
    
    // Query methods
    List<User> findByName(String name);
    Optional<User> findByEmail(String email);
    List<User> findByNameContainingIgnoreCase(String name);
    List<User> findByAgeBetween(int minAge, int maxAge);
    
    // JPQL query
    @Query("SELECT u FROM User u WHERE u.email LIKE :domain")
    List<User> findByEmailDomain(@Param("domain") String domain);
    
    // Native SQL query
    @Query(value = "SELECT * FROM users WHERE age > :age", nativeQuery = true)
    List<User> findUsersOlderThan(@Param("age") int age);
    
    // Count
    long countByAgeGreaterThan(int age);
    
    // Check existence
    boolean existsByEmail(String email);
    
    // Delete
    void deleteByName(String name);
}

// Service using repository
@Service
public class UserService {
    @Autowired
    private UserRepository userRepository;
    
    public List<User> getUsersByName(String name) {
        return userRepository.findByName(name);
    }
    
    public User getUserByEmail(String email) {
        return userRepository.findByEmail(email)
            .orElseThrow(() -> new RuntimeException("User not found"));
    }
    
    public List<User> getUsersByAgeRange(int min, int max) {
        return userRepository.findByAgeBetween(min, max);
    }
}""",
                        "interview_questions": """1. What is Spring Data JPA?
2. What is the difference between JpaRepository and CrudRepository?
3. How do you write custom queries in Spring Data JPA?
4. What is the purpose of @Query annotation?
5. What are the naming conventions for query methods?""",
                        "duration": 25,
                        "order": 1,
                        "quiz": [
                            {
                                "question": "Which interface extends JpaRepository?",
                                "options": ["@Repository", "CrudRepository", "PagingAndSortingRepository", "All"],
                                "correct_answer": 3,
                                "explanation": "All are used in Spring Data JPA hierarchy."
                            }
                        ]
                    }
                ]
            },
            # Module 16
            {
                "title": "Module 16: Microservices",
                "description": "Microservices architecture",
                "order": 16,
                "lessons": [
                    {
                        "title": "Microservices Basics",
                        "description": "Microservices architecture",
                        "concept": """# Microservices Architecture
Microservices is an architectural style for building applications as a collection of services.

## Key Concepts:
1. **Services** - Independent, deployable units
2. **API Gateway** - Single entry point
3. **Service Registry** - Service discovery
4. **Circuit Breaker** - Fault tolerance
5. **Distributed Tracing** - Monitoring

## Service Communication:
1. **Synchronous** - REST APIs, gRPC
2. **Asynchronous** - Message queues, Events

## Benefits:
- Scalability- Independent deployment
- Technology diversity
- Team autonomy

## Challenges:
- Complexity
- Network latency
- Distributed transactions
- Monitoring""",
                        "example": """# Microservices Examples
import org.springframework.cloud.openfeign.*;
import org.springframework.web.bind.annotation.*;

// Service A - User Service
@RestController
@RequestMapping("/users")
public class UserController {
    
    @GetMapping("/{id}")
    public User getUser(@PathVariable Long id) {
        return userService.findById(id);
    }
}

// Service B - Order Service with Feign Client
@FeignClient(name = "user-service", url = "${user.service.url}")
public interface UserServiceClient {
    @GetMapping("/users/{id}")
    User getUser(@PathVariable("id") Long id);
}

@RestController
@RequestMapping("/orders")
public class OrderController {
    
    @Autowired
    private UserServiceClient userServiceClient;
    
    @GetMapping("/user/{userId}")
    public List<Order> getOrdersForUser(@PathVariable Long userId) {
        User user = userServiceClient.getUser(userId);
        // Process orders for user
        return orderService.findByUser(user);
    }
}

// Service Registry (Eureka)
@SpringBootApplication
@EnableEurekaServer
public class ServiceRegistryApplication {
    public static void main(String[] args) {
        SpringApplication.run(ServiceRegistryApplication.class, args);
    }
}

// API Gateway
@SpringBootApplication
@EnableZuulProxy
public class ApiGatewayApplication {
    public static void main(String[] args) {
        SpringApplication.run(ApiGatewayApplication.class, args);
    }
}""",
                        "interview_questions": """1. What are microservices?
2. What is the difference between monolithic and microservices?
3. What is an API Gateway?
4. What is service discovery?
5. What is circuit breaker pattern?""",
                        "duration": 30,
                        "order": 1,
                        "quiz": [
                            {
                                "question": "What is the main advantage of microservices?",
                                "options": ["Independent deployment", "Less complexity", "No network calls", "Single codebase"],
                                "correct_answer": 0,
                                "explanation": "Microservices allow independent deployment and scaling of each service."
                            }
                        ]
                    }
                ]
            },
            # Module 17
            {
                "title": "Module 17: Docker",
                "description": "Containerization with Docker",
                "order": 17,
                "lessons": [
                    {
                        "title": "Docker Basics",
                        "description": "Containerization fundamentals",
                        "concept": """# Docker Fundamentals
Docker is a platform for containerizing applications.

## Key Concepts:
- **Image** - Read-only template
- **Container** - Running instance of image
- **Dockerfile** - Instructions to build image
- **Docker Compose** - Multi-container orchestration

## Dockerfile:
```dockerfile
FROM openjdk:11-jre-slim
WORKDIR /app
COPY target/app.jar app.jar
EXPOSE 8080
ENTRYPOINT ["java", "-jar", "app.jar"]
```

## Common Commands:
- `docker build` - Build image
- `docker run` - Run container
- `docker ps` - List containers
- `docker stop` - Stop container
- `docker rm` - Remove container
- `docker images` - List images""",
                        "example": """# Dockerfile Examples
# Dockerfile for Spring Boot
FROM openjdk:11-jre-slim
COPY target/app.jar app.jar
EXPOSE 8080
ENTRYPOINT ["java", "-jar", "app.jar"]

# Dockerfile for Python
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "app.py"]

# Dockerfile for Node.js
FROM node:18-alpine
WORKDIR /app
COPY package*.json .
RUN npm install
COPY . .
CMD ["npm", "start"]

# docker-compose.yml
version: '3.8'
services:
  app:
    build: .
    ports:
      - "8080:8080"
    environment:
      - SPRING_PROFILES_ACTIVE=docker
    depends_on:
      - db
  
  db:
    image: postgres:15
    environment:
      - POSTGRES_USER=user
      - POSTGRES_PASSWORD=pass
      - POSTGRES_DB=app
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  postgres_data:
  ```""",
                        "interview_questions": """1. What is Docker?
2. What is the difference between Docker image and container?
3. What is the purpose of Dockerfile?
4. What is Docker Compose?
5. What is the difference between Docker and virtual machines?""",
                        "duration": 25,
                        "order": 1,
                        "quiz": [
                            {
                                "question": "Which file defines Docker container instructions?",
                                "options": ["Dockerfile", "docker-compose.yml", "Docker.json", "container.txt"],
                                "correct_answer": 0,
                                "explanation": "Dockerfile contains instructions to build a Docker image."
                            }
                        ]
                    }
                ]
            },
            # Module 18
            {
                "title": "Module 18: Kubernetes",
                "description": "Container orchestration",
                "order": 18,
                "lessons": [
                    {
                        "title": "Kubernetes Basics",
                        "description": "Container orchestration platform",
                        "concept": """# Kubernetes Fundamentals
Kubernetes is a container orchestration platform.

## Key Concepts:
- **Pod** - Smallest deployable unit
- **Service** - Stable networking endpoint
- **Deployment** - Application management
- **Ingress** - External access

## Kubectl Commands:
- `kubectl apply` - Apply configuration
- `kubectl get pods` - List pods
- `kubectl logs` - View logs
- `kubectl describe` - Show details
- `kubectl delete` - Delete resource

## Resources:
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: app-deployment
spec:
  replicas: 3
  selector:
    matchLabels:
      app: myapp
  template:
    metadata:
      labels:
        app: myapp
    spec:
      containers:
      - name: app
        image: app:latest
        ports:
        - containerPort: 8080
```""",
                        "example": """# Kubernetes Examples
# deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: app-deployment
spec:
  replicas: 3
  selector:
    matchLabels:
      app: myapp
  template:
    metadata:
      labels:
        app: myapp
    spec:
      containers:
      - name: app
        image: myapp:1.0
        ports:
        - containerPort: 8080
        env:
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: db-secret
              key: url

# service.yaml
apiVersion: v1
kind: Service
metadata:
  name: app-service
spec:
  selector:
    app: myapp
  ports:
  - port: 80
    targetPort: 8080
  type: LoadBalancer

# ingress.yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: app-ingress
spec:
  rules:
  - host: myapp.example.com
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: app-service
            port:
              number: 80

# secret.yaml
apiVersion: v1
kind: Secret
metadata:
  name: db-secret
type: Opaque
data:
  url: amRiYzpwb3N0Z3Jlc3FsOi8vbG9jYWxob3N0...  # base64 encoded
  ```""",
                        "interview_questions": """1. What is Kubernetes?
2. What is the difference between Docker and Kubernetes?
3. What is a pod in Kubernetes?
4. What is the purpose of a service in Kubernetes?
5. What is the difference between Deployment and StatefulSet?""",
                        "duration": 25,
                        "order": 1,
                        "quiz": [
                            {
                                "question": "What is the smallest deployable unit in Kubernetes?",
                                "options": ["Pod", "Container", "Service", "Deployment"],
                                "correct_answer": 0,
                                "explanation": "Pod is the smallest deployable unit in Kubernetes."
                            }
                        ]
                    }
                ]
            },
            # Module 19
            {
                "title": "Module 19: AWS Cloud",
                "description": "Amazon Web Services",
                "order": 19,
                "lessons": [
                    {
                        "title": "AWS Basics",
                        "description": "Cloud computing with AWS",
                        "concept": """# Amazon Web Services
AWS is a comprehensive cloud computing platform.

## Core Services:
1. **Compute** - EC2, Lambda
2. **Storage** - S3, EBS
3. **Database** - RDS, DynamoDB
4. **Networking** - VPC, Route53
5. **Security** - IAM, KMS

## EC2 (Virtual Machines):
```bash
# Launch EC2 instance
aws ec2 run-instances \
  --image-id ami-0abcdef1234567890 \
  --instance-type t2.micro \
  --key-name my-key \
  --security-group-ids sg-12345678
```

## S3 (Storage):
```bash
# Create bucket
aws s3 mb s3://my-bucket

# Upload file
aws s3 cp file.txt s3://my-bucket/file.txt

# List objects
aws s3 ls s3://my-bucket
```""",
                        "example": """# AWS Examples
import boto3
import boto3_session

# S3 Operations
s3 = boto3.client('s3')

# Create bucket
s3.create_bucket(Bucket='my-bucket')

# Upload file
s3.upload_file('local.txt', 'my-bucket', 'remote.txt')

# Download file
s3.download_file('my-bucket', 'remote.txt', 'local2.txt')

# List objects
response = s3.list_objects_v2(Bucket='my-bucket')
for obj in response.get('Contents', []):
    print(obj['Key'])

# EC2 Operations
ec2 = boto3.resource('ec2')

# Create instance
instance = ec2.create_instances(
    ImageId='ami-0abcdef1234567890',
    MinCount=1,
    MaxCount=1,
    InstanceType='t2.micro'
)

# Start/stop instances
instance[0].start()
instance[0].stop()

# Lambda Function
import json
def lambda_handler(event, context):
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }

# DynamoDB
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('Users')

# Put item
table.put_item(
    Item={
        'id': '123',
        'name': 'John',
        'email': 'john@example.com'
    }
)

# Get item
response = table.get_item(Key={'id': '123'})
item = response.get('Item')
  ```""",
                        "interview_questions": """1. What are the main AWS services?
2. What is EC2 and how does it work?
3. What is S3 and what is it used for?
4. What is the difference between RDS and DynamoDB?
5. What is IAM and why is it important?""",
                        "duration": 25,
                        "order": 1,
                        "quiz": [
                            {
                                "question": "Which AWS service is used for object storage?",
                                "options": ["S3", "EC2", "RDS", "Lambda"],
                                "correct_answer": 0,
                                "explanation": "S3 is used for object storage."
                            }
                        ]
                    }
                ]
            },
            # Module 20
            {
                "title": "Module 20: DevOps",
                "description": "DevOps practices and tools",
                "order": 20,
                "lessons": [
                    {
                        "title": "DevOps Fundamentals",
                        "description": "DevOps practices",
                        "concept": """# DevOps Fundamentals
DevOps combines development and operations.

## Key Principles:
1. **CI/CD** - Continuous Integration/Continuous Deployment
2. **Automation** - Infrastructure as Code
3. **Monitoring** - Observability
4. **Collaboration** - Dev and Ops together

## CI/CD Pipeline:
1. **Code** - Source control
2. **Build** - Compile, test
3. **Package** - Create artifacts
4. **Deploy** - Release to environments
5. **Monitor** - Track performance

## Popular Tools:
- **Jenkins** - CI/CD automation
- **Git** - Version control
- **Maven/Gradle** - Build tools
- **Docker** - Containerization
- **Kubernetes** - Orchestration
- **Terraform** - Infrastructure as Code
- **Prometheus** - Monitoring
- **Grafana** - Visualization""",
                        "example": """# Jenkins Pipeline (Jenkinsfile)
pipeline {
    agent any
    
    stages {
        stage('Checkout') {
            steps {
                git 'https://github.com/username/repo.git'
            }
        }
        
        stage('Build') {
            steps {
                sh 'mvn clean install'
            }
        }
        
        stage('Test') {
            steps {
                sh 'mvn test'
            }
        }
        
        stage('Package') {
            steps {
                sh 'docker build -t myapp:latest .'
            }
        }
        
        stage('Deploy') {
            steps {
                sh 'docker push myapp:latest'
                sh 'kubectl apply -f deployment.yaml'
            }
        }
    }
    
    post {
        always {
            emailext (
                subject: "Build ${currentBuild.fullDisplayName}",
                body: "Build result: ${currentBuild.result}",
                to: "team@example.com"
            )
        }
    }
}

# Terraform (main.tf)
provider "aws" {
    region = "us-west-2"
}

resource "aws_instance" "web" {
    ami = "ami-0abcdef1234567890"
    instance_type = "t2.micro"
    
    tags = {
        Name = "web-server"
        Environment = "production"
    }
}

resource "aws_s3_bucket" "app_bucket" {
    bucket = "my-app-bucket"
    acl = "private"
}

# GitHub Actions (.github/workflows/ci.yml)
name: CI/CD Pipeline

on:
    push:
        branches: [main]
    pull_request:
        branches: [main]

jobs:
    build:
        runs-on: ubuntu-latest
        
        steps:
        - uses: actions/checkout@v2
        
        - name: Set up JDK 11
          uses: actions/setup-java@v2
          with:
            java-version: '11'
        
        - name: Build with Maven
          run: mvn clean install
        
        - name: Run tests
          run: mvn test
        
        - name: Deploy to AWS
          if: github.ref == 'refs/heads/main'
          env:
            AWS_ACCESS_KEY_ID: ${{ secrets.AWS_ACCESS_KEY_ID }}
            AWS_SECRET_ACCESS_KEY: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
          run: |
            aws deploy create-deployment \
              --application-name my-app \
              --deployment-group-name production \
              --github-location repository=username/repo,commitId=${{ github.sha }}
  ```""",
                        "interview_questions": """1. What is DevOps?
2. What is CI/CD?
3. What is Infrastructure as Code?
4. What are some popular DevOps tools?
5. What is the difference between continuous delivery and continuous deployment?""",
                        "duration": 25,
                        "order": 1,
                        "quiz": [
                            {
                                "question": "What does CI/CD stand for?",
                                "options": ["Continuous Integration/Continuous Deployment", "Code Integration/Code Deployment", "Continuous Infrastructure/Continuous Development", "Code Integration/Continuous Development"],
                                "correct_answer": 0,
                                "explanation": "CI/CD stands for Continuous Integration and Continuous Deployment/Delivery."
                            }
                        ]
                    }
                ]
            }
        ]

        # Add Java modules to database
        for mod_data in java_modules:
            module = Module(
                course_id=java_course.id,
                title=mod_data["title"],
                description=mod_data["description"],
                order=mod_data["order"]
            )
            db.add(module)
            db.commit()
            db.refresh(module)

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
                db.refresh(lesson)

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

        print(f"✅Java Course: {len(java_course.modules)} modules created!")

        print("\n" + "=" * 50)
        print("✅ALL COURSES SEEDED SUCCESSFULLY!")
        print("=" * 50)
        print(f"   ✅ Python Course: {len(python_course.modules)} modules")
        print(f"   ✅ Java Course: {len(java_course.modules)} modules")
        print("=" * 50)

    except Exception as e:
        print(f"❌ Error: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    seed_courses()


