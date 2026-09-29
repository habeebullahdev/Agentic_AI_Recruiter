from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse

router = APIRouter(tags=["Web UI Dashboard"])

HTML_CONTENT = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Agentic AI Recruitment Assistant - Dashboard</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap" rel="stylesheet">
    <style>
        body { font-family: 'Plus Jakarta Sans', sans-serif; background-color: #0b0f19; color: #f3f4f6; }
        .glass-card { background: rgba(17, 24, 39, 0.85); backdrop-filter: blur(12px); border: 1px solid rgba(55, 65, 81, 0.5); }
        .gradient-text { background: linear-gradient(135deg, #60a5fa 0%, #a855f7 50%, #ec4899 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
        .tab-btn.active { background: #3b82f6; color: white; }
    </style>
</head>
<body class="min-h-screen flex flex-col">

    <!-- Header / Navbar -->
    <header class="border-b border-gray-800 glass-card sticky top-0 z-50">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
            <div class="flex items-center space-x-3">
                <div class="w-10 h-10 rounded-xl bg-gradient-to-tr from-blue-600 via-indigo-600 to-purple-600 flex items-center justify-center shadow-lg shadow-blue-500/30">
                    <i class="fa-solid fa-robot text-white text-lg"></i>
                </div>
                <div>
                    <span class="font-bold text-lg text-white">Recruit<span class="text-blue-500">AI</span></span>
                    <span class="text-xs ml-2 px-2 py-0.5 rounded-full bg-blue-500/10 text-blue-400 border border-blue-500/20 font-medium">Agentic v1.0</span>
                </div>
            </div>
            <div class="flex items-center space-x-4">
                <a href="/docs" target="_blank" class="text-xs font-semibold px-3 py-1.5 rounded-lg bg-gray-800 hover:bg-gray-700 text-gray-300 border border-gray-700 transition flex items-center">
                    <i class="fa-solid fa-book mr-1.5 text-blue-400"></i> Swagger API Docs
                </a>
                <a href="/health" target="_blank" class="text-xs font-semibold px-3 py-1.5 rounded-lg bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 flex items-center">
                    <span class="w-2 h-2 rounded-full bg-emerald-400 animate-pulse mr-1.5"></span> System Online
                </a>
            </div>
        </div>
    </header>

    <!-- Main Content Container -->
    <main class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 flex-1 w-full">
        
        <!-- Hero Title -->
        <div class="text-center max-w-3xl mx-auto mb-10">
            <h1 class="text-3xl sm:text-4xl font-extrabold tracking-tight mb-3">
                Autonomous <span class="gradient-text">Agentic Recruitment</span> Platform
            </h1>
            <p class="text-gray-400 text-sm sm:text-base">
                Upload candidate resume PDF, run multi-agent AI pipeline for automated parsing, ATS scoring (50/20/20/10), tailored interview questions, and enhancement suggestions.
            </p>
        </div>

        <!-- Workflow Grid -->
        <div class="grid grid-cols-1 lg:grid-cols-12 gap-8">
            
            <!-- Left Panel: Upload & Config (5 cols) -->
            <div class="lg:col-span-5 space-y-6">
                
                <div class="glass-card rounded-2xl p-6 shadow-xl border border-gray-800">
                    <h2 class="text-base font-bold text-white mb-4 flex items-center">
                        <i class="fa-solid fa-file-arrow-up text-blue-500 mr-2"></i> Step 1: Upload Candidate Resume
                    </h2>
                    
                    <!-- Drag and Drop Box -->
                    <div id="dropZone" class="border-2 border-dashed border-gray-700 hover:border-blue-500 rounded-xl p-6 text-center cursor-pointer transition bg-gray-900/50 hover:bg-blue-500/5 group">
                        <input type="file" id="resumeInput" accept=".pdf" class="hidden">
                        <div class="w-12 h-12 mx-auto mb-3 rounded-full bg-blue-500/10 text-blue-400 flex items-center justify-center group-hover:scale-110 transition">
                            <i class="fa-solid fa-cloud-arrow-up text-xl"></i>
                        </div>
                        <p class="text-sm font-semibold text-gray-200" id="fileStatusText">Click or Drag & Drop Resume PDF</p>
                        <p class="text-xs text-gray-500 mt-1">Supports PDF format (Max 10MB)</p>
                    </div>

                    <div id="uploadedInfo" class="hidden mt-4 p-3 bg-blue-950/40 border border-blue-800/40 rounded-lg text-xs text-blue-300 flex items-center justify-between">
                        <div class="flex items-center space-x-2 truncate">
                            <i class="fa-solid fa-circle-check text-blue-400"></i>
                            <span id="uploadedFileName" class="truncate font-medium">resume.pdf</span>
                        </div>
                        <span id="resumeIdBadge" class="bg-blue-500/20 px-2 py-0.5 rounded text-blue-300 font-mono text-[11px]">ID #1</span>
                    </div>

                    <!-- Target Job Description -->
                    <div class="mt-6">
                        <label class="block text-xs font-bold text-gray-300 uppercase tracking-wider mb-2 flex items-center justify-between">
                            <span><i class="fa-solid fa-briefcase text-purple-400 mr-1.5"></i> Target Job Description</span>
                            <span class="text-[11px] text-gray-500 font-normal">Select open position</span>
                        </label>
                        <select id="jdSelect" class="w-full bg-gray-900 border border-gray-700 rounded-xl px-4 py-2.5 text-sm text-gray-200 focus:outline-none focus:border-blue-500">
                            <option value="" disabled selected>Loading Job Descriptions...</option>
                        </select>
                    </div>

                    <!-- Analyze Button -->
                    <button id="analyzeBtn" onclick="runAnalysis()" class="mt-6 w-full py-3.5 px-4 rounded-xl bg-gradient-to-r from-blue-600 via-indigo-600 to-purple-600 hover:from-blue-500 hover:to-purple-500 text-white font-bold text-sm shadow-lg shadow-indigo-600/30 transition flex items-center justify-center space-x-2 disabled:opacity-50 disabled:cursor-not-allowed">
                        <i class="fa-solid fa-wand-magic-sparkles"></i>
                        <span id="analyzeBtnText">Run Multi-Agent Analysis</span>
                    </button>
                    
                    <div id="statusAlert" class="hidden mt-4 p-3 rounded-xl text-xs flex items-center space-x-2"></div>
                </div>

                <!-- Pipeline Status Tracker -->
                <div class="glass-card rounded-2xl p-5 border border-gray-800/80">
                    <h3 class="text-xs font-bold text-gray-400 uppercase tracking-wider mb-3">Multi-Agent Workflow Stages</h3>
                    <div class="space-y-2 text-xs">
                        <div class="flex items-center space-x-2 text-gray-400" id="step1">
                            <i class="fa-solid fa-circle-notch text-blue-400"></i>
                            <span>1. Resume Parsing Agent (Info Extraction)</span>
                        </div>
                        <div class="flex items-center space-x-2 text-gray-400" id="step2">
                            <i class="fa-solid fa-circle text-gray-600"></i>
                            <span>2. Skill Matching Agent (Semantic Gap Analysis)</span>
                        </div>
                        <div class="flex items-center space-x-2 text-gray-400" id="step3">
                            <i class="fa-solid fa-circle text-gray-600"></i>
                            <span>3. ATS Scoring Agent (50/20/20/10 Weighted)</span>
                        </div>
                        <div class="flex items-center space-x-2 text-gray-400" id="step4">
                            <i class="fa-solid fa-circle text-gray-600"></i>
                            <span>4. Interview Question Generator Agent</span>
                        </div>
                        <div class="flex items-center space-x-2 text-gray-400" id="step5">
                            <i class="fa-solid fa-circle text-gray-600"></i>
                            <span>5. Resume Improvement & Keyword Agent</span>
                        </div>
                    </div>
                </div>

            </div>

            <!-- Right Panel: Results & Breakdown (7 cols) -->
            <div class="lg:col-span-7 space-y-6">

                <!-- Placeholder state before analysis -->
                <div id="placeholderState" class="glass-card rounded-2xl p-12 text-center border border-gray-800 h-full flex flex-col items-center justify-center">
                    <div class="w-16 h-16 rounded-2xl bg-blue-500/10 text-blue-400 flex items-center justify-center mb-4">
                        <i class="fa-solid fa-chart-pie text-2xl"></i>
                    </div>
                    <h3 class="text-lg font-bold text-gray-200 mb-2">No Analysis Report Generated Yet</h3>
                    <p class="text-sm text-gray-400 max-w-sm">
                        Upload a resume PDF on the left and click "Run Multi-Agent Analysis" to generate candidate insights.
                    </p>
                </div>

                <!-- Analysis Report Section (Initially Hidden) -->
                <div id="reportSection" class="hidden space-y-6">

                    <!-- Score Header Card -->
                    <div class="glass-card rounded-2xl p-6 border border-gray-800 bg-gradient-to-br from-gray-900 via-gray-900 to-indigo-950/40">
                        <div class="flex flex-col sm:flex-row items-center justify-between gap-4">
                            <div>
                                <span class="text-xs font-bold text-blue-400 uppercase tracking-wider">Candidate Evaluation Report</span>
                                <h2 class="text-2xl font-black text-white mt-1" id="candidateName">Jane Doe</h2>
                                <p class="text-xs text-gray-400 mt-0.5" id="targetRole">Target Role: Senior FastAPI Backend Engineer</p>
                            </div>
                            <div class="flex items-center space-x-4">
                                <div class="text-center px-4 py-2 bg-blue-500/10 rounded-xl border border-blue-500/20">
                                    <div class="text-xs text-blue-400 font-semibold">Match Rate</div>
                                    <div class="text-2xl font-black text-blue-300" id="matchPct">87.5%</div>
                                </div>
                                <div class="text-center px-4 py-2 bg-gradient-to-tr from-emerald-500/20 to-teal-500/20 rounded-xl border border-emerald-500/30">
                                    <div class="text-xs text-emerald-400 font-semibold">ATS Score</div>
                                    <div class="text-3xl font-black text-emerald-300" id="atsScore">87/100</div>
                                </div>
                            </div>
                        </div>

                        <!-- ATS Breakdown Grid -->
                        <div class="grid grid-cols-2 sm:grid-cols-4 gap-3 mt-6 pt-6 border-t border-gray-800">
                            <div class="bg-gray-900/60 p-3 rounded-xl border border-gray-800/80">
                                <span class="text-[11px] text-gray-400 block">Skills (50%)</span>
                                <span class="text-base font-bold text-blue-400" id="skillScore">90%</span>
                            </div>
                            <div class="bg-gray-900/60 p-3 rounded-xl border border-gray-800/80">
                                <span class="text-[11px] text-gray-400 block">Projects (20%)</span>
                                <span class="text-base font-bold text-indigo-400" id="projectScore">85%</span>
                            </div>
                            <div class="bg-gray-900/60 p-3 rounded-xl border border-gray-800/80">
                                <span class="text-[11px] text-gray-400 block">Experience (20%)</span>
                                <span class="text-base font-bold text-purple-400" id="expScore">85%</span>
                            </div>
                            <div class="bg-gray-900/60 p-3 rounded-xl border border-gray-800/80">
                                <span class="text-[11px] text-gray-400 block">Education (10%)</span>
                                <span class="text-base font-bold text-pink-400" id="eduScore">80%</span>
                            </div>
                        </div>
                    </div>

                    <!-- Tabs: Skills, Questions, Improvements -->
                    <div class="glass-card rounded-2xl border border-gray-800 overflow-hidden">
                        <div class="flex border-b border-gray-800 bg-gray-900/50 p-1.5 space-x-1">
                            <button onclick="switchTab('tabSkills')" id="btnTabSkills" class="tab-btn active flex-1 py-2 px-3 rounded-lg text-xs font-bold transition flex items-center justify-center space-x-1.5">
                                <i class="fa-solid fa-code"></i><span>Skills Breakdown</span>
                            </button>
                            <button onclick="switchTab('tabQuestions')" id="btnTabQuestions" class="tab-btn flex-1 py-2 px-3 rounded-lg text-xs font-bold text-gray-400 hover:text-white transition flex items-center justify-center space-x-1.5">
                                <i class="fa-solid fa-circle-question"></i><span>Interview Questions</span>
                            </button>
                            <button onclick="switchTab('tabImprovements')" id="btnTabImprovements" class="tab-btn flex-1 py-2 px-3 rounded-lg text-xs font-bold text-gray-400 hover:text-white transition flex items-center justify-center space-x-1.5">
                                <i class="fa-solid fa-lightbulb"></i><span>Resume Optimization</span>
                            </button>
                        </div>

                        <!-- Tab 1: Skills Breakdown -->
                        <div id="tabSkills" class="p-6 space-y-6">
                            <div>
                                <h4 class="text-xs font-bold uppercase tracking-wider text-emerald-400 mb-3 flex items-center">
                                    <i class="fa-solid fa-circle-check mr-1.5"></i> Matched Competencies
                                </h4>
                                <div id="matchedSkillsList" class="flex flex-wrap gap-2"></div>
                            </div>
                            <div>
                                <h4 class="text-xs font-bold uppercase tracking-wider text-rose-400 mb-3 flex items-center">
                                    <i class="fa-solid fa-circle-xmark mr-1.5"></i> Missing Skills
                                </h4>
                                <div id="missingSkillsList" class="flex flex-wrap gap-2"></div>
                            </div>
                        </div>

                        <!-- Tab 2: Interview Questions -->
                        <div id="tabQuestions" class="hidden p-6 space-y-6">
                            <div>
                                <h4 class="text-xs font-bold uppercase tracking-wider text-blue-400 mb-3 flex items-center">
                                    <i class="fa-solid fa-laptop-code mr-1.5"></i> Technical Questions
                                </h4>
                                <ul id="techQuestionsList" class="space-y-2 text-xs text-gray-300"></ul>
                            </div>
                            <div>
                                <h4 class="text-xs font-bold uppercase tracking-wider text-purple-400 mb-3 flex items-center">
                                    <i class="fa-solid fa-diagram-project mr-1.5"></i> Project Deep-Dives
                                </h4>
                                <ul id="projQuestionsList" class="space-y-2 text-xs text-gray-300"></ul>
                            </div>
                            <div>
                                <h4 class="text-xs font-bold uppercase tracking-wider text-indigo-400 mb-3 flex items-center">
                                    <i class="fa-solid fa-users mr-1.5"></i> Behavioral (STAR Format)
                                </h4>
                                <ul id="behavioralQuestionsList" class="space-y-2 text-xs text-gray-300"></ul>
                            </div>
                        </div>

                        <!-- Tab 3: Resume Improvements -->
                        <div id="tabImprovements" class="hidden p-6 space-y-6">
                            <div>
                                <h4 class="text-xs font-bold uppercase tracking-wider text-amber-400 mb-3 flex items-center">
                                    <i class="fa-solid fa-file-pen mr-1.5"></i> Action Verb & Bullet Point Enhancements
                                </h4>
                                <ul id="enhancementsList" class="space-y-2 text-xs text-gray-300"></ul>
                            </div>
                            <div>
                                <h4 class="text-xs font-bold uppercase tracking-wider text-teal-400 mb-3 flex items-center">
                                    <i class="fa-solid fa-tags mr-1.5"></i> ATS Keyword Density Suggestions
                                </h4>
                                <ul id="keywordsList" class="space-y-2 text-xs text-gray-300"></ul>
                            </div>
                        </div>

                    </div>
                </div>

            </div>

        </div>

    </main>

    <!-- Footer -->
    <footer class="border-t border-gray-800/80 py-4 text-center text-xs text-gray-500">
        Agentic AI Recruitment Assistant &copy; 2026. Built with FastAPI, PostgreSQL, Gemini API, and ChromaDB.
    </footer>

    <!-- Client-side Logic -->
    <script>
        let currentResumeId = null;

        // Load JDs on page startup
        window.addEventListener('DOMContentLoaded', async () => {
            await loadJobDescriptions();
        });

        async function loadJobDescriptions() {
            try {
                const res = await fetch('/api/v1/jd/options');
                if (!res.ok) throw new Error(`Request failed (${res.status})`);
                const data = await res.json();
                const select = document.getElementById('jdSelect');
                select.innerHTML = '';
                if (Array.isArray(data) && data.length > 0) {
                    data.forEach(jd => {
                        const opt = document.createElement('option');
                        opt.value = jd.id;
                        opt.textContent = jd.title;
                        select.appendChild(opt);
                    });
                } else {
                    select.innerHTML = '<option value="">No Job Descriptions Found</option>';
                }
            } catch (err) {
                console.error('Failed to load JDs:', err);
                document.getElementById('jdSelect').innerHTML = '<option value="">Unable to load job roles</option>';
            }
        }

        // Drag and Drop Handling
        const dropZone = document.getElementById('dropZone');
        const resumeInput = document.getElementById('resumeInput');

        dropZone.addEventListener('click', () => resumeInput.click());
        dropZone.addEventListener('dragover', (e) => { e.preventDefault(); dropZone.classList.add('border-blue-500'); });
        dropZone.addEventListener('dragleave', () => dropZone.classList.remove('border-blue-500'));
        dropZone.addEventListener('drop', (e) => {
            e.preventDefault();
            dropZone.classList.remove('border-blue-500');
            if (e.dataTransfer.files.length) {
                resumeInput.files = e.dataTransfer.files;
                uploadSelectedResume();
            }
        });

        resumeInput.addEventListener('change', () => {
            if (resumeInput.files.length) uploadSelectedResume();
        });

        async function uploadSelectedResume() {
            const file = resumeInput.files[0];
            if (!file) return;

            document.getElementById('fileStatusText').textContent = 'Uploading & Parsing with ResumeAgent...';
            const formData = new FormData();
            formData.append('file', file);

            try {
                const res = await fetch('/api/v1/resume/upload', {
                    method: 'POST',
                    body: formData
                });
                const result = await res.json();
                if (res.ok && result.data) {
                    currentResumeId = result.data.id;
                    document.getElementById('uploadedFileName').textContent = file.name;
                    document.getElementById('resumeIdBadge').textContent = `ID #${currentResumeId}`;
                    document.getElementById('uploadedInfo').classList.remove('hidden');
                    document.getElementById('fileStatusText').textContent = `Uploaded: ${file.name}`;
                    showAlert('Resume uploaded and parsed successfully!', 'success');
                } else {
                    showAlert(result.message || 'Failed to upload resume', 'error');
                }
            } catch (err) {
                showAlert('Error uploading resume: ' + err.message, 'error');
            }
        }

        async function runAnalysis() {
            if (!currentResumeId) {
                showAlert('Please upload a resume PDF first.', 'error');
                return;
            }
            const jdId = document.getElementById('jdSelect').value;
            if (!jdId) {
                showAlert('Please select a target Job Description.', 'error');
                return;
            }

            const btn = document.getElementById('analyzeBtn');
            const btnText = document.getElementById('analyzeBtnText');
            btn.disabled = true;
            btnText.textContent = 'Running Multi-Agent Pipeline...';

            try {
                const res = await fetch('/api/v1/analysis/run', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        resume_id: parseInt(currentResumeId),
                        jd_id: parseInt(jdId)
                    })
                });

                const result = await res.json();
                if (res.ok && result.data) {
                    renderReport(result.data);
                    showAlert('Multi-Agent Analysis completed successfully!', 'success');
                } else {
                    showAlert(result.message || 'Analysis failed', 'error');
                }
            } catch (err) {
                showAlert('Error running analysis: ' + err.message, 'error');
            } finally {
                btn.disabled = false;
                btnText.textContent = 'Run Multi-Agent Analysis';
            }
        }

        function renderReport(data) {
            const report = data.report_json;
            document.getElementById('placeholderState').classList.add('hidden');
            document.getElementById('reportSection').classList.remove('hidden');

            document.getElementById('candidateName').textContent = report.candidate_name || 'Candidate';
            document.getElementById('targetRole').textContent = `Target Role: ${report.job_title || 'Position'}`;
            document.getElementById('matchPct').textContent = `${data.match_percentage}%`;
            document.getElementById('atsScore').textContent = `${data.ats_score}/100`;

            // Breakdown
            if (report.ats_breakdown) {
                document.getElementById('skillScore').textContent = `${report.ats_breakdown.skill_match.score}%`;
                document.getElementById('projectScore').textContent = `${report.ats_breakdown.projects.score}%`;
                document.getElementById('expScore').textContent = `${report.ats_breakdown.experience.score}%`;
                document.getElementById('eduScore').textContent = `${report.ats_breakdown.education.score}%`;
            }

            // Matched & Missing Skills
            const matchedContainer = document.getElementById('matchedSkillsList');
            matchedContainer.innerHTML = '';
            (report.skill_match.matched_skills || []).forEach(s => {
                matchedContainer.innerHTML += `<span class="px-2.5 py-1 rounded-lg bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 text-xs font-semibold"><i class="fa-solid fa-check text-[10px] mr-1"></i>${s}</span>`;
            });

            const missingContainer = document.getElementById('missingSkillsList');
            missingContainer.innerHTML = '';
            (report.skill_match.missing_skills || []).forEach(s => {
                missingContainer.innerHTML += `<span class="px-2.5 py-1 rounded-lg bg-rose-500/10 text-rose-400 border border-rose-500/20 text-xs font-semibold"><i class="fa-solid fa-xmark text-[10px] mr-1"></i>${s}</span>`;
            });

            // Interview Questions
            const techList = document.getElementById('techQuestionsList');
            techList.innerHTML = '';
            (report.interview_questions.technical_questions || []).forEach(q => {
                techList.innerHTML += `<li class="p-3 bg-gray-900/60 rounded-xl border border-gray-800 flex items-start space-x-2"><i class="fa-solid fa-terminal text-blue-400 mt-0.5"></i><span>${q}</span></li>`;
            });

            const projList = document.getElementById('projQuestionsList');
            projList.innerHTML = '';
            (report.interview_questions.project_questions || []).forEach(q => {
                projList.innerHTML += `<li class="p-3 bg-gray-900/60 rounded-xl border border-gray-800 flex items-start space-x-2"><i class="fa-solid fa-layer-group text-purple-400 mt-0.5"></i><span>${q}</span></li>`;
            });

            const behList = document.getElementById('behavioralQuestionsList');
            behList.innerHTML = '';
            (report.interview_questions.behavioral_questions || []).forEach(q => {
                behList.innerHTML += `<li class="p-3 bg-gray-900/60 rounded-xl border border-gray-800 flex items-start space-x-2"><i class="fa-solid fa-user-check text-indigo-400 mt-0.5"></i><span>${q}</span></li>`;
            });

            // Improvements
            const enhList = document.getElementById('enhancementsList');
            enhList.innerHTML = '';
            (report.improvements.resume_enhancement_suggestions || []).forEach(s => {
                enhList.innerHTML += `<li class="p-3 bg-gray-900/60 rounded-xl border border-gray-800 flex items-start space-x-2"><i class="fa-solid fa-arrow-trend-up text-amber-400 mt-0.5"></i><span>${s}</span></li>`;
            });

            const kwList = document.getElementById('keywordsList');
            kwList.innerHTML = '';
            (report.improvements.keyword_optimization_suggestions || []).forEach(s => {
                kwList.innerHTML += `<li class="p-3 bg-gray-900/60 rounded-xl border border-gray-800 flex items-start space-x-2"><i class="fa-solid fa-bullseye text-teal-400 mt-0.5"></i><span>${s}</span></li>`;
            });
        }

        function switchTab(tabId) {
            ['tabSkills', 'tabQuestions', 'tabImprovements'].forEach(id => {
                document.getElementById(id).classList.add('hidden');
            });
            ['btnTabSkills', 'btnTabQuestions', 'btnTabImprovements'].forEach(id => {
                document.getElementById(id).classList.remove('active');
                document.getElementById(id).classList.add('text-gray-400');
            });
            document.getElementById(tabId).classList.remove('hidden');
            const btnId = 'btn' + tabId.charAt(0).toUpperCase() + tabId.slice(1);
            document.getElementById(btnId).classList.add('active');
            document.getElementById(btnId).classList.remove('text-gray-400');
        }

        function showAlert(message, type) {
            const el = document.getElementById('statusAlert');
            el.classList.remove('hidden', 'bg-rose-950/60', 'text-rose-300', 'border-rose-800', 'bg-emerald-950/60', 'text-emerald-300', 'border-emerald-800');
            if (type === 'error') {
                el.classList.add('bg-rose-950/60', 'text-rose-300', 'border', 'border-rose-800');
                el.innerHTML = `<i class="fa-solid fa-circle-exclamation"></i><span>${message}</span>`;
            } else {
                el.classList.add('bg-emerald-950/60', 'text-emerald-300', 'border', 'border-emerald-800');
                el.innerHTML = `<i class="fa-solid fa-circle-check"></i><span>${message}</span>`;
            }
        }
    </script>
</body>
</html>
"""

@router.get("/", response_class=HTMLResponse, summary="Web UI Dashboard")
@router.get("/dashboard", response_class=HTMLResponse, summary="Web UI Dashboard")
@router.get("/upload", response_class=HTMLResponse, summary="Web UI Upload Page")
def serve_dashboard(request: Request):
    """
    Renders the rich interactive Web UI Dashboard for resume uploading and multi-agent AI analysis.
    """
    return HTMLResponse(content=HTML_CONTENT)
