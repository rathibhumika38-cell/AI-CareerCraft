/* ─── AI CareerCraft – Frontend JavaScript ─── */

// ─── TOAST ────────────────────────────────────────────────────────────────
const toastContainer = document.getElementById("toastContainer");

function showToast(message, type = "info", duration = 3500) {
  if (!toastContainer) return;
  const icons = { success: "✓", error: "✕", info: "ℹ" };
  const toast = document.createElement("div");
  toast.className = `toast toast-${type}`;
  toast.innerHTML = `<span>${icons[type] || "ℹ"}</span><span>${message}</span>`;
  toastContainer.appendChild(toast);
  setTimeout(() => {
    toast.style.opacity = "0";
    setTimeout(() => toast.remove(), 300);
  }, duration);
}

// ─── LOADING OVERLAY ──────────────────────────────────────────────────────
function showLoading(text = "AI is generating your content…") {
  const el = document.getElementById("loadingOverlay");
  if (!el) return;
  const lt = el.querySelector(".loading-text");
  if (lt) lt.textContent = text;
  el.classList.remove("hidden");
}
function hideLoading() {
  const el = document.getElementById("loadingOverlay");
  if (el) el.classList.add("hidden");
}

// ─── TABS ─────────────────────────────────────────────────────────────────
document.addEventListener("click", function (e) {
  const btn = e.target.closest(".tab-btn");
  if (!btn) return;
  const list = btn.closest(".tab-list");
  if (!list) return;
  const target = btn.dataset.tab;
  list.querySelectorAll(".tab-btn").forEach(b => b.classList.remove("active"));
  btn.classList.add("active");
  const container = list.parentElement;
  container.querySelectorAll(".tab-content").forEach(c => c.classList.remove("active"));
  const tc = container.querySelector(`[data-tab-content="${target}"]`);
  if (tc) tc.classList.add("active");
});

// ─── MOBILE SIDEBAR ───────────────────────────────────────────────────────
const sidebarToggle = document.getElementById("sidebarToggle");
const sidebar = document.getElementById("sidebar");
if (sidebarToggle && sidebar) {
  sidebarToggle.addEventListener("click", () => sidebar.classList.toggle("open"));
  document.addEventListener("click", (e) => {
    if (!sidebar.contains(e.target) && !sidebarToggle.contains(e.target)) {
      sidebar.classList.remove("open");
    }
  });
}

// ─── MULTI-STEP RESUME FORM ───────────────────────────────────────────────
const stepPanels = document.querySelectorAll(".step-panel");
const stepItems = document.querySelectorAll(".step");
let currentStep = 0;

function goToStep(n) {
  if (n < 0 || n >= stepPanels.length) return;
  stepPanels.forEach((p, i) => p.classList.toggle("active", i === n));
  stepItems.forEach((s, i) => {
    s.classList.remove("active", "completed");
    if (i === n) s.classList.add("active");
    if (i < n) s.classList.add("completed");
  });
  currentStep = n;
  window.scrollTo({ top: 0, behavior: "smooth" });
}

window.nextStep = function () {
  if (currentStep < stepPanels.length - 1) goToStep(currentStep + 1);
};
window.prevStep = function () {
  if (currentStep > 0) goToStep(currentStep - 1);
};

if (stepPanels.length > 0) goToStep(0);

// ─── RESUME FORM SUBMIT ────────────────────────────────────────────────────
const resumeForm = document.getElementById("resumeForm");
if (resumeForm) {
  resumeForm.addEventListener("submit", async function (e) {
    e.preventDefault();
    const fd = new FormData(resumeForm);
    const data = {};
    fd.forEach((v, k) => { data[k] = v; });
    showLoading("✨ AI is crafting your resume…");
    try {
      const res = await fetch("/api/generate-resume", {
        method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(data)
      });
      const json = await res.json();
      hideLoading();
      if (json.success) {
        window.location.href = `/resume/${json.resume_id}?generated=1`;
      } else {
        showToast(json.error || "Failed to generate resume", "error");
      }
    } catch (err) {
      hideLoading();
      showToast("Network error. Please try again.", "error");
    }
  });
}

// ─── RESUME PREVIEW ────────────────────────────────────────────────────────
function renderResumePreview(data, ai) {
  const wrap = document.getElementById("resumePreview");
  if (!wrap) return;
  const name = data.full_name || "Your Name";
  const email = data.email || "";
  const phone = data.phone || "";
  const location = data.location || "";
  const linkedin = data.linkedin || "";
  const github = data.github || "";
  const summary = ai.professional_summary || data.career_objective || "";
  const skills = data.skills || "";
  const education = data.education || "";
  const experience = data.experience || "";
  const achievements = data.achievements || "";
  const certifications = data.certifications || "";
  const languages = data.languages || "";
  const interests = data.interests || "";

  const skillsList = skills.split(/[,\n]+/).filter(s => s.trim()).map(s =>
    `<span class="skill-chip">${s.trim()}</span>`).join("");

  const improvedProjects = (ai.improved_projects || []).map(p =>
    `<div class="resume-item">
      <div class="resume-item-title">${p.title || ""}</div>
      <div class="resume-item-desc">${p.description || ""}</div>
    </div>`).join("") || (data.projects ? `<div class="resume-item"><div class="resume-item-desc">${data.projects}</div></div>` : "");

  const atsKeywords = (ai.ats_keywords || []).map(k => `<span class="skill-chip">${k}</span>`).join("");

  wrap.innerHTML = `
    <div class="resume-document">
      <div class="resume-header">
        <h1>${name}</h1>
        <div class="contact-row">
          ${email ? `<span>✉ ${email}</span>` : ""}
          ${phone ? `<span>📞 ${phone}</span>` : ""}
          ${location ? `<span>📍 ${location}</span>` : ""}
          ${linkedin ? `<span>🔗 ${linkedin}</span>` : ""}
          ${github ? `<span>⌨ ${github}</span>` : ""}
        </div>
      </div>
      <div class="resume-body">
        ${summary ? `<div class="resume-section">
          <div class="resume-section-title">Professional Summary</div>
          <div class="resume-item-desc">${summary}</div>
        </div>` : ""}
        ${skills ? `<div class="resume-section">
          <div class="resume-section-title">Skills</div>
          <div class="skills-chips">${skillsList}</div>
        </div>` : ""}
        ${education ? `<div class="resume-section">
          <div class="resume-section-title">Education</div>
          <div class="resume-item"><div class="resume-item-desc">${education}</div></div>
        </div>` : ""}
        ${improvedProjects ? `<div class="resume-section">
          <div class="resume-section-title">Projects</div>
          ${improvedProjects}
        </div>` : ""}
        ${experience ? `<div class="resume-section">
          <div class="resume-section-title">Experience</div>
          <div class="resume-item"><div class="resume-item-desc">${experience}</div></div>
        </div>` : ""}
        ${achievements ? `<div class="resume-section">
          <div class="resume-section-title">Achievements</div>
          <div class="resume-item"><div class="resume-item-desc">${achievements}</div></div>
        </div>` : ""}
        ${certifications ? `<div class="resume-section">
          <div class="resume-section-title">Certifications</div>
          <div class="resume-item"><div class="resume-item-desc">${certifications}</div></div>
        </div>` : ""}
        ${languages ? `<div class="resume-section">
          <div class="resume-section-title">Languages</div>
          <div class="resume-item"><div class="resume-item-desc">${languages}</div></div>
        </div>` : ""}
        ${interests ? `<div class="resume-section">
          <div class="resume-section-title">Interests</div>
          <div class="resume-item"><div class="resume-item-desc">${interests}</div></div>
        </div>` : ""}
        ${atsKeywords ? `<div class="resume-section">
          <div class="resume-section-title">ATS Keywords</div>
          <div class="skills-chips">${atsKeywords}</div>
        </div>` : ""}
      </div>
    </div>`;
}

// ─── COVER LETTER ──────────────────────────────────────────────────────────
const coverLetterForm = document.getElementById("coverLetterForm");
const coverLetterOutput = document.getElementById("coverLetterOutput");
const regenerateCLBtn = document.getElementById("regenerateCL");
const copyCLBtn = document.getElementById("copyCL");
let lastCLData = null;

async function generateCoverLetter(data) {
  showLoading("✍ AI is writing your cover letter…");
  try {
    const res = await fetch("/api/generate-cover-letter", {
      method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(data)
    });
    const json = await res.json();
    hideLoading();
    if (json.success) {
      if (coverLetterOutput) {
        coverLetterOutput.textContent = json.cover_letter;
        coverLetterOutput.closest(".card") && coverLetterOutput.closest(".card").classList.remove("hidden");
        document.getElementById("clActions") && document.getElementById("clActions").classList.remove("hidden");
        if (json.demo_mode) showToast("Demo mode: sample cover letter generated", "info");
        else showToast("Cover letter generated!", "success");
      }
      lastCLData = data;
    } else {
      showToast(json.error || "Failed to generate cover letter", "error");
    }
  } catch (err) {
    hideLoading();
    showToast("Network error. Please try again.", "error");
  }
}

if (coverLetterForm) {
  coverLetterForm.addEventListener("submit", (e) => {
    e.preventDefault();
    const fd = new FormData(coverLetterForm);
    const data = {};
    fd.forEach((v, k) => { data[k] = v; });
    generateCoverLetter(data);
  });
}
if (regenerateCLBtn) regenerateCLBtn.addEventListener("click", () => { if (lastCLData) generateCoverLetter(lastCLData); });
if (copyCLBtn) copyCLBtn.addEventListener("click", () => {
  if (coverLetterOutput) {
    navigator.clipboard.writeText(coverLetterOutput.textContent);
    showToast("Copied to clipboard!", "success");
  }
});

// ─── PORTFOLIO ─────────────────────────────────────────────────────────────
const portfolioForm = document.getElementById("portfolioForm");
const portfolioOutput = document.getElementById("portfolioOutput");

if (portfolioForm) {
  portfolioForm.addEventListener("submit", async (e) => {
    e.preventDefault();
    const fd = new FormData(portfolioForm);
    const data = {};
    fd.forEach((v, k) => { data[k] = v; });
    showLoading("🎨 AI is building your portfolio…");
    try {
      const res = await fetch("/api/generate-portfolio", {
        method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(data)
      });
      const json = await res.json();
      hideLoading();
      if (json.success) {
        renderPortfolio(json.form_data, json.ai_content);
        if (json.demo_mode) showToast("Demo mode: sample portfolio generated", "info");
        else showToast("Portfolio content generated!", "success");
      } else {
        showToast(json.error || "Failed to generate portfolio", "error");
      }
    } catch (err) {
      hideLoading();
      showToast("Network error. Please try again.", "error");
    }
  });
}

function renderPortfolio(data, ai) {
  if (!portfolioOutput) return;
  const projects = (ai.project_descriptions || []).map(p =>
    `<div class="project-list-item">
      <div class="project-list-name">🔧 ${p.name}</div>
      <div class="project-list-desc">${p.description}</div>
    </div>`).join("");
  portfolioOutput.innerHTML = `
    <div class="portfolio-section">
      <div class="portfolio-section-label">About Me</div>
      <div class="portfolio-text">${ai.about_me || ""}</div>
    </div>
    <div class="portfolio-section">
      <div class="portfolio-section-label">Professional Tagline</div>
      <div class="portfolio-text" style="font-size:18px;font-weight:700;color:var(--primary)">${ai.professional_tagline || ""}</div>
    </div>
    <div class="portfolio-section">
      <div class="portfolio-section-label">Skills</div>
      <div class="portfolio-text">${ai.skills_description || data.skills || ""}</div>
    </div>
    ${projects ? `<div class="portfolio-section">
      <div class="portfolio-section-label">Projects</div>
      ${projects}
    </div>` : ""}
    <div class="portfolio-section">
      <div class="portfolio-section-label">Call to Action</div>
      <div class="portfolio-text" style="font-style:italic;color:var(--primary)">${ai.call_to_action || ""}</div>
    </div>`;
  portfolioOutput.classList.remove("hidden");
}

// ─── CAREER SUGGESTIONS ────────────────────────────────────────────────────
const careerForm = document.getElementById("careerForm");
const careerOutput = document.getElementById("careerOutput");

if (careerForm) {
  careerForm.addEventListener("submit", async (e) => {
    e.preventDefault();
    const fd = new FormData(careerForm);
    const data = {};
    fd.forEach((v, k) => { data[k] = v; });
    showLoading("🔮 AI is mapping your career path…");
    try {
      const res = await fetch("/api/career-suggestions", {
        method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(data)
      });
      const json = await res.json();
      hideLoading();
      if (json.success) {
        renderCareer(json.suggestions);
        if (json.demo_mode) showToast("Demo mode: sample suggestions generated", "info");
        else showToast("Career analysis complete!", "success");
      } else {
        showToast(json.error || "Failed to get suggestions", "error");
      }
    } catch (err) {
      hideLoading();
      showToast("Network error. Please try again.", "error");
    }
  });
}

function renderCareer(s) {
  if (!careerOutput) return;
  const roles = (s.suitable_roles || []).map(r => `<div class="career-list-item"><span class="career-list-dot"></span>${r}</div>`).join("");
  const skills = (s.skills_to_learn || []).map(sk => `<div class="career-list-item"><span class="career-list-dot"></span>${sk}</div>`).join("");
  const paths = (s.career_paths || []).map(p => `<div class="career-path-item"><div class="career-path-title">${p.path}</div><div class="career-path-time">⏱ ${p.timeline}</div></div>`).join("");
  const projects = (s.recommended_projects || []).map(p => `<div class="career-list-item"><span class="career-list-dot"></span>${p}</div>`).join("");
  const interview = (s.interview_topics || []).map(t => `<div class="career-list-item"><span class="career-list-dot"></span>${t}</div>`).join("");
  careerOutput.innerHTML = `
    <div class="career-grid">
      <div class="career-card">
        <div class="career-card-header">
          <div class="career-card-icon" style="background:#ede9ff">💼</div>
          <div class="career-card-title">Suitable Job Roles</div>
        </div>${roles}</div>
      <div class="career-card">
        <div class="career-card-header">
          <div class="career-card-icon" style="background:#dcfce7">📚</div>
          <div class="career-card-title">Skills to Learn</div>
        </div>${skills}</div>
      <div class="career-card">
        <div class="career-card-header">
          <div class="career-card-icon" style="background:#fef3c7">🗺️</div>
          <div class="career-card-title">Career Paths</div>
        </div>${paths}</div>
      <div class="career-card">
        <div class="career-card-header">
          <div class="career-card-icon" style="background:#fee2e2">🔧</div>
          <div class="career-card-title">Recommended Projects</div>
        </div>${projects}</div>
      <div class="career-card" style="grid-column:1/-1">
        <div class="career-card-header">
          <div class="career-card-icon" style="background:#e0f7f2">🎯</div>
          <div class="career-card-title">Interview Preparation Topics</div>
        </div>
        <div style="display:grid;grid-template-columns:1fr 1fr;gap:4px">${interview}</div>
      </div>
    </div>`;
  careerOutput.classList.remove("hidden");
}

// ─── ATS CHECKER ──────────────────────────────────────────────────────────
const atsForm = document.getElementById("atsForm");
const atsOutput = document.getElementById("atsOutput");

if (atsForm) {
  atsForm.addEventListener("submit", async (e) => {
    e.preventDefault();
    const fd = new FormData(atsForm);
    const data = {};
    fd.forEach((v, k) => { data[k] = v; });
    showLoading("🔍 Analyzing your resume against the job description…");
    try {
      const res = await fetch("/api/ats-check", {
        method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(data)
      });
      const json = await res.json();
      hideLoading();
      if (json.success) {
        renderATS(json.result);
        if (json.demo_mode) showToast("Demo mode: sample analysis generated", "info");
        else showToast("ATS analysis complete!", "success");
      } else {
        showToast(json.error || "Failed to analyze resume", "error");
      }
    } catch (err) {
      hideLoading();
      showToast("Network error. Please try again.", "error");
    }
  });
}

function renderATS(r) {
  if (!atsOutput) return;
  const score = r.score || 0;
  const pct = `${score * 3.6}deg`;
  const color = score >= 80 ? "var(--success)" : score >= 60 ? "var(--warning)" : "var(--error)";
  const matching = (r.matching_skills || []).map(s => `<span class="keyword-chip keyword-match">✓ ${s}</span>`).join("");
  const missing = (r.missing_keywords || []).map(s => `<span class="keyword-chip keyword-missing">✕ ${s}</span>`).join("");
  const suggestions = (r.suggestions || []).map(s => `<li style="padding:6px 0;font-size:14px;border-bottom:1px solid var(--surface-2)">${s}</li>`).join("");
  atsOutput.innerHTML = `
    <div style="text-align:center;margin-bottom:28px">
      <div class="ats-score-ring" style="background:conic-gradient(${color} ${score * 3.6}deg, var(--surface-2) 0deg)">
        <div class="ats-score-inner">
          <div class="ats-score-num" style="color:${color}">${score}</div>
          <div class="ats-score-label">/ 100</div>
        </div>
      </div>
      <div style="font-size:18px;font-weight:800;margin-top:8px">${score >= 80 ? "Excellent" : score >= 60 ? "Good" : "Needs Work"} ATS Score</div>
      <div style="font-size:13px;color:var(--text-muted);margin-top:4px">${score >= 80 ? "Your resume is highly optimized for ATS." : score >= 60 ? "Your resume has good compatibility but can be improved." : "Your resume needs significant optimization."}</div>
    </div>
    <div class="ats-results-grid">
      <div class="card">
        <div class="card-title" style="margin-bottom:14px">✅ Matching Keywords</div>
        <div class="keyword-list">${matching || '<span style="color:var(--text-muted);font-size:14px">No matches found</span>'}</div>
      </div>
      <div class="card">
        <div class="card-title" style="margin-bottom:14px">❌ Missing Keywords</div>
        <div class="keyword-list">${missing || '<span style="color:var(--text-muted);font-size:14px">No missing keywords</span>'}</div>
      </div>
    </div>
    <div class="card" style="margin-top:20px">
      <div class="card-title" style="margin-bottom:14px">💡 Improvement Suggestions</div>
      <ul style="padding-left:0">${suggestions}</ul>
    </div>`;
  atsOutput.classList.remove("hidden");
}

// ─── PRINT RESUME ──────────────────────────────────────────────────────────
window.printResume = function () {
  window.print();
};

// ─── COPY TEXT ─────────────────────────────────────────────────────────────
window.copyText = function (elementId) {
  const el = document.getElementById(elementId);
  if (el) {
    navigator.clipboard.writeText(el.innerText || el.textContent);
    showToast("Copied to clipboard!", "success");
  }
};
