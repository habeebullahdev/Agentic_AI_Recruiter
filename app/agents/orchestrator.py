import asyncio
from typing import Dict, Any, Optional
from app.core.logging import logger
from app.core.exceptions import AIProcessingException
from app.agents.resume_agent import ResumeAgent
from app.agents.matcher_agent import MatcherAgent
from app.agents.ats_agent import ATSAgent
from app.agents.interview_agent import InterviewAgent
from app.agents.improvement_agent import ImprovementAgent
from app.schemas.resume import ParsedResumeData
from app.schemas.analysis import (
    FullAnalysisReportData,
    SkillMatchResult,
    ATSScoreBreakdown,
    InterviewQuestionsResult,
    ResumeImprovementResult
)


class RecruitmentWorkflowOrchestrator:
    """
    Multi-Agent Workflow Orchestrator.
    Coordinates sequential and parallel execution of AI recruitment agents:
      1. Resume Parsing Agent (ResumeAgent)
      2. Skill Matching Agent (MatcherAgent)
      3. ATS Scoring Agent (ATSAgent)
      4. Interview Question Generator Agent (InterviewAgent)
      5. Resume Improvement Agent (ImprovementAgent)
      6. Aggregated Final Analysis Report
    """

    def __init__(
        self,
        resume_agent: Optional[ResumeAgent] = None,
        matcher_agent: Optional[MatcherAgent] = None,
        ats_agent: Optional[ATSAgent] = None,
        interview_agent: Optional[InterviewAgent] = None,
        improvement_agent: Optional[ImprovementAgent] = None,
    ):
        self.resume_agent = resume_agent or ResumeAgent()
        self.matcher_agent = matcher_agent or MatcherAgent()
        self.ats_agent = ats_agent or ATSAgent()
        self.interview_agent = interview_agent or InterviewAgent()
        self.improvement_agent = improvement_agent or ImprovementAgent()

    async def run_full_pipeline(
        self,
        resume_text: str,
        jd_title: str,
        jd_text: str,
        existing_parsed_data: Optional[Dict[str, Any]] = None,
        required_skills: Optional[list] = None
    ) -> FullAnalysisReportData:
        """
        Executes the complete multi-agent recruitment analysis pipeline.
        """
        logger.info(f"Starting Multi-Agent Recruitment Pipeline for target role: '{jd_title}'")

        # Step 1: Resume Parsing Agent (or use cached/existing structured data)
        if existing_parsed_data:
            logger.info("Using pre-parsed resume data.")
            parsed_resume = ParsedResumeData(**existing_parsed_data)
        else:
            logger.info("Executing Step 1: ResumeAgent parsing...")
            parsed_resume = await self.resume_agent.parse_resume(resume_text)

        # Step 2: Skill Matcher Agent
        logger.info("Executing Step 2: MatcherAgent skill comparison...")
        skill_match: SkillMatchResult = await self.matcher_agent.match_skills(
            parsed_resume=parsed_resume,
            jd_title=jd_title,
            jd_text=jd_text,
            required_skills=required_skills
        )

        # Step 3: ATS Scoring Agent
        logger.info("Executing Step 3: ATSAgent weighted scoring...")
        ats_breakdown: ATSScoreBreakdown = await self.ats_agent.calculate_ats(
            parsed_resume=parsed_resume,
            skill_match=skill_match,
            jd_title=jd_title,
            jd_text=jd_text
        )

        # Steps 4 & 5: Run Interview Agent and Improvement Agent concurrently for optimal performance
        logger.info("Executing Steps 4 & 5: InterviewAgent & ImprovementAgent concurrently...")
        interview_task = self.interview_agent.generate_questions(
            parsed_resume=parsed_resume,
            jd_title=jd_title,
            jd_text=jd_text,
            missing_skills=skill_match.missing_skills
        )
        improvement_task = self.improvement_agent.generate_improvements(
            parsed_resume=parsed_resume,
            skill_match=skill_match,
            jd_title=jd_title,
            jd_text=jd_text
        )

        interview_questions, improvements = await asyncio.gather(
            interview_task,
            improvement_task,
            return_exceptions=False
        )

        logger.info(
            f"Multi-Agent Pipeline completed successfully. ATS Score: {ats_breakdown.ats_score}, Match: {skill_match.match_percentage}%"
        )

        # Step 6: Construct Unified Multi-Agent Report
        return FullAnalysisReportData(
            candidate_name=parsed_resume.name,
            job_title=jd_title,
            ats_score=ats_breakdown.ats_score,
            match_percentage=skill_match.match_percentage,
            parsed_resume=parsed_resume.dict(),
            skill_match=skill_match,
            ats_breakdown=ats_breakdown,
            interview_questions=interview_questions,
            improvements=improvements
        )
