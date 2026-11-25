# Student Business Data Processing System

## 1. Project Description

The Student Business Data Processing System is a Python-based project designed to load, clean, process, analyse and generate reports from student and business datasets.

The project uses Python, NumPy and Pandas to perform data processing, numerical analysis and reporting.

## 2. Business Objectives

- Load student, sales and department datasets.
- Identify and handle missing values.
- Detect and remove duplicate records.
- Handle invalid numerical values.
- Perform numerical analysis using NumPy.
- Analyse data using Pandas.
- Perform filtering, sorting, grouping and data merging.
- Generate student performance, business sales and data quality reports.

## 3. Technologies Used

- Python
- NumPy
- Pandas
- PyCharm IDE

## 4. Project Structure

```text
Student_Business_Data_Processing/
│
├── data/
│   ├── students.csv
│   ├── sales.csv
│   ├── departments.csv
│   └── empty.csv
│
├── src/
│   ├── data_loader.py
│   ├── data_cleaning.py
│   ├── collections_ops.py
│   ├── numpy_analysis.py
│   ├── pandas_analysis.py
│   ├── reports.py
│   ├── main.py
│   └── test.py
│
├── tests/
│   └── test_log.md
│
├── output/
│   ├── student_report.csv
│   ├── sales_report.csv
│   └── data_quality_report.csv
│
└── README.md
```

## 5. Libraries Required

The project uses the following Python libraries:

- NumPy
- Pandas

Install them using:

```bash
pip install numpy pandas
```

## 6. How to Run the Project

### Step 1: Open the project

Open the `Student_Business_Data_Processing` folder in PyCharm.

### Step 2: Install libraries

Open the terminal and install the required libraries:

```bash
pip install numpy pandas
```

### Step 3: Open the source directory

From the project root directory, execute:

```bash
cd src
```

### Step 4: Run the main program

Execute:

```bash
python main.py
```

### Step 5: Run the test cases

To execute all 20 test cases, run:

```bash
python test.py
```

## 7. Project Modules

### Data Loading

- Loads CSV files into Pandas DataFrames.
- Creates DataFrames from dictionaries.
- Displays dataset shape, columns, data types and sample records.
- Handles missing files and empty CSV files.

### Data Cleaning

- Identifies missing values.
- Removes duplicate records.
- Handles duplicate IDs.
- Handles invalid marks and negative numerical values.
- Fills missing numerical and text values.

### Python Collections

- Demonstrates Lists, Tuples, Sets and Dictionaries.
- Converts DataFrames into lists of dictionaries.
- Performs set operations.
- Calculates department frequency.
- Sorts student records using lambda functions.

### NumPy Analysis

- Creates NumPy arrays from student marks.
- Calculates mean, median, standard deviation and variance.
- Calculates minimum, maximum, totals and averages.
- Performs Boolean masking, normalization and clipping.
- Analyses student performance using numerical operations.

### Pandas Analysis

- Performs Series and DataFrame operations.
- Creates derived columns such as total marks, average and percentage.
- Calculates grades and pass/fail results.
- Performs filtering and sorting.
- Groups students by department, gender and city.
- Performs sales aggregation and pivot table analysis.
- Merges student and department datasets.
- Performs monthly sales analysis.

### Reports

Generates three reports:

1. Student Performance Report
2. Business Sales Report
3. Data Quality Report

The reports are exported as CSV files into the output directory.

### Main Program

Connects all project modules and executes the complete data processing pipeline:

**LOAD → CLEAN → PROCESS → ANALYSE → REPORT**

## 8. Expected Output

The system generates:

- Student performance report.
- Sales revenue report.
- Department-wise student analysis.
- Region-wise and category-wise sales analysis.
- Monthly sales analysis.
- Data quality report.
- Numerical statistics using NumPy.

All generated CSV reports are stored in the `output` directory.

## 9. Testing

The project includes 20 test cases covering:

- CSV loading and error handling.
- Missing and duplicate values.
- Invalid marks.
- Python collections.
- Filtering and sorting.
- Grouping and frequency percentages.
- NumPy operations.
- Grade boundary conditions.
- Empty DataFrame handling.
- Full project integration.

**Test Results:**
- Total Test Cases: 20
- Passed: 20
- Failed: 0

## 10. Conclusion

The Student Business Data Processing System demonstrates how Python, NumPy and Pandas can be used to load, clean, process and analyse student and business datasets efficiently.

The project provides practical experience in data cleaning, numerical analysis, data manipulation, grouping, reporting and Python programming.
