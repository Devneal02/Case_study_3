from Course import Course
import random
import time
import pyodbc

server = r"HAISE\SQLEXPRESS"
database = "E_Learning_Platform"
connection_string = (
  f"DRIVER={{ODBC Driver 17 for SQL Server}};"
  f"SERVER={server};DATABASE={database};Trusted_Connection=yes;")
  
class Assignment(Course):
  
  assignment_taken = 0

  def __init__(self, assign_score = 0, assignment_posted = ""):
    self.assign_score = assign_score
    self.assignment_posted = assignment_posted
    self.connection = pyodbc.connect(connection_string)
    self.cursor = self.connection.cursor()

  def Post_assignment(self, instructor_id):
    # Check if the assignment is already posted
    self.cursor.execute(
        "SELECT Assignment_posted FROM Courses WHERE Instructor_id = ?",
        (instructor_id,)
    )
    result = self.cursor.fetchone()
    
    if result and result[0] == 'Yes':
        print("You already posted the assignment for this course.")
    else:
        # Update the record to mark the assignment as posted
        self.cursor.execute(
            "UPDATE Courses SET Assignment_posted = 'Yes' WHERE Instructor_id = ?",
            (instructor_id,)
        )
        self.cursor.commit()
        print("Posting an assignment...")
        time.sleep(3)
        print("Assignment has been posted.")


  def Answer_assignment(self, student_id, course_id):
    # Check if the assignment has been posted for the course
    self.cursor.execute(
        "SELECT Assignment_posted FROM Courses WHERE Course_id = ?",
        (course_id,)
    )
    result = self.cursor.fetchone()
    
    if result and result[0] == 'Yes':  # Assignment is posted
        # Check if the student has already answered the assignment
        self.cursor.execute(
            "SELECT Assignment_score FROM Grades WHERE Student_id = ? AND Course_id = ?",
            (student_id, course_id)
        )
        grade_result = self.cursor.fetchone()
        
        if grade_result and grade_result[0] is not None:
            print("You already answered the assignment for this course.")
        else:
            print("Student answering assignment...")
            self.assign_score = random.randint(70, 100)
            time.sleep(3)
            print(f"Student finished answering the assignment.\nScore: {self.assign_score}")
            
            # Update the assignment score in the Grades table
            self.cursor.execute(
                "UPDATE Grades SET Assignment_score = ? WHERE Student_id = ? AND Course_id = ?",
                (self.assign_score, student_id, course_id)
            )
            self.connection.commit()
            Assignment.assignment_taken_increment()
            
    else:
        print("Assignment has not been posted for this course.")


  @staticmethod
  def print_assignment_taken():
        print("Assignment Taken:", Assignment.assignment_taken)

  @staticmethod
  def assignment_taken_increment():
       Assignment.assignment_taken += 1

  @classmethod
  def set_assignment_taken(cls, value):
        cls.assignment_taken = value
