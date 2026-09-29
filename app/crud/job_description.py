"""CRUD helpers for job descriptions and the startup role catalog."""

from sqlalchemy import text
from sqlalchemy.orm import Session

from app.data.predefined_job_descriptions import PREDEFINED_JOB_DESCRIPTIONS
from app.models.job_description import JobDescription


def seed_predefined_job_descriptions(db: Session) -> int:
    """Insert predefined roles that are not already present by title."""
    try:
        if db.get_bind().dialect.name == "postgresql":
            db.execute(text("LOCK TABLE job_descriptions IN SHARE ROW EXCLUSIVE MODE"))

        existing_titles = {
            title
            for (title,) in db.query(JobDescription.title).all()
        }
        missing_roles = [
            role
            for role in PREDEFINED_JOB_DESCRIPTIONS
            if role["title"] not in existing_titles
        ]
        if not missing_roles:
            return 0

        db.add_all(
            JobDescription(
                title=role["title"],
                jd_text=role["jd_text"],
                required_skills=role["required_skills"],
            )
            for role in missing_roles
        )
        db.commit()
        return len(missing_roles)
    except Exception:
        db.rollback()
        raise


def get_job_description_options(db: Session) -> list[dict[str, int | str]]:
    """Return every job description's ID and title for selection controls."""
    rows = (
        db.query(JobDescription.id, JobDescription.title)
        .order_by(JobDescription.title.asc(), JobDescription.id.asc())
        .all()
    )
    return [{"id": row.id, "title": row.title} for row in rows]