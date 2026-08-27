# Week 1 Data Source

---

## Proposed Dataset

The Week 1 analysis proposes using a publicly available logistics and supply-chain dataset based on the DataCo Smart Supply Chain dataset[cite: 1], containing over 180,000 order records across multi-regional warehouse operations (North, Central, and South regions)[cite: 1].

## Variables of Interest

The proposed analysis will examine variables such as[cite: 1]:

* Order ID and Product Category[cite: 1]
* Warehouse Location (North, Central, South)[cite: 1]
* Order Date and Promised vs. Actual Delivery Timestamps[cite: 1]
* Distance (km)[cite: 1]
* Transportation Cost per Delivery[cite: 1]
* Order Quantity and Unit Price[cite: 1]
* Lead Time / Fulfilment Cycle Time[cite: 1]
* Inventory and Stockout Indicators[cite: 1]

## Purpose

The dataset will be used to analyze inventory balance, optimize last-mile routing, and build baseline predictive regression models for delivery times and transportation costs[cite: 1].

## Important Note

The dataset will undergo data cleaning—including median imputation for missing values, IQR-based outlier detection, and deduplication—before exploratory clustering and predictive modeling are performed[cite: 1].
