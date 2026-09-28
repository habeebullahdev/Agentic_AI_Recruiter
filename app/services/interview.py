from typing import Optional, List
from app.agents.interview_agent import InterviewAgent
from app.schemas.analysis import InterviewQuestionsResult
from app.schemas.resume import ParsedResumeData
from app.models.job_description import JobDescription


class InterviewService:
    """
    Business service layer for Interview Question Generation.
    """

    def __init__(self, interview_agent: Optional[InterviewAgent] = None):
        self.interview_agent = interview_agent or InterviewAgent()

    async def generate_interview_questions(
        self,
        parsed_resume: ParsedResumeData,
        jd: JobDescription,
        missing_skills: Optional[List[str]] = None
    ) -> InterviewQuestionsResult:
        """
        Generates tailored interview questions across technical, project, behavioral, and HR categories.
        """
        return await self.interview_agent.generate_questions(
            parsed_resume=parsed_resume,
            jd_title=jd.title,
            jd_text=jd.jd_text,
            missing_skills=missing_skills
        )


interview_service = InterviewService()
