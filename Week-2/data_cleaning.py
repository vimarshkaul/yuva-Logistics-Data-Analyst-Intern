import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler

# 1. Simulate Raw Dataset with Defects
np.random.seed(7)
n = 5000
warehouses = ['North', 'Central', 'South']
categories = ['Electronics', 'apparel', 'Home Goods', 'GROCERY', 'Apparel']

df = pd.DataFrame({
    'order_id': range(1, n + 1),
    'warehouse': np.random.choice(warehouses, n),
    'order_date': pd.date_range('2026-01-01', periods=n, freq='30min'),
    'distance_km': np.random.gamma(5, 2, n).round(2),
    'quantity': np.random.randint(1, 12, n),
    'unit_price': np.round(np.random.uniform(5, 200, n), 2),
    'product_category': np.random.choice(categories, n),
})

df['transport_cost'] = (
    df['distance_km'] * np.random.uniform(1.2, 1.8, n)
).round(2)

# Inject delivery date missing values (~4%)
missing_idx = df.sample(frac=0.04, random_state=1).index
df.loc[missing_idx, 'actual_delivery_date'] = pd.NaT

# Inject duplicate records
df = pd.concat([df, df.sample(40, random_state=2)], ignore_index=True)

# Inject extreme cost outliers
outlier_idx = df.sample(15, random_state=3).index
df.loc[outlier_idx, 'transport_cost'] *= 12

print("--- Raw Data Summary ---")
print(f"Total raw rows: {len(df)}")
print(f"Missing delivery dates: {df['actual_delivery_date'].isna().sum()}")

# 2. Data Cleaning & Transformation
# Flag undelivered orders and median-impute distance
df['is_delivered'] = df['actual_delivery_date'].notna()
df['distance_km'] = df['distance_km'].fillna(df['distance_km'].median())

# Deduplicate on order_id
before_len = len(df)
df = df.drop_duplicates(subset='order_id', keep='first')
print(f"Removed {before_len - len(df)} duplicate order records")

# Outlier detection and Winsorization (IQR method)
q1, q3 = df['transport_cost'].quantile([0.25, 0.75])
iqr = q3 - q1
lower, upper = q1 - 1.5 * iqr, q3 + 1.5 * iqr

df['cost_is_outlier'] = ~df['transport_cost'].between(lower, upper)
print(f"Flagged {df['cost_is_outlier'].sum()} cost outliers")

# Cap extreme values at IQR boundaries
df['transport_cost_clean'] = df['transport_cost'].clip(lower, upper)

# Standardize categorical text casing
df['product_category'] = df['product_category'].str.strip().str.title()
print("\n--- Standardized Categories ---")
print(df['product_category'].value_counts())


# 3. Feature Scaling & Normalization
scaler = MinMaxScaler()
df[['distance_km_norm', 'transport_cost_norm']] = scaler.fit_transform(
    df[['distance_km', 'transport_cost_clean']]
)

print("\n--- Cleaned Data Preview ---")
print(
    df[
        [
            'order_id',
            'warehouse',
            'product_category',
            'distance_km_norm',
            'transport_cost_norm',
            'is_delivered',
        ]
    ].head()
)
