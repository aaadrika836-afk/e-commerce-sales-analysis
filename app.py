import pandas as pd
import numpy as np

FILE_NAME = "ecommerce_sales_100_records.csv"


# -----------------------------
# LOAD DATA
# -----------------------------
def load_data():
    try:
        df = pd.read_csv(FILE_NAME)
        print("\n✅ Dataset Loaded Successfully")
        return df
    except Exception as e:
        print(f"\n❌ Error Loading File: {e}")
        return None


# -----------------------------
# DATASET OVERVIEW
# -----------------------------
def dataset_overview(df):
    print("\n" + "=" * 50)
    print("DATASET OVERVIEW")
    print("=" * 50)

    print(f"Rows    : {df.shape[0]}")
    print(f"Columns : {df.shape[1]}")

    print("\nColumns:")
    print(df.columns.tolist())

    print("\nData Types:")
    print(df.dtypes)

    print("\nFirst 5 Records:")
    print(df.head())


# -----------------------------
# MISSING VALUES CHECK
# -----------------------------
def check_missing_values(df):
    print("\n" + "=" * 50)
    print("MISSING VALUES REPORT")
    print("=" * 50)

    missing = df.isnull().sum()
    print(missing)

    print(
        f"\nTotal Missing Values: {missing.sum()}"
    )


# -----------------------------
# DUPLICATE CHECK
# -----------------------------
def check_duplicates(df):
    print("\n" + "=" * 50)
    print("DUPLICATE REPORT")
    print("=" * 50)

    duplicate_rows = df.duplicated().sum()

    if "Order_ID" in df.columns:
        duplicate_order_ids = (
            df["Order_ID"].duplicated().sum()
        )
    else:
        duplicate_order_ids = 0

    print(f"Duplicate Rows      : {duplicate_rows}")
    print(f"Duplicate Order IDs : {duplicate_order_ids}")


# -----------------------------
# SALES ANALYSIS
# -----------------------------
def sales_analysis(df):

    print("\n" + "=" * 50)
    print("SALES ANALYSIS")
    print("=" * 50)

    sales = pd.to_numeric(
        df["Net_Sales_INR"],
        errors="coerce"
    )

    profit = pd.to_numeric(
        df["Profit_INR"],
        errors="coerce"
    )

    print(f"Total Sales  : ₹{sales.sum():,.2f}")
    print(f"Total Profit : ₹{profit.sum():,.2f}")

    if "Category" in df.columns:
        print("\nSales By Category:")
        result = (
            df.groupby("Category")["Net_Sales_INR"]
            .sum()
            .sort_values(ascending=False)
        )
        print(result)


# -----------------------------
# TOP PRODUCTS
# -----------------------------
def top_products(df):

    print("\n" + "=" * 50)
    print("TOP PRODUCTS")
    print("=" * 50)

    if "Product" not in df.columns:
        return

    result = (
        df.groupby("Product")["Net_Sales_INR"]
        .sum()
        .sort_values(ascending=False)
        .head(10)
    )

    print(result)


# -----------------------------
# CITY PERFORMANCE
# -----------------------------
def city_performance(df):

    print("\n" + "=" * 50)
    print("CITY PERFORMANCE")
    print("=" * 50)

    if "City" not in df.columns:
        return

    result = (
        df.groupby("City")["Net_Sales_INR"]
        .sum()
        .sort_values(ascending=False)
    )

    print(result)


# -----------------------------
# ORDER STATUS REPORT
# -----------------------------
def order_status_report(df):

    print("\n" + "=" * 50)
    print("ORDER STATUS REPORT")
    print("=" * 50)

    if "Order_Status" not in df.columns:
        return

    print(
        df["Order_Status"]
        .value_counts()
    )


# -----------------------------
# NUMERIC VALIDATION
# -----------------------------
def validation_report(df):

    print("\n" + "=" * 50)
    print("VALIDATION REPORT")
    print("=" * 50)

    issues = {}

    if "Quantity" in df.columns:
        invalid_qty = (
            pd.to_numeric(
                df["Quantity"],
                errors="coerce"
            ) <= 0
        ).sum()

        issues["Invalid Quantity"] = invalid_qty

    if "Discount_Percent" in df.columns:

        discount = pd.to_numeric(
            df["Discount_Percent"],
            errors="coerce"
        )

        invalid_discount = (
            (~discount.between(0, 100))
        ).sum()

        issues["Invalid Discount %"] = invalid_discount

    for k, v in issues.items():
        print(f"{k}: {v}")


# -----------------------------
# EXPORT SUMMARY
# -----------------------------
def export_report(df):

    sales = pd.to_numeric(
        df["Net_Sales_INR"],
        errors="coerce"
    ).sum()

    profit = pd.to_numeric(
        df["Profit_INR"],
        errors="coerce"
    ).sum()

    with open(
        "data_quality_report.txt",
        "w",
        encoding="utf-8"
    ) as f:

        f.write("E-COMMERCE SALES REPORT\n")
        f.write("=" * 40 + "\n")

        f.write(f"Rows: {df.shape[0]}\n")
        f.write(f"Columns: {df.shape[1]}\n")

        f.write(
            f"\nTotal Sales: ₹{sales:,.2f}\n"
        )
        f.write(
            f"Total Profit: ₹{profit:,.2f}\n"
        )

        f.write("\nMissing Values\n")
        f.write(
            str(df.isnull().sum())
        )

    print(
        "\n✅ Report exported as data_quality_report.txt"
    )


# -----------------------------
# MENU
# -----------------------------
def menu():

    df = load_data()

    if df is None:
        return

    while True:

        print("\n")
        print("=" * 50)
        print("E-COMMERCE SALES ANALYSIS SYSTEM")
        print("=" * 50)

        print("1. Dataset Overview")
        print("2. Missing Values Report")
        print("3. Duplicate Report")
        print("4. Sales Analysis")
        print("5. Top Products")
        print("6. City Performance")
        print("7. Order Status Report")
        print("8. Validation Report")
        print("9. Export Report")
        print("0. Exit")

        choice = input("\nEnter Choice: ")

        if choice == "1":
            dataset_overview(df)

        elif choice == "2":
            check_missing_values(df)

        elif choice == "3":
            check_duplicates(df)

        elif choice == "4":
            sales_analysis(df)

        elif choice == "5":
            top_products(df)

        elif choice == "6":
            city_performance(df)

        elif choice == "7":
            order_status_report(df)

        elif choice == "8":
            validation_report(df)

        elif choice == "9":
            export_report(df)

        elif choice == "0":
            print("\nThank You!")
            break

        else:
            print("\nInvalid Choice")


if __name__ == "__main__":
    menu()