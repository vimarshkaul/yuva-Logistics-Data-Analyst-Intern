import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.linear_model import LinearRegression
from sklearn.metrics import root_mean_squared_error
from sklearn.model_selection import train_test_split

# Stage 1: Data Simulation & Collection
np.random.seed(42)
n = 5000
warehouses = ['North', 'Central', 'South']

orders = pd.DataFrame({
    'order_id': range(1, n + 1),
    'warehouse': np.random.choice(warehouses, n),
    'order_date': pd.date_range('2026-01-01', periods=n, freq='30min'),
    'distance_km': np.random.gamma(5, 2, n),
    'promised_hours': np.random.choice([24, 48, 72], n),
})

# Generate transport cost based on distance
orders['transport_cost'] = orders['distance_km'] * np.random.uniform(
    1.2, 1.8, n
)

# Inspect raw dataset
print("--- Raw Dataset Info ---")
print(orders.head())
print(orders.info())


# Stage 2: Data Cleaning & Preprocessing
# Median imputation for missing distance values
orders['distance_km'] = orders['distance_km'].fillna(
    orders['distance_km'].median()
)

# Deduplicate records by order ID
orders = orders.drop_duplicates(subset='order_id')

# Outlier detection using Interquartile Range (IQR)
q1, q3 = orders['transport_cost'].quantile([0.25, 0.75])
iqr = q3 - q1
orders['cost_outlier'] = orders['transport_cost'] > (q3 + 1.5 * iqr)


# Stage 3: Exploratory Analysis & Clustering
# Descriptive KPI summary per warehouse
summary = orders.groupby('warehouse')['transport_cost'].agg(
    ['mean', 'median', 'std']
)
print("\n--- Transport Cost Summary by Warehouse ---")
print(summary)

# Zone clustering via K-Means
features = orders[['distance_km', 'transport_cost']]
kmeans = KMeans(n_clusters=3, random_state=42, n_init=10)
orders['zone_cluster'] = kmeans.fit_predict(features)

# Stage 4: Predictive Modeling
X = orders[['distance_km', 'promised_hours']]
y = orders['transport_cost']

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Train baseline linear regression model
model = LinearRegression().fit(X_train, y_train)
preds = model.predict(X_test)

# Model evaluation
rmse = root_mean_squared_error(y_test, preds)
print(f"\n--- Baseline Model Evaluation ---\nRMSE: {rmse:.2f}")
