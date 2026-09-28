import asyncio
import json
from typing import Dict, Any, Optional
import google.generativeai as genai
from app.core.config import settings
from app.core.logging import logger
from app.schemas.analysis import ATSScoreBreakdown, ATSComponentScore, SkillMatchResult
from app.schemas.resume import ParsedResumeData
from app.utils.helpers import parse_llm_json_response


class ATSAgent:
    """
    Agent responsible for calculating an accurate Applicant Tracking System (ATS) score.
    Weights:
      - Skill Match: 50%
      - Projects Relevance: 20%
      - Experience Relevance: 20%
      - Education Background: 10%
    """

    def __init__(self, api_key: Optional[str] = None, model_name: Optional[str] = None):
        self.api_key = api_key or settings.GEMINI_API_KEY
        self.model_name = model_name or settings.GEMINI_MODEL
        if self.api_key:
            genai.configure(api_key=self.api_key)

    async def calculate_ats(
        self,
        parsed_resume: ParsedResumeData,
        skill_match: SkillMatchResult,
        jd_title: str,
        jd_text: str
    ) -> ATSScoreBreakdown:
        """
        Calculates ATS component scores and final weighted score using Gemini API.
        """
        if not self.api_key:
            logger.warning("Gemini API key is not configured. Running mathematical ATS scorer.")
            return self._heuristic_ats_calculator(parsed_resume, skill_match)

        prompt = f"""
You are a Senior Talent Screening and ATS Scoring Evaluation Agent.
Calculate a comprehensive ATS score for the candidate based on their match to the target Job Description.

Formula & Weights:
1. Skill Match = 50% weight
2. Projects Relevance = 20% weight
3. Experience Relevance = 20% weight
4. Education Relevance = 10% weight
Total ATS Score = (Skill * 0.50) + (Projects * 0.20) + (Experience * 0.20) + (Education * 0.10)

=== CANDIDATE RESUME PROFILE ===
Candidate Name: {parsed_resume.name}
Extracted Skills: {json.dumps(parsed_resume.skills)}
Skill Match Percentage: {skill_match.match_percentage}%
Matched Skills: {json.dumps(skill_match.matched_skills)}
Missing Skills: {json.dumps(skill_match.missing_skills)}
Projects: {json.dumps([p.dict() for p in parsed_resume.projects])}
Experience: {json.dumps([e.dict() for e in parsed_resume.experience])}
Education: {json.dumps([ed.dict() for ed in parsed_resume.education])}

=== TARGET JOB DESCRIPTION ===
Job Title: {jd_title}
Job Text:
{jd_text}
==============================

Evaluate each component on a scale of 0 to 100, then compute the exact total weighted ATS score.
Output must match EXACTLY this JSON structure:
{{
    "ats_score": 87.0,
    "skill_match": {{
        "score": 90.0,
        "weight": 50.0,
        "weighted_score": 45.0,
        "reasoning": "Strong match on primary backend skills and frameworks."
    }},
    "projects": {{
        "score": 85.0,
        "weight": 20.0,
        "weighted_score": 17.0,
        "reasoning": "Projects demonstrate production backend and API architecture."
    }},
    "experience": {{
        "score": 85.0,
        "weight": 20.0,
        "weighted_score": 17.0,
        "reasoning": "Relevant software engineering experience matching role expectations."
    }},
    "education": {{
        "score": 80.0,
        "weight": 10.0,
        "weighted_score": 8.0,
        "reasoning": "Relevant degree in Computer Science or related engineering discipline."
    }},
    "overall_summary": "High suitability candidate with strong alignment in core stack and project experience."
}}
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
            return ATSScoreBreakdown(**data)
        except Exception as e:
            logger.error(f"Gemini ATSAgent error: {e}. Falling back to mathematical scorer.")
            return self._heuristic_ats_calculator(parsed_resume, skill_match)

    def _heuristic_ats_calculator(
        self,
        parsed_resume: ParsedResumeData,
        skill_match: SkillMatchResult
    ) -> ATSScoreBreakdown:
        """
        Strict mathematical ATS scoring based on exact formula weights.
        """
        # 1. Skill Score (50%)
        skill_score = float(skill_match.match_percentage)

        # 2. Projects Score (20%)
        has_projects = len(parsed_resume.projects) > 0
        projects_score = 85.0 if has_projects else 50.0

        # 3. Experience Score (20%)
        has_experience = len(parsed_resume.experience) > 0
        experience_score = 80.0 if has_experience else 50.0

        # 4. Education Score (10%)
        has_education = len(parsed_resume.education) > 0
        education_score = 85.0 if has_education else 60.0

        # Weighted calculation
        weighted_skill = round(skill_score * 0.50, 2)
        weighted_proj = round(projects_score * 0.20, 2)
        weighted_exp = round(experience_score * 0.20, 2)
        weighted_edu = round(education_score * 0.10, 2)

        total_ats = round(weighted_skill + weighted_proj + weighted_exp + weighted_edu, 1)

        return ATSScoreBreakdown(
            ats_score=min(100.0, max(0.0, total_ats)),
            skill_match=ATSComponentScore(
                score=skill_score,
                weight=50.0,
                weighted_score=weighted_skill,
                reasoning=f"Matched {len(skill_match.matched_skills)} required competencies."
            ),
            projects=ATSComponentScore(
                score=projects_score,
                weight=20.0,
                weighted_score=weighted_proj,
                reasoning="Demonstrated technical application in projects."
            ),
            experience=ATSComponentScore(
                score=experience_score,
                weight=20.0,
                weighted_score=weighted_exp,
                reasoning="Work history and technical responsibilities align with expectations."
            ),
            education=ATSComponentScore(
                score=education_score,
                weight=10.0,
                weighted_score=weighted_edu,
                reasoning="Academic qualification meets standard entry criteria."
            ),
            overall_summary=f"Calculated ATS score of {total_ats}/100 with strongest contributor being skill matching."
        )
