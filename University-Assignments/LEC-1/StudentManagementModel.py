
from abc import ABC, abstractmethod


# 1. Abstract Person Base Class
class Person(ABC):
    def __init__(self, name, email):
        self.name = name
        self.email = email

    # Property to validate email
    @property
    def email(self):
        return self._email

    @email.setter
    def email(self, value):
        if "@" not in value or "." not in value:
            raise ValueError("Invalid email address!")
        self._email = value

    # Abstract method
    @abstractmethod
    def role_info(self):
        pass

    def __str__(self):
        return f"Name: {self.name}, Email: {self.email}"


# 2. Student Subclass
class Student(Person):
    def __init__(self, name, email, student_id):
        super().__init__(name, email)
        self.student_id = student_id

    # Override role_info()
    def role_info(self):
        return f"I am a Student. My Student ID is {self.student_id}."

    def __str__(self):
        return f"Student: {self.name}, Email: {self.email}, ID: {self.student_id}"


# 3. Lecturer Subclass
class Lecturer(Person):
    def __init__(self, name, email, subject):
        super().__init__(name, email)
        self.subject = subject

    # Override role_info()
    def role_info(self):
        return f"I am a Lecturer. I teach {self.subject}."

    def __str__(self):
        return f"Lecturer: {self.name}, Email: {self.email}, Subject: {self.subject}"


# 4. Course Class (Composition)
class Course:
    def __init__(self, course_name, lecturer):
        self.course_name = course_name
        self.lecturer = lecturer
        self.students = []

    # Add Student objects to Course
    def add_student(self, student):
        if isinstance(student, Student):
            self.students.append(student)
            print(f"{student.name} added to {self.course_name}.")
        else:
            print("Only Student objects can be added!")

    def show_course_info(self):
        print("\nCourse Name:", self.course_name)
        print("Lecturer:", self.lecturer.name)

        print("\nStudents:")
        for student in self.students:
            print(student)

    def __str__(self):
        return f"Course: {self.course_name}, Lecturer: {self.lecturer.name}, Students: {len(self.students)}"


# 5. Create Objects

student1 = Student("Ahmad", "ahmad@gmail.com", 101)
student2 = Student("Ali", "ali@gmail.com", 102)

lecturer1 = Lecturer("Mr. Khan", "khan@gmail.com", "Python Programming")


# 6. Create a Course
python_course = Course("Python Programming", lecturer1)

# Add students to course
python_course.add_student(student1)
python_course.add_student(student2)


# 7. Polymorphism
people = [student1, student2, lecturer1]

print("\n--- People Information ---")

for person in people:
    print(person)
    print(person.role_info())
    print("------------------------")


# 8. Display Course Information
print("\n--- Course Information ---")
print(python_course)
python_course.show_course_info()
