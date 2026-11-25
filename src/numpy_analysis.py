import numpy as np
from data_loader import load_csv
from data_cleaning import clean_data

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
        mark_columns=["maths", "science", "english"]
    )
    return cleaned_df

# 2. NUMPY ANALYSIS
def analyse_marks(df):
    if df is None or df.empty:
        print("No student data available.")
        return
    subjects = ["maths", "science", "english"]

    # Convert subject marks into a NumPy array
    marks = df[subjects].to_numpy(dtype=float)
    print("\n========== NUMPY ANALYSIS ==========")

    # Array attributes
    print("\n========== ARRAY ATTRIBUTES ==========")
    print("Array:\n", marks)
    print("Shape:", marks.shape)
    print("Dimensions:", marks.ndim)
    print("Total elements:", marks.size)
    print("Data type:", marks.dtype)

    # General statistical operations
    print("\n========== STATISTICAL ANALYSIS ==========")
    print("Mean:", np.mean(marks))
    print("Median:", np.median(marks))
    print("Standard deviation:", np.std(marks))
    print("Variance:", np.var(marks))
    print("Minimum marks:", np.min(marks))
    print("Maximum marks:", np.max(marks))

    # Percentiles
    print("\n========== PERCENTILE ANALYSIS ==========")
    print("25th percentile:", np.percentile(marks, 25))
    print("50th percentile:", np.percentile(marks, 50))
    print("75th percentile:", np.percentile(marks, 75))

    # Subject-wise averages using axis=0
    print("\n========== SUBJECT-WISE AVERAGES ==========")
    subject_averages = np.mean(marks, axis=0)
    for subject, average in zip(subjects, subject_averages):
        print(subject, "average:", round(average, 2))

    # Student-wise total and average using axis=1
    print("\n========== STUDENT-WISE ANALYSIS ==========")
    total_marks = np.sum(marks, axis=1)
    average_marks = np.mean(marks, axis=1)
    print("Total marks:\n", total_marks)
    print("Average marks:\n", average_marks)

    # Boolean masking: students with average above 75
    print("\n========== BOOLEAN MASKING ==========")
    high_performers = average_marks > 75
    print("Students with average above 75:")
    print(df.loc[high_performers, "name"].to_list())

    # Identify failing marks below 35
    print("\n========== FAILING MARKS ==========")
    failing_mask = marks < 35
    print("Failing marks:", marks[failing_mask])
    print("Number of failing marks:", np.sum(failing_mask))

    # Pass/Fail result using the minimum subject mark
    print("\n========== PASS / FAIL RESULT ==========")
    student_minimum = np.min(marks, axis=1)
    results = np.where(
        student_minimum >= 35,
        "Pass",
        "Fail"
    )
    for name, result in zip(df["name"], results):
        print(name, "-", result)

    # Normalization using min-max normalization
    print("\n========== NORMALIZATION ==========")
    minimum = np.min(marks)
    maximum = np.max(marks)
    if maximum != minimum:
        normalized_marks = (marks - minimum) / (maximum - minimum)
    else:
        normalized_marks = np.zeros_like(marks)
    print(normalized_marks)

    # Sorting students by average marks
    print("\n========== STUDENT RANKING ==========")
    sorted_indices = np.argsort(average_marks)[::-1]
    for index in sorted_indices:
        print(
            df.iloc[index]["name"],
            "- Average:",
            round(average_marks[index], 2)
        )

    # Grace marks: add 5 and keep scores between 0 and 100
    print("\n========== GRACE MARKS ==========")
    grace_marks = np.clip(marks + 5, 0, 100)
    print("Original marks:\n", marks)
    print("Marks after adding 5 grace marks:\n", grace_marks)

# 3. MAIN PROGRAM
def main():
    print("========== STUDENT NUMPY ANALYSIS SYSTEM ==========")
    df = load_student_data()
    if df is not None:
        analyse_marks(df)

if __name__ == "__main__":
    main()
