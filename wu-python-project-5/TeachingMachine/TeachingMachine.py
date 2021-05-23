# File: TeachingMachine.py

from TMCourse import TMCourse

def teaching_machine():
    course = read_course_file()
    course.run()

def read_course_file():
    """
    Prompts the user for a course name and then reads in the
    data for that course from the associated data file.  If
    TMCourse.read_course raises an IOError exception, the user
    is asked to supply a new course name.
    """
    while True:
        try:
            filename = input("Enter course name: ")
            with open(filename + ".txt") as f:
                return TMCourse.read_course(f)
        except IOError:
            print("Please enter a valid course name.")

# Startup code

if __name__ == "__main__":
    teaching_machine()
