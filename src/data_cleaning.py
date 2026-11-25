import pandas as pd

def missing_report(df):
    if df is None or df.empty:
        print("No data available.")
        return None
    report = df.isna().sum()

    print("\n========== MISSING VALUE REPORT ==========")
    print(report)
    return report

def clean_data(
        df,
        id_column,
        numeric_columns,
        text_columns,
        num_strategy="mean",
        text_strategy="unknown",
        mark_columns=None,
        non_negative_columns=None
):

    if df is None or df.empty:
        print("No data available for cleaning.")
        return None, None

    if num_strategy not in ["mean", "median", "zero"]:
        raise ValueError("Invalid numeric strategy.")

    if text_strategy not in ["unknown", "drop"]:
        raise ValueError("Invalid text strategy.")

    # Work on a copy to protect original data
    cleaned_df = df.copy(deep=True)
    rows_before = len(cleaned_df)

    # Validate required columns
    required_columns = (
        [id_column] + numeric_columns + text_columns
    )

    if mark_columns:
        required_columns += mark_columns

    if non_negative_columns:
        required_columns += non_negative_columns

    missing_columns = [
        column for column in required_columns
        if column not in cleaned_df.columns
    ]

    if missing_columns:
        raise KeyError(
            "Missing columns: " + ", ".join(missing_columns)
        )
    missing_report(cleaned_df)

    # Convert numeric columns
    for column in numeric_columns:
        cleaned_df[column] = pd.to_numeric(
            cleaned_df[column],
            errors="coerce"
        )

    # Detect invalid marks
    invalid_marks = 0
    if mark_columns:
        for column in mark_columns:
            invalid_condition = (
                (cleaned_df[column] < 0) |
                (cleaned_df[column] > 100)
            )
            invalid_marks += int(invalid_condition.sum())
            cleaned_df.loc[
                invalid_condition, column
            ] = float("nan")

    # Detect negative values
    invalid_negative_values = 0
    if non_negative_columns:
        for column in non_negative_columns:
            invalid_condition = cleaned_df[column] < 0
            invalid_negative_values += int(
                invalid_condition.sum()
            )
            cleaned_df.loc[
                invalid_condition, column
            ] = float("nan")

    # IMPORTANT: Detect duplicate IDs before removing duplicates
    duplicate_id_condition = cleaned_df.duplicated(
        subset=[id_column],
        keep="first"
    )
    duplicate_id_rows_detected = int(
        duplicate_id_condition.sum()
    )
    duplicate_ids_detected = (
        cleaned_df.loc[
            duplicate_id_condition, id_column
        ]
        .dropna()
        .unique()
        .tolist()
    )

    # Remove exact duplicate rows
    exact_duplicates = int(
        cleaned_df.duplicated().sum()
    )
    cleaned_df = cleaned_df.drop_duplicates(
        keep="first"
    )

    # Remove remaining duplicate IDs, if any
    remaining_duplicate_condition = cleaned_df.duplicated(
        subset=[id_column],
        keep="first"
    )
    duplicate_id_rows_removed = int(
        remaining_duplicate_condition.sum()
    )
    cleaned_df = cleaned_df.drop_duplicates(
        subset=[id_column],
        keep="first"
    )

    # Fill missing numeric values
    numeric_values_filled = 0
    for column in numeric_columns:
        missing_count = int(
            cleaned_df[column].isna().sum()
        )
        if missing_count > 0:

            if num_strategy == "mean":
                fill_value = cleaned_df[column].mean()

            elif num_strategy == "median":
                fill_value = cleaned_df[column].median()

            else:
                fill_value = 0

            if pd.isna(fill_value):
                fill_value = 0

            cleaned_df[column] = cleaned_df[column].fillna(
                fill_value
            )

            numeric_values_filled += missing_count

    # Standardise and fill text values
    text_values_filled = 0
    for column in text_columns:
        cleaned_df[column] = (
            cleaned_df[column]
            .astype("string")
            .str.strip()
            .str.title()
        )
        cleaned_df[column] = cleaned_df[column].replace(
            "", pd.NA
        )
        if text_strategy == "unknown":
            missing_count = int(
                cleaned_df[column].isna().sum()
            )
            cleaned_df[column] = cleaned_df[column].fillna(
                "Unknown"
            )
            text_values_filled += missing_count

    # Drop rows with missing text if requested
    if text_strategy == "drop" and text_columns:
        cleaned_df = cleaned_df.dropna(
            subset=text_columns
        )
    rows_after = len(cleaned_df)

    # Cleaning summary
    summary = {
        "rows_before": rows_before,
        "exact_duplicates_removed": exact_duplicates,
        "duplicate_id_rows_detected": duplicate_id_rows_detected,
        "duplicate_ids_detected": duplicate_ids_detected,
        "duplicate_id_rows_removed": duplicate_id_rows_removed,
        "invalid_marks": invalid_marks,
        "invalid_negative_values": invalid_negative_values,
        "numeric_values_filled": numeric_values_filled,
        "text_values_filled": text_values_filled,
        "numeric_strategy": num_strategy,
        "text_strategy": text_strategy,
        "rows_after": rows_after
    }

    print("\n========== CLEANING SUMMARY ==========")
    print("Rows before cleaning:", rows_before)
    print("Exact duplicate rows removed:", exact_duplicates)
    print("Duplicate ID rows detected:", duplicate_id_rows_detected)
    print("Duplicate IDs detected:", duplicate_ids_detected)
    print("Additional duplicate ID rows removed:", duplicate_id_rows_removed)
    print("Invalid marks detected:", invalid_marks)
    print("Negative values detected:", invalid_negative_values)
    print("Numeric values filled:", numeric_values_filled)
    print("Text values filled:", text_values_filled)
    print("Numeric filling strategy:", num_strategy)
    print("Text filling strategy:", text_strategy)
    print("Rows after cleaning:", rows_after)
    print("\nMissing values after cleaning:")
    print(cleaned_df.isna().sum())
    return cleaned_df, summary

if __name__ == "__main__":
    from data_loader import load_csv

    # STUDENT DATA
    print("\n========== STUDENT DATA CLEANING ==========")
    students = load_csv("../data/students.csv")

    if students is not None:
        cleaned_students, student_summary = clean_data(
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
            mark_columns=[
                "maths", "science", "english"
            ]
        )

    # SALES DATA
    print("\n========== SALES DATA CLEANING ==========")
    sales = load_csv("../data/sales.csv")

    if sales is not None:
        cleaned_sales, sales_summary = clean_data(
            sales,
            id_column="order_id",
            numeric_columns=[
                "quantity", "unit_price"
            ],
            text_columns=[
                "product", "category", "region"
            ],
            num_strategy="mean",
            text_strategy="unknown",
            non_negative_columns=[
                "quantity"
            ]
        )
