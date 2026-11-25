import pandas as pd
from data_loader import load_csv
from data_cleaning import clean_data

# CONSTANTS
SUBJECTS = ["maths", "science", "english"]
GRADE_BINS = [0, 35, 50, 60, 70, 80, 90, 100]
GRADE_LABELS = ["F", "E", "D", "C", "B", "A", "A+"]

# 1. LOAD AND CLEAN STUDENT DATA
def load_student_data():
    df = load_csv(
        "../data/students.csv",
        required_columns=[
            "student_id", "name", "department", "gender",
            "maths", "science", "english",
            "attendance_pct", "city"
        ]
    )

    if df is None:
        return None
    cleaned_df, summary = clean_data(
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
        mark_columns=SUBJECTS
    )
    return cleaned_df

# 2. PANDAS SERIES
def series_operations(df):
    print("\n========== PANDAS SERIES ==========")
    total_series = pd.Series(
        df[SUBJECTS].sum(axis=1).values,
        index=df["name"],
        name="Total Marks"
    )

    print("\nTotal marks Series:")
    print(total_series)

    print("\nFirst five students:")
    print(total_series.head())

    print("\nSeries arithmetic (adding 5 marks):")
    print(total_series + 5)

    print("\nTotal marks frequency:")
    print(total_series.value_counts())

# 3. DERIVED COLUMNS
def add_derived_columns(df):
    print("\n========== DERIVED COLUMNS ==========")
    df = df.copy()

    # Total marks out of 300
    df["total"] = df[SUBJECTS].sum(axis=1)

    # Average marks
    df["average"] = df[SUBJECTS].mean(axis=1)

    # Percentage
    df["percentage"] = (
        df["total"] / 300 * 100
    ).round(2)

    # Grade using exact assignment boundaries
    df["grade"] = pd.cut(
        df["percentage"],
        bins=GRADE_BINS,
        labels=GRADE_LABELS,
        include_lowest=True,
        right=False
    )

    # Include exactly 100 in A+
    df.loc[df["percentage"] == 100, "grade"] = "A+"

    # Pass or Fail using the minimum subject mark
    df["result"] = df[SUBJECTS].min(axis=1).apply(
        lambda mark: "Pass" if mark >= 35 else "Fail"
    )

    # Map grades to remarks
    grade_remarks = {
        "F": "Fail",
        "E": "Needs Improvement",
        "D": "Satisfactory",
        "C": "Average",
        "B": "Good",
        "A": "Very Good",
        "A+": "Excellent"
    }
    df["remark"] = df["grade"].astype(str).map(grade_remarks)
    print(
        df[
            ["name", "total", "average", "percentage",
             "grade", "result", "remark"]
        ].to_string(index=False)
    )
    return df

# 4. DATAFRAME OVERVIEW
def dataframe_overview(df):
    print("\n========== DATAFRAME OVERVIEW ==========")
    print("\nFirst five rows:")
    print(df.head())
    print("\nLast five rows:")
    print(df.tail())
    print("\nDataset information:")
    df.info()
    print("\nStatistical description:")
    print(df.describe())

# 5. COLUMN OPERATIONS
def column_operations(df):
    print("\n========== COLUMN OPERATIONS ==========")

    # Rename a column
    renamed_df = df.rename(
        columns={"attendance_pct": "attendance"}
    )
    print("\nRenamed column:")
    print(renamed_df.columns.tolist())

    # Reorder columns
    ordered_columns = [
        "student_id", "name", "department",
        "maths", "science", "english",
        "total", "average", "percentage",
        "grade", "result", "remark",
        "attendance", "gender", "city"
    ]
    reordered_df = renamed_df[ordered_columns]
    print("\nReordered columns:")
    print(reordered_df.head())

    # Drop a column from a copy
    reduced_df = reordered_df.drop(columns=["remark"])
    print("\nDataFrame after dropping remark:")
    print(reduced_df.columns.tolist())


# 6. GROUPING AND PIVOT TABLE
def grouping_and_pivot_analysis(df):

    print("\n========== STUDENT GROUPING ANALYSIS ==========")

    # Group by department
    print("\nDepartment-wise student count:")
    print(df.groupby("department").size())

    # Group by gender
    print("\nGender-wise student count:")
    print(df.groupby("gender").size())

    # Group by city
    print("\nCity-wise student count:")
    print(df.groupby("city").size())

    # Multi-column grouping
    print("\nDepartment and gender-wise average marks:")
    print(
        df.groupby(["department", "gender"])[SUBJECTS]
        .mean()
        .round(2)
    )

    print("\n========== SALES GROUPING AND PIVOT ==========")
    sales = load_csv(
        "../data/sales.csv",
        required_columns=[
            "order_id", "product", "category", "region",
            "quantity", "unit_price", "order_date"
        ]
    )

    if sales is None:
        print("Sales data could not be loaded.")
        return
    sales, summary = clean_data(
        sales,
        id_column="order_id",
        numeric_columns=["quantity", "unit_price"],
        text_columns=["product", "category", "region"],
        num_strategy="mean",
        text_strategy="unknown",
        non_negative_columns=["quantity", "unit_price"]
    )
    sales["revenue"] = sales["quantity"] * sales["unit_price"]

    # Category-wise revenue
    print("\nCategory-wise sales revenue:")
    print(sales.groupby("category")["revenue"].sum())

    # Region-wise revenue
    print("\nRegion-wise sales revenue:")
    print(sales.groupby("region")["revenue"].sum())

    # Pivot table: category versus region
    print("\nSales Pivot Table:")
    pivot = pd.pivot_table(
        sales,
        values="revenue",
        index="category",
        columns="region",
        aggfunc="sum",
        fill_value=0
    )
    print(pivot.round(2))

# 6. MERGE STUDENTS WITH DEPARTMENT INFORMATION
def merge_department_data(df):

    print("\n========== DEPARTMENT DATA MERGE ==========")
    departments = load_csv(
        "../data/departments.csv",
        required_columns=[
            "department", "department_name", "department_head"
        ]
    )
    if departments is None:
        print("Department data could not be loaded.")
        return df
    student_data = df.copy()
    department_data = departments.copy()

    # Standardize department names for matching
    student_data["department_key"] = (
        student_data["department"].astype("string").str.strip().str.upper()
    )
    department_data["department_key"] = (
        department_data["department"].astype("string").str.strip().str.upper()
    )

    # Keep only the merge key and department information
    department_data = department_data[
        ["department_key", "department_name", "department_head"]
    ]

    # Merge both datasets
    merged_df = pd.merge(
        student_data,
        department_data,
        on="department_key",
        how="left"
    )
    print("\nMerged student and department data:")
    print(
        merged_df[
            ["name", "department", "department_name", "department_head"]
        ].to_string(index=False)
    )

    # Show departments without matching information
    unmatched = merged_df[merged_df["department_name"].isna()]
    if not unmatched.empty:
        print("\nDepartments without matching information:")
        print(unmatched["department"].unique())
    return merged_df

# 7. SALES DATA AND MONTHLY ANALYSIS
def monthly_sales_analysis():
    print("\n========== MONTHLY SALES ANALYSIS ==========")
    sales = load_csv(
        "../data/sales.csv",
        required_columns=[
            "order_id", "product", "category", "region",
            "quantity", "unit_price", "order_date"
        ]
    )
    if sales is None:
        return
    sales, cleaning_summary = clean_data(
        sales,
        id_column="order_id",
        numeric_columns=["quantity", "unit_price"],
        text_columns=["product", "category", "region"],
        num_strategy="mean",
        text_strategy="unknown",
        non_negative_columns=["quantity", "unit_price"]
    )

    # Convert order_date into datetime
    sales["order_date"] = pd.to_datetime(
        sales["order_date"],
        errors="coerce"
    )

    # Calculate revenue
    sales["revenue"] = (
        sales["quantity"] * sales["unit_price"]
    )

    # Remove rows whose dates could not be converted
    valid_sales = sales.dropna(subset=["order_date"]).copy()

    # Extract month
    valid_sales["month"] = (
        valid_sales["order_date"].dt.to_period("M")
    )

    # Calculate monthly revenue
    monthly_sales = (
        valid_sales.groupby("month")["revenue"]
        .sum()
        .reset_index()
    )
    print("\nMonthly sales revenue:")
    print(monthly_sales.to_string(index=False))

# 8. MAIN PROGRAM
def main():
    print("========== PANDAS ANALYSIS SYSTEM ==========")
    df = load_student_data()
    if df is None:
        print("Student data is unavailable.")
        return
    series_operations(df)
    df = add_derived_columns(df)
    dataframe_overview(df)
    column_operations(df)
    grouping_and_pivot_analysis(df)
    merge_department_data(df)
    monthly_sales_analysis()

if __name__ == "__main__":
    main()
