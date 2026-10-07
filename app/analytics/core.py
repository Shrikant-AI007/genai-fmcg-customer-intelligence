from pathlib import Path
import pandas as pd
import numpy as np

REQUIRED = ["transaction_id", "customer_id", "product_id", "date", "quantity", "unit_price", "discount_pct", "store_id", "region", "channel"]


def load_data(data_dir="data"):
    path = Path(data_dir) / "transactions.csv"
    df = pd.read_csv(path, parse_dates=["date"])
    missing = [c for c in REQUIRED if c not in df.columns]
    if missing:
        raise ValueError(f"Missing columns: {missing}")
    df["gross_sales"] = df["quantity"] * df["unit_price"]
    df["net_sales"] = df["gross_sales"] * (1 - df["discount_pct"] / 100)
    return df


def sales_summary(df, region=None, category=None):
    x = df.copy()
    if region and region != "All": x = x[x.region == region]
    if category and category != "All": x = x[x.category == category]
    return {
        "revenue": float(x.net_sales.sum()),
        "units": int(x.quantity.sum()),
        "orders": int(x.transaction_id.nunique()),
        "avg_order_value": float(x.groupby("transaction_id").net_sales.sum().mean()) if len(x) else 0,
        "top_product": x.groupby("product_name").net_sales.sum().idxmax() if len(x) else None,
    }


def monthly_trend(df):
    x = df.copy()
    x["month"] = x.date.dt.to_period("M").astype(str)
    return x.groupby("month", as_index=False).agg(revenue=("net_sales", "sum"), units=("quantity", "sum"))


def customer_rfm(df):
    ref = df.date.max() + pd.Timedelta(days=1)
    g = df.groupby("customer_id")
    rfm = g.agg(last_purchase=("date", "max"), frequency=("transaction_id", "nunique"), monetary=("net_sales", "sum")).reset_index()
    rfm["recency"] = (ref - rfm.last_purchase).dt.days
    # rank-based scores: 1-5, higher is better for frequency/monetary, inverse for recency
    rfm["R"] = pd.qcut(rfm.recency.rank(method="first"), 5, labels=[5,4,3,2,1]).astype(int)
    rfm["F"] = pd.qcut(rfm.frequency.rank(method="first"), 5, labels=[1,2,3,4,5]).astype(int)
    rfm["M"] = pd.qcut(rfm.monetary.rank(method="first"), 5, labels=[1,2,3,4,5]).astype(int)
    rfm["segment"] = np.select(
        [rfm.R.ge(4) & rfm.F.ge(4) & rfm.M.ge(4), rfm.R.ge(4) & rfm.F.ge(3), rfm.R.le(2) & rfm.M.ge(4)],
        ["Champions", "Loyal / Active", "High Value At Risk"], default="Growth / Nurture"
    )
    return rfm


def product_performance(df):
    return df.groupby(["category", "product_name"], as_index=False).agg(revenue=("net_sales", "sum"), units=("quantity", "sum"), orders=("transaction_id", "nunique")).sort_values("revenue", ascending=False)


def promotion_lift(df):
    x = df.copy()
    x["promoted"] = x.discount_pct > 0
    out = x.groupby("promoted").agg(revenue=("net_sales", "sum"), units=("quantity", "sum"), orders=("transaction_id", "nunique")).reset_index()
    return out


def inventory_risk(data_dir="data"):
    inv = pd.read_csv(Path(data_dir) / "inventory.csv")
    inv["daily_velocity"] = inv["units_sold_7d"] / 7
    inv["days_of_cover"] = np.where(inv.daily_velocity > 0, inv.stock_on_hand / inv.daily_velocity, 999)
    inv["risk"] = np.select([inv.days_of_cover < 3, inv.days_of_cover < 7], ["HIGH", "MEDIUM"], default="LOW")
    return inv.sort_values("days_of_cover")


def product_affinity(df, product_name, top_n=5):
    orders = df.groupby("transaction_id")["product_name"].apply(set)
    base = {p for s in orders for p in s if p == product_name}
    counts = {}
    base_orders = sum(product_name in s for s in orders)
    for s in orders:
        if product_name in s:
            for p in s:
                if p != product_name: counts[p] = counts.get(p, 0) + 1
    rows = [{"product": p, "co_purchase_orders": c, "affinity_rate": c / base_orders if base_orders else 0} for p,c in counts.items()]
    return pd.DataFrame(rows).sort_values("affinity_rate", ascending=False).head(top_n) if rows else pd.DataFrame(columns=["product","co_purchase_orders","affinity_rate"])
