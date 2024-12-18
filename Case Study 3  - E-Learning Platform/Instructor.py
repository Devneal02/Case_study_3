from Person import Person
import pyodbc

server = r"HAISE\SQLEXPRESS"
database = "E_Learning_Platform"
connection_string = (
  f"DRIVER={{ODBC Driver 17 for SQL Server}};"
  f"SERVER={server};DATABASE={database};Trusted_Connection=yes;")

class Instructor(Person):

  num_of_instructors = 6

  def __init__(self, fname = "", mname = "", lname = "", gender = "", age = 0, email = "", phonenum  = "", address = "", instructor_id = 0, course_id = 0,course_instructing = ""):
    super().__init__(fname, mname, lname, gender, age, email, phonenum, address)
    self.instructor_id = instructor_id
    self.course_id = course_id
    self.course_instructing = course_instructing
    self.connection = pyodbc.connect(connection_string)
    self.cursor = self.connection.cursor()
  
  #Methods
  def LogIn(self):
    print("Instructor Logging In")
    num_of_tries = 0
    while num_of_tries < 3:
        self._username = input("Enter Username: ")
        self.__password = input("Enter Password: ")

        self.cursor.execute("""
            SELECT i.Instructor_id, i.First_name, i.Middle_name, i.Last_name, i.Gender, i.Age, i.Email, i.Phone_number, Addresses, c.Course_id ,c.Name
            FROM Instructors i
            JOIN Courses c ON i.Instructor_id = c.Instructor_id
            WHERE Username = ? AND Passwords = ?
        """, (self._username, self.__password))
        
        profile = self.cursor.fetchone()

        if profile:
            print("Instructor logged in")
            self.isloggedIn = True

            (self.instructor_id, self.fname, self.mname, self.lname, self.gender, self.age, self.email, self.phonenum, 
            self.address, self.course_id, self.course_instructing) = profile
            return
        else:
            print("Incorrect Username or Password!")
            num_of_tries += 1

    print("You have used all attempts. Please try again later.")
    quit()

  def Profile(self):
      if self.isloggedIn:
          print(f"\nInstructor ID: {self.instructor_id}\n"
                  f"Full Name: {self.fname} {self.mname} {self.lname}\n"
                  f"Age: {self.age}\n" 
                  f"Gender: {self.gender}\n"
                  f"Phone Number: {self.phonenum}\n"
                  f"Address: {self.address}\n"
                  f"Email: {self.email}\n"
                  f"Course Instructing: {self.course_instructing}\n")
      else:
          print("User not logged in. Please log in first.")

  @staticmethod
  def print_num_of_instructors():
        print("Number of Instructors:", Instructor.num_of_instructors)

  @classmethod
  def set_num_of_instructors(cls, value):
        cls.num_of_instructors = value