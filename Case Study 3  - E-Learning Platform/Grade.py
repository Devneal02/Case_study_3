import pyodbc
from Course import Course
import time

server = r"HAISE\SQLEXPRESS"
database = "E_Learning_Platform"
connection_string = (
  f"DRIVER={{ODBC Driver 17 for SQL Server}};"
  f"SERVER={server};DATABASE={database};Trusted_Connection=yes;")

class Grade(Course):
  
  grade_count = 0

  def __init__(self, course_id = 0, name = "", description = "", exam_percentage = 0.5, assign_percentage = 0.2, quiz_percentage = 0.2 ,grade_id = 0, grade_status = 0.00, quiz_score = 0, assign_score = 0, exam_score = 0, final_grade = 0.00):
    super().__init__(course_id, name, description, exam_percentage, assign_percentage, quiz_percentage)
    self.grade_id = grade_id
    self.grade_status = grade_status
    self.quiz_score = quiz_score
    self.assign_score = assign_score
    self.exam_score = exam_score
    self.final_grade = final_grade
    self.connection = pyodbc.connect(connection_string) 
    self.cursor = self.connection.cursor()

  def Calculate_grade(self, course_id):
    student_id = input("Enter the ID of the Student: ")
    self.cursor.execute(
        "SELECT Quiz_score, Exam_score, Assignment_score FROM Grades WHERE Student_id = ? AND Course_id = ?",
        (student_id, course_id),
    )
    grade = self.cursor.fetchone()
    if grade is None:
        print("No grades found for the given student.")

    self.quiz_score, self.exam_score, self.assign_score = grade

    if not (0 <= self.quiz_score <= 100 and 0 <= self.exam_score <= 100 and 0 <= self.assign_score <= 100):
        print("Scores must be between 0 and 100.")
        
    self.final_grade = (self.quiz_score * self.quiz_percentage) + (self.exam_score * self.exam_percentage) + (self.assign_score * self.assign_percentage)

    self.cursor.execute(
        "UPDATE Grades SET Final_grade = ? WHERE Student_id = ? AND Course_id = ?",
        (self.final_grade, student_id, course_id),
    )
    self.connection.commit()

    self.GradeStatus(self.final_grade)

  def GradeStatus(self, finalGrade):
    if 96 <= finalGrade <= 100:
        self.grade_status = 1.00
    elif 94 <= finalGrade <= 95.99:
        self.grade_status = 1.25
    elif 91 <= finalGrade <= 93.99:
        self.grade_status = 1.50
    elif 89 <= finalGrade <= 90.99:
        self.grade_status = 1.75
    elif 86 <= finalGrade <= 88.99:
        self.grade_status = 2.0
    elif 83 <= finalGrade <= 85.99:
        self.grade_status = 2.25
    elif 80 <= finalGrade <= 82.99:
        self.grade_status = 2.50
    elif 77 <= finalGrade <= 79.99:
        self.grade_status = 2.75
    elif 75 <= finalGrade <= 76.99:
        self.grade_status = 3.0
    else:
        self.grade_status = 5.0


    self.cursor.execute(
        "UPDATE Grades SET Grade_status = ? WHERE Final_grade = ?",
        (self.grade_status, finalGrade),
    )
    self.connection.commit()

    print("\nComputing grade...")
    time.sleep(3)
    print(f"Final Grade: {finalGrade}\nGrade status: {self.grade_status}")
  
    
  def View_final_grade(self, student_id):
      self.cursor.execute("SELECT Final_grade FROM Grades WHERE Student_id = ?", (student_id,))
      final = self.cursor.fetchone()
      
      # Check if the query returned a result and if Final_grade is not NULL
      if final is None or final[0] is None:
          print("Final grade is not computed yet.")
          return
      
      self.final_grade = final[0]
      print(f"Final Grade: {self.final_grade}")

  def View_grade_status(self, student_id):
      self.cursor.execute("SELECT Grade_status FROM Grades WHERE Student_id = ?", (student_id,))
      status = self.cursor.fetchone()
      
      # Check if the query returned a result and if Grade_status is not NULL
      if status is None or status[0] is None:
          print("Grade status is not computed yet.")
          return
      
      self.grade_status = status[0]
      print(f"Grade Status: {self.grade_status}")

  @staticmethod
  def print_grade_count():
        print("Grade Count:", Grade.grade_count)

  @classmethod
  def set_grade_count(cls, value):
        cls.grade_count = value
 