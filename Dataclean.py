import numpy as np
import pandas as pd

# Load the messy CSV dataset
df = pd.read_csv('ecommerce_sales_messy.csv')
print(df.head(10))

# 1. Remove duplicate Order IDs
df = df.drop_duplicates(subset=['Order_ID'], keep='first')

# 2. Parse and standardize Order_Date into datetime (YYYY-MM-DD)
df['Order_Date'] = pd.to_datetime(
    df['Order_Date'], format='mixed', errors='coerce'
)

# 3. Clean text columns (strip whitespace & standardize casing)
df['Customer_ID'] = df['Customer_ID'].astype(str).str.strip().str.upper()
df['Customer_ID'] = df['Customer_ID'].replace(
    {'NAN': 'UNKNOWN', 'NONE': 'UNKNOWN', '': 'UNKNOWN'}
)

df['Product'] = df['Product'].astype(str).str.strip().str.title()
df['Product'] = df['Product'].replace({'Usb-C Hub': 'USB-C Hub'})

df['Category'] = df['Category'].astype(str).str.strip().str.title()
category_map = {
    'Electronics': 'Electronics',
    'Books': 'Books',
    'Beauty': 'Beauty',
    'Fashion': 'Fashion',
    'Home & Kitchen': 'Home & Kitchen',
}
df['Category'] = df['Category'].map(category_map).fillna('Unknown')

df['Payment_Method'] = df['Payment_Method'].astype(str).str.strip().str.title()
payment_map = {
    'Upi': 'UPI',
    'Credit Card': 'Credit Card',
    'Credit Crad': 'Credit Card',
    'Debit Card': 'Debit Card',
    'Net Banking': 'Net Banking',
    'Cash On Delivery': 'Cash on Delivery',
}
df['Payment_Method'] = df['Payment_Method'].map(payment_map).fillna('Unknown')

df['City'] = df['City'].astype(str).str.strip().str.title()
city_map = {
    'Newdelhi': 'New Delhi',
    'New Delhi': 'New Delhi',
    'Mum Bai': 'Mumbai',
}
df['City'] = df['City'].replace(city_map)

df['Region'] = df['Region'].astype(str).str.strip().str.title()
region_map = {
    'North': 'North',
    'South': 'South',
    'East': 'East',
    'West': 'West',
    'Central': 'Central',
}
df['Region'] = df['Region'].map(region_map).fillna('Unknown')

df['Order_Status'] = df['Order_Status'].astype(str).str.strip().str.title()
status_map = {
    'Delivered': 'Delivered',
    'Deliverd': 'Delivered',
    'Cancelled': 'Cancelled',
    'Returned': 'Returned',
}
df['Order_Status'] = df['Order_Status'].map(status_map).fillna('Unknown')

# 4. Clean currency & numeric columns (strip ₹ / â‚¹, commas, handle NaNs)
num_cols = [
    'Quantity',
    'Unit_Price_INR',
    'Discount_Percent',
    'Discount_Amount_INR',
    'Net_Sales_INR',
    'Cost_INR',
    'Profit_INR',
]

for col in num_cols:
  df[col] = (
      df[col]
      .astype(str)
      .str.replace('â‚¹', '', regex=False)
      .str.replace('₹', '', regex=False)
      .str.replace(',', '', regex=False)
      .str.strip()
      .replace({'nan': np.nan, 'None': np.nan, '': np.nan})
  )
  df[col] = pd.to_numeric(df[col], errors='coerce')

# 5. Clean Quantity (fix negative values & impute missing with median)
df['Quantity'] = df['Quantity'].abs()
median_qty = df['Quantity'].median()
df['Quantity'] = df['Quantity'].fillna(median_qty).astype(int)

# 6. Clean Discount_Percent (keep between 0 and 100, impute missing with median)
df.loc[
    (df['Discount_Percent'] < 0) | (df['Discount_Percent'] > 100),
    'Discount_Percent',
] = np.nan
median_disc = df['Discount_Percent'].median()
df['Discount_Percent'] = df['Discount_Percent'].fillna(median_disc)

# 7. Impute missing numeric INR values with median
for col in [
    'Unit_Price_INR',
    'Discount_Amount_INR',
    'Net_Sales_INR',
    'Cost_INR',
    'Profit_INR',
]:
  df[col] = df[col].fillna(df[col].median())

# Export cleaned dataset
df.to_csv('cleaned_ecommerce_sales_2.csv', index=False)