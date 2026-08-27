# Week 2 Data Collection, Cleaning, and Preprocessing

---

## Simulated Dataset Overview

The Week 2 dataset simulates 90 days (Q1 2026) of operations across DataCo's three USCA regional warehouses: North, Central, and South. The simulated batch consists of 5,000 order records generated to reflect realistic operational conditions and common supply-chain data defects.

## Variables of Interest

The dataset records key operational and transactional variables:

* **order_id**: Unique identifier for each order transaction
* **warehouse**: Fulfillment hub location (`North`, `Central`, `South`)
* **order_date**: Order placement timestamp at 30-minute intervals
* **actual_delivery_date**: Delivery completion timestamp
* **distance_km**: Delivery transit distance in kilometers (gamma-distributed)
* **transport_cost**: Cost per delivery run
* **quantity**: Number of units purchased per order
* **unit_price**: Unit price of ordered items
* **product_category**: Categorical item type (e.g., Electronics, Apparel, Grocery, Home Goods)

## Injected Data Defects & Cleaning Protocol

The raw data simulates four prototypical supply chain data quality issues:

* **Missing Delivery Dates (~4%)**: Flagged using a boolean indicator (`is_delivered`) rather than placeholder timestamps to avoid corrupting On-Time Delivery KPIs.
* **Missing Distance Values**: Imputed using the median to handle right-skewed distributions.
* **Duplicate Entries**: Exactly deduplicated on `order_id`.
* **Extreme Transport Cost Outliers**: Identified via Interquartile Range (IQR) and capped (winsorized) at boundary thresholds.
* **Inconsistent Text Labels**: Standardized to title case to eliminate fragmented category labels.
* **Feature Normalization**: Min-Max scaling applied to `distance_km` and `transport_cost_clean` to bound values into $[0, 1]$ for downstream clustering and regression.
