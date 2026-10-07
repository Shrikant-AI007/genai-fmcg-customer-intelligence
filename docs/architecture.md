# Architecture

The solution separates deterministic analytics from generative synthesis.

1. Data layer: synthetic CSVs representing transactions, customers, products, stores, promotions and inventory.
2. Analytics layer: Pandas-based KPI and segmentation calculations.
3. Knowledge layer: business markdown documents retrieved with a lightweight lexical retriever.
4. LLM layer: provider abstraction with a local deterministic fallback and optional OpenAI-compatible API.
5. API layer: FastAPI endpoints for reusable services.
6. Presentation: Streamlit business interface.

This separation makes the system testable and allows enterprise data and LLM providers to be replaced independently.
