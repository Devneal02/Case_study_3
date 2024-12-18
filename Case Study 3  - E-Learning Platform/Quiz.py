from Course import Course
import random
import time
import pyodbc

server = r"HAISE\SQLEXPRESS"
database = "E_Learning_Platform"
connection_string = (
  f"DRIVER={{ODBC Driver 17 for SQL Server}};"
  f"SERVER={server};DATABASE={database};Trusted_Connection=yes;")

class Quiz(Course):
  
  quiz_taken = 0
  
  def __init__(self, quiz_score = 0, quiz_posted = ""):
    self.quiz_score = quiz_score
    self.quiz_posted = quiz_posted
    self.connection = pyodbc.connect(connection_string)
    self.cursor = self.connection.cursor()

  def Post_quiz(self, instructor_id):
    # Check if the quiz is already posted
    self.cursor.execute(
        "SELECT Quiz_posted FROM Courses WHERE Instructor_id = ?",
        (instructor_id,)
    )
    result = self.cursor.fetchone()
    
    if result and result[0] == 'Yes':
        print("You already posted the quiz for this course.")
    else:
        # Update the record to mark the quiz as posted
        self.cursor.execute(
            "UPDATE Courses SET Quiz_posted = 'Yes' WHERE Instructor_id = ?",
            (instructor_id,)
        )
        self.cursor.commit()
        print("Posting a quiz...")
        time.sleep(3)
        print("Quiz has been posted.")


  def Answer_quiz(self, student_id, course_id):
    # Check if the quiz has been posted for the course
    self.cursor.execute(
        "SELECT Quiz_posted FROM Courses WHERE Course_id = ?",
        (course_id,)
    )
    result = self.cursor.fetchone()
    
    if result and result[0] == 'Yes':
        # Check if the student has already answered the quiz
        self.cursor.execute(
            "SELECT Quiz_score FROM Grades WHERE Student_id = ? AND Course_id = ?",
            (student_id, course_id)
        )
        grade_result = self.cursor.fetchone()
        
        if grade_result and grade_result[0] is not None:
            print("You already answered the quiz for this course.")
        else:
            print("Student answering quiz...")
            self.quiz_score = random.randint(70, 100)
            time.sleep(3)
            print(f"Student finished answering the quiz.\nScore: {self.quiz_score}")
            
            # Update the quiz score in the Grades table
            self.cursor.execute(
                "UPDATE Grades SET Quiz_score = ? WHERE Student_id = ? AND Course_id = ?",
                (self.quiz_score, student_id, course_id)
            )
            self.connection.commit()
            Quiz.quiz_taken_increment()
    
    else:
        print("Quiz has not been posted for this course.")

  @staticmethod
  def print_quiz_taken():
        print("Quiz Taken:", Quiz.quiz_taken)

  @staticmethod
  def quiz_taken_increment():
      Quiz.quiz_taken += 1

  @classmethod
  def set_quiz_taken(cls, value):
        cls.quiz_taken = value