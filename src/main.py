import data_loader
import data_cleaning
import collections_ops
import numpy_analysis
import pandas_analysis
import reports

def main():
    print("\n========================================")
    print(" STUDENT BUSINESS DATA PROCESSING SYSTEM")
    print("========================================")

    # STEP 1: DATA LOADING
    print("\n\nSTEP 1: DATA LOADING")
    students = data_loader.load_csv("../data/students.csv")
    if students is None:
        print("Student data could not be loaded.")
        return
    data_loader.display_data(students)

    # STEP 2: DATA CLEANING
    print("\n\nSTEP 2: DATA CLEANING")
    cleaned_students, cleaning_summary = data_cleaning.clean_data(
        students,
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
    print("\nCleaning Summary:")
    print(cleaning_summary)

    # STEP 3: PYTHON COLLECTIONS
    print("\n\nSTEP 3: PYTHON COLLECTIONS")
    records = collections_ops.get_student_records(cleaned_students)
    departments, cities = collections_ops.get_unique_values(records)
    collections_ops.department_frequency(records)
    collections_ops.set_operations(departments, cities)
    collections_ops.sort_students(records)

    # STEP 4: NUMPY ANALYSIS
    print("\n\nSTEP 4: NUMPY ANALYSIS")
    numpy_analysis.analyse_marks(cleaned_students)

    # STEP 5: PANDAS ANALYSIS
    print("\n\nSTEP 5: PANDAS ANALYSIS")
    pandas_df = pandas_analysis.load_student_data()
    if pandas_df is not None:
        pandas_analysis.series_operations(pandas_df)
        pandas_df = pandas_analysis.add_derived_columns(pandas_df)
        pandas_analysis.dataframe_overview(pandas_df)
        pandas_analysis.column_operations(pandas_df)
        pandas_analysis.merge_department_data(pandas_df)
        pandas_analysis.monthly_sales_analysis()

    # STEP 6: FINAL REPORTS
    print("\n\nSTEP 6: FINAL REPORTS")
    reports.student_report()
    reports.sales_report()
    reports.data_quality_report()
    print("\n========================================")
    print(" PROJECT EXECUTED SUCCESSFULLY")
    print("========================================")

if __name__ == "__main__":
    main()