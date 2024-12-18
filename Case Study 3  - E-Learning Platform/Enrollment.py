from Student import Student
from Grade import Grade
from Course import Course
from tabulate import tabulate
import pyodbc

server = r"HAISE\SQLEXPRESS"
database = "E_Learning_Platform"
connection_string = (
  f"DRIVER={{ODBC Driver 17 for SQL Server}};"
  f"SERVER={server};DATABASE={database};Trusted_Connection=yes;")

class Enrollment(Student, Grade, Course):

  enrollment_count = 0

  def __init__(self, enroll_id = 0, enroll_date = ""):
    self.enroll_id = enroll_id
    self.enroll_date = enroll_date
    self.connection = pyodbc.connect(connection_string)
    self.cursor = self.connection.cursor()

  def Enroll_course(self, student_id):
      # Get course ID input
      self.View_all_courses()
      course_id = input("Enter course ID to enroll: ")

      # Check if the student is already enrolled in the course
      self.cursor.execute(
          "SELECT c.Course_id, c.Name, c.Descriptions FROM Enrollments e "
          "JOIN Courses c ON e.Course_id = c.Course_id "
          "WHERE e.Course_id = ? AND e.Student_id = ?",
          (course_id, student_id)
      )
      result = self.cursor.fetchone()
      
      if result:
          # Display a message if already enrolled
          print("\nYou are already enrolled in this course.")
      else:
          # Proceed with enrollment
          enroll_date = input("Enter enroll date (YYYY-MM-DD): ")
          self.cursor.execute(
              "INSERT INTO Enrollments(Course_id, Student_id, Enrollment_date) VALUES(?, ?, ?)",
              (course_id, student_id, enroll_date)
          )
          # Commit the transaction
          self.connection.commit()
          print("\nEnrollment successful!")
          self.Enrollment_details(student_id, course_id)


  def Enrollment_details(self, student_id, course_id):
    self.cursor.execute("""SELECT e.Enrollment_id, c.Name, c.Descriptions, e.Enrollment_date
                           FROM Enrollments e 
                           JOIN Courses c ON e.Course_id = c.Course_id
                           WHERE e.Student_id = ? AND e.Course_id = ?""", (student_id, course_id))
    
    details = self.cursor.fetchone()
    print("\nEnrollment Details:")
    self.enroll_id = details[0]
    self.name = details[1]
    self.description = details[2]
    self.enroll_date = details[3]
    print(f"Course name: {self.name}\nDescription: {self.description}\nEnroll date: {self.enroll_date}")

  def Drop_course(self, course_id, student_id):
    self.cursor.execute("DELETE FROM Enrollments WHERE Course_id = ? AND Student_id = ?", (course_id, student_id))
    self.cursor.commit()
    print("Course successfully dropped.")
    
  def View_studentEnrolled_in_course(self, course_id):
      self.cursor.execute("""
          SELECT e.Student_id, s.First_name, s.Middle_name, s.Last_name, g.Assignment_score,
                g.Quiz_score, g.Exam_score 
          FROM Enrollments e 
          JOIN Students s ON e.Student_id = s.Student_id
          JOIN Grades g ON e.Student_id = g.Student_id
          WHERE e.Course_id = ?
      """, (course_id,))
      
      students = self.cursor.fetchall()
      
      # Check if there are no students enrolled
      if not students:
          print("\nNo students are enrolled in this course.\n")
          return

      # Prepare data for tabulate
      table = [
          [student[0], student[1], student[2], student[3], student[4], student[5], student[6]] 
          for student in students
      ]
      
      # Define headers
      headers = ["Student ID", "First Name", "Middle Name", "Last Name", "Assignment Score", "Quiz Score", "Exam Score"]
      
      # Print the table using tabulate with fancy_grid style
      print("\nList of students enrolled in the course:")       
      print(tabulate(table, headers=headers, tablefmt="fancy_grid"))


  def Show_all_enrollments(self):
      # Fetch enrollment data
      self.cursor.execute("""
          SELECT c.Name, s.First_name, s.Middle_name, s.Last_name, e.Enrollment_date
          FROM Enrollments e 
          JOIN Courses c ON e.Course_id = c.Course_id
          JOIN Students s ON e.Student_id = s.Student_id
      """)  
      
      enrollments = self.cursor.fetchall()

      # Check if there are no enrollments
      if not enrollments:
          print("\nNo enrollments found.\n")
          return

      # Prepare data for tabulate
      table = [
          [enrollment[1], enrollment[2], enrollment[3], enrollment[0], enrollment[4]] 
          for enrollment in enrollments
      ]
      
      # Define headers
      headers = ["First Name", "Middle Name", "Last Name", "Course Name", "Enrollment Date"]
      
      # Print the table using tabulate with fancy_grid style
      print("\nEnrollment List:")
      print(tabulate(table, headers=headers, tablefmt="fancy_grid"))


  @staticmethod
  def print_enrollment_count():
        print("Enrollment Count:", Enrollment.enrollment_count)
  
  @staticmethod
  def enrollment_count_increment():
    Enrollment.enrollment_count += 1

  @classmethod
  def set_enrollment_count(cls, value):
        cls.enrollment_count = value