# Week 3 Advanced Data Analysis and Visualization in Logistics

---

## Dataset & Derived Variables

This analysis builds upon the cleaned Week 2 logistics dataset covering 90 days (Q1 2026) across DataCo's North, Central, and South regional warehouses. Two additional analytical variables were derived:

* **`delivery_time_hours`**: Calculated transit duration in hours ($(\text{actual\_delivery\_date} - \text{order\_date}) / 3600$).
* **`shipment_volume`**: Daily aggregated order volume per warehouse.

---

## Exploratory Data Analysis & Visualizations

| Figure | Output File | Description & Performance Metric Mapping |
| :--- | :--- | :--- |
| **Figure 1** | `delivery_time_distribution.png` | Histogram with KDE overlay showing right-skewed delivery times and extended delay risks. |
| **Figure 2** | `correlation_heatmap.png` | Correlation matrix identifying transit distance as the primary driver of delivery time and transport cost ($r = 0.94$). |
| **Figure 3** | `delivery_time_by_warehouse.png` | Boxplot comparing transit spreads, showing higher median delivery time and wider IQR at the South hub. |
| **Figure 4** | `daily_volume_trend.png` | Multi-line time series displaying weekend volume peaks and promotional demand spikes at the Central warehouse. |
| **Figure 5** | `cost_by_category.png` | Horizontal bar chart ranking categories by mean cost, highlighting Home Goods and Electronics as leading cost drivers. |
| **Figure 6** | `distance_vs_cost.png` | Scatter plot evaluating the linear distance-cost relationship across regional hubs. |

---

## Key Strategic Insights

* **Operational Bottlenecks**: The South warehouse exhibits higher transit times and cost-to-distance ratios, requiring route optimization and fleet capacity reviews.
* **Cost Drivers**: Distance is the primary determinant of transport cost, with product categories (Home Goods and Electronics) acting as secondary drivers.
* **Capacity Planning**: Weekly weekend spikes and promotional surges at the Central warehouse indicate that dynamic fleet and labor allocation is required to prevent dispatch backlogs.
