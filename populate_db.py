import sqlite3
from faker import Faker
import random
from datetime import datetime, timedelta

fake = Faker()

conn = sqlite3.connect('university.db')
cursor = conn.cursor()

with open('schem.sql', 'r') as f:
    cursor.executescript(f.read())

groups = ['Group A', 'Group B', 'Group C']
teachers = [(fake.first_name(), fake.last_name()) for _ in range(4)]
subjects = ['Math', 'History', 'Physics', 'Chemistry', 'Biology', 'English']

cursor.executemany('INSERT INTO groups (name) VALUES (?)', [(group,) for group in groups])
group_ids = [row[0] for row in cursor.execute('SELECT id FROM groups')]

cursor.executemany('INSERT INTO teachers (first_name, last_name) VALUES (?, ?)', teachers)
teacher_ids = [row[0] for row in cursor.execute('SELECT id FROM teachers')]

for subject in subjects:
    cursor.execute('INSERT INTO subjects (name, teacher_id) VALUES (?, ?)', (subject, random.choice(teacher_ids)))
subject_ids = [row[0] for row in cursor.execute('SELECT id FROM subjects')]

for _ in range(50):
    cursor.execute('INSERT INTO students (first_name, last_name, group_id) VALUES (?, ?, ?)',
                   (fake.first_name(), fake.last_name(), random.choice(group_ids)))
student_ids = [row[0] for row in cursor.execute('SELECT id FROM students')]

for student_id in student_ids:
    for subject_id in subject_ids:
        for _ in range(random.randint(15, 20)):
            grade = random.randint(1, 100)
            date = fake.date_between(start_date='-1y', end_date='today')
            cursor.execute('INSERT INTO grades (student_id, subject_id, grade, date) VALUES (?, ?, ?, ?)',
                           (student_id, subject_id, grade, date))

conn.commit()
conn.close()
