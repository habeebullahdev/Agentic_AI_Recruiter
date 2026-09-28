import sys
import io
import json
from fastapi.testclient import TestClient
from main import app
from app.core.config import settings

# Force utf-8 stdout on Windows console
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")

client = TestClient(app)

def run_all_checks():
    print("\n" + "="*60)
    print("RUNNING FULL END-TO-END VALIDATION SUITE")
    print("="*60)

    # 1. Health Check
    print("\n[1/6] Checking Health Endpoint (/health)...")
    res = client.get("/health")
    assert res.status_code == 200, f"Health check failed: {res.text}"
    print(f"[OK] Health OK: {res.json()}")

    # 2. Root Endpoint
    print("\n[2/6] Checking Root Endpoint (/)...")
    res = client.get("/")
    assert res.status_code == 200, f"Root endpoint failed: {res.text}"
    print(f"[OK] Root OK: {res.json()}")

    # 3. Authentication Check
    print("\n[3/6] Testing Login (POST /api/v1/auth/login)...")
    login_payload = {
        "email": "recruiter@recruitmentai.com",
        "password": "RecruiterPass123!"
    }
    res = client.post("/api/v1/auth/login", json=login_payload)
    assert res.status_code == 200, f"Login failed: {res.text}"
    token_data = res.json()
    token = token_data["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    print(f"[OK] Login OK! Access Token generated for: {token_data['user']['email']}")

    # 4. Job Descriptions Check
    print("\n[4/6] Testing Job Descriptions (GET /api/v1/jd/)...")
    res = client.get("/api/v1/jd/", headers=headers)
    assert res.status_code == 200, f"List JDs failed: {res.text}"
    jds = res.json()["items"]
    assert len(jds) > 0, "No Job Descriptions found!"
    target_jd = jds[0]
    print(f"[OK] Found {len(jds)} Job Descriptions. Target JD: ID {target_jd['id']} - '{target_jd['title']}'")

    # 5. Resume Upload & Multi-Agent Parsing Check
    print("\n[5/6] Testing Resume PDF Upload & ResumeAgent (POST /api/v1/resume/upload)...")
    sample_pdf_content = b"""%PDF-1.4
1 0 obj
<< /Type /Catalog /Pages 2 0 R >>
endobj
2 0 obj
<< /Type /Pages /Kids [3 0 R] /Count 1 >>
endobj
3 0 obj
<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] /Contents 4 0 R /Resources << /Font << /F1 5 0 R >> >> >>
endobj
4 0 obj
<< /Length 285 >>
stream
BT
/F1 12 Tf
72 712 Td
(Jane Doe - Senior Backend Engineer) Tj
0 -20 Td
(Email: jane.doe@example.com | Phone: +1 555 0199) Tj
0 -20 Td
(Skills: Python, FastAPI, PostgreSQL, SQLAlchemy, Docker, Redis, REST API, CI/CD) Tj
0 -20 Td
(Experience: Senior Engineer at TechCorp 2021-Present. Architected FastAPI services.) Tj
0 -20 Td
(Education: BS in Computer Science, Stanford University 2020) Tj
ET
endstream
endobj
5 0 obj
<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>
endobj
xref
0 6
0000000000 65535 f 
0000000009 00000 n 
0000000058 00000 n 
0000000115 00000 n 
0000000227 00000 n 
0000000564 00000 n 
trailer
<< /Size 6 /Root 1 0 R >>
startxref
635
%%EOF"""

    files = {"file": ("jane_doe_resume.pdf", sample_pdf_content, "application/pdf")}
    res = client.post("/api/v1/resume/upload", files=files, headers=headers)
    assert res.status_code == 201, f"Resume upload failed: {res.text}"
    resume_data = res.json()["data"]
    resume_id = resume_data["id"]
    print(f"[OK] Resume Upload & Parsing OK! Resume ID: {resume_id}, Candidate: {resume_data['parsed_data']['name']}")
    print(f"     Extracted Skills: {resume_data['parsed_data']['skills']}")

    # 6. Multi-Agent Analysis Pipeline Check
    print("\n[6/6] Testing Full Multi-Agent Pipeline (POST /api/v1/analysis/run)...")
    analysis_req = {
        "resume_id": resume_id,
        "jd_id": target_jd["id"]
    }
    res = client.post("/api/v1/analysis/run", json=analysis_req, headers=headers)
    assert res.status_code == 201, f"Analysis run failed: {res.text}"
    analysis_res = res.json()["data"]
    report = analysis_res["report_json"]

    print(f"[OK] Multi-Agent Pipeline Execution Complete!")
    print(f"     ATS Score: {analysis_res['ats_score']}/100")
    print(f"     Match %: {analysis_res['match_percentage']}%")
    print(f"     Matched Skills: {report['skill_match']['matched_skills']}")
    print(f"     Missing Skills: {report['skill_match']['missing_skills']}")
    print(f"     Sample Technical Question: {report['interview_questions']['technical_questions'][0]}")
    print(f"     Sample Resume Tip: {report['improvements']['resume_enhancement_suggestions'][0]}")

    print("\n" + "="*60)
    print("ALL SYSTEMS AND AGENTS ARE FULLY OPERATIONAL AND VERIFIED!")
    print("="*60 + "\n")

if __name__ == "__main__":
    run_all_checks()
