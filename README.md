# Agentic AI Recruiter

An AI-powered recruitment platform that streamlines resume screening, candidate evaluation, and job matching using Generative AI, RAG (Retrieval-Augmented Generation), and FastAPI.

## Features

- Resume Upload & Parsing
- AI-Powered Resume Analysis
- Job Description Matching
- ATS Score Generation
- Candidate Skill Extraction
- Semantic Search using Embeddings
- RAG-Based Candidate Evaluation
- Authentication & Authorization
- Recruiter Dashboard
- RESTful API Architecture

## Tech Stack

### Backend
- FastAPI
- Python
- SQLAlchemy
- PostgreSQL
- Alembic

### AI & GenAI
- OpenAI API
- Gemini API
- LangChain
- RAG
- Embeddings
- ChromaDB

### Authentication
- JWT Authentication

### Dev Tools
- Docker
- Git
- GitHub
- Postman

## Project Structure

```text
app/
alembic/
chroma_db/
uploads/
Dockerfile
requirements.txt
```

## Installation

```bash
git clone https://github.com/habeebullahdev/Agentic_AI_Recruiter.git
cd Agentic_AI_Recruiter
```

Create virtual environment:

```bash
python -m venv venv
```

Activate environment:

```bash
venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Create `.env` file:

```env
OPENAI_API_KEY=your_key
GEMINI_API_KEY=your_key
DATABASE_URL=your_database_url
SECRET_KEY=your_secret_key
```

Run the application:

```bash
uvicorn app.main:app --reload
```

## API Documentation

Swagger UI:

```text
http://localhost:8000/docs
```

ReDoc:

```text
http://localhost:8000/redoc
```

## Future Enhancements

- Multi-Agent Recruitment Workflow
- AI Interview Assistant
- Candidate Ranking Engine
- Automated Interview Scheduling
- HR Analytics Dashboard

## Author

Mohamed Habeebullah M

LinkedIn: Add Your LinkedIn URL

GitHub: https://github.com/habeebullahdev
