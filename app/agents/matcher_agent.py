import asyncio
import json
from typing import Dict, Any, Optional, List
import google.generativeai as genai
from app.core.config import settings
from app.core.logging import logger
from app.schemas.analysis import SkillMatchResult
from app.schemas.resume import ParsedResumeData
from app.utils.helpers import parse_llm_json_response


class MatcherAgent:
    """
    Agent responsible for matching resume skills and candidate qualifications against Job Descriptions.
    Calculates match percentage, matched skills, missing skills, and key candidate strengths.
    """

    def __init__(self, api_key: Optional[str] = None, model_name: Optional[str] = None):
        self.api_key = api_key or settings.GEMINI_API_KEY
        self.model_name = model_name or settings.GEMINI_MODEL
        if self.api_key:
            genai.configure(api_key=self.api_key)

    async def match_skills(
        self,
        parsed_resume: ParsedResumeData,
        jd_title: str,
        jd_text: str,
        required_skills: Optional[List[str]] = None
    ) -> SkillMatchResult:
        """
        Executes semantic skill matching using Gemini API.
        """
        if not self.api_key:
            logger.warning("Gemini API key is not configured. Running rule-based skill matcher.")
            return self._heuristic_matcher(parsed_resume, jd_text, required_skills)

        prompt = f"""
You are an expert AI Recruitment Skill Matcher and Technical Talent Evaluator.
Compare the candidate's parsed resume profile against the target Job Description (JD).

=== CANDIDATE RESUME PROFILE ===
Candidate Name: {parsed_resume.name}
Extracted Skills: {json.dumps(parsed_resume.skills)}
Projects: {json.dumps([p.dict() for p in parsed_resume.projects])}
Experience: {json.dumps([e.dict() for e in parsed_resume.experience])}
Education: {json.dumps([ed.dict() for ed in parsed_resume.education])}

=== TARGET JOB DESCRIPTION ===
Job Title: {jd_title}
Explicit Required Skills: {json.dumps(required_skills or [])}
Job Description Text:
{jd_text}
==============================

Perform a rigorous, fair technical skill comparison.
Output must match EXACTLY this JSON structure:
{{
    "match_percentage": 85.0,
    "matched_skills": ["Skill A", "Skill B"],
    "missing_skills": ["Skill C", "Skill D"],
    "strong_skills": ["Skill A", "Skill E"],
    "analysis_notes": "Concise summary explaining the match score and critical skill gaps."
}}
Note: "match_percentage" must be a float between 0.0 and 100.0.
"""
        try:
            model = genai.GenerativeModel(
                model_name=self.model_name,
                generation_config={
                    "temperature": 0.2,
                    "response_mime_type": "application/json"
                }
            )
            response = await asyncio.to_thread(model.generate_content, prompt)
            data = parse_llm_json_response(response.text)
            return SkillMatchResult(**data)
        except Exception as e:
            logger.error(f"Gemini MatcherAgent error: {e}. Falling back to rule-based matcher.")
            return self._heuristic_matcher(parsed_resume, jd_text, required_skills)

    def _heuristic_matcher(
        self,
        parsed_resume: ParsedResumeData,
        jd_text: str,
        required_skills: Optional[List[str]] = None
    ) -> SkillMatchResult:
        """
        Rule-based heuristic matching between resume skills and job description keywords.
        """
        candidate_skills = [s.strip().lower() for s in (parsed_resume.skills or [])]

        # If explicit required skills provided, use them; otherwise extract from text
        target_skills = [s.strip() for s in (required_skills or [])]
        if not target_skills:
            common_kw = [
                "Python", "FastAPI", "SQLAlchemy", "PostgreSQL", "Docker", "Kubernetes", "AWS",
                "LangChain", "LLM", "REST API", "Git", "CI/CD", "Redis", "Kafka", "Microservices"
            ]
            target_skills = [kw for kw in common_kw if kw.lower() in jd_text.lower()]

        if not target_skills:
            target_skills = ["Python", "FastAPI", "SQLAlchemy", "PostgreSQL"]

        matched = []
        missing = []
        for req in target_skills:
            if any(req.lower() in cand or cand in req.lower() for cand in candidate_skills):
                matched.append(req)
            elif req.lower() in jd_text.lower() and any(req.lower() in str(parsed_resume.dict()).lower() for _ in [1]):
                matched.append(req)
            else:
                missing.append(req)

        match_pct = round((len(matched) / max(len(target_skills), 1)) * 100, 1)

        return SkillMatchResult(
            match_percentage=min(100.0, max(0.0, match_pct)),
            matched_skills=matched,
            missing_skills=missing,
            strong_skills=matched[:3] if matched else ["Software Engineering"],
            analysis_notes=f"Candidate matched {len(matched)} of {len(target_skills)} core technical requirements."
        )
