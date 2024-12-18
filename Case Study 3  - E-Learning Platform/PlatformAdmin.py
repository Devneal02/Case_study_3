from Person import Person
from tabulate import tabulate
import pyodbc

server = r"HAISE\SQLEXPRESS"
database = "E_Learning_Platform"
connection_string = (
  f"DRIVER={{ODBC Driver 17 for SQL Server}};"
  f"SERVER={server};DATABASE={database};Trusted_Connection=yes;")

class PlatformAdmin(Person):

  num_of_admins = 3
  Platform_name = "Learn_programming"

  def __init__(self, fname = "", mname = "", lname = "", gender = "", age = 0, email = "", phonenum  = "", address = "", admin_id = 0):
    super().__init__(fname, mname, lname, gender, age, email, phonenum, address)
    self.admin_id = admin_id
    self.connection = pyodbc.connect(connection_string)
    self.cursor = self.connection.cursor()

  def LogIn(self):
    print("Platform Admin Logging In")
    num_of_tries = 0
    while num_of_tries < 3:
        self._username = input("Enter Username: ")
        self.__password = input("Enter Password: ") 

        self.cursor.execute("""
          SELECT Admin_id, First_name, Middle_name, Last_name, Gender, Age, Email, Phone_number, Addresses
          FROM Administrator WHERE Username = ? AND Passwords = ?
        """, (self._username, self.__password))
        
        profile = self.cursor.fetchone()

        if profile:
            print("Platform Admin logged in")
            self.isloggedIn = True

            (self.admin_id, self.fname, self.mname, self.lname, self.gender, self.age, self.email, self.phonenum, 
            self.address) = profile
            return
        else:
            print("Incorrect Username or Password!")
            num_of_tries += 1

    print("You have used all attempts. Please try again later.")
    quit()

  def Profile(self):
      if self.isloggedIn:
          print(f"\nPlatform Admin ID: {self.admin_id}\n"
                  f"Full Name: {self.fname} {self.mname} {self.lname}\n"
                  f"Age: {self.age}\n" 
                  f"Gender: {self.gender}\n"
                  f"Phone Number: {self.phonenum}\n"
                  f"Address: {self.address}\n"
                  f"Email: {self.email}\n")
      else:
          print("User not logged in. Please log in first.")

  def Show_all_students(self):
      if self.isloggedIn:
          print("\nStudent List:")
          # Fetch student data
          self.cursor.execute("SELECT First_name, Middle_name, Last_name FROM Students")
          students = self.cursor.fetchall()

          # Prepare data for tabulate
          table = [[i + 1, student[0], student[1], student[2]] for i, student in enumerate(students)]
          headers = ["#", "First Name", "Middle Name", "Last Name"]

          # Print the table using tabulate
          print(tabulate(table, headers=headers, tablefmt="fancy_grid"))

  def Show_all_instructors(self):
      if self.isloggedIn:
          print("\nInstructors List:")
          # Fetch instructor data
          self.cursor.execute("SELECT First_name, Middle_name, Last_name FROM Instructors")
          instructors = self.cursor.fetchall()

          # Prepare data for tabulate
          table = [[i + 1, instructor[0], instructor[1], instructor[2]] for i, instructor in enumerate(instructors)]
          headers = ["#", "First Name", "Middle Name", "Last Name"]

          # Print the table using tabulate
          print(tabulate(table, headers=headers, tablefmt="fancy_grid"))

  @staticmethod
  def print_num_of_admins():
        print("Number of Admins:", PlatformAdmin.num_of_admins)
        
  @staticmethod
  def print_platform_name():
        print("Platform Name:", PlatformAdmin.platform_name)

  @classmethod
  def set_num_of_admins(cls, value):
        cls.num_of_admins = value

  @classmethod
  def set_platform_name(cls, value):
        cls.platform_name = value
