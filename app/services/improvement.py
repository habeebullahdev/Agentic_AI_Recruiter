from typing import Optional
from app.agents.improvement_agent import ImprovementAgent
from app.schemas.analysis import ResumeImprovementResult, SkillMatchResult
from app.schemas.resume import ParsedResumeData
from app.models.job_description import JobDescription


class ImprovementService:
    """
    Business service layer for Resume Improvement and ATS optimization.
    """

    def __init__(self, improvement_agent: Optional[ImprovementAgent] = None):
        self.improvement_agent = improvement_agent or ImprovementAgent()

    async def generate_improvements(
        self,
        parsed_resume: ParsedResumeData,
        skill_match: SkillMatchResult,
        jd: JobDescription
    ) -> ResumeImprovementResult:
        """
        Generates actionable suggestions to optimize candidate resume and bridge skill gaps.
        """
        return await self.improvement_agent.generate_improvements(
            parsed_resume=parsed_resume,
            skill_match=skill_match,
            jd_title=jd.title,
            jd_text=jd.jd_text
        )


improvement_service = ImprovementService()
