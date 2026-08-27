import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

# Visual formatting setup
sns.set_theme(style='whitegrid')
plt.rcParams.update({'font.sans-serif': 'DejaVu Sans', 'font.size': 11})

# Load cleaned Week 2 dataset
df = pd.read_csv('cleaned_week2_logistics_dataset.csv')
df['order_date'] = pd.to_datetime(df['order_date'])
df['actual_delivery_date'] = pd.to_datetime(df['actual_delivery_date'])

# Derive operational metrics
df['delivery_time_hours'] = (
    df['actual_delivery_date'] - df['order_date']
).dt.total_seconds() / 3600

daily_volume = (
    df[df['is_delivered']]
    .groupby([df['order_date'].dt.date.rename('order_date'), 'warehouse'])
    .size()
    .reset_index(name='shipment_volume')
)

# Figure 1: Delivery Time Distribution
fig, ax = plt.subplots(figsize=(8, 5))
sns.histplot(
    df['delivery_time_hours'].dropna(),
    bins=40,
    kde=True,
    ax=ax,
    color='#1f77b4',
)
ax.set_title(
    'Distribution of Delivery Time (hours)',
    fontsize=14,
    fontweight='bold',
    pad=12,
)
ax.set_xlabel('Delivery Time (hours)', fontsize=12)
ax.set_ylabel('Count', fontsize=12)
plt.savefig('delivery_time_distribution.png', dpi=150, bbox_inches='tight')
plt.close()

# Figure 2: Correlation Matrix Heatmap
corr = df[
    [
        'delivery_time_hours',
        'distance_km',
        'transport_cost_clean',
        'quantity',
    ]
].corr()
fig, ax = plt.subplots(figsize=(6, 5))
sns.heatmap(
    corr,
    annot=True,
    cmap='coolwarm',
    center=0,
    fmt='.2f',
    ax=ax,
    cbar_kws={'label': 'Correlation'},
)
ax.set_title(
    'Correlation Matrix: Logistics Variables',
    fontsize=13,
    fontweight='bold',
    pad=12,
)
plt.savefig('correlation_heatmap.png', dpi=150, bbox_inches='tight')
plt.close()

# Figure 3: Delivery Time Spread by Warehouse (Boxplot)
fig, ax = plt.subplots(figsize=(8, 5))
sns.boxplot(
    data=df.dropna(subset=['delivery_time_hours']),
    x='warehouse',
    y='delivery_time_hours',
    palette='Blues',
    ax=ax,
)
ax.set_title(
    'Delivery Time Spread by Warehouse', fontsize=14, fontweight='bold', pad=12
)
ax.set_xlabel('Warehouse', fontsize=12)
ax.set_ylabel('Delivery Time (hours)', fontsize=12)
plt.savefig('delivery_time_by_warehouse.png', dpi=150, bbox_inches='tight')
plt.close()

# Figure 4: Daily Shipment Volume Trend (Line Chart)
fig, ax = plt.subplots(figsize=(10, 5))
for wh in ['North', 'Central', 'South']:
  subset = daily_volume[daily_volume['warehouse'] == wh]
  ax.plot(
      pd.to_datetime(subset['order_date']),
      subset['shipment_volume'],
      label=wh,
      linewidth=1.8,
  )
ax.set_title(
    'Daily Shipment Volume by Warehouse', fontsize=14, fontweight='bold', pad=12
)
ax.set_xlabel('Date', fontsize=12)
ax.set_ylabel('Shipment Volume', fontsize=12)
ax.legend(title='Warehouse')
plt.savefig('daily_volume_trend.png', dpi=150, bbox_inches='tight')
plt.close()

# Figure 5: Cost Drivers by Product Category (Horizontal Bar Chart)
cat_cost = (
    df.groupby('product_category')['transport_cost_clean'].mean().sort_values()
)
fig, ax = plt.subplots(figsize=(8, 5))
cat_cost.plot(
    kind='barh', ax=ax, color='#C55A11', edgecolor='black', linewidth=0.5
)
ax.set_title(
    'Average Transport Cost by Product Category',
    fontsize=14,
    fontweight='bold',
    pad=12,
)
ax.set_xlabel('Average Transport Cost ($)', fontsize=12)
ax.set_ylabel('Product Category', fontsize=12)
plt.savefig('cost_by_category.png', dpi=150, bbox_inches='tight')
plt.close()

# Figure 6: Distance vs. Cost Relationship (Scatter Plot)
fig, ax = plt.subplots(figsize=(8, 5))
sns.scatterplot(
    data=df,
    x='distance_km',
    y='transport_cost_clean',
    hue='warehouse',
    alpha=0.5,
    palette='tab10',
    ax=ax,
)
ax.set_title('Transport Cost vs. Distance', fontsize=14, fontweight='bold', pad=12)
ax.set_xlabel('Distance (km)', fontsize=12)
ax.set_ylabel('Cleaned Transport Cost ($)', fontsize=12)
plt.savefig('distance_vs_cost.png', dpi=150, bbox_inches='tight')
plt.close()
