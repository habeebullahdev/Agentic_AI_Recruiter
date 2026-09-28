"""
Database Initialization and Comprehensive Seed Script.
Creates all database tables and seeds initial administrative users and full catalog of Fresher & Experienced Tech Roles.
"""
import sys
from app.database.session import SessionLocal, engine
from app.database.base import Base
from app.models.user import User, UserRole
from app.models.job_description import JobDescription
import app.models
from app.core.security import get_password_hash
from app.core.config import settings
from app.core.logging import logger
from app.services.rag_service import rag_service


def init_db() -> None:
    logger.info("Initializing database tables...")
    Base.metadata.create_all(bind=engine)
    logger.info("Tables created / verified.")

    db = SessionLocal()
    try:
        # 1. Seed Superuser / Admin
        admin_email = settings.FIRST_SUPERUSER_EMAIL.lower().strip()
        admin_user = db.query(User).filter(User.email == admin_email).first()
        if not admin_user:
            admin_user = User(
                name="System Administrator",
                email=admin_email,
                password_hash=get_password_hash(settings.FIRST_SUPERUSER_PASSWORD),
                role=UserRole.ADMIN,
                is_active=True
            )
            db.add(admin_user)
            db.commit()
            db.refresh(admin_user)
            logger.info(f"Created default Admin user: {admin_email}")
        else:
            logger.info(f"Admin user already exists: {admin_email}")

        # 2. Seed Recruiter
        recruiter_email = "recruiter@recruitmentai.com"
        recruiter = db.query(User).filter(User.email == recruiter_email).first()
        if not recruiter:
            recruiter = User(
                name="Sarah Jenkins",
                email=recruiter_email,
                password_hash=get_password_hash("RecruiterPass123!"),
                role=UserRole.RECRUITER,
                is_active=True
            )
            db.add(recruiter)
            db.commit()
            db.refresh(recruiter)
            logger.info(f"Created default Recruiter user: {recruiter_email}")

        # 3. Comprehensive Industry Tech Roles (Fresher & Experienced)
        all_tech_roles = [
            # ==========================================
            # 🎓 FRESHER / ENTRY-LEVEL ROLES (0 - 2 Years)
            # ==========================================
            {
                "title": "[Fresher] Junior Python & Django Developer (0-1 Year)",
                "required_skills": ["Python", "Django", "REST API", "PostgreSQL", "Git", "HTML/CSS", "SQL", "OOP"],
                "jd_text": (
                    "Role: Junior Python & Django Developer (Fresher / Entry-Level)\n"
                    "Experience: 0 - 1 Year\n\n"
                    "Job Summary:\n"
                    "We are hiring enthusiastic Fresher Python Developers to build core backend logic and RESTful endpoints.\n\n"
                    "Key Responsibilities:\n"
                    "- Write clean, readable, and maintainable Python code following PEP8 standards.\n"
                    "- Build basic CRUD APIs using Django / Django REST Framework.\n"
                    "- Integrate PostgreSQL / SQLite databases and write basic relational queries.\n"
                    "- Collaborate with the frontend team and write unit tests for backend views.\n\n"
                    "Requirements:\n"
                    "- B.E./B.Tech/B.Sc/MCA in Computer Science or related degree.\n"
                    "- Strong fundamentals in Python, Object-Oriented Programming (OOP), and Data Structures.\n"
                    "- Basic understanding of Git version control, HTTP methods, and relational databases."
                ),
                "created_by": recruiter.id
            },
            {
                "title": "[Fresher] Graduate Frontend Engineer - React / Next.js (0-1 Year)",
                "required_skills": ["JavaScript", "React", "Next.js", "HTML5", "CSS3", "Tailwind CSS", "TypeScript", "Git", "REST API"],
                "jd_text": (
                    "Role: Graduate Frontend Engineer (Fresher / Entry-Level)\n"
                    "Experience: 0 - 1 Year\n\n"
                    "Job Summary:\n"
                    "Join our product engineering team to craft responsive, modern web user interfaces using React and Tailwind CSS.\n\n"
                    "Key Responsibilities:\n"
                    "- Develop interactive React components and responsive layouts.\n"
                    "- Consume backend RESTful APIs using Fetch / Axios.\n"
                    "- Ensure cross-browser compatibility and mobile responsiveness.\n"
                    "- Use Git for code commits and participate in peer code reviews.\n\n"
                    "Requirements:\n"
                    "- Degree in Computer Science, IT, or completion of recognized Frontend Bootcamp.\n"
                    "- Hands-on portfolio or academic projects built with React.js.\n"
                    "- Solid foundation in JavaScript (ES6+), DOM manipulation, and CSS Grid/Flexbox."
                ),
                "created_by": recruiter.id
            },
            {
                "title": "[Fresher] Junior Java & Spring Boot Developer (0-2 Years)",
                "required_skills": ["Java", "Spring Boot", "MySQL", "Hibernate", "REST API", "Maven", "Git", "OOP"],
                "jd_text": (
                    "Role: Junior Java Developer\n"
                    "Experience: 0 - 2 Years\n\n"
                    "Job Summary:\n"
                    "Looking for Junior Java Developers with strong Core Java and Spring Boot knowledge to join enterprise software projects.\n\n"
                    "Key Responsibilities:\n"
                    "- Assist in developing microservices and backend modules using Java 17+ and Spring Boot.\n"
                    "- Write JPA/Hibernate queries and manage MySQL relational schemas.\n"
                    "- Troubleshoot bugs, write JUnit test cases, and assist senior engineers.\n\n"
                    "Requirements:\n"
                    "- Strong knowledge of Core Java, Collections, Multithreading, and OOP design patterns.\n"
                    "- Basic familiarity with Spring Boot, REST APIs, and relational databases (MySQL/PostgreSQL)."
                ),
                "created_by": recruiter.id
            },
            {
                "title": "[Fresher] Associate Data Analyst / BI Trainee (0-1 Year)",
                "required_skills": ["Python", "SQL", "Pandas", "PowerBI", "Tableau", "Excel", "Data Cleaning", "Statistics"],
                "jd_text": (
                    "Role: Associate Data Analyst\n"
                    "Experience: 0 - 1 Year\n\n"
                    "Job Summary:\n"
                    "We are seeking an entry-level Data Analyst to transform business raw data into actionable visual insights.\n\n"
                    "Key Responsibilities:\n"
                    "- Extract, clean, and analyze datasets using Python (Pandas/NumPy) and SQL.\n"
                    "- Design interactive dashboards and KPI reports in Power BI / Tableau.\n"
                    "- Perform exploratory data analysis (EDA) and report insights to stakeholders.\n\n"
                    "Requirements:\n"
                    "- Degree in Statistics, Mathematics, Computer Science, Economics, or Data Science.\n"
                    "- Strong SQL query skills (Joins, Aggregations, Window functions).\n"
                    "- Proficiency in Excel (VLOOKUP, Pivot Tables) and Python data visualization (Matplotlib/Seaborn)."
                ),
                "created_by": recruiter.id
            },
            {
                "title": "[Fresher] QA / Automation Testing Engineer (0-2 Years)",
                "required_skills": ["Python", "Selenium", "PyTest", "Manual Testing", "Postman", "REST API", "Jira", "Git"],
                "jd_text": (
                    "Role: QA Engineer (Manual & Automation)\n"
                    "Experience: 0 - 2 Years\n\n"
                    "Job Summary:\n"
                    "Join our Quality Assurance team to ensure high quality and zero-defect deployments for web and API platforms.\n\n"
                    "Key Responsibilities:\n"
                    "- Write and execute comprehensive test plans, test cases, and bug reports in Jira.\n"
                    "- Develop automated UI regression test scripts using Selenium with Python/Java.\n"
                    "- Perform REST API testing using Postman.\n\n"
                    "Requirements:\n"
                    "- Understanding of Software Testing Life Cycle (STLC) and Agile methodologies.\n"
                    "- Scripting knowledge in Python or Java.\n"
                    "- Eager eye for detail and identifying edge case bugs."
                ),
                "created_by": recruiter.id
            },
            {
                "title": "[Fresher] Entry-Level Cloud & DevOps Associate (0-1 Year)",
                "required_skills": ["Linux", "Bash", "Docker", "AWS", "Git", "CI/CD", "Networking", "Python"],
                "jd_text": (
                    "Role: Cloud & DevOps Associate\n"
                    "Experience: 0 - 1 Year\n\n"
                    "Job Summary:\n"
                    "Entry-level role for cloud enthusiasts looking to build a career in cloud infrastructure, automation, and CI/CD.\n\n"
                    "Key Responsibilities:\n"
                    "- Assist in containerizing applications using Docker.\n"
                    "- Monitor cloud workloads on AWS (EC2, S3, RDS, CloudWatch).\n"
                    "- Write basic Bash/Shell and Python automation scripts.\n\n"
                    "Requirements:\n"
                    "- Strong Linux OS administration and command line basics.\n"
                    "- Basic understanding of Docker, Git, and networking concepts (TCP/IP, DNS, SSL)."
                ),
                "created_by": recruiter.id
            },

            # ==========================================
            # 💼 EXPERIENCED & SENIOR ROLES (3 - 8+ Years)
            # ==========================================
            {
                "title": "[Experienced] Senior FastAPI Backend Engineer (3-6 Years)",
                "required_skills": ["Python", "FastAPI", "PostgreSQL", "SQLAlchemy", "Docker", "Redis", "REST API", "Microservices", "CI/CD"],
                "jd_text": (
                    "Role: Senior FastAPI Backend Engineer\n"
                    "Experience: 3 - 6 Years\n\n"
                    "Job Summary:\n"
                    "We are seeking an experienced Backend Engineer to architect high-throughput microservices and data pipelines.\n\n"
                    "Key Responsibilities:\n"
                    "- Design and scale async RESTful microservices using FastAPI and SQLAlchemy 2.0.\n"
                    "- Optimize PostgreSQL query plans, connection pools, and Redis caching layers.\n"
                    "- Implement Docker containerization, automated testing, and CI/CD pipelines.\n\n"
                    "Requirements:\n"
                    "- 3+ years of production Python backend engineering experience.\n"
                    "- Deep knowledge of FastAPI, asynchronous I/O (asyncio), and PostgreSQL tuning.\n"
                    "- Experience building resilient microservices architectures."
                ),
                "created_by": recruiter.id
            },
            {
                "title": "[Experienced] Agentic AI / LLM Engineer (3-7 Years)",
                "required_skills": ["Python", "LangChain", "Gemini API", "ChromaDB", "RAG", "Embeddings", "FastAPI", "Vector Search", "LLM"],
                "jd_text": (
                    "Role: Agentic AI & LLM Systems Engineer\n"
                    "Experience: 3 - 7 Years\n\n"
                    "Job Summary:\n"
                    "Join our AI lab building autonomous multi-agent recruitment workflows and enterprise RAG systems.\n\n"
                    "Key Responsibilities:\n"
                    "- Architect multi-agent workflows using LangChain, LangGraph, and Google Gemini models.\n"
                    "- Construct dense vector retrieval pipelines with ChromaDB and custom embedding stores.\n"
                    "- Deploy scalable GenAI microservices with FastAPI.\n\n"
                    "Requirements:\n"
                    "- 3+ years in AI / ML engineering with hands-on GenAI, Prompt Engineering, and RAG architectures.\n"
                    "- Strong Python 3.12 skills, vector search experience, and familiarity with LLM evaluation benchmarks."
                ),
                "created_by": recruiter.id
            },
            {
                "title": "[Experienced] Lead Full-Stack Engineer (React + Node.js / Python) (5+ Years)",
                "required_skills": ["TypeScript", "React", "Node.js", "Python", "PostgreSQL", "AWS", "GraphQL", "System Design", "Docker"],
                "jd_text": (
                    "Role: Lead Full-Stack Engineer\n"
                    "Experience: 5+ Years\n\n"
                    "Job Summary:\n"
                    "Lead end-to-end web architecture and mentor engineers across frontend and backend technologies.\n\n"
                    "Key Responsibilities:\n"
                    "- Architect resilient web apps using TypeScript, React, Node.js, and Python.\n"
                    "- Lead technical design reviews and establish coding best practices.\n"
                    "- Manage cloud infrastructure on AWS and optimize full-stack web performance.\n\n"
                    "Requirements:\n"
                    "- 5+ years of full-stack development experience.\n"
                    "- Strong architectural grasp of microfrontends, distributed APIs, and database modeling."
                ),
                "created_by": recruiter.id
            },
            {
                "title": "[Experienced] Senior DevOps & Kubernetes Platform Engineer (4-8 Years)",
                "required_skills": ["Kubernetes", "Docker", "Terraform", "AWS", "CI/CD", "GitHub Actions", "Prometheus", "Grafana", "Linux"],
                "jd_text": (
                    "Role: Senior DevOps & Platform Engineer\n"
                    "Experience: 4 - 8 Years\n\n"
                    "Job Summary:\n"
                    "Own our cloud infrastructure automation, Kubernetes clusters, and deployment pipelines.\n\n"
                    "Key Responsibilities:\n"
                    "- Provision and maintain multi-region infrastructure using Terraform on AWS/GCP.\n"
                    "- Manage production Kubernetes (EKS/GKE) clusters, Helm charts, and ingress controllers.\n"
                    "- Implement observability with Prometheus, Grafana, and ELK stack.\n\n"
                    "Requirements:\n"
                    "- 4+ years of hands-on DevOps and Infrastructure-as-Code experience.\n"
                    "- Strong Kubernetes administration and cloud security expertise."
                ),
                "created_by": recruiter.id
            },
            {
                "title": "[Experienced] Senior Data Engineer & Big Data Architect (4-7 Years)",
                "required_skills": ["Python", "Apache Spark", "PySpark", "Airflow", "Snowflake", "PostgreSQL", "Kafka", "Data Modeling", "Big Data"],
                "jd_text": (
                    "Role: Senior Data Engineer\n"
                    "Experience: 4 - 7 Years\n\n"
                    "Job Summary:\n"
                    "Build robust, real-time and batch data pipelines powering analytics and machine learning engines.\n\n"
                    "Key Responsibilities:\n"
                    "- Design scalable ETL/ELT pipelines using PySpark, Apache Airflow, and Kafka.\n"
                    "- Architect data warehouses and data lakes on Snowflake / BigQuery.\n"
                    "- Ensure data quality, governance, and low-latency query performance.\n\n"
                    "Requirements:\n"
                    "- 4+ years in data engineering with strong distributed systems knowledge.\n"
                    "- Advanced SQL and Python data pipeline development."
                ),
                "created_by": recruiter.id
            },
            {
                "title": "[Experienced] Senior Machine Learning / MLOps Engineer (3-6 Years)",
                "required_skills": ["Python", "PyTorch", "TensorFlow", "Scikit-Learn", "MLOps", "Docker", "MLflow", "FastAPI", "Deep Learning"],
                "jd_text": (
                    "Role: Senior Machine Learning Engineer\n"
                    "Experience: 3 - 6 Years\n\n"
                    "Job Summary:\n"
                    "Train, evaluate, and productionize deep learning and predictive models at scale.\n\n"
                    "Key Responsibilities:\n"
                    "- Develop NLP, classification, and ranking models using PyTorch / TensorFlow.\n"
                    "- Implement automated MLOps pipelines using MLflow, Docker, and CI/CD.\n"
                    "- Deploy low-latency model inference APIs using FastAPI.\n\n"
                    "Requirements:\n"
                    "- 3+ years experience designing, training, and deploying ML models in production.\n"
                    "- Strong statistical foundation and hands-on MLOps lifecycle experience."
                ),
                "created_by": recruiter.id
            },
            {
                "title": "[Experienced] Senior Mobile App Developer - Flutter / React Native (3-6 Years)",
                "required_skills": ["Flutter", "Dart", "React Native", "iOS", "Android", "REST API", "State Management", "Firebase"],
                "jd_text": (
                    "Role: Senior Mobile Developer\n"
                    "Experience: 3 - 6 Years\n\n"
                    "Job Summary:\n"
                    "Lead cross-platform mobile application development for Android and iOS devices.\n\n"
                    "Key Responsibilities:\n"
                    "- Build performant mobile apps using Flutter or React Native.\n"
                    "- Implement state management (Bloc/Provider/Redux) and secure offline caching.\n"
                    "- Publish and maintain apps on Google Play Store and Apple App Store.\n\n"
                    "Requirements:\n"
                    "- 3+ years of professional mobile development experience with published apps.\n"
                    "- Deep understanding of native iOS/Android bridge capabilities and UI animation."
                ),
                "created_by": recruiter.id
            },
            {
                "title": "[Experienced] Senior Cybersecurity & DevSecOps Engineer (4-8 Years)",
                "required_skills": ["Application Security", "OWASP", "Penetration Testing", "IAM", "Docker Security", "SIEM", "Python", "Vulnerability Management"],
                "jd_text": (
                    "Role: Senior Cybersecurity Engineer\n"
                    "Experience: 4 - 8 Years\n\n"
                    "Job Summary:\n"
                    "Safeguard enterprise infrastructure, applications, and customer data against cyber threats.\n\n"
                    "Key Responsibilities:\n"
                    "- Conduct vulnerability assessments, penetration tests, and threat modeling.\n"
                    "- Integrate SAST/DAST security scanning into CI/CD build pipelines.\n"
                    "- Implement zero-trust network policies, identity access management (IAM), and compliance.\n\n"
                    "Requirements:\n"
                    "- 4+ years in Information Security, DevSecOps, or Security Operations (SOC).\n"
                    "- Certifications like CEH, CISSP, or AWS Security Specialist are a major plus."
                ),
                "created_by": recruiter.id
            }
        ]

        seeded_count = 0
        for jd_data in all_tech_roles:
            existing_jd = db.query(JobDescription).filter(JobDescription.title == jd_data["title"]).first()
            if not existing_jd:
                jd = JobDescription(
                    title=jd_data["title"],
                    jd_text=jd_data["jd_text"],
                    required_skills=jd_data["required_skills"],
                    created_by=jd_data["created_by"]
                )
                db.add(jd)
                db.commit()
                db.refresh(jd)

                # Index in ChromaDB
                try:
                    rag_service.index_jd(
                        jd_id=jd.id,
                        title=jd.title,
                        jd_text=jd.jd_text,
                        required_skills=jd.required_skills
                    )
                except Exception as ex:
                    logger.warning(f"Could not index JD '{jd.title}' in ChromaDB: {ex}")

                seeded_count += 1
                logger.info(f"Seeded Job Description: '{jd.title}'")

        logger.info(f"Database initialization complete! Seeded {seeded_count} new job descriptions.")
    except Exception as e:
        logger.error(f"Error during database initialization: {e}", exc_info=True)
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    init_db()
