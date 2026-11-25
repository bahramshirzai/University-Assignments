
# Lab 1 - Collection Operations

# 1. Create a list of at least 10 student scores
scores = [85, 45, 90, 65, 72, 55, 100, 85, 30, 78, 60]

print("Student Scores:", scores)


# 2. Calculate minimum, maximum and average
minimum = min(scores)
maximum = max(scores)
average = sum(scores) / len(scores)

print("\nMinimum Score:", minimum)
print("Maximum Score:", maximum)
print("Average Score:", average)


# 3. Create a new list containing scores >= 60
passed_scores = [score for score in scores if score >= 60]

print("\nPassed Scores:", passed_scores)


# 4. Convert the list to a set
unique_scores = set(scores)

print("\nUnique Scores:", unique_scores)


# 5. Create a dictionary mapping student IDs to names
students = {
    101: "Ahmad",
    102: "Ali",
    103: "Farid",
    104: "Omar",
    105: "Khalid",
    106: "Hamid",
    107: "Karim",
    108: "Zahir",
    109: "Nasir",
    110: "Wahid",
    111: "Bilal"
}

print("\nStudent Dictionary:", students)


# 6. Search for one student by ID
search_id = 103

if search_id in students:
    print("\nStudent Found:", students[search_id])
else:
    print("\nStudent Not Found!")


# 7. Sort student records by score
student_records = list(zip(students.values(), scores))

sorted_records = sorted(student_records, key=lambda x: x[1])

print("\nStudents Sorted by Score:")

for name, score in sorted_records:
    print(name, ":", score)


# 8. Use enumerate()
print("\nStudent List with Numbers:")

for index, name in enumerate(students.values(), start=1):
    print(index, name)


# 9. Use zip()
print("\nStudent Names and Scores:")

for name, score in zip(students.values(), scores):
    print(name, "scored", score)
