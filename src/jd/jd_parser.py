"""
Enhanced JD parser that extracts structured requirements from the job description.
Returns a JDRequirements dataclass used by all downstream components.
"""

from dataclasses import dataclass, field


@dataclass
class JDRequirements:
    """Structured representation of the job description requirements."""

    # Role basics
    role_title: str = "Senior AI/ML Engineer"
    experience_min: float = 5.0
    experience_max: float = 9.0
    experience_ideal_min: float = 6.0
    experience_ideal_max: float = 8.0

    # Location
    preferred_locations: list = field(default_factory=lambda: [
        "pune", "noida", "hyderabad", "mumbai", "delhi", "ncr",
        "delhi ncr", "new delhi", "gurgaon", "gurugram"
    ])
    country: str = "India"

    # Must-have capabilities (from JD "Things you absolutely need")
    must_have_capabilities: list = field(default_factory=lambda: [
        "EMBEDDING_RETRIEVAL",
        "VECTOR_SEARCH",
        "RANKING_SYSTEMS",
        "EVALUATION_FRAMEWORKS",
        "PYTHON_ENGINEERING",
    ])

    # Nice-to-have capabilities
    nice_to_have_capabilities: list = field(default_factory=lambda: [
        "FINE_TUNING",
        "LLM_SYSTEMS",
        "HYBRID_SEARCH",
        "DISTRIBUTED_SYSTEMS",
        "PRODUCT_ENGINEERING",
        "MLOPS",
    ])

    # Must-have skill keywords (for text matching)
    must_have_keywords: list = field(default_factory=lambda: [
        "embedding", "embeddings", "sentence-transformers", "bge", "e5",
        "semantic search", "dense retrieval", "retrieval",
        "pinecone", "faiss", "weaviate", "milvus", "qdrant",
        "vector database", "vector search", "vector db",
        "elasticsearch", "opensearch",
        "ranking", "reranking", "re-ranking", "recommendation",
        "learning to rank", "ltr", "search ranking",
        "ndcg", "mrr", "map", "a/b testing", "evaluation",
        "python",
    ])

    # Nice-to-have skill keywords
    nice_to_have_keywords: list = field(default_factory=lambda: [
        "lora", "qlora", "peft", "fine-tuning", "finetuning",
        "llm", "rag", "langchain",
        "bm25", "hybrid search",
        "distributed systems", "spark", "ray",
        "mlops", "kubeflow", "airflow",
        "model deployment", "model serving", "inference",
    ])

    # Relevant titles (high to low relevance)
    high_relevance_titles: list = field(default_factory=lambda: [
        "ml engineer", "machine learning engineer",
        "senior ml engineer", "senior machine learning engineer",
        "staff ml engineer", "staff machine learning engineer",
        "ai engineer", "senior ai engineer",
        "nlp engineer", "senior nlp engineer",
        "search engineer", "ranking engineer",
        "recommendation engineer",
        "applied scientist", "applied ml scientist",
        "research engineer", "ml research engineer",
        "data scientist",  # with caveats
    ])

    medium_relevance_titles: list = field(default_factory=lambda: [
        "backend engineer", "senior backend engineer",
        "software engineer", "senior software engineer",
        "data engineer", "senior data engineer",
        "full stack engineer", "platform engineer",
        "junior ml engineer", "junior machine learning engineer",
        "analytics engineer",
    ])

    low_relevance_titles: list = field(default_factory=lambda: [
        "marketing manager", "hr manager", "accountant",
        "civil engineer", "mechanical engineer",
        "graphic designer", "content writer",
        "sales executive", "customer support",
        "operations manager", "project manager",
        "business analyst", "financial analyst",
        "teacher", "professor",
    ])

    # Consulting companies (explicit disqualifier if entire career)
    consulting_companies: set = field(default_factory=lambda: {
        "tcs", "infosys", "wipro", "accenture", "cognizant",
        "capgemini", "hcl", "tech mahindra", "mindtree",
        "mphasis", "hexaware", "ltimindtree", "persistent",
    })

    # Work mode
    preferred_work_modes: list = field(default_factory=lambda: [
        "hybrid", "onsite", "flexible"
    ])

    # Notice period
    max_notice_preferred: int = 30
    max_notice_acceptable: int = 60

    # Salary range (INR LPA) — inferred from senior AI/ML role in India
    salary_min_lpa: float = 15.0
    salary_max_lpa: float = 50.0

    # JD full text for semantic matching
    jd_summary: str = field(default_factory=lambda: (
        "Senior AI/ML Engineer for Redrob's intelligence layer. "
        "Own ranking, retrieval, and matching systems for recruiter search "
        "and candidate discovery. Ship v2 ranking with embeddings, hybrid retrieval, "
        "and LLM-based re-ranking. Build evaluation infrastructure with NDCG, MRR, MAP, "
        "A/B testing. Need production experience with embedding retrieval systems like "
        "sentence-transformers, BGE, E5. Production experience with vector databases "
        "like Pinecone, Weaviate, Qdrant, Milvus, FAISS, Elasticsearch. Strong Python. "
        "Hands-on evaluation frameworks for ranking systems. 5-9 years experience, "
        "product company background preferred, not pure consulting. Looking for someone "
        "who builds production systems, not just demos or research."
    ))

    jd_full_text: str = field(default_factory=lambda: (
        "We are looking for a Senior AI ML Engineer to own the intelligence layer "
        "of Redrob product. That means the ranking retrieval and matching systems "
        "that decide what recruiters see when they search for candidates and what "
        "candidates see when they search for roles. "
        "Production experience with embeddings based retrieval systems such as "
        "sentence-transformers OpenAI embeddings BGE E5 deployed to real users. "
        "Production experience with vector databases or hybrid search infrastructure "
        "such as Pinecone Weaviate Qdrant Milvus OpenSearch Elasticsearch FAISS. "
        "Strong Python and code quality. "
        "Hands on experience designing evaluation frameworks for ranking systems "
        "including NDCG MRR MAP offline to online correlation A/B test interpretation. "
        "Nice to have LLM fine-tuning experience LoRA QLoRA PEFT. "
        "Experience with learning to rank models XGBoost based or neural. "
        "Prior exposure to HR-tech recruiting tech or marketplace products. "
        "Background in distributed systems or large scale inference optimization. "
        "We do not want title chasers who switch companies every 1.5 years. "
        "We do not want people who have only worked at consulting firms TCS Infosys "
        "Wipro Accenture Cognizant Capgemini in their entire career. "
        "We do not want people whose primary expertise is computer vision speech or "
        "robotics without significant NLP IR exposure. "
        "Ideal candidate is 6 to 8 years total experience with 4 to 5 in applied ML "
        "AI roles at product companies. Has shipped at least one end to end ranking "
        "search or recommendation system to real users at meaningful scale. "
        "Located in or willing to relocate to Noida or Pune. "
        "Active on Redrob platform with clear signal of being in the job market."
    ))


def parse_jd():
    """
    Return the structured JD requirements.
    In a real system this would parse a JD document;
    here the JD is hardcoded since it's a single known JD.
    """
    return JDRequirements()