from tabulate import tabulate
import pyodbc

server = r"HAISE\SQLEXPRESS"
database = "E_Learning_Platform"
connection_string = (
  f"DRIVER={{ODBC Driver 17 for SQL Server}};"
  f"SERVER={server};DATABASE={database};Trusted_Connection=yes;")

class Course():

  num_of_courses = 6
  courses_type = "Programming languages"

  def __init__(self,course_id = 0, name = "", description = "", exam_percentage = 0.5, assign_percentage = 0.2, quiz_percentage = 0.2):
    self.course_id = course_id
    self.name = name
    self.description = description
    self.isEnrolled = False
    self.exam_percentage = exam_percentage
    self.assign_percentage = assign_percentage
    self.quiz_percentage = quiz_percentage
    self.connection = pyodbc.connect(connection_string)
    self.cursor = self.connection.cursor()
  
  def View_all_courses(self):
      # Fetch course data
      self.cursor.execute("SELECT name, Descriptions FROM Courses")
      courses = self.cursor.fetchall()

      # Prepare data for tabulate
      table = [[i + 1, course[0], course[1]] for i, course in enumerate(courses)]
      headers = ["#", "Course Name", "Description"]

      # Print the table using tabulate with fancy_grid style
      print("\nALL COURSES")
      print(tabulate(table, headers=headers, tablefmt="fancy_grid"))


  def View_enrolled_courses(self, student_id):
      # Fetch enrolled courses data
      self.cursor.execute("""
          SELECT e.Course_id, c.Name, c.Descriptions
          FROM Enrollments e
          JOIN Courses c ON e.Course_id = c.Course_id
          WHERE Student_id = ?
      """, (student_id,))
      
      courses = self.cursor.fetchall()
      
      # Check if there are no enrolled courses
      if not courses:
          print("\nCurrently not enrolled in any course.\n")
          return

      # Prepare data for tabulate
      table = [[course[0], course[1], course[2]] for course in courses]
      headers = ["Course ID", "Course Name", "Description"]

      # Print the table using tabulate with fancy_grid style
      print("\nENROLLED COURSES")
      print(tabulate(table, headers=headers, tablefmt="fancy_grid"))


  def Show_all_courses(self):
      # Fetch course data
      self.cursor.execute("SELECT Name, Descriptions FROM Courses")
      courses = self.cursor.fetchall()

      table = [[i + 1, course[0], course[1]] for i, course in enumerate(courses)]
      headers = ["#", "Course Name", "Description"]

      # Print the table using tabulate with fancy_grid style
      print("\nCOURSE LIST")
      print(tabulate(table, headers=headers, tablefmt="fancy_grid"))

    
  @staticmethod
  def print_num_of_courses():
        print("Number of Courses:", Course.num_of_courses)

  @staticmethod
  def print_courses_type():
        print("Courses Type:", Course.courses_type)

  @classmethod
  def set_num_of_courses(cls, value):
        cls.num_of_courses = value

  @classmethod
  def set_courses_type(cls, value):
        cls.courses_type = value