from typing import Optional
from app.agents.ats_agent import ATSAgent
from app.schemas.analysis import ATSScoreBreakdown, SkillMatchResult
from app.schemas.resume import ParsedResumeData
from app.models.job_description import JobDescription


class ATSService:
    """
    Business service layer for ATS scoring evaluation.
    """

    def __init__(self, ats_agent: Optional[ATSAgent] = None):
        self.ats_agent = ats_agent or ATSAgent()

    async def calculate_ats_score(
        self,
        parsed_resume: ParsedResumeData,
        skill_match: SkillMatchResult,
        jd: JobDescription
    ) -> ATSScoreBreakdown:
        """
        Calculates weighted ATS breakdown for resume against target job description.
        """
        return await self.ats_agent.calculate_ats(
            parsed_resume=parsed_resume,
            skill_match=skill_match,
            jd_title=jd.title,
            jd_text=jd.jd_text
        )


ats_service = ATSService()
