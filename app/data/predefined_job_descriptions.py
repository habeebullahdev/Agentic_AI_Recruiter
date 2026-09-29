"""Default job descriptions used to initialize an empty database."""

PREDEFINED_JOB_DESCRIPTIONS = [
    {
        "title": "AI Engineer",
        "required_skills": ["Python", "Machine Learning", "PyTorch", "TensorFlow", "Model Serving", "MLOps"],
        "jd_text": (
            "Role: AI Engineer\n\n"
            "Job Summary:\n"
            "Build and productionize AI systems that solve product and business problems, from data preparation through model deployment.\n\n"
            "Responsibilities:\n"
            "- Develop, evaluate, and improve machine-learning and deep-learning models.\n"
            "- Prepare training data, establish evaluation metrics, and monitor model quality.\n"
            "- Integrate models into reliable services and collaborate with product and platform teams.\n\n"
            "Requirements:\n"
            "- Strong Python and software engineering fundamentals.\n"
            "- Practical experience with PyTorch or TensorFlow, model evaluation, and deployment."
        ),
    },
    {
        "title": "GenAI Engineer",
        "required_skills": ["Python", "Generative AI", "LLMs", "Prompt Engineering", "RAG", "Vector Databases"],
        "jd_text": (
            "Role: GenAI Engineer\n\n"
            "Job Summary:\n"
            "Design and deliver generative AI features using foundation models, retrieval, and responsible evaluation practices.\n\n"
            "Responsibilities:\n"
            "- Build LLM-powered applications, prompt workflows, and retrieval-augmented generation pipelines.\n"
            "- Evaluate quality, latency, cost, safety, and grounding across representative use cases.\n"
            "- Integrate model providers and vector search into production services.\n\n"
            "Requirements:\n"
            "- Production Python development experience and familiarity with LLM APIs.\n"
            "- Hands-on experience with RAG, embeddings, vector stores, and prompt evaluation."
        ),
    },
    {
        "title": "Python Backend Developer",
        "required_skills": ["Python", "REST APIs", "SQL", "PostgreSQL", "ORM", "Testing", "Git"],
        "jd_text": (
            "Role: Python Backend Developer\n\n"
            "Job Summary:\n"
            "Develop maintainable backend services and APIs that support secure, dependable product experiences.\n\n"
            "Responsibilities:\n"
            "- Implement business logic, REST endpoints, and integrations in Python.\n"
            "- Design relational data models and improve query performance.\n"
            "- Write automated tests, review code, and contribute to production operations.\n\n"
            "Requirements:\n"
            "- Strong Python, SQL, and API design fundamentals.\n"
            "- Experience with a Python web framework, PostgreSQL, and automated testing."
        ),
    },
    {
        "title": "FastAPI Developer",
        "required_skills": ["Python", "FastAPI", "Pydantic", "SQLAlchemy", "PostgreSQL", "REST APIs", "Pytest"],
        "jd_text": (
            "Role: FastAPI Developer\n\n"
            "Job Summary:\n"
            "Build typed, high-performance HTTP services with FastAPI and integrate them with databases and external systems.\n\n"
            "Responsibilities:\n"
            "- Design API routes, request and response schemas, and dependency-managed services.\n"
            "- Implement persistence with SQLAlchemy and optimize PostgreSQL access.\n"
            "- Add authentication, validation, tests, API documentation, and operational logging.\n\n"
            "Requirements:\n"
            "- Professional Python experience and practical FastAPI knowledge.\n"
            "- Familiarity with Pydantic, SQLAlchemy, PostgreSQL, and pytest."
        ),
    },
    {
        "title": "Machine Learning Engineer",
        "required_skills": ["Python", "Scikit-learn", "PyTorch", "Feature Engineering", "Model Evaluation", "MLOps"],
        "jd_text": (
            "Role: Machine Learning Engineer\n\n"
            "Job Summary:\n"
            "Develop and deploy machine-learning models that deliver measurable improvements to customer and operational outcomes.\n\n"
            "Responsibilities:\n"
            "- Prepare datasets, engineer features, and train models for defined product use cases.\n"
            "- Establish reproducible experiments and evaluate model performance and fairness.\n"
            "- Deploy models and build monitoring for data drift, reliability, and quality.\n\n"
            "Requirements:\n"
            "- Strong Python, statistics, and machine-learning fundamentals.\n"
            "- Experience with Scikit-learn or deep-learning frameworks and production model workflows."
        ),
    },
    {
        "title": "Software Development Engineer",
        "required_skills": ["Data Structures", "Algorithms", "Python", "Java", "System Design", "Testing", "Git"],
        "jd_text": (
            "Role: Software Development Engineer\n\n"
            "Job Summary:\n"
            "Design, implement, and maintain software components for reliable, scalable products.\n\n"
            "Responsibilities:\n"
            "- Translate product requirements into clear technical designs and tested code.\n"
            "- Build services and integrations with attention to performance and reliability.\n"
            "- Participate in code reviews, incident resolution, and continuous improvement.\n\n"
            "Requirements:\n"
            "- Proficiency in at least one general-purpose programming language.\n"
            "- Knowledge of data structures, algorithms, testing, and collaborative development practices."
        ),
    },
    {
        "title": "Full Stack Developer",
        "required_skills": ["JavaScript", "TypeScript", "React", "Python", "REST APIs", "SQL", "HTML", "CSS"],
        "jd_text": (
            "Role: Full Stack Developer\n\n"
            "Job Summary:\n"
            "Deliver end-to-end web product features across responsive user interfaces, backend services, and data persistence.\n\n"
            "Responsibilities:\n"
            "- Build accessible frontend experiences and integrate them with backend APIs.\n"
            "- Implement server-side features, data models, and secure integrations.\n"
            "- Test and monitor features and collaborate with design and product partners.\n\n"
            "Requirements:\n"
            "- Experience with a modern JavaScript framework and a backend language or framework.\n"
            "- Understanding of REST APIs, relational databases, web security, and responsive design."
        ),
    },
    {
        "title": "Data Engineer",
        "required_skills": ["Python", "SQL", "ETL", "Data Modeling", "Airflow", "Spark", "Cloud Data Platforms"],
        "jd_text": (
            "Role: Data Engineer\n\n"
            "Job Summary:\n"
            "Build dependable data pipelines and platforms that make high-quality data available for analytics and machine learning.\n\n"
            "Responsibilities:\n"
            "- Develop batch and streaming ingestion, transformation, and validation workflows.\n"
            "- Model warehouse data and improve pipeline performance and observability.\n"
            "- Partner with analysts and scientists to deliver trusted, documented datasets.\n\n"
            "Requirements:\n"
            "- Strong SQL and Python skills with experience building data pipelines.\n"
            "- Familiarity with orchestration, distributed processing, and cloud data services."
        ),
    },
    {
        "title": "AI Application Developer",
        "required_skills": ["Python", "LLM APIs", "FastAPI", "RAG", "Prompt Design", "REST APIs", "Testing"],
        "jd_text": (
            "Role: AI Application Developer\n\n"
            "Job Summary:\n"
            "Create user-facing applications that combine conventional software engineering with practical AI capabilities.\n\n"
            "Responsibilities:\n"
            "- Integrate language and machine-learning APIs into secure application workflows.\n"
            "- Build retrieval, tool-use, and structured-output features with measurable quality.\n"
            "- Develop service interfaces, tests, and monitoring for AI-enabled features.\n\n"
            "Requirements:\n"
            "- Strong Python application development and API integration experience.\n"
            "- Familiarity with LLM workflows, data privacy, evaluation, and production testing."
        ),
    },
    {
        "title": "LLM Engineer",
        "required_skills": ["Python", "Large Language Models", "Transformers", "RAG", "Fine-tuning", "Evaluation", "Inference"],
        "jd_text": (
            "Role: LLM Engineer\n\n"
            "Job Summary:\n"
            "Engineer language-model systems, from model selection and adaptation to efficient inference and ongoing evaluation.\n\n"
            "Responsibilities:\n"
            "- Build LLM applications and retrieval pipelines for domain-specific tasks.\n"
            "- Evaluate prompting, fine-tuning, and model-serving strategies against quality and cost targets.\n"
            "- Improve inference reliability, observability, and safeguards.\n\n"
            "Requirements:\n"
            "- Strong Python and experience with transformer-based language models.\n"
            "- Knowledge of RAG, model evaluation, inference optimization, and responsible AI practices."
        ),
    },
    {
        "title": "NLP Engineer",
        "required_skills": ["Python", "Natural Language Processing", "Transformers", "Text Classification", "Embeddings", "Evaluation"],
        "jd_text": (
            "Role: NLP Engineer\n\n"
            "Job Summary:\n"
            "Develop natural-language processing solutions for extracting, classifying, searching, and understanding text.\n\n"
            "Responsibilities:\n"
            "- Prepare text datasets and build NLP models and language-processing pipelines.\n"
            "- Evaluate model quality across relevant languages, cohorts, and edge cases.\n"
            "- Deploy NLP capabilities as maintainable services and communicate results to partners.\n\n"
            "Requirements:\n"
            "- Strong Python and applied NLP or computational linguistics experience.\n"
            "- Familiarity with transformer models, embeddings, text evaluation, and production deployment."
        ),
    },
    {
        "title": "Backend Engineer",
        "required_skills": ["Backend Development", "REST APIs", "Python", "SQL", "PostgreSQL", "Distributed Systems", "Testing"],
        "jd_text": (
            "Role: Backend Engineer\n\n"
            "Job Summary:\n"
            "Build robust server-side systems, APIs, and data services that power reliable product experiences.\n\n"
            "Responsibilities:\n"
            "- Design and implement service interfaces and domain logic.\n"
            "- Improve database performance, service observability, and system resilience.\n"
            "- Collaborate on architecture, testing, security, and production support.\n\n"
            "Requirements:\n"
            "- Experience developing backend systems and API-based services.\n"
            "- Strong database fundamentals and knowledge of testing, security, and distributed systems."
        ),
    },
    {
        "title": "Software Engineer",
        "required_skills": ["Software Design", "Python", "Java", "Algorithms", "Testing", "Databases", "Git"],
        "jd_text": (
            "Role: Software Engineer\n\n"
            "Job Summary:\n"
            "Contribute to the design and delivery of maintainable software that meets product requirements and quality standards.\n\n"
            "Responsibilities:\n"
            "- Design, implement, test, and document software features.\n"
            "- Diagnose defects and improve code quality, performance, and reliability.\n"
            "- Work with engineers and stakeholders through planning, review, and release.\n\n"
            "Requirements:\n"
            "- Proficiency in a modern programming language and software development fundamentals.\n"
            "- Familiarity with version control, testing, databases, and collaborative engineering practices."
        ),
    },
    {
        "title": "Data Analyst",
        "required_skills": ["SQL", "Python", "Pandas", "Statistics", "Data Visualization", "Excel", "Power BI"],
        "jd_text": (
            "Role: Data Analyst\n\n"
            "Job Summary:\n"
            "Turn business data into clear analysis, trusted metrics, and actionable recommendations.\n\n"
            "Responsibilities:\n"
            "- Query, clean, and analyze structured datasets using SQL and analytical tools.\n"
            "- Build dashboards and communicate trends, limitations, and findings to stakeholders.\n"
            "- Define and validate metrics in partnership with business and engineering teams.\n\n"
            "Requirements:\n"
            "- Strong SQL, analytical reasoning, and data-quality practices.\n"
            "- Experience with Python or spreadsheets and a business intelligence or visualization tool."
        ),
    },
    {
        "title": "Cloud Engineer",
        "required_skills": ["AWS", "Azure", "GCP", "Linux", "Docker", "Kubernetes", "Terraform", "CI/CD"],
        "jd_text": (
            "Role: Cloud Engineer\n\n"
            "Job Summary:\n"
            "Provision and operate secure, scalable cloud infrastructure for application and data workloads.\n\n"
            "Responsibilities:\n"
            "- Automate cloud infrastructure, deployment workflows, and environment configuration.\n"
            "- Improve availability, security, cost efficiency, and observability of cloud services.\n"
            "- Partner with development teams on containerized workloads and incident response.\n\n"
            "Requirements:\n"
            "- Hands-on experience with a major cloud provider and Linux-based systems.\n"
            "- Familiarity with infrastructure as code, containers, networking, and CI/CD."
        ),
    },
]