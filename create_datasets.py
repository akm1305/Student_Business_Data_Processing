import os
import pandas as pd

def create_data_folder():
    os.makedirs("data", exist_ok=True)

def create_students_dataset():
    students = [
        [101, "Asha Rao", "CSE", "Female", 85, 90, 88, 95, "Delhi"],
        [102, "Kiran Das", "ECE", "Male", 78, 82, 80, 88, "Mumbai"],
        [103, "Neha Singh", "CSE", "Female", 92, 89, 95, 92, "Delhi"],
        [101, "Asha Rao", "CSE", "Female", 85, 90, 88, 95, "Delhi"],
        [104, "Meena Iyer", "MECH", "Female", 45, 55, 60, 60, "Chennai"],
        [105, "Sameer Khan", "ECE", "Male", 65, 70, 68, 74, "Delhi"],
        [106, "Rahul Verma", "CSE", "Male", 90, 85, 88, 96, "Mumbai"],
        [107, "Priya Sharma", "MECH", "Female", 72, 75, 80, 85, "Jaipur"],
        [108, "Arjun Patel", "ECE", "Male", None, 68, 72, 78, "Ahmedabad"],
        [109, "Simran Kaur", "CSE", "Female", 105, 88, 91, 89, "Delhi"],
        [110, "Rohan Mehta", "MECH", "Male", 55, 60, 58, 82, "Mumbai"],
        [111, "Ananya Roy", "CSE", "Female", 88, 92, 90, 97, None],
        [112, "Vikram Joshi", "ECE", "Male", 67, None, 75, 80, "Jaipur"],
        [113, "Divya Nair", "MECH", "Female", 81, 84, 79, 91, "Chennai"],
        [114, "Aman Gupta", None, "Male", 76, 73, 70, 86, "Delhi"]
    ]
    columns = [
        "student_id", "name", "department", "gender",
        "maths", "science", "english", "attendance_pct", "city"
    ]
    df = pd.DataFrame(students, columns=columns)
    df.to_csv("data/students.csv", index=False)
    print("students.csv created successfully!")

def create_sales_dataset():
    sales = [
        [1001, "Laptop", "Electronics", "North", 2, 55000, "2026-01-05"],
        [1002, "Mouse", "Electronics", "South", 5, 500, "2026-01-12"],
        [1003, "Chair", "Furniture", "East", 3, 4500, "2026-01-18"],
        [1004, "Keyboard", "Electronics", "West", 4, 1200, "2026-02-02"],
        [1005, "Table", "Furniture", "North", 2, 8000, "2026-02-10"],
        [1006, "Notebook", "Stationery", "South", 20, 50, "2026-02-15"],
        [1007, "Laptop", "Electronics", "East", 1, 55000, "2026-02-20"],
        [1008, "Stapler", "Stationery", "West", 10, 120, "2026-03-01"],
        [1009, "Monitor", "Electronics", "North", 3, 15000, "2026-03-08"],
        [1010, "Desk", "Furniture", "South", 2, 9500, "2026-03-15"],
        [1011, "Mouse", "Electronics", "East", -2, 500, "2026-03-20"],
        [1012, "Notebook", "Stationery", "West", 15, 50, "2026-03-25"],
        [1013, "Keyboard", "Electronics", "North", 3, None, "2026-04-02"],
        [1014, "Chair", "Furniture", "South", 4, 4500, "2026-04-10"],
        [1015, "Laptop", "Electronics", "West", 2, 55000, "2026-04-15"],
        [1016, "Stapler", "Stationery", "East", 8, 120, "invalid-date"],
        [1017, "Monitor", "Electronics", "North", 2, 15000, "2026-04-20"],
        [1018, "Desk", "Furniture", "West", 1, 9500, "2026-04-25"],
        [1001, "Laptop", "Electronics", "North", 2, 55000, "2026-01-05"]
    ]
    columns = [
        "order_id", "product", "category", "region",
        "quantity", "unit_price", "order_date"
    ]
    df = pd.DataFrame(sales, columns=columns)
    df.to_csv("data/sales.csv", index=False)
    print("sales.csv created successfully!")

def create_departments_dataset():
    departments = [
        ["CSE", "Computer Science and Engineering", "Dr. Sharma"],
        ["ECE", "Electronics and Communication Engineering", "Dr. Mehta"],
        ["MECH", "Mechanical Engineering", "Dr. Verma"],
        ["CIVIL", "Civil Engineering", "Dr. Gupta"]
    ]
    columns = ["department", "department_name", "department_head"]
    df = pd.DataFrame(departments, columns=columns)
    df.to_csv("data/departments.csv", index=False)
    print("departments.csv created successfully!")

def main():
    create_data_folder()
    create_students_dataset()
    create_sales_dataset()
    create_departments_dataset()
    print("\nAll datasets generated successfully!")
    print("\nGenerated files:")
    for filename in os.listdir("data"):
        print(" -", filename)

if __name__ == "__main__":
    main()
