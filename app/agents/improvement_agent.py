import asyncio
import json
from typing import Dict, Any, Optional, List
import google.generativeai as genai
from app.core.config import settings
from app.core.logging import logger
from app.schemas.analysis import ResumeImprovementResult, SkillMatchResult
from app.schemas.resume import ParsedResumeData
from app.utils.helpers import parse_llm_json_response


class ImprovementAgent:
    """
    Agent responsible for analyzing gaps and providing actionable resume improvement suggestions:
      - Missing Skills Suggestions
      - Resume Enhancement Suggestions
      - Keyword Optimization Suggestions
      - Project Improvement Suggestions
    """

    def __init__(self, api_key: Optional[str] = None, model_name: Optional[str] = None):
        self.api_key = api_key or settings.GEMINI_API_KEY
        self.model_name = model_name or settings.GEMINI_MODEL
        if self.api_key:
            genai.configure(api_key=self.api_key)

    async def generate_improvements(
        self,
        parsed_resume: ParsedResumeData,
        skill_match: SkillMatchResult,
        jd_title: str,
        jd_text: str
    ) -> ResumeImprovementResult:
        """
        Generates structured resume enhancement suggestions using Gemini API.
        """
        if not self.api_key:
            logger.warning("Gemini API key is not configured. Running rule-based improvement adviser.")
            return self._heuristic_improvement_adviser(parsed_resume, skill_match, jd_title)

        prompt = f"""
You are an expert Resume Strategist, Career Coach, and ATS Optimization Specialist.
Review the candidate's profile against the target Job Description and provide high-impact, actionable recommendations to improve their resume and boost their ATS ranking.

=== CANDIDATE RESUME PROFILE ===
Candidate Name: {parsed_resume.name}
Extracted Skills: {json.dumps(parsed_resume.skills)}
Missing Skills Identified: {json.dumps(skill_match.missing_skills)}
Matched Skills: {json.dumps(skill_match.matched_skills)}
Projects: {json.dumps([p.dict() for p in parsed_resume.projects])}
Experience: {json.dumps([e.dict() for e in parsed_resume.experience])}

=== TARGET JOB DESCRIPTION ===
Job Title: {jd_title}
Job Text:
{jd_text}
==============================

Provide concrete, actionable bullet points for each category:
1. Missing Skills Suggestions (how to bridge technical skill gaps, certifications, quick-start projects)
2. Resume Enhancement Suggestions (action verbs, quantifiable metrics, formatting improvements, STAR bullet points)
3. Keyword Optimization Suggestions (exact keywords and phrasing from JD to include naturally)
4. Project Improvement Suggestions (ways to showcase architectural complexity, latency reductions, test coverage, and deployment pipelines)

Output must match EXACTLY this JSON structure:
{{
    "missing_skills_suggestions": [
        "Learn and earn certification in Docker & Kubernetes container orchestration.",
        "Build a hands-on project utilizing LangChain and Vector Databases to demonstrate GenAI competency."
    ],
    "resume_enhancement_suggestions": [
        "Quantify backend accomplishments (e.g. 'Improved API response latency by 42% through Redis caching').",
        "Start bullet points with strong action verbs like 'Architected', 'Spearheaded', 'Optimized'."
    ],
    "keyword_optimization_suggestions": [
        "Explicitly include 'PostgreSQL connection pooling' and 'FastAPI Dependency Injection' in skills section.",
        "Include industry standard keywords matching the JD such as 'RESTful Microservices' and 'CI/CD pipeline'."
    ],
    "project_improvement_suggestions": [
        "Add GitHub repository links and live deployed demo URLs to your project entries.",
        "Detail your data model design and throughput metrics under each project description."
    ]
}}
"""
        try:
            model = genai.GenerativeModel(
                model_name=self.model_name,
                generation_config={
                    "temperature": 0.3,
                    "response_mime_type": "application/json"
                }
            )
            response = await asyncio.to_thread(model.generate_content, prompt)
            data = parse_llm_json_response(response.text)
            return ResumeImprovementResult(**data)
        except Exception as e:
            logger.error(f"Gemini ImprovementAgent error: {e}. Falling back to rule-based adviser.")
            return self._heuristic_improvement_adviser(parsed_resume, skill_match, jd_title)

    def _heuristic_improvement_adviser(
        self,
        parsed_resume: ParsedResumeData,
        skill_match: SkillMatchResult,
        jd_title: str
    ) -> ResumeImprovementResult:
        """
        Rule-based improvement recommendations fallback.
        """
        missing = skill_match.missing_skills or ["Docker", "Kubernetes", "Redis", "CI/CD"]

        missing_suggestions = [
            f"Gain practical familiarity with '{skill}' and create a showcase repository on GitHub."
            for skill in missing[:3]
        ]
        if not missing_suggestions:
            missing_suggestions = ["Continuously update cloud certifications (AWS/GCP/Azure) to stand out."]

        return ResumeImprovementResult(
            missing_skills_suggestions=missing_suggestions,
            resume_enhancement_suggestions=[
                "Use the XYZ formula: 'Accomplished [X] as measured by [Y], by doing [Z]' for all experience bullets.",
                "Replace generic verbs with high-impact power words (e.g., 'Engineered', 'Orchestrated', 'Optimized').",
                "Ensure clean single-column ATS-friendly layout without tables, text boxes, or complex graphics."
            ],
            keyword_optimization_suggestions=[
                f"Incorporate exact terms from the '{jd_title}' posting into your core competency header.",
                "Ensure relevant frameworks (FastAPI, SQLAlchemy, Docker, PostgreSQL) appear in both skills and work experience sections.",
                "Standardize terminology to match industry keywords (e.g. 'RESTful APIs', 'Microservices', 'RAG')."
            ],
            project_improvement_suggestions=[
                "Include concrete engineering metrics: RPS handled, latency reduction, cost savings, or test coverage percentage.",
                "Highlight system architecture decisions, database indexing strategies, and Docker containerization.",
                "Provide public GitHub repository links and live deployment URLs for recruiters to review."
            ]
        )
