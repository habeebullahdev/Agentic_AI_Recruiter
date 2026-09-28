"""Initial database schema creation

Revision ID: 001_initial_tables
Revises: 
Create Date: 2026-09-28 12:00:00.000000

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '001_initial_tables'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Create users table
    op.create_table(
        'users',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.Column('email', sa.String(length=255), nullable=False),
        sa.Column('password_hash', sa.String(length=255), nullable=False),
        sa.Column('role', sa.Enum('ADMIN', 'RECRUITER', 'CANDIDATE', name='user_roles_enum'), nullable=False),
        sa.Column('is_active', sa.Boolean(), nullable=False, server_default='true'),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_users_email'), 'users', ['email'], unique=True)
    op.create_index(op.f('ix_users_id'), 'users', ['id'], unique=False)

    # Create resumes table
    op.create_table(
        'resumes',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=True),
        sa.Column('file_name', sa.String(length=255), nullable=False),
        sa.Column('file_path', sa.String(length=512), nullable=False),
        sa.Column('extracted_text', sa.Text(), nullable=False),
        sa.Column('parsed_data', sa.JSON(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_resumes_id'), 'resumes', ['id'], unique=False)
    op.create_index(op.f('ix_resumes_user_id'), 'resumes', ['user_id'], unique=False)

    # Create job_descriptions table
    op.create_table(
        'job_descriptions',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('title', sa.String(length=255), nullable=False),
        sa.Column('jd_text', sa.Text(), nullable=False),
        sa.Column('required_skills', sa.JSON(), nullable=True),
        sa.Column('created_by', sa.Integer(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(['created_by'], ['users.id'], ondelete='SET NULL'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_job_descriptions_id'), 'job_descriptions', ['id'], unique=False)
    op.create_index(op.f('ix_job_descriptions_title'), 'job_descriptions', ['title'], unique=False)
    op.create_index(op.f('ix_job_descriptions_created_by'), 'job_descriptions', ['created_by'], unique=False)

    # Create analysis_reports table
    op.create_table(
        'analysis_reports',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('resume_id', sa.Integer(), nullable=False),
        sa.Column('jd_id', sa.Integer(), nullable=False),
        sa.Column('ats_score', sa.Float(), nullable=False),
        sa.Column('match_percentage', sa.Float(), nullable=False),
        sa.Column('report_json', sa.JSON(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(['jd_id'], ['job_descriptions.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['resume_id'], ['resumes.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_analysis_reports_id'), 'analysis_reports', ['id'], unique=False)
    op.create_index(op.f('ix_analysis_reports_resume_id'), 'analysis_reports', ['resume_id'], unique=False)
    op.create_index(op.f('ix_analysis_reports_jd_id'), 'analysis_reports', ['jd_id'], unique=False)
    op.create_index(op.f('ix_analysis_reports_ats_score'), 'analysis_reports', ['ats_score'], unique=False)
    op.create_index(op.f('ix_analysis_reports_match_percentage'), 'analysis_reports', ['match_percentage'], unique=False)


def downgrade() -> None:
    op.drop_index(op.f('ix_analysis_reports_match_percentage'), table_name='analysis_reports')
    op.drop_index(op.f('ix_analysis_reports_ats_score'), table_name='analysis_reports')
    op.drop_index(op.f('ix_analysis_reports_jd_id'), table_name='analysis_reports')
    op.drop_index(op.f('ix_analysis_reports_resume_id'), table_name='analysis_reports')
    op.drop_index(op.f('ix_analysis_reports_id'), table_name='analysis_reports')
    op.drop_table('analysis_reports')

    op.drop_index(op.f('ix_job_descriptions_created_by'), table_name='job_descriptions')
    op.drop_index(op.f('ix_job_descriptions_title'), table_name='job_descriptions')
    op.drop_index(op.f('ix_job_descriptions_id'), table_name='job_descriptions')
    op.drop_table('job_descriptions')

    op.drop_index(op.f('ix_resumes_user_id'), table_name='resumes')
    op.drop_index(op.f('ix_resumes_id'), table_name='resumes')
    op.drop_table('resumes')

    op.drop_index(op.f('ix_users_id'), table_name='users')
    op.drop_index(op.f('ix_users_email'), table_name='users')
    op.drop_table('users')
