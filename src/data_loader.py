import pandas as pd

def load_csv(path, required_columns=None):
    try:
        df = pd.read_csv(path)
        if df.empty:
            print("No data available in file:", path)
            return None

        if required_columns is not None:
            missing_columns = [
                column for column in required_columns
                if column not in df.columns
            ]

            if missing_columns:
                raise KeyError(
                    "Missing required columns: "
                    + ", ".join(missing_columns)
                )
        print("\nFile loaded successfully:", path)
        return df

    except FileNotFoundError:
        print("\nFile not found:", path)

    except pd.errors.EmptyDataError:
        print("\nFile is empty:", path)

    except KeyError as error:
        print("\nColumn validation error:", error)
    return None

def create_dataframe(records):
    try:
        df = pd.DataFrame(records)
        if df.empty:
            print("No records available to create DataFrame.")
            return None
        return df
    except (ValueError, TypeError) as error:
        print("Unable to create DataFrame:", error)
        return None

def display_data(df):
    if df is None or df.empty:
        print("\nNo data available.")
        return
    print("\nShape:")
    print(df.shape)
    print("\nColumn Names:")
    print(df.columns.tolist())
    print("\nData Types:")
    print(df.dtypes)
    print("\nFirst 5 Rows:")
    print(df.head(5))

if __name__ == "__main__":

    print("\n========== STUDENT DATA ==========")
    student_columns = [
        "student_id", "name", "department", "gender",
        "maths", "science", "english", "attendance_pct", "city"
    ]
    students = load_csv(
        "../data/students.csv",
        student_columns
    )
    display_data(students)

    print("\n========== SALES DATA ==========")
    sales_columns = [
        "order_id", "product", "category", "region",
        "quantity", "unit_price", "order_date"
    ]
    sales = load_csv(
        "../data/sales.csv",
        sales_columns
    )
    display_data(sales)

    print("\n========== DEPARTMENT DATA ==========")
    department_columns = [
        "department", "department_name", "department_head"
    ]
    departments = load_csv(
        "../data/departments.csv",
        department_columns
    )
    display_data(departments)

    print("\n========== DICTIONARY TO DATAFRAME ==========")
    records = [
        {"student_id": 201, "name": "Rahul", "marks": 85},
        {"student_id": 202, "name": "Priya", "marks": 90},
        {"student_id": 203, "name": "Aman", "marks": 78}
    ]
    dictionary_df = create_dataframe(records)
    display_data(dictionary_df)

    print("\n========== ERROR HANDLING ==========")
    load_csv("../data/wrong_file.csv")
    load_csv("../data/students.csv", ["student_id", "wrong_column"])
