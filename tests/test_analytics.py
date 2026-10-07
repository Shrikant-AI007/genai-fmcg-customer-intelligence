from pathlib import Path
import subprocess
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from app.analytics.core import load_data, sales_summary, customer_rfm, inventory_risk

def setup_module():
    subprocess.run([sys.executable, "scripts_generate_data.py"], check=True)

def test_load_data():
    df = load_data()
    assert len(df) > 1000
    assert "net_sales" in df.columns

def test_sales_summary():
    df = load_data()
    s = sales_summary(df)
    assert s["revenue"] > 0
    assert s["orders"] > 0

def test_rfm():
    df = load_data()
    r = customer_rfm(df)
    assert {"R","F","M","segment"}.issubset(r.columns)

def test_inventory_risk():
    inv = inventory_risk()
    assert "days_of_cover" in inv.columns
    assert set(inv.risk.unique()).issubset({"HIGH","MEDIUM","LOW"})
