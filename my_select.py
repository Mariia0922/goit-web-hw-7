from sqlalchemy import func, desc
from sqlalchemy.orm import sessionmaker
from models import Student, Grade, Subject, Teacher, Group
from sqlalchemy import create_engine

engine = create_engine('postgresql+psycopg2://username:password@localhost/dbname')
Session = sessionmaker(bind=engine)
session = Session()

def select_1():
    return session.query(Student.first_name, Student.last_name, func.round(func.avg(Grade.grade), 2).label('avg_grade'))\
                  .join(Grade).group_by(Student.id).order_by(desc('avg_grade')).limit(5).all()

# Аналогічно створюються інші функції select_2, select_3, ..., select_10

if __name__ == "__main__":
    print(select_1())
