from app.rag.retriever import SimpleRetriever

def test_retriever():
    r = SimpleRetriever()
    results = r.search("promotion discount sales")
    assert results
    assert "promotion_playbook.md" in [x["source"] for x in results]
