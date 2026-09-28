import asyncio
import json
from typing import Dict, Any, Optional, List
import google.generativeai as genai
from app.core.config import settings
from app.core.logging import logger
from app.schemas.analysis import InterviewQuestionsResult
from app.schemas.resume import ParsedResumeData
from app.utils.helpers import parse_llm_json_response


class InterviewAgent:
    """
    Agent responsible for generating tailored, high-signal interview questions:
      - Technical Questions
      - Project Questions
      - Behavioral Questions
      - HR Questions
    """

    def __init__(self, api_key: Optional[str] = None, model_name: Optional[str] = None):
        self.api_key = api_key or settings.GEMINI_API_KEY
        self.model_name = model_name or settings.GEMINI_MODEL
        if self.api_key:
            genai.configure(api_key=self.api_key)

    async def generate_questions(
        self,
        parsed_resume: ParsedResumeData,
        jd_title: str,
        jd_text: str,
        missing_skills: Optional[List[str]] = None
    ) -> InterviewQuestionsResult:
        """
        Generates categorized interview questions using Gemini API.
        """
        if not self.api_key:
            logger.warning("Gemini API key is not configured. Running structured template question generator.")
            return self._heuristic_question_generator(parsed_resume, jd_title)

        prompt = f"""
You are an expert Technical Interviewer and Senior Hiring Manager.
Create tailored, deep interview questions for this candidate applying for the role of '{jd_title}'.

=== CANDIDATE RESUME PROFILE ===
Candidate Name: {parsed_resume.name}
Skills: {json.dumps(parsed_resume.skills)}
Projects: {json.dumps([p.dict() for p in parsed_resume.projects])}
Experience: {json.dumps([e.dict() for e in parsed_resume.experience])}
Identified Missing Skills: {json.dumps(missing_skills or [])}

=== TARGET JOB DESCRIPTION ===
Job Title: {jd_title}
Job Text:
{jd_text}
==============================

Generate 3-5 high quality, specific questions for each of the 4 categories:
1. Technical Questions (architecture, coding concepts, core frameworks)
2. Project Questions (deep-dive into specific projects on their resume and architectural trade-offs)
3. Behavioral Questions (STAR methodology, conflict resolution, ownership, teamwork)
4. HR Questions (cultural alignment, career goals, remote/office preferences, salary and availability)

Output must match EXACTLY this JSON structure:
{{
    "technical_questions": [
        "Explain how you handle asynchronous I/O and connection pooling in FastAPI with SQLAlchemy 2.0.",
        "How would you optimize PostgreSQL queries with complex joins and JSONB indexing?"
    ],
    "project_questions": [
        "In your project, what was the biggest scalability bottleneck you encountered and how did you resolve it?",
        "Walk us through your design decisions regarding microservices communication vs monolithic architecture."
    ],
    "behavioral_questions": [
        "Describe a situation where you had a disagreement with a team member about technical architecture. How was it resolved?",
        "Tell us about a time a production issue occurred due to your code. How did you handle incident triage?"
    ],
    "hr_questions": [
        "What motivated you to apply for this specific position?",
        "What are your expectations regarding team culture, growth, and work flexibility?"
    ]
}}
"""
        try:
            model = genai.GenerativeModel(
                model_name=self.model_name,
                generation_config={
                    "temperature": 0.4,
                    "response_mime_type": "application/json"
                }
            )
            response = await asyncio.to_thread(model.generate_content, prompt)
            data = parse_llm_json_response(response.text)
            return InterviewQuestionsResult(**data)
        except Exception as e:
            logger.error(f"Gemini InterviewAgent error: {e}. Falling back to template generator.")
            return self._heuristic_question_generator(parsed_resume, jd_title)

    def _heuristic_question_generator(self, parsed_resume: ParsedResumeData, jd_title: str) -> InterviewQuestionsResult:
        """
        Rule-based interview question generator fallback.
        """
        skills = parsed_resume.skills or ["Python", "FastAPI", "SQL"]
        primary_skill = skills[0] if skills else "Software Engineering"
        proj_title = parsed_resume.projects[0].title if parsed_resume.projects else "your recent software project"

        return InterviewQuestionsResult(
            technical_questions=[
                f"How would you design a scalable backend service using {primary_skill} to handle 10,000 requests per second?",
                f"What are the best practices for transaction management and connection pooling when using SQLAlchemy with PostgreSQL?",
                "Can you explain the difference between synchronous and asynchronous request handling in FastAPI?",
                "How do you implement secure JWT authentication and token revocation in a distributed backend?"
            ],
            project_questions=[
                f"In '{proj_title}', what were the key architectural challenges and how did you address them?",
                "If you had to rebuild this project today with higher scale requirements, what would you change?",
                "How did you approach database schema design, indexing, and migration management for your project?"
            ],
            behavioral_questions=[
                "Describe a challenging technical deadline you faced. How did you prioritize tasks to deliver on time?",
                "Can you share an instance where you mentored a junior engineer or championed a code quality improvement?",
                "Tell us about a time you had to adapt quickly to an ambiguous project requirement."
            ],
            hr_questions=[
                f"What specifically excites you about the {jd_title} role at our company?",
                "What are your compensation expectations and notice period?",
                "How do you ensure effective communication and collaboration in a hybrid or remote engineering team?"
            ]
        )
