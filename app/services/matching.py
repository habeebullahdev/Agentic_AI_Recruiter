from typing import Optional, List
from sqlalchemy.orm import Session
from app.agents.matcher_agent import MatcherAgent
from app.schemas.analysis import SkillMatchResult
from app.schemas.resume import ParsedResumeData
from app.models.resume import Resume
from app.models.job_description import JobDescription
from app.core.exceptions import EntityNotFoundException


class MatchingService:
    """
    Business service layer for Skill Matching.
    """

    def __init__(self, matcher_agent: Optional[MatcherAgent] = None):
        self.matcher_agent = matcher_agent or MatcherAgent()

    async def match_resume_and_jd(
        self,
        parsed_resume: ParsedResumeData,
        jd: JobDescription
    ) -> SkillMatchResult:
        """
        Runs skill comparison between candidate resume and job description.
        """
        return await self.matcher_agent.match_skills(
            parsed_resume=parsed_resume,
            jd_title=jd.title,
            jd_text=jd.jd_text,
            required_skills=jd.required_skills
        )


matching_service = MatchingService()
