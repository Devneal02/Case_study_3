from Course import Course
import pyodbc
import time
import random

server = r"HAISE\SQLEXPRESS"
database = "E_Learning_Platform"
connection_string = (
  f"DRIVER={{ODBC Driver 17 for SQL Server}};"
  f"SERVER={server};DATABASE={database};Trusted_Connection=yes;")

class Exam(Course):
  
  exam_taken = 0

  def __init__(self, exam_score = 0, exam_posted = ""):
    self.exam_score = exam_score
    self.exam_posted = exam_posted
    self.connection = pyodbc.connect(connection_string)
    self.cursor = self.connection.cursor()

  def Post_exam(self, instructor_id):
    # Check if the exam is already posted
    self.cursor.execute(
        "SELECT Exam_posted FROM Courses WHERE Instructor_id = ?",
        (instructor_id,)
    )
    result = self.cursor.fetchone()
    
    if result and result[0] == 'Yes':
        print("You already posted the exam for this course.")
    else:
        # Update the record to mark the exam as posted
        self.cursor.execute(
            "UPDATE Courses SET Exam_posted = 'Yes' WHERE Instructor_id = ?",
            (instructor_id,)
        )
        self.cursor.commit()
        print("Posting an exam...")
        time.sleep(3)
        print("Exam has been posted.")

  def Answer_exam(self, student_id, course_id):
    # Check if the exam has been posted for the course
    self.cursor.execute(
        "SELECT Exam_posted FROM Courses WHERE Course_id = ?",
        (course_id,)
    )
    result = self.cursor.fetchone()
    
    if result and result[0] == 'Yes':  # Exam is posted
        # Check if the student has already answered the exam
        self.cursor.execute(
            "SELECT Exam_score FROM Grades WHERE Student_id = ? AND Course_id = ?",
            (student_id, course_id)
        )
        grade_result = self.cursor.fetchone()
        
        if grade_result and grade_result[0] is not None:
            print("You already answered the exam for this course.")
        else:
            print("Student answering exam...")
            self.exam_score = random.randint(70, 100)
            time.sleep(3)
            print(f"Student finished answering the exam. \nScore: {self.exam_score}")
            
            # Update the exam score in the Grades table
            self.cursor.execute(
                "UPDATE Grades SET Exam_score = ? WHERE Student_id = ? AND Course_id = ?",
                (self.exam_score, student_id, course_id)
            )
            self.connection.commit()
            Exam.exam_taken_increment()
           
    else:
        print("Exam has not been posted for this course.")

  @staticmethod
  def print_exam_taken():
        print("Exam Taken:", Exam.exam_taken)

  @staticmethod
  def exam_taken_increment():
      Exam.exam_taken += 1

  @classmethod
  def set_exam_taken(cls, value):
        cls.exam_taken = value
