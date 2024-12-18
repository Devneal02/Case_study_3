#Imported classes from diff files
from Student import Student
from Instructor import Instructor
from PlatformAdmin import PlatformAdmin
from Course import Course
from Schedule import Schedule
from Enrollment import Enrollment
from Assignment import Assignment
from Quiz import Quiz
from Exam import Exam
from Grade import Grade

# Objects 
student = Student()
instructor = Instructor()
platform_admin = PlatformAdmin()
course = Course()
schedule = Schedule()
enrollment = Enrollment()
assignment = Assignment()
quiz = Quiz()
exam = Exam()
grade = Grade()

# Menus stored in dictionaries
main_menu = {
    "1": "Student",
    "2": "Instructor",
    "3": "Platform admin",
    "4": "Exit program"
}

student_menu = {
    "1": "Profile",
    "2": "Enroll to a course",
    "3": "View enrolled courses",
    "4": "Logout"
}

instructor_menu = {
    "1": "Profile",
    "2": "Post assignment",
    "3": "Post quiz",
    "4": "Post exam",
    "5": "Compute grade", 
    "6": "Logout"
}

admin_menu = {
    "1": "Profile",
    "2": "Show all Students",
    "3": "Show all Instructors",
    "4": "Show all Courses",
    "5": "Show all Enrollments",
    "6": "Show all Schedules",
    "7": "Logout"
}

course_menu = {
    "1": "Answer Assignment",
    "2": "Answer Quiz", 
    "3": "Answer Exam",
    "4": "View course schedule",
    "5": "View final grade",
    "6": "View grade status",
    "7": "Drop course",
    "8": "Dashboard"
}


def display_menu(menu):
    for key, value in menu.items():
        print(f"{key}. {value}")


def Student_menu(student):
  student.LogIn()
  while True:
    print("\nSTUDENT MENU")
    display_menu(student_menu)
    stud_command = input("Enter command number: ")

    if stud_command == "1":
      student.Profile()

    elif stud_command == "2":
      enrollment.Enroll_course(student.student_id)

    elif stud_command == "3":
      course.View_enrolled_courses(student.student_id)
      course_id = input("Enter course ID to attend (X to go back): ")
      if course_id == "x":
        continue
      Course_menu(course_id, student.student_id)

    elif stud_command == "4":
      break

    else:
      print("Invalid command!") 

def Course_menu(course_id, student_id):
  while True:
    print("\nCOURSE MENU")
    display_menu(course_menu)
    course_command = input("Enter command number: ")
    if course_command == "1":
      assignment.Answer_assignment(student_id, course_id)
    
    elif course_command == "2":
      quiz.Answer_quiz(student_id, course_id)
    
    elif course_command == "3":
      exam.Answer_exam(student_id, course_id)
    
    elif course_command == "4":   
      schedule.View_course_schedule(course_id)
    
    elif course_command == "5":
      grade.View_final_grade(student_id)

    elif course_command == "6":
      grade.View_grade_status(student_id)
    
    elif course_command == "7":
      enrollment.Drop_course(course_id, student_id)
      break

    elif course_command == "8":
      break

    else:
      print("Invalid command!")


def Instructor_menu(instructor):
  instructor.LogIn()
  while True:
    print("\nINSTRUCTOR MENU")
    display_menu(instructor_menu)
    inst_command = input("Enter command number: ")

    if inst_command == "1":
      instructor.Profile()

    elif inst_command == "2":
      assignment.Post_assignment(instructor.instructor_id)

    elif inst_command == "3":
      quiz.Post_quiz(instructor.instructor_id)

    elif inst_command == "4":
      exam.Post_exam(instructor.instructor_id)

    elif inst_command == "5":
      enrollment.View_studentEnrolled_in_course(instructor.course_id)
      grade.Calculate_grade(instructor.course_id)

    elif inst_command == "6":
      break

    else:
      print("Invalid command!")

def Platform_Admin_menu():
  platform_admin.LogIn()
  while True:
    print("\nADMIN MENU")
    display_menu(admin_menu)
    admin_command = input("Enter command number: ")

    if admin_command == "1":
      platform_admin.Profile()

    elif admin_command == "2":
      platform_admin.Show_all_students()

    elif admin_command == "3":
      platform_admin.Show_all_instructors()

    elif admin_command == "4":
      course.Show_all_courses()

    elif admin_command == "5":
      enrollment.Show_all_enrollments()
    
    elif admin_command == "6":
      schedule.Show_all_schedules()

    elif admin_command == "7":
      break

    else:
      print("Invalid command!")

def main():
  while True:
    print("\n\nWelcome to E-learning Platform!")
    display_menu(main_menu)
    user = input("Enter number of user type: ")

    if user.lower() == "1":
      Student_menu(student)
    
    elif user.lower() == "2":
      Instructor_menu(instructor)
    
    elif user.lower() == "3":
      Platform_Admin_menu()

    elif user.lower() == "4":  # Exit
      print("Exiting the program...")
      quit()

    else:
      print("Invalid User type!")

if __name__ == "__main__":
    main()