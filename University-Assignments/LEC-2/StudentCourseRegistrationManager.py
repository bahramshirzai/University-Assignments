
from typing import TypeVar, Iterable


# Generic Type Variable
T = TypeVar("T")


# Generic Helper Function
def get_unique_items(items: Iterable[T]) -> set[T]:
    return set(items)


# Student Class
class Student:

    def __init__(self, student_id: int, name: str):
        self.student_id: int = student_id
        self.name: str = name
        self.courses: set[str] = set()

    def __str__(self) -> str:
        return (
            f"ID: {self.student_id}, "
            f"Name: {self.name}, "
            f"Courses: {sorted(self.courses)}"
        )


# Student Management Class
class RegistrationManager:

    def __init__(self):
        self.students: dict[int, Student] = {}

    # 1. Add Student
    def add_student(self, student_id: int, name: str) -> None:

        if student_id in self.students:
            print("Student ID already exists!")
        else:
            self.students[student_id] = Student(student_id, name)
            print(f"Student {name} added successfully!")

    # 2. Register Course
    def register_course(self, student_id: int, course: str) -> None:

        student = self.students.get(student_id)

        if student is None:
            print("Student not found!")
        elif course in student.courses:
            print(f"{course} is already registered!")
        else:
            student.courses.add(course)
            print(f"{course} registered successfully!")

    # 3. Drop Course
    def drop_course(self, student_id: int, course: str) -> None:

        student = self.students.get(student_id)

        if student is None:
            print("Student not found!")
        elif course in student.courses:
            student.courses.remove(course)
            print(f"{course} dropped successfully!")
        else:
            print("Course not found!")

    # 4. Search Student
    def search_student(self, student_id: int) -> Student | None:

        return self.students.get(student_id)

    # 5. Display All Unique Courses
    def display_all_courses(self) -> None:

        all_courses = get_unique_items(
            course
            for student in self.students.values()
            for course in student.courses
        )

        print("\nAll Unique Registered Courses:")
        print(sorted(all_courses))

    # 6. Find Students Sharing a Course
    def find_students_by_course(self, course: str) -> list[Student]:

        matching_students = [
            student
            for student in self.students.values()
            if course in student.courses
        ]

        return matching_students

    # 7. Sort Students by Name
    def display_sorted_students(self) -> None:

        sorted_students = sorted(
            self.students.values(),
            key=lambda student: student.name.lower()
        )

        print("\nStudents Sorted by Name:")

        for student in sorted_students:
            print(student)


# MAIN PROGRAM

manager = RegistrationManager()


# Add Students
print("--- Adding Students ---")

manager.add_student(101, "Ahmad")
manager.add_student(102, "Ali")
manager.add_student(103, "Farid")
manager.add_student(104, "Zahra")
manager.add_student(105, "Omar")


# Register Courses
print("\n--- Registering Courses ---")

manager.register_course(101, "CS101")
manager.register_course(101, "CS102")

manager.register_course(102, "CS101")
manager.register_course(102, "CS103")

manager.register_course(103, "CS102")
manager.register_course(103, "CS104")

manager.register_course(104, "CS101")
manager.register_course(104, "CS104")

manager.register_course(105, "CS103")
manager.register_course(105, "CS105")


# Test Duplicate Registration
print("\n--- Testing Duplicate Registration ---")

manager.register_course(101, "CS101")


# Drop a Course
print("\n--- Dropping Course ---")

manager.drop_course(101, "CS102")


# Search Student
print("\n--- Searching Student ---")

student = manager.search_student(103)

if student is not None:
    print("Student Found:")
    print(student)
else:
    print("Student Not Found!")


# Display All Unique Courses
manager.display_all_courses()


# Find Students Sharing a Course
print("\n--- Students Registered in CS101 ---")

matching_students = manager.find_students_by_course("CS101")

for student in matching_students:
    print(student.name)


# Display Students Sorted by Name
manager.display_sorted_students()
