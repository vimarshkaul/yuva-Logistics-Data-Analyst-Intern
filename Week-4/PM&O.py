import numpy as np
import pandas as pd
from scipy.optimize import linprog
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, r2_score, root_mean_squared_error
from sklearn.model_selection import GridSearchCV, cross_val_score, train_test_split
from sklearn.tree import DecisionTreeRegressor

# 1. Load Dataset & Feature Engineering
df = pd.read_csv('cleaned_week2_logistics_dataset.csv')
df['order_date'] = pd.to_datetime(df['order_date'])
df['actual_delivery_date'] = pd.to_datetime(df['actual_delivery_date'])

# Derive operational metrics
df['delivery_time_hours'] = (
    df['actual_delivery_date'] - df['order_date']
).dt.total_seconds() / 3600
df['day_of_week'] = df['order_date'].dt.day_name()

np.random.seed(42)
if 'promised_hours' not in df.columns:
  df['promised_hours'] = np.random.choice([24, 48, 72], len(df))

# Filter out unfulfilled orders for model training
df_model = df.dropna(subset=['delivery_time_hours']).copy()


# 2. One-Hot Encoding & Train-Test Split
features = [
    'distance_km',
    'quantity',
    'day_of_week',
    'warehouse',
    'product_category',
]
X = pd.get_dummies(
    df_model[features],
    columns=['warehouse', 'product_category', 'day_of_week'],
    drop_first=True,
)
y = df_model['delivery_time_hours']

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)


# 3. Model Training & Evaluation
models = {
    'Linear Regression': LinearRegression(),
    'Decision Tree': DecisionTreeRegressor(max_depth=6, random_state=42),
    'Random Forest': RandomForestRegressor(
        n_estimators=200, max_depth=8, random_state=42
    ),
}

results = {}
for name, model in models.items():
  model.fit(X_train, y_train)
  preds = model.predict(X_test)
  results[name] = {
      'RMSE': root_mean_squared_error(y_test, preds),
      'MAE': mean_absolute_error(y_test, preds),
      'R2': r2_score(y_test, preds),
  }

print('--- Model Evaluation Comparison ---')
print(pd.DataFrame(results).T)


# 4. Cross-Validation, Tuning & Feature Importance
cv_scores = cross_val_score(
    RandomForestRegressor(random_state=42),
    X,
    y,
    cv=5,
    scoring='neg_root_mean_squared_error',
)
print(
    f'\nCross-validated RMSE: {-cv_scores.mean():.2f} (+/-'
    f' {cv_scores.std():.2f})'
)

param_grid = {'n_estimators': [100, 200], 'max_depth': [4, 6, 8]}
grid = GridSearchCV(
    RandomForestRegressor(random_state=42),
    param_grid,
    cv=5,
    scoring='neg_root_mean_squared_error',
    n_jobs=-1,
)
grid.fit(X_train, y_train)
print('Best Parameters:', grid.best_params_)
best_model = grid.best_estimator_

importances = pd.Series(
    best_model.feature_importances_, index=X.columns
).sort_values(ascending=False)
print('\n--- Top 10 Feature Importances ---')
print(importances.head(10))


# 5. Prescriptive Optimization
# 5.1 Fleet Resource Allocation (Linear Programming)
efficiency_gain = [0.8, 0.5, 1.1]
c = [-g for g in efficiency_gain]
A_eq = [[1, 1, 1]]
b_eq = [30]
bounds = [(5, 15), (5, 15), (5, 15)]

result = linprog(c, A_eq=A_eq, b_eq=b_eq, bounds=bounds, method='highs')
print(
    '\nOptimal Vehicle Allocation (North, Central, South):',
    result.x.round(1),
)

# 5.2 Priority Routing Queue for At-Risk Deliveries
df_model['predicted_delivery_hours'] = best_model.predict(X)
df_model['at_risk'] = (
    df_model['predicted_delivery_hours'] > df_model['promised_hours']
)

priority_queue = df_model[df_model['at_risk']].sort_values(
    'predicted_delivery_hours', ascending=False
)
standard_queue = df_model[~df_model['at_risk']]
print(f'Orders flagged for priority dispatch: {len(priority_queue)}')
