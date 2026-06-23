"""
Canonical capability taxonomy for the Redrob ranking engine.

This file defines:
1. Capabilities
2. Capability aliases
3. Skill -> Capability mappings
"""

CAPABILITY_TAXONOMY = {

    "EMBEDDING_RETRIEVAL": [
        "embedding",
        "embeddings",
        "semantic search",
        "dense retrieval",
        "retrieval",
        "sentence-transformers",
        "sentence transformers",
        "openai embeddings",
        "bge",
        "e5",
        "colbert"
    ],

    "VECTOR_SEARCH": [
        "pinecone",
        "faiss",
        "weaviate",
        "milvus",
        "qdrant",
        "vector database",
        "vector db",
        "vector search"
    ],

    "HYBRID_SEARCH": [
        "hybrid search",
        "bm25",
        "elasticsearch",
        "opensearch",
        "lucene"
    ],

    "RANKING_SYSTEMS": [
        "ranking",
        "reranking",
        "re-ranking",
        "learning to rank",
        "ltr",
        "recommendation",
        "recommendation system",
        "search ranking"
    ],

    "EVALUATION_FRAMEWORKS": [
        "ndcg",
        "mrr",
        "map",
        "ab testing",
        "a/b testing",
        "offline evaluation",
        "online evaluation",
        "ranking evaluation"
    ],

    "PRODUCTION_ML": [
        "machine learning",
        "production ml",
        "model deployment",
        "model serving",
        "inference"
    ],

    "LLM_SYSTEMS": [
        "llm",
        "rag",
        "langchain",
        "llama",
        "gpt",
        "prompt engineering",
        "agentic ai"
    ],

    "FINE_TUNING": [
        "fine tuning",
        "finetuning",
        "lora",
        "qlora",
        "peft"
    ],

    "MLOPS": [
        "mlops",
        "kubeflow",
        "airflow",
        "ml pipeline",
        "feature store"
    ],

    "DISTRIBUTED_SYSTEMS": [
        "distributed systems",
        "distributed computing",
        "spark",
        "ray",
        "hadoop"
    ],

    "PYTHON_ENGINEERING": [
        "python",
        "fastapi",
        "flask",
        "pandas",
        "numpy"
    ],

    "PRODUCT_ENGINEERING": [
        "product development",
        "user feedback",
        "experimentation",
        "rapid prototyping",
        "feature ownership"
    ]
}


# ---------------------------------------------------------
# Reverse lookup index
# ---------------------------------------------------------

SKILL_TO_CAPABILITY = {}

for capability, aliases in CAPABILITY_TAXONOMY.items():

    for alias in aliases:

        SKILL_TO_CAPABILITY[alias.lower()] = capability


# ---------------------------------------------------------
# Capability priorities for this JD
# ---------------------------------------------------------

JD_PRIORITY_CAPABILITIES = {

    "EMBEDDING_RETRIEVAL": 1.0,
    "VECTOR_SEARCH": 1.0,
    "RANKING_SYSTEMS": 1.0,
    "EVALUATION_FRAMEWORKS": 1.0,
    "PYTHON_ENGINEERING": 1.0,

    "HYBRID_SEARCH": 0.9,
    "PRODUCTION_ML": 0.9,

    "FINE_TUNING": 0.6,
    "DISTRIBUTED_SYSTEMS": 0.5,
    "PRODUCT_ENGINEERING": 0.8,
    "MLOPS": 0.5
}