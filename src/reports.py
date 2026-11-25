import pandas as pd

# 1. STUDENT PERFORMANCE REPORT
def student_report():
    students = pd.read_csv("../data/students.csv")

    # Remove duplicate rows
    students = students.drop_duplicates()

    # Handle missing department
    students["department"] = students["department"].fillna("Unknown")
    subjects = ["maths", "science", "english"]

    # Clean marks
    for column in subjects:
        students[column] = pd.to_numeric(
            students[column], errors="coerce"
        )
        students.loc[
            (students[column] < 0) | (students[column] > 100),
            column
        ] = None
        students[column] = students[column].fillna(
            students[column].mean()
        )

    # Handle missing attendance
    students["attendance_pct"] = pd.to_numeric(
        students["attendance_pct"], errors="coerce"
    )
    students["attendance_pct"] = students["attendance_pct"].fillna(
        students["attendance_pct"].mean()
    )

    # Calculate total and average marks
    students["total_marks"] = students[subjects].sum(axis=1)
    students["percentage"] = students[subjects].mean(axis=1)

    # Pass or fail
    students["result"] = students[subjects].ge(35).all(axis=1)
    students["result"] = students["result"].map({
        True: "Pass",
        False: "Fail"
    })

    # Grade calculation according to PDF
    students["grade"] = pd.cut(
        students["percentage"],
        bins=[0, 35, 50, 60, 70, 80, 90, 100],
        labels=["F", "E", "D", "C", "B", "A", "A+"],
        include_lowest=True,
        right=False
    )
    students.loc[
        students["percentage"] == 100, "grade"
    ] = "A+"

    print("\n========== STUDENT PERFORMANCE REPORT ==========")
    print("\nTotal Students:", len(students))
    print("Overall Average:", round(students["percentage"].mean(), 2))
    print("\nHighest Scorer:")
    print(
        students.loc[
            students["percentage"].idxmax(),
            ["name", "percentage"]
        ]
    )
    print("\nLowest Scorer:")
    print(
        students.loc[
            students["percentage"].idxmin(),
            ["name", "percentage"]
        ]
    )
    print("\nPass Count:", (students["result"] == "Pass").sum())
    print("Fail Count:", (students["result"] == "Fail").sum())

    # Department-wise summary
    print("\n========== DEPARTMENT SUMMARY ==========")
    department_summary = students.groupby("department").agg(
        student_count=("student_id", "count"),
        average_percentage=("percentage", "mean")
    )
    print(department_summary.round(2))

    # Top 5 students
    print("\n========== TOP 5 STUDENTS ==========")
    top_students = students.sort_values(
        by="percentage", ascending=False
    ).head(5)
    print(
        top_students[
            ["name", "department", "percentage"]
        ].round(2)
    )

    # Bottom 5 students
    print("\n========== BOTTOM 5 STUDENTS ==========")
    bottom_students = students.sort_values(
        by="percentage", ascending=True
    ).head(5)
    print(
        bottom_students[
            ["name", "department", "percentage"]
        ].round(2)
    )

    # Grade distribution
    print("\n========== GRADE DISTRIBUTION ==========")
    print(students["grade"].value_counts(sort=False))

    # Attendance below 75%
    print("\n========== ATTENDANCE CONCERNS ==========")
    attendance = students[
        students["attendance_pct"] < 75
    ]
    print(
        attendance[
            ["name", "attendance_pct"]
        ]
    )

    # Save student report
    students.to_csv(
        "../output/student_report.csv", index=False
    )
    print("\nStudent Report saved successfully.")

# 2. BUSINESS SALES REPORT
def sales_report():
    sales = pd.read_csv("../data/sales.csv")

    # Remove duplicate rows
    sales = sales.drop_duplicates()

    # Convert numerical columns
    sales["quantity"] = pd.to_numeric(
        sales["quantity"], errors="coerce"
    )
    sales["unit_price"] = pd.to_numeric(
        sales["unit_price"], errors="coerce"
    )

    # Handle negative quantity
    sales.loc[sales["quantity"] < 0, "quantity"] = None

    # Fill missing numerical values
    sales["quantity"] = sales["quantity"].fillna(
        sales["quantity"].mean()
    )
    sales["unit_price"] = sales["unit_price"].fillna(
        sales["unit_price"].mean()
    )

    # Calculate revenue
    sales["revenue"] = sales["quantity"] * sales["unit_price"]

    print("\n========== BUSINESS SALES REPORT ==========")
    print("\nTotal Orders:", sales["order_id"].nunique())
    print("Total Revenue:", round(sales["revenue"].sum(), 2))
    print(
        "Average Order Value:",
        round(
            sales.groupby("order_id")["revenue"].sum().mean(), 2
        )
    )

    # Region-wise revenue
    print("\n========== REGION-WISE REVENUE ==========")
    print(
        sales.groupby("region")["revenue"].sum().round(2)
    )

    # Category-wise revenue
    print("\n========== CATEGORY-WISE REVENUE ==========")
    print(
        sales.groupby("category")["revenue"].sum().round(2)
    )

    # Product-wise revenue
    print("\n========== PRODUCT-WISE REVENUE ==========")
    product_sales = sales.groupby("product")["revenue"].sum()
    print(product_sales.sort_values(ascending=False).round(2))
    print("\nBest Product:", product_sales.idxmax())
    print("Worst Product:", product_sales.idxmin())

    # Monthly sales
    sales["order_date"] = pd.to_datetime(
        sales["order_date"], errors="coerce"
    )
    sales["month"] = sales["order_date"].dt.strftime("%B")

    print("\n========== MONTHLY SALES ==========")
    monthly_sales = sales.groupby("month")["revenue"].sum()
    print(monthly_sales.round(2))
    if not monthly_sales.empty:
        print("Best Month:", monthly_sales.idxmax())

    # Save sales report
    sales.to_csv(
        "../output/sales_report.csv", index=False
    )
    print("\nSales Report saved successfully.")

# 3. DATA QUALITY REPORT
def data_quality_report():
    students = pd.read_csv("../data/students.csv")
    sales = pd.read_csv("../data/sales.csv")

    print("\n========== DATA QUALITY REPORT ==========")
    # Student data quality
    print("\nSTUDENT DATA")
    print("\nMissing Values:")
    print(students.isnull().sum())
    print("\nDuplicate Rows:")
    print(students.duplicated().sum())
    print("\nDuplicate Student IDs:")
    print(students["student_id"].duplicated().sum())
    subjects = ["maths", "science", "english"]

    for column in subjects:
        students[column] = pd.to_numeric(
            students[column], errors="coerce"
        )
    invalid_marks = (
        (students[subjects] < 0) |
        (students[subjects] > 100)
    ).sum().sum()
    print("\nInvalid Marks:", invalid_marks)

    # Sales data quality
    print("\nSALES DATA")
    print("\nMissing Values:")
    print(sales.isnull().sum())
    print("\nDuplicate Rows:")
    print(sales.duplicated().sum())
    print("\nDuplicate Order IDs:")
    print(sales["order_id"].duplicated().sum())
    sales["quantity"] = pd.to_numeric(
        sales["quantity"], errors="coerce"
    )
    negative_quantity = (sales["quantity"] < 0).sum()
    print("\nNegative Quantities:", negative_quantity)

    # Create data quality summary
    quality = pd.DataFrame({
        "Report": ["Student Data", "Sales Data"],
        "Missing Values": [
            students.isnull().sum().sum(),
            sales.isnull().sum().sum()
        ],
        "Duplicate Rows": [
            students.duplicated().sum(),
            sales.duplicated().sum()
        ],
        "Duplicate IDs": [
            students["student_id"].duplicated().sum(),
            sales["order_id"].duplicated().sum()
        ],
        "Invalid Values": [
            invalid_marks,
            negative_quantity
        ]
    })

    print("\n========== CLEANING ACTIONS ==========")
    print("1. Duplicate rows removed during processing.")
    print("2. Missing numerical values filled using mean.")
    print("3. Missing department values filled with Unknown.")
    print("4. Invalid marks identified and handled.")
    print("5. Negative quantities identified and handled.")
    print("6. Revenue calculated using quantity * unit price.")

    # Save data quality report
    quality.to_csv(
        "../output/data_quality_report.csv", index=False
    )
    print("\nData Quality Report saved successfully.")

# MAIN PROGRAM
if __name__ == "__main__":
    student_report()
    sales_report()
    data_quality_report()
    print("\nAll Three Reports Generated Successfully.")