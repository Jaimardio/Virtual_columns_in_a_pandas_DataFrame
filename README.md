# 📊 Sales Data Pipeline & Virtual Column Generator

> **Author:** [Jakub Imiński (Jaimardio)](https://github.com/Jaimardio)

---
## 🛠️ Project Structure & Components

The repository is organized into core modular components corresponding to the task requirements:
* **`solution.py` (Part 1):** Contains the core `add_virtual_column` function.
It dynamically evaluates mathematical expressions (addition, subtraction, multiplication) on pandas DataFrames,
validates strict column naming rules (letters and underscores only),
and safely returns an empty DataFrame if validation fails.
* **`pipeline.py` (Part 2):** Implements the end-to-end ETL data pipeline. It reads raw sales data, cleans and imputes missing values,
sequentially invokes `add_virtual_column` to calculate item revenues, and aggregates the results into `revenue_by_region.csv`.
* **`test_custom.py` & `test_virtual_column.py` (Part 3):** Comprehensive test suites validating both the virtual column utility function and the pipeline's data cleaning logic.

---
## 🚀 1. Setup, Pipeline & Test Execution

This section covers how to set up the environment and execute the project components.

### Prerequisites
* Python 3.8+
* `pandas` and `pytest` libraries

### Installation & Setup
Clone the repository and install all required project dependencies using the configuration file:

```bash
git clone https://github.com/Jaimardio/Virtual_columns_in_a_pandas_DataFrame.git

cd Virtual_columns_in_a_pandas_DataFrame

pip install -r requirements.txt
```

Running the Pipeline
To execute the data cleaning pipeline, compute revenues using the custom virtual column function,
and generate the final regional report (revenue_by_region.csv): 
```bash
python pipeline.py
```

Running the Tests
To execute all test suites (including instructor-provided tests and custom verification scripts)
with a single command:
```bash
python -m pytest
```

🧠 2. Assumptions & Design Decisions
Where the task guidelines left decisions open or ambiguous,
the following architectural and business choices were made:

Two-Step Virtual Column Chaining: Because the required add_virtual_column function
is designed to handle a single binary operation at a time (col1 op col2),
I made the architectural decision to invoke it sequentially in the pipeline:

First, computing Subtotal = Quantity * Unit_Price

Second, computing Revenue = Subtotal - Discount

Zero Discount Assumption: Blank or missing discount fields were assumed to represent $0 discounts,
ensuring that every valid order line contributes accurately to revenue calculations without dropping records.

Product-Level Price Imputation: Assumed that missing unit prices within the same product category
share a uniform baseline price, allowing safe data recovery without introducing external pricing bias.

🧹 3. Data Quality Problems Found in sales.csv & Handling
During exploratory data inspection of sales.csv, several anomalies and data quality issues were identified,
along with the exact impact on dataset rows and their resolutions:

Header Anomaly (Ghost Row)

Problem: Exactly 1 row contained an artifact where the Region column value literally duplicated the header name ("Region").

Rows affected: 1 row.

Handling: Explicitly filtered out and dropped this specific artifact row using df = df[df["Region"] != "Region"].

Missing Unit Prices

Problem: Several order lines lacked pricing data entirely.

Rows affected: A minor subset of rows across the dataset.

Handling: Rather than dropping valuable sales data, missing prices were imputed by calculating the mean Unit Price
grouped specifically by the product category (df.groupby("Product")["Unit Price"].transform("mean")).

Malformed & Missing Numeric Values (Quantity, Unit Price, Discount)

Problem: Numeric columns contained trailing spaces, non-numeric strings, or null entries.

Rows affected: A small percentage of total rows.

Handling: Forced conversion using errors='coerce'. Missing Discount values were filled with 0.
Unsalvageable rows missing critical quantities were dropped.

Hidden Whitespace in Column Headers

Problem: Raw headers contained invisible trailing spaces (e.g., 'Quantity ', 'Unit Price '), causing lookup failures.

Rows affected: All columns in the header row.

Handling: Stripped whitespace across all column names (.str.strip()) at the ingestion stage.

Inconsistent Text Formatting (Region & Product)

Problem: Mixed casing and leading/trailing spaces across text fields.

Rows affected: Multiple rows containing untrimmed categorical strings.

Handling: Standardized all categorical text fields using .str.strip() and .str.title() to ensure accurate
aggregation by region.
