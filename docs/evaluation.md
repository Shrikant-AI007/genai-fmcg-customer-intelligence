# Evaluation Strategy

A production GenAI system should be evaluated on both analytics correctness and generation quality.

## Retrieval
- Recall@k
- Precision@k
- Source relevance

## Generation
- Groundedness
- Answer completeness
- Numerical consistency with source analytics
- Actionability
- Hallucination rate

## Operational
- Latency
- Token/cost consumption
- Failure rate

The repository includes a small retrieval evaluation script; the next iteration should add a labeled benchmark of 50-100 business questions.
