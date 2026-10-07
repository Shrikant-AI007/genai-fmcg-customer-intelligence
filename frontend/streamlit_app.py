import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parents[1]))
import streamlit as st
from app.analytics.core import load_data, sales_summary, monthly_trend, customer_rfm, product_performance, inventory_risk, product_affinity
from app.rag.retriever import SimpleRetriever
from app.llm.client import LLMClient

st.set_page_config(page_title="FMCG GenAI Copilot", layout="wide")
st.title("🛒 FMCG GenAI Customer Intelligence Copilot")
st.caption("Synthetic portfolio dataset | Analytics + RAG + GenAI")

df = load_data()
retriever = SimpleRetriever()
llm = LLMClient()

with st.sidebar:
    st.header("Filters")
    region = st.selectbox("Region", ["All"] + sorted(df.region.unique().tolist()))
    category = st.selectbox("Category", ["All"] + sorted(df.category.unique().tolist()))

x = df.copy()
if region != "All": x = x[x.region == region]
if category != "All": x = x[x.category == category]
s = sales_summary(x)
cols = st.columns(4)
cols[0].metric("Revenue", f"₹{s['revenue']/1e5:.1f}L")
cols[1].metric("Units", f"{s['units']:,}")
cols[2].metric("Orders", f"{s['orders']:,}")
cols[3].metric("Avg Order Value", f"₹{s['avg_order_value']:,.0f}")

st.subheader("Sales trend")
st.line_chart(monthly_trend(x).set_index("month")["revenue"])

left, right = st.columns(2)
with left:
    st.subheader("Top products")
    st.dataframe(product_performance(x).head(10), use_container_width=True, hide_index=True)
with right:
    st.subheader("Inventory risk")
    st.dataframe(inventory_risk().query("risk != 'LOW'").head(10), use_container_width=True, hide_index=True)

st.subheader("GenAI Business Copilot")
question = st.text_input("Ask a business question", "Why did sales change and what should the sales team investigate?")
if st.button("Analyze", type="primary"):
    docs = retriever.search(question)
    context = "\n\n".join(f"SOURCE: {d['source']}\n{d['text']}" for d in docs)
    answer = llm.generate(question, {"sales_summary": s}, context)
    st.markdown(answer)
    if docs:
        st.caption("Retrieved evidence: " + ", ".join(d["source"] for d in docs))
