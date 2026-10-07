# Exploratory Analysis

Use `scripts_generate_data.py` to generate data, then explore:

```python
import pandas as pd
from app.analytics.core import load_data, customer_rfm, product_performance

df = load_data()
print(df.describe(include="all"))
print(customer_rfm(df).head())
print(product_performance(df).head(10))
```
