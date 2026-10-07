# GenAI FMCG Customer Intelligence Platform

An end-to-end portfolio project that combines **GenAI, RAG, SQL-style analytics, customer segmentation, product intelligence, promotion analysis, inventory signals, and a natural-language business copilot** for an FMCG business.

> **Portfolio / demonstration project:** all transaction and business data in this repository are synthetic and created for demonstration. No confidential client data is included.

## Business Problem

FMCG teams work across sales, customers, products, stores, promotions and inventory. Business users often need answers such as:

- Why did sales decline in a region?
- Which products are driving revenue growth?
- Which customer segments are most valuable?
- Did a promotion improve sales?
- Which products show stock-out risk?
- What actions should a sales manager investigate?

The platform provides a single business copilot for these questions.

## Solution

```text
                         FMCG Business User
                                |
                                v
                       Streamlit Business UI
                                |
                                v
                            FastAPI
                                |
              +-----------------+-----------------+
              |                                   |
              v                                   v
       Business Analytics                    RAG Knowledge
              |                                   |
      +-------+--------+                    +-----+------+
      |       |        |                    |            |
    Sales  Customer  Product              SOPs      Business Docs
      |       |        |                    |            |
      +-------+--------+                    +-----+------+
              |                                   |
              +----------------+------------------+
                               |
                               v
                        GenAI Response Layer
                               |
                               v
                  Insight + Evidence + Action
```

## Features

- Customer RFM segmentation
- Product/category/region/channel sales analytics
- Promotion lift analysis
- Inventory and stock-out risk signals
- Product affinity / cross-sell analysis
- Natural-language business questions
- Retrieval-Augmented Generation (RAG) over business documents
- Structured business response format
- FastAPI backend
- Streamlit dashboard
- Synthetic data generator
- Unit tests
- Docker support
- LLM provider abstraction with a deterministic local demo fallback

## Tech Stack

Python, Pandas, NumPy, FastAPI, Streamlit, scikit-learn, SQLite, sentence-transformers, FAISS, OpenAI-compatible LLM interface, Docker, pytest.

## Quick Start

### 1. Create environment

```bash
python -m venv .venv
# Windows
.venv\\Scripts\\activate
# macOS/Linux
source .venv/bin/activate
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Generate synthetic FMCG data

```bash
python scripts_generate_data.py
```

### 4. Run the Streamlit application

```bash
streamlit run frontend/streamlit_app.py
```

### 5. Run the API

```bash
uvicorn app.api.main:app --reload
```

API documentation: `http://127.0.0.1:8000/docs`

## Optional LLM Configuration

The project runs without an API key using a deterministic demo response generator. For a real LLM provider, configure:

```text
LLM_PROVIDER=openai_compatible
LLM_API_KEY=your_key
LLM_MODEL=your_model
LLM_BASE_URL=https://api.openai.com/v1
```

Do not commit API keys. Use `.env` locally.

## Example Questions

- `Why did shampoo sales decline in Maharashtra?`
- `Which customer segment contributes the most revenue?`
- `What products should we cross-sell with toothpaste?`
- `Which products have stock-out risk?`
- `Did promotions improve detergent sales?`
- `Give me a management summary for the latest month.`

## Project Structure

```text
app/
  api/                 FastAPI routes
  analytics/           FMCG analytics and business logic
  llm/                 LLM abstraction and prompts
  rag/                 Document ingestion/retrieval
  utils/               Configuration/helpers
data/
  sample_documents/    Synthetic business knowledge documents
evaluation/            Evaluation questions and scoring
docs/                  Architecture and business documentation
frontend/              Streamlit UI
tests/                 Automated tests
```

## Business Value

The project demonstrates how GenAI can sit on top of existing analytics rather than replacing analytics. The LLM translates a business question into a structured investigation, while deterministic Python analytics provide measurable evidence.

## Responsible AI Notes

- Synthetic data only.
- Business recommendations are decision support, not autonomous decisions.
- The system should cite retrieved evidence when connected to an LLM.
- Production deployment would require access control, audit logs, PII governance, model evaluation, prompt-injection controls and human review.

## Portfolio Positioning

This project demonstrates practical experience across **GenAI + RAG + analytics + ML + APIs + business problem solving**, rather than a simple chatbot.
