from fastapi import FastAPI
from pydantic import BaseModel
from app.analytics.core import load_data, sales_summary, monthly_trend, customer_rfm, product_performance, inventory_risk, product_affinity
from app.rag.retriever import SimpleRetriever
from app.llm.client import LLMClient

app = FastAPI(title="GenAI FMCG Customer Intelligence API", version="1.0.0")

df = load_data()
retriever = SimpleRetriever()
llm = LLMClient()

class Question(BaseModel):
    question: str
    region: str | None = None
    category: str | None = None

@app.get("/health")
def health(): return {"status": "ok"}

@app.get("/sales/summary")
def sales(region: str | None = None, category: str | None = None):
    return sales_summary(df, region, category)

@app.get("/sales/trend")
def trend():
    return monthly_trend(df).to_dict(orient="records")

@app.get("/customers/rfm")
def rfm():
    return customer_rfm(df).to_dict(orient="records")

@app.get("/products/performance")
def products():
    return product_performance(df).head(50).to_dict(orient="records")

@app.get("/inventory/risk")
def inventory():
    return inventory_risk().head(50).to_dict(orient="records")

@app.post("/copilot/ask")
def ask(payload: Question):
    evidence = retriever.search(payload.question)
    docs = "\n\n".join(f"SOURCE: {d['source']}\n{d['text']}" for d in evidence)
    analytics = {"sales_summary": sales_summary(df, payload.region, payload.category)}
    answer = llm.generate(payload.question, analytics, docs)
    return {"answer": answer, "sources": [d["source"] for d in evidence], "analytics": analytics}
