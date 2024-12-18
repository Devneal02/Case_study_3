from Course import Course
from tabulate import tabulate
import pyodbc

server = r"HAISE\SQLEXPRESS"
database = "E_Learning_Platform"
connection_string = (
  f"DRIVER={{ODBC Driver 17 for SQL Server}};"
  f"SERVER={server};DATABASE={database};Trusted_Connection=yes;")

class Schedule(Course):
  def __init__(self, time = "", week_day = "", date = ""):
    self.time = time  
    self.week_day = week_day
    self.date = date
    self.connection = pyodbc.connect(connection_string)
    self.cursor = self.connection.cursor()
  
  def View_course_schedule(self, course_id):
    self.cursor.execute("""SELECT Time_sched, Week_day, Schedule_date
                           FROM Schedule s 
                           WHERE Course_id = ?""", (course_id))
    sched = self.cursor.fetchone()
    self.time = sched[0]
    self.week_day = sched[1]
    self.date = sched[2]
    print(f"\nCourse Schedule: \nTime: {self.time} | Day: {self.week_day} | Date: {self.date} ")
  
  def Show_all_schedules(self):
      # Fetch schedule data
      self.cursor.execute("""
          SELECT c.Name, s.Time_sched, s.Week_day, s.Schedule_date
          FROM Courses c 
          JOIN Schedule s ON c.Course_id = s.Course_id
      """)
      
      schedules = self.cursor.fetchall()

      # Check if there are no schedules
      if not schedules:
          print("\nNo schedules available.\n")
          return

      # Prepare data for tabulate
      table = [
          [schedule[0], schedule[1], schedule[2], schedule[3]] 
          for schedule in schedules
      ]
      
      # Define headers
      headers = ["Course Name", "Time", "Week Day", "Schedule Date"]
      
      # Print the table using tabulate with fancy_grid style
      print("\nSchedule of Courses List:")
      print(tabulate(table, headers=headers, tablefmt="fancy_grid"))

