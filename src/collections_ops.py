from data_loader import load_csv
from data_cleaning import clean_data

# 1. TUPLES
subjects = ("maths", "science", "english")

# Grade boundaries specified in the assignment
grade_boundaries = (0, 35, 50, 60, 70, 80, 90, 100)
grade_labels = ("F", "E", "D", "C", "B", "A", "A+")

# 2. CONVERT DATAFRAME INTO A LIST OF DICTIONARIES
def get_student_records(df):
    return df.to_dict("records")

# 3. LIST OPERATIONS
def list_operations(records):
    student_names = [student["name"] for student in records]

    print("\n========== LIST OPERATIONS ==========")
    print("Total students:", len(student_names))
    print("First student:", student_names[0])
    print("First five students:", student_names[:5])
    student_names.append("Sample Student")
    print("After append:", student_names[-3:])
    return student_names

# 4. SET OPERATIONS
def get_unique_values(records):
    departments = {student["department"] for student in records}
    cities = {student["city"] for student in records}

    print("\n========== UNIQUE VALUES ==========")
    print("Unique departments:", departments)
    print("Unique cities:", cities)
    return departments, cities

def set_operations(departments, cities):
    print("\n========== SET OPERATIONS ==========")
    print("Union:", departments.union(cities))
    print("Intersection:", departments.intersection(cities))
    print("Difference (departments - cities):",
          departments.difference(cities))

# 5. DICTIONARY OPERATIONS
def department_frequency(records):
    frequency = {}
    for student in records:
        department = student["department"]
        frequency[department] = frequency.get(department, 0) + 1

    print("\n========== DEPARTMENT FREQUENCY ==========")
    print(frequency)
    return frequency

# 6. SORTING USING sorted() AND lambda
def sort_students(records):
    sorted_students = sorted(
        records,
        key=lambda student: student["maths"],
        reverse=True
    )

    print("\n========== STUDENTS SORTED BY MATHS ==========")
    for student in sorted_students:
        print(student["name"], "-", student["maths"])
    return sorted_students

# 7. MAIN PROGRAM
def main():
    print("========== COLLECTIONS OPERATIONS ==========")
    df = load_csv(
        "../data/students.csv",
        required_columns=[
            "student_id", "name", "department", "gender",
            "maths", "science", "english",
            "attendance_pct", "city"
        ]
    )
    if df is None:
        print("Student data could not be loaded.")
        return
    cleaned_df, cleaning_summary = clean_data(
        df,
        id_column="student_id",
        numeric_columns=[
            "maths", "science", "english", "attendance_pct"
        ],
        text_columns=[
            "name", "department", "gender", "city"
        ],
        num_strategy="mean",
        text_strategy="unknown",
        mark_columns=["maths", "science", "english"]
    )
    records = get_student_records(cleaned_df)
    print("\nSubjects tuple:", subjects)
    print("Grade boundaries tuple:", grade_boundaries)
    print("Grade labels tuple:", grade_labels)
    list_operations(records)
    departments, cities = get_unique_values(records)
    department_frequency(records)
    set_operations(departments, cities)
    sort_students(records)

if __name__ == "__main__":
    main()
