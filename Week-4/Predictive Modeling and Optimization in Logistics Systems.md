# Week 4 Predictive Modeling and Optimization in Logistics Systems

---

## Predictive Modeling Pipeline

This final module establishes a machine learning and prescriptive optimization framework for DataCo’s North American (USCA) network across the North, Central, and South warehouses. The target is forecasting `delivery_time_hours` at order placement to anticipate fulfillment bottlenecks and proactively rebalance operational resources.

### Target & Feature Schema

* **Target Variable**: `delivery_time_hours` (actual delivery timestamp minus order timestamp)
* **Predictor Features**: `distance_km`, `quantity`, `day_of_week`, `warehouse` (one-hot encoded), `product_category` (one-hot encoded)

---

## Model Selection & Performance Comparison

Three model architectures were trained on an 80/20 train-test split and evaluated across RMSE, MAE, and R²:

* **Linear Regression**: Baseline model quantifying the marginal effects of distance and features.
* **Decision Tree Regressor**: Captures non-linear thresholds and step-change delays.
* **Random Forest Regressor**: Tuned ensemble model mitigating single-tree variance and capturing multi-feature interactions.

5-fold cross-validation and hyperparameter grid search (`GridSearchCV`) were conducted on the Random Forest regressor to optimize tree depth and estimator count.

---

## Feature Importance Highlights

* **Primary Predictor**: `distance_km` accounts for the majority of predictive importance, confirming transit mileage as the leading driver of delivery duration.
* **Secondary Drivers**: `quantity`, `warehouse_South` indicator (highlighting the regional bottleneck), and `day_of_week` (capturing weekend demand surges).

---

## Prescriptive Optimization Strategies

* **Fleet Resource Allocation**: Utilized linear programming (`scipy.optimize.linprog`) to reallocate 30 available fleet vehicles based on warehouse efficiency gains, shifting maximum capacity (15 vehicles) to the bottlenecked South hub.
* **Priority Routing Queue**: Filtered at-risk orders (`predicted_delivery_hours > promised_hours`) into an expedited dispatch queue to prevent SLA breaches.
* **Cost Consolidation**: Identified high-cost, low-urgency categories (Home Goods and Electronics) for multi-stop route batching.
