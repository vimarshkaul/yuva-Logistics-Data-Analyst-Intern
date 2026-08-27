# Week 1 Data Source

---

## Proposed Dataset

The Week 1 analysis proposes using a publicly available logistics and supply-chain dataset based on the DataCo Smart Supply Chain dataset, containing over 180,000 order records across multi-regional warehouse operations (North, Central, and South regions).

## Variables of Interest

The proposed analysis will examine variables such as:

* Order ID and Product Category
* Warehouse Location (North, Central, South)
* Order Date and Promised vs. Actual Delivery Timestamps
* Distance (km)
* Transportation Cost per Delivery
* Order Quantity and Unit Price
* Lead Time / Fulfilment Cycle Time
* Inventory and Stockout Indicators

## Purpose

The dataset will be used to analyze inventory balance, optimize last-mile routing, and build baseline predictive regression models for delivery times and transportation costs.

## Important Note

The dataset will undergo data cleaning—including median imputation for missing values, IQR-based outlier detection, and deduplication—before exploratory clustering and predictive modeling are performed.
