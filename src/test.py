import os
import runpy
import io
import contextlib

import pandas as pd
import numpy as np

from data_loader import load_csv
from data_cleaning import clean_data
from collections_ops import (
    get_student_records,
    get_unique_values,
    department_frequency
)
import reports

# ==================================================
# TESTING SYSTEM
# ==================================================

passed = 0
failed = 0

def run_test(test_id, description, test_function):
    global passed, failed
    print("\n" + "=" * 55)
    print(test_id, "-", description)
    print("=" * 55)
    try:
        result = test_function()
        if result:
            print(test_id + ": PASS")
            passed += 1
        else:
            print(test_id + ": FAIL")
            failed += 1
    except Exception as error:
        print(test_id + ": FAIL")
        print("Error:", error)
        failed += 1

# ==================================================
# HELPER FUNCTION
# ==================================================
def get_clean_students():
    students = load_csv("../data/students.csv")
    if students is None:
        raise Exception("Students data could not be loaded")

    cleaned, summary = clean_data(
        students,
        id_column="student_id",
        numeric_columns=[
            "maths", "science", "english", "attendance_pct"
        ],
        text_columns=["name", "department", "gender", "city"],
        num_strategy="mean",
        text_strategy="unknown",
        mark_columns=["maths", "science", "english"]
    )

    return cleaned


# ==================================================
# TC-01: VALID CSV LOADING
# ==================================================
def tc01():
    df = load_csv("../data/students.csv")
    return (
        df is not None
        and not df.empty
        and df.shape == (15, 9)
    )

# ==================================================
# TC-02: WRONG FILE PATH
# ==================================================
def tc02():
    df = load_csv("../data/not_existing.csv")
    return df is None

# ==================================================
# TC-03: EMPTY CSV FILE
# ==================================================
def tc03():
    df = load_csv("../data/empty.csv")
    return df is None

# ==================================================
# TC-04: REMOVE EXACT DUPLICATE ROWS
# ==================================================
def tc04():
    data = {
        "student_id": list(range(1, 19)) + [1, 2],
        "name": (
            ["Student " + str(i) for i in range(1, 19)]
            + ["Student 1", "Student 2"]
        )
    }
    df = pd.DataFrame(data)
    cleaned_df = df.drop_duplicates()
    print("Rows before cleaning:", len(df))
    print("Rows after cleaning:", len(cleaned_df))
    return len(df) == 20 and len(cleaned_df) == 18

# ==================================================
# TC-05: FILL MISSING MARKS USING MEDIAN
# ==================================================
def tc05():
    df = pd.DataFrame({
        "maths": [60, 70, None, 90, None]
    })
    median_value = df["maths"].median()
    df["maths"] = df["maths"].fillna(median_value)
    print("Median:", median_value)
    print("Missing values:", df["maths"].isnull().sum())
    return (
        median_value == 70
        and df["maths"].isnull().sum() == 0
        and (df["maths"] == 70).sum() == 3
    )

# ==================================================
# TC-06: HANDLE INVALID MARKS
# ==================================================
def tc06():
    df = pd.DataFrame({
        "student_id": [1, 2, 3, 4],
        "maths": [80, 105, 60, 90]
    })
    invalid = (
        (df["maths"] < 0) |
        (df["maths"] > 100)
    )
    print("Invalid marks found:", invalid.sum())
    df.loc[invalid, "maths"] = np.nan
    df["maths"] = df["maths"].fillna(
        df["maths"].mean()
    )
    print("Cleaned marks:")
    print(df["maths"])
    return (
        invalid.sum() == 1
        and df["maths"].between(0, 100).all()
    )

# ==================================================
# TC-07: UNIQUE DEPARTMENTS USING SET
# ==================================================
def tc07():
    df = get_clean_students()
    records = get_student_records(df)
    departments, cities = get_unique_values(records)
    print("Unique departments:", departments)
    return (
        isinstance(departments, set)
        and len(departments) == df["department"].nunique()
    )

# ==================================================
# TC-08: DEPARTMENT FREQUENCY
# ==================================================\
def tc08():
    df = get_clean_students()
    records = get_student_records(df)
    department_frequency(records)
    frequency = {}
    for record in records:
        department = record["department"]
        frequency[department] = (
            frequency.get(department, 0) + 1
        )
    print("Frequency dictionary:", frequency)
    return sum(frequency.values()) == len(records)

# ==================================================
# TC-09: FILTER MATHS ABOVE 80
# ==================================================
def tc09():
    df = get_clean_students()
    filtered = df[df["maths"] > 80]
    print(filtered[["name", "maths"]])
    return (
        not filtered.empty
        and (filtered["maths"] > 80).all()
    )

# ==================================================
# TC-10: FILTER WITH NO MATCHING RECORDS
# ==================================================
def tc10():
    df = get_clean_students()
    filtered = df[df["maths"] > 100]
    if filtered.empty:
        print("No matching records")
    return filtered.empty

# ==================================================
# TC-11: SORT TOTAL MARKS DESCENDING
# ==================================================
def tc11():
    df = get_clean_students()
    df["total"] = df[
        ["maths", "science", "english"]
    ].sum(axis=1)
    sorted_df = df.sort_values(
        by="total",
        ascending=False
    )
    print(sorted_df[["name", "total"]].head())
    return sorted_df["total"].is_monotonic_decreasing

# ==================================================
# TC-12: MULTI-COLUMN SORTING
# ==================================================
def tc12():
    df = get_clean_students()
    df["total"] = df[
        ["maths", "science", "english"]
    ].sum(axis=1)
    sorted_df = df.sort_values(
        by=["department", "total"],
        ascending=[True, False]
    )
    for department, group in sorted_df.groupby("department"):
        if not group["total"].is_monotonic_decreasing:
            return False
    print(sorted_df[["department", "name", "total"]])
    return True

# ==================================================
# TC-13: GROUP STUDENTS BY DEPARTMENT
# ==================================================
def tc13():
    df = get_clean_students()
    counts = df.groupby("department").size()
    print(counts)
    return counts.sum() == len(df)

# ==================================================
# TC-14: FREQUENCY PERCENTAGES
# ==================================================
def tc14():
    df = get_clean_students()
    percentages = (
        df["department"].value_counts(normalize=True) * 100
    )
    print(percentages)
    print("Percentage total:", percentages.sum())
    return round(percentages.sum(), 2) == 100.00

# ==================================================
# TC-15: NUMPY ROW SUMS AND COLUMN MEANS
# ==================================================
def tc15():
    arr = np.array([
        [80, 70, 60],
        [90, 85, 75]
    ])
    row_sums = np.sum(arr, axis=1)
    column_means = np.mean(arr, axis=0)
    print("Row sums:", row_sums)
    print("Column means:", column_means)
    return (
        np.array_equal(row_sums, [210, 250])
        and np.allclose(
            column_means, [85, 77.5, 67.5]
        )
    )

# ==================================================
# TC-16: NUMPY BOOLEAN MASK
# ==================================================
def tc16():
    marks = np.array([80, 34, 60, 20, 90])
    failing_marks = marks[marks < 35]
    print("Failing marks:", failing_marks)
    return np.array_equal(failing_marks, [34, 20])

# ==================================================
# TC-17: NUMPY CLIPPING
# ==================================================
def tc17():
    marks = np.array([96, 98, 100])
    updated_marks = np.clip(
        marks + 5, 0, 100
    )
    print("Updated marks:", updated_marks)
    return (
        np.array_equal(updated_marks, [100, 100, 100])
        and updated_marks.max() <= 100
    )

# ==================================================
# TC-18: GRADE BOUNDARY TEST
# ==================================================
def tc18():
    marks = pd.Series([90, 35, 34])
    grades = pd.cut(
        marks,
        bins=[0, 35, 50, 60, 70, 80, 90, 100],
        labels=["F", "E", "D", "C", "B", "A", "A+"],
        include_lowest=True,
        right=False
    )
    grades = grades.astype("object")
    grades[marks == 100] = "A+"
    print("90 marks:", grades.iloc[0])
    print("35 marks:", grades.iloc[1])
    print("34 marks:", grades.iloc[2])
    return (
        grades.iloc[0] == "A+"
        and grades.iloc[1] == "E"
        and grades.iloc[2] == "F"
    )

# ==================================================
# TC-19: EMPTY DATAFRAME REPORT
# ==================================================
def tc19():
    df = pd.DataFrame()
    if df.empty:
        print("No data available")
    return df.empty

# ==================================================
# TC-20: FULL PROJECT EXECUTION
# ==================================================
def tc20():
    print("Running complete main.py project...")
    # Capture main.py output to avoid flooding the test log
    output = io.StringIO()
    with contextlib.redirect_stdout(output):
        runpy.run_path("main.py", run_name="__main__")
    result = output.getvalue()
    required_files = [
        "../output/student_report.csv",
        "../output/sales_report.csv",
        "../output/data_quality_report.csv"
    ]
    reports_exist = all(
        os.path.exists(file) for file in required_files
    )
    successful_run = (
        "PROJECT EXECUTED SUCCESSFULLY" in result
    )
    print("Student report:", os.path.exists(required_files[0]))
    print("Sales report:", os.path.exists(required_files[1]))
    print("Data quality report:", os.path.exists(required_files[2]))
    return successful_run and reports_exist

# ==================================================
# RUN ALL 20 TEST CASES
# ==================================================
print("\n")
print("=" * 55)
print(" STUDENT BUSINESS DATA PROCESSING SYSTEM")
print("             TEST EXECUTION")
print("=" * 55)

run_test("TC-01", "Valid CSV Loading", tc01)
run_test("TC-02", "Wrong File Path", tc02)
run_test("TC-03", "Empty CSV File", tc03)
run_test("TC-04", "Remove Exact Duplicate Rows", tc04)
run_test("TC-05", "Fill Missing Marks Using Median", tc05)
run_test("TC-06", "Handle Invalid Marks", tc06)
run_test("TC-07", "Unique Departments Using Set", tc07)
run_test("TC-08", "Department Frequency", tc08)
run_test("TC-09", "Filter Maths Above 80", tc09)
run_test("TC-10", "Filter With No Matching Records", tc10)
run_test("TC-11", "Sort Total Marks Descending", tc11)
run_test("TC-12", "Multi-Column Sorting", tc12)
run_test("TC-13", "Group Students By Department", tc13)
run_test("TC-14", "Frequency Percentages", tc14)
run_test("TC-15", "NumPy Row Sums And Column Means", tc15)
run_test("TC-16", "NumPy Boolean Mask", tc16)
run_test("TC-17", "NumPy Clipping", tc17)
run_test("TC-18", "Grade Boundary Test", tc18)
run_test("TC-19", "Empty DataFrame Report", tc19)
run_test("TC-20", "Full Project Execution", tc20)

# ==================================================
# FINAL TEST SUMMARY
# ==================================================
print("\n")
print("=" * 55)
print("              FINAL TEST SUMMARY")
print("=" * 55)
print("Total Test Cases:", passed + failed)
print("Passed:", passed)
print("Failed:", failed)

if failed == 0:
    print("\nALL TEST CASES PASSED SUCCESSFULLY!")
else:
    print("\nSOME TEST CASES FAILED. CHECK THE OUTPUT.")
print("=" * 55)
