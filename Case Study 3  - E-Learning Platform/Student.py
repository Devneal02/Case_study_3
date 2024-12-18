from Person import Person
import pyodbc

server = r"HAISE\SQLEXPRESS"
database = "E_Learning_Platform"
connection_string = (
  f"DRIVER={{ODBC Driver 17 for SQL Server}};"
  f"SERVER={server};DATABASE={database};Trusted_Connection=yes;")
  
class Student(Person):

  num_of_students = 20
  acc_connected = "gmail" 

  def __init__(self, fname = "", mname = "", lname = "", gender = "", age = 0, email = "", phonenum  = "", address = "", student_id = 0):
    super().__init__(fname, mname, lname, gender, age, email, phonenum, address)
    self.student_id = student_id
    self.connection = pyodbc.connect(connection_string)
    self.cursor = self.connection.cursor()

  #Methods
  def LogIn(self):
    print("Student Logging In")
    num_of_tries = 0
    while num_of_tries < 3:
        self._username = input("Enter Username: ")
        self.__password = input("Enter Password: ")

        self.cursor.execute("""
          SELECT Student_id, First_name, Middle_name, Last_name, Gender, Age, Email, Phone_number, Addresses
          FROM Students WHERE Username = ? AND Passwords = ?
        """, (self._username, self.__password))
        
        profile = self.cursor.fetchone()

        if profile:
            print("Student logged in")
            self.isloggedIn = True

            (self.student_id, self.fname, self.mname, self.lname, self.gender, self.age, self.email, self.phonenum, 
            self.address) = profile
            return
        else:
            print("Incorrect Username or Password!")
            num_of_tries += 1

    print("You have used all attempts. Please try again later.")
    quit()

  def Profile(self):
      if self.isloggedIn:
          print(f"\nStudent ID: {self.student_id}\n"
                  f"Full Name: {self.fname} {self.mname} {self.lname}\n"
                  f"Age: {self.age}\n" 
                  f"Gender: {self.gender}\n"
                  f"Phone Number: {self.phonenum}\n"
                  f"Address: {self.address}\n"
                  f"Email: {self.email}\n")
      else:
          print ("User not logged in. Please log in first.")

  @staticmethod
  def print_num_of_students():
        print("Number of Students:", Student.num_of_students)

  @staticmethod
  def print_acc_connected():
        print("Account Connected:", Student.acc_connected)

  @classmethod
  def set_num_of_students(cls, value):
        cls.num_of_students = value

  @classmethod
  def set_acc_connected(cls, value):
        cls.acc_connected = value
