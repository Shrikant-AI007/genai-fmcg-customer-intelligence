from pathlib import Path
import numpy as np
import pandas as pd

rng = np.random.default_rng(42)
ROOT = Path(__file__).parent
DATA = ROOT / "data"
DOCS = DATA / "sample_documents"
DOCS.mkdir(parents=True, exist_ok=True)

products = pd.DataFrame([
    ["P001","FreshGlow Shampoo 250ml","Personal Care",220],
    ["P002","FreshGlow Shampoo 650ml","Personal Care",480],
    ["P003","PureCare Bath Soap 100g","Personal Care",55],
    ["P004","SmileMax Toothpaste 150g","Oral Care",125],
    ["P005","CleanPro Detergent 1kg","Home Care",190],
    ["P006","CleanPro Detergent 2kg","Home Care",350],
    ["P007","CrunchBite Biscuits 200g","Foods",70],
    ["P008","DailyFresh Cooking Oil 1L","Foods",160],
    ["P009","DailyFresh Cooking Oil 5L","Foods",720],
    ["P010","CoolFizz Beverage 750ml","Beverages",65],
], columns=["product_id","product_name","category","unit_price"])
products.to_csv(DATA/"products.csv", index=False)

regions = ["Maharashtra","Gujarat","Delhi NCR","Karnataka","West Bengal"]
channels = ["Modern Trade","General Trade","E-commerce"]
stores = pd.DataFrame([[f"S{i:03d}", rng.choice(regions), rng.choice(channels)] for i in range(1,31)], columns=["store_id","region","channel"])
stores.to_csv(DATA/"stores.csv", index=False)

customers = pd.DataFrame({"customer_id":[f"C{i:04d}" for i in range(1,801)], "age":rng.integers(18,65,800), "city":rng.choice(["Mumbai","Pune","Nagpur","Ahmedabad","Delhi","Bengaluru","Kolkata"],800)})
customers.to_csv(DATA/"customers.csv", index=False)

n = 12000
dates = pd.date_range("2025-01-01","2026-08-31",freq="D")
product_ids = rng.choice(products.product_id, n, p=np.array([.11,.06,.13,.10,.12,.06,.16,.10,.03,.13]))
prod = products.set_index("product_id").loc[product_ids].reset_index()
st = stores.iloc[rng.integers(0,len(stores),n)].reset_index(drop=True)
df = pd.DataFrame({
    "transaction_id":[f"T{i:06d}" for i in range(1,n+1)],
    "customer_id":rng.choice(customers.customer_id,n),
    "product_id":product_ids,
    "date":rng.choice(dates,n),
    "quantity":rng.poisson(2.2,n)+1,
    "discount_pct":rng.choice([0,0,0,5,10,15],n,p=[.45,.15,.1,.12,.1,.08]),
    "store_id":st.store_id,
    "region":st.region,
    "channel":st.channel,
})
df["unit_price"] = prod.unit_price.values
df["product_name"] = prod.product_name.values
df["category"] = prod.category.values
# Add a mild seasonality and promotion effect to make analysis interesting.
df["month"] = pd.to_datetime(df.date).dt.month
df.loc[df.month.isin([10,11,12]), "quantity"] += rng.poisson(1.0, df.month.isin([10,11,12]).sum())
df.drop(columns=["month"]).sort_values("date").to_csv(DATA/"transactions.csv", index=False)

inv = products[["product_id","product_name"]].copy()
inv["store_id"] = rng.choice(stores.store_id, len(inv))
inv["units_sold_7d"] = rng.integers(10,120,len(inv))
inv["stock_on_hand"] = rng.integers(10,450,len(inv))
inv.to_csv(DATA/"inventory.csv", index=False)

pd.DataFrame({"promotion_id":[f"PR{i:03d}" for i in range(1,16)], "product_id":rng.choice(products.product_id,15), "discount_pct":rng.choice([5,10,15,20],15), "start_date":rng.choice(pd.date_range("2025-02-01","2026-07-01",freq="MS"),15)}).to_csv(DATA/"promotions.csv", index=False)

(DOCS/"promotion_playbook.md").write_text("""# FMCG Promotion Playbook\n\nPromotions can increase unit movement but may reduce net revenue per unit. Evaluate promotion performance by comparing units, net sales, margin where available, channel and baseline periods. Avoid concluding causality from a simple before/after comparison.\n""", encoding="utf-8")
(DOCS/"inventory_policy.md").write_text("""# Inventory Policy\n\nDays of cover is calculated as stock on hand divided by recent daily sales velocity. A portfolio demonstration threshold of under 3 days is treated as high risk and 3-7 days as medium risk. Production systems should use SKU-specific service levels and lead times.\n""", encoding="utf-8")
(DOCS/"customer_strategy.md").write_text("""# Customer Strategy\n\nRFM segmentation uses recency, purchase frequency and monetary value. Champions can be protected with retention activity, while high-value-at-risk customers warrant investigation of recency decline, product mix, competition, service and availability.\n""", encoding="utf-8")
print("Synthetic FMCG data generated in data/")
