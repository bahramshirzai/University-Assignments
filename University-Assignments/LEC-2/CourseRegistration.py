
# Lab 2 - Course Registration Data Model

# 1. Create a dictionary using student ID as the key
# Each student has a name and a set of registered courses

students: dict[int, dict[str, str | set[str]]] = {
    101: {
        "name": "Ahmad",
        "courses": {"CS101", "CS102", "CS103"}
    },

    102: {
        "name": "Ali",
        "courses": {"CS101", "CS104", "CS105"}
    },

    103: {
        "name": "Farid",
        "courses": {"CS102", "CS103", "CS106"}
    }
}


# 2. Function to add a course
def add_course(student_id: int, course_code: str) -> None:
    if student_id in students:
        courses = students[student_id]["courses"]
        courses.add(course_code)
        print(f"{course_code} added successfully!")
    else:
        print("Student not found!")


# 3. Function to drop a course
def drop_course(student_id: int, course_code: str) -> None:
    if student_id in students:
        courses = students[student_id]["courses"]

        if course_code in courses:
            courses.remove(course_code)
            print(f"{course_code} dropped successfully!")
        else:
            print("Course not found!")
    else:
        print("Student not found!")


# 4. Add courses
print("--- Adding Courses ---")

add_course(101, "CS104")
add_course(102, "CS106")

# Adding duplicate course
add_course(101, "CS101")


# 5. Drop a course
print("\n--- Dropping Courses ---")

drop_course(101, "CS103")


# 6. Find common courses between two students
print("\n--- Common Courses ---")

student1_courses = students[101]["courses"]
student2_courses = students[102]["courses"]

common_courses = student1_courses.intersection(student2_courses)

print("Common Courses:", common_courses)


# 7. Find all unique courses using union
print("\n--- All Unique Courses ---")

all_courses = set()

for student in students.values():
    all_courses = all_courses.union(student["courses"])

print("All Courses:", all_courses)


# 8. Display all student records
print("\n--- Student Registration Records ---")

for student_id, record in students.items():
    print("Student ID:", student_id)
    print("Name:", record["name"])
    print("Courses:", record["courses"])
    print("------------------------")
