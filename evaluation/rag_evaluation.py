from app.rag.retriever import SimpleRetriever

questions = [
    "How should promotions be evaluated?",
    "What does days of cover mean?",
    "How should high-value customers be handled?",
]
retriever = SimpleRetriever()
for q in questions:
    results = retriever.search(q)
    print(q, "->", [r["source"] for r in results])
