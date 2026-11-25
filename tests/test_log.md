# Test Log – Student Business Data Processing System

## 1. Testing Objective

To verify that all project modules work correctly with valid, missing, duplicate, invalid, and empty data.

## 2. Test Environment

- Language: Python
- Libraries: Pandas, NumPy
- IDE: PyCharm
- Operating System: Windows

## 3. Test Cases

| Test ID | Module | Test Description | Expected Result | Actual Result | Status |
|---|---|---|---|---|---|
| TC-01 | Data Loading | Load valid CSV file | DataFrame loaded and shape displayed | CSV loaded successfully | PASS |
| TC-02 | Data Loading | Load non-existing file | File not found message without crash | Error handled successfully | PASS |
| TC-03 | Data Loading | Load empty CSV file | File is empty message | File is empty message displayed | PASS |
| TC-04 | Data Cleaning | Remove 2 duplicate rows from 20 rows | 18 rows remain | 20 rows reduced to 18 | PASS |
| TC-05 | Data Cleaning | Fill missing marks using median | Missing values filled with median | Both missing values filled with 70 | PASS |
| TC-06 | Data Cleaning | Handle invalid mark 105 | Invalid mark treated as missing | 105 replaced with mean 76.67 | PASS |
| TC-07 | Collections | Identify unique departments | Set contains unique values | Unique departments generated | PASS |
| TC-08 | Collections | Count department frequency | Correct frequency dictionary | Department counts generated | PASS |
| TC-09 | Pandas | Filter students with maths > 80 | Only matching students displayed | Matching students displayed | PASS |
| TC-10 | Pandas | Filter with no matching records | No matching records message | No matching records displayed | PASS |
| TC-11 | Pandas | Sort total marks descending | Highest total appears first | Records sorted correctly | PASS |
| TC-12 | Pandas | Sort by department and total marks | Correct order within departments | Multi-column sorting successful | PASS |
| TC-13 | Pandas | Group students by department | Counts add up to total records | Department counts total 14 | PASS |
| TC-14 | Pandas | Calculate frequency percentages | Percentages sum to 100% | Percentage total verified | PASS |
| TC-15 | NumPy | Calculate row sums and column means | Expected array results | Row sums and means verified | PASS |
| TC-16 | NumPy | Apply Boolean mask for marks below 35 | Only failing marks returned | Boolean mask verified | PASS |
| TC-17 | NumPy | Apply clipping to marks + 5 | No value exceeds 100 | Values clipped to 100 | PASS |
| TC-18 | Pandas | Test grade boundaries | 90 = A+, 35 = E, 34 = F | All three grades correct | PASS |
| TC-19 | Reports | Test empty DataFrame | No data available message | Message displayed correctly | PASS |
| TC-20 | Integration | Execute main.py | All three reports generated without errors | All reports generated successfully | PASS |

## 4. Test Summary

- Total Test Cases: 20
- Passed: 20
- Failed: 0

## 5. Generated Reports

The following reports were generated successfully:

1. `student_report.csv`
2. `sales_report.csv`
3. `data_quality_report.csv`

## 6. Final Result

The Student Business Data Processing System was tested using valid, missing, duplicate, invalid, and empty data.

The individual module tests and full project execution completed successfully. All 20 listed test cases produced the expected results.

**Final Status: PASS**
