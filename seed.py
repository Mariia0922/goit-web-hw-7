from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, Group, Teacher, Subject, Student, Grade
from faker import Faker
import random
from datetime import datetime, timedelta

engine = create_engine('postgresql+psycopg2://username:password@localhost/dbname')
Session = sessionmaker(bind=engine)
session = Session()

fake = Faker()

# Створення груп
groups = [Group(name=f'Group {i}') for i in range(1, 4)]
session.add_all(groups)
session.commit()

# Створення викладачів
teachers = [Teacher(first_name=fake.first_name(), last_name=fake.last_name()) for _ in range(5)]
session.add_all(teachers)
session.commit()

# Створення предметів
subjects = ['Math', 'History', 'Physics', 'Chemistry', 'Biology', 'English', 'Art']
subjects = [Subject(name=subj, teacher_id=random.choice(teachers).id) for subj in subjects]
session.add_all(subjects)
session.commit()

# Створення студентів
students = [Student(first_name=fake.first_name(), last_name=fake.last_name(), group_id=random.choice(groups).id) for _ in range(50)]
session.add_all(students)
session.commit()

# Створення оцінок
for student in students:
    for subject in subjects:
        for _ in range(random.randint(15, 20)):
            grade = Grade(student_id=student.id, subject_id=subject.id, grade=random.uniform(1, 100), date=fake.date_between(start_date='-1y', end_date='today'))
            session.add(grade)
session.commit()
