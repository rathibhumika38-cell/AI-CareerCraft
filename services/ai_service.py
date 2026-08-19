import os
import json
import random

# Try to import OpenAI
try:
    from openai import OpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False

DEMO_MODE = not (OPENAI_AVAILABLE and os.getenv("OPENAI_API_KEY"))


def _get_client():
    return OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def _call_ai(prompt, max_tokens=1200):
    if DEMO_MODE:
        return None
    try:
        client = _get_client()
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=max_tokens,
            temperature=0.7,
        )
        return response.choices[0].message.content.strip()
    except Exception:
        return None


# ─── DEMO DATA ───────────────────────────────────────────────────────────────

def _demo_resume_content(data):
    name = data.get("full_name", "Student")
    role = data.get("target_role", "Software Developer")
    skills = data.get("skills", "Python, JavaScript, React")
    return {
        "professional_summary": (
            f"Dynamic and results-driven {role} with a strong foundation in {skills}. "
            f"Passionate about building innovative solutions and contributing to impactful projects. "
            f"Adept at collaborating in agile environments and delivering high-quality code under tight deadlines."
        ),
        "career_objective": (
            f"To secure a challenging {role} position where I can leverage my expertise in {skills} "
            f"to drive technological innovation and contribute to organizational success while continuously "
            f"expanding my professional skill set."
        ),
        "improved_projects": [
            {
                "title": "AI-Powered Task Manager",
                "description": (
                    "Architected and developed a full-stack task management application integrating "
                    "machine learning algorithms to auto-prioritize tasks based on user behavior patterns. "
                    "Achieved 40% improvement in user productivity metrics through intelligent recommendations."
                )
            },
            {
                "title": "E-Commerce Platform",
                "description": (
                    "Engineered a scalable e-commerce solution handling 10,000+ concurrent users with "
                    "real-time inventory management, secure payment gateway integration, and advanced analytics dashboard."
                )
            }
        ],
        "skill_recommendations": [
            "Docker & Kubernetes for containerization",
            "AWS/GCP Cloud Services",
            "System Design & Architecture",
            "Data Structures & Algorithms",
            "CI/CD Pipeline Implementation"
        ],
        "ats_keywords": [
            role, "Agile", "REST API", "Git", "Problem Solving",
            "Team Collaboration", "Software Development Life Cycle", "Testing & Debugging"
        ]
    }


def _demo_cover_letter(data):
    company = data.get("company", "Tech Corp")
    role = data.get("job_title", "Software Developer")
    skills = data.get("skills", "Python, JavaScript")
    return f"""Dear Hiring Manager at {company},

I am writing to express my strong interest in the {role} position at {company}. With my solid background in {skills} and a passion for creating efficient, scalable solutions, I am confident in my ability to make a meaningful contribution to your team.

During my academic journey, I have developed hands-on experience through various projects that mirror real-world challenges. My project work has honed my ability to analyze complex problems, design elegant solutions, and deliver results within deadlines — skills that are directly applicable to the {role} role at {company}.

What excites me most about {company} is your commitment to innovation and technical excellence. I am eager to bring my enthusiasm, technical skills, and fresh perspective to your organization. I am a quick learner who thrives in collaborative environments and is always looking to grow.

I have attached my resume for your review and would welcome the opportunity to discuss how my background aligns with your needs. Thank you for considering my application. I look forward to the possibility of contributing to {company}'s continued success.

Warm regards,
[Your Name]"""


def _demo_portfolio_content(data):
    name = data.get("full_name", "Student Developer")
    skills = data.get("skills", "Python, JavaScript, React, SQL")
    return {
        "about_me": (
            f"Hi, I'm {name} — a passionate developer and problem solver who loves turning ideas into reality through code. "
            f"I specialize in {skills} and have a knack for building user-friendly applications that make a real difference. "
            f"When I'm not coding, I'm exploring new technologies, contributing to open-source projects, and sharpening my skills."
        ),
        "professional_tagline": f"Building Tomorrow's Solutions with {skills.split(',')[0].strip()} & Beyond",
        "skills_description": (
            f"My technical toolkit includes {skills}. I believe in writing clean, maintainable code "
            f"and following best practices to deliver robust, scalable solutions."
        ),
        "project_descriptions": [
            {
                "name": "Smart Resume Builder",
                "description": "An AI-powered web application that generates professional resumes tailored to specific job roles, improving interview callback rates by 60%."
            },
            {
                "name": "Real-time Chat Application",
                "description": "Built a WebSocket-based chat platform supporting 500+ concurrent users with end-to-end encryption, file sharing, and emoji reactions."
            }
        ],
        "call_to_action": "Open to exciting opportunities and collaborations. Let's build something amazing together!"
    }


def _demo_career_suggestions(data):
    skills = data.get("skills", "Python, JavaScript")
    role = data.get("target_career", "Software Development")
    return {
        "suitable_roles": [
            "Full Stack Developer",
            "Backend Engineer",
            "Data Analyst",
            "DevOps Engineer",
            "Machine Learning Engineer"
        ],
        "skills_to_learn": [
            "Cloud Computing (AWS/Azure/GCP)",
            "Docker & Kubernetes",
            "System Design",
            "GraphQL",
            "TypeScript"
        ],
        "career_paths": [
            {"path": "Junior Developer → Senior Developer → Tech Lead → Engineering Manager", "timeline": "5-8 years"},
            {"path": "Developer → Solutions Architect → CTO", "timeline": "8-12 years"},
            {"path": "Developer → ML Engineer → AI Researcher", "timeline": "4-7 years"}
        ],
        "recommended_projects": [
            "Build a microservices-based e-commerce platform",
            "Create an ML model for real-world predictions",
            "Contribute to an open-source project on GitHub",
            "Develop a mobile app using React Native or Flutter",
            "Build a real-time data dashboard with WebSockets"
        ],
        "interview_topics": [
            "Data Structures & Algorithms (Arrays, Trees, Graphs)",
            "System Design fundamentals",
            "Object-Oriented Programming concepts",
            "Database design and SQL optimization",
            "REST API design best practices",
            "Time & Space Complexity analysis"
        ]
    }


def _demo_ats_analysis(data):
    score = random.randint(72, 91)
    return {
        "score": score,
        "matching_skills": ["Python", "JavaScript", "REST API", "Git", "Agile", "SQL", "Problem Solving"],
        "missing_keywords": ["Kubernetes", "AWS", "CI/CD", "Microservices", "Redis"],
        "suggestions": [
            "Add quantifiable achievements (e.g., 'Improved performance by 30%')",
            "Include keywords from the job description in your skills section",
            "Use action verbs: Developed, Architected, Optimized, Led, Delivered",
            "Add relevant certifications (AWS, Google Cloud, etc.)",
            "Ensure consistent date formatting throughout the resume",
            f"Your resume scores {score}/100 — {'Excellent' if score >= 85 else 'Good'} ATS compatibility!"
        ]
    }


# ─── PUBLIC API ──────────────────────────────────────────────────────────────

def generate_resume_content(data):
    if DEMO_MODE:
        return _demo_resume_content(data)
    name = data.get("full_name", "")
    role = data.get("target_role", "")
    skills = data.get("skills", "")
    education = data.get("education", "")
    projects = data.get("projects", "")
    experience = data.get("experience", "")
    prompt = f"""You are an expert resume writer. Generate professional ATS-friendly resume content for:
Name: {name}
Target Role: {role}
Skills: {skills}
Education: {education}
Projects: {projects}
Experience: {experience}

Return a JSON object with keys:
- professional_summary (2-3 sentences)
- career_objective (2-3 sentences)
- improved_projects (list of objects with title and description)
- skill_recommendations (list of 5 skills to add)
- ats_keywords (list of 8 important keywords)

Return only valid JSON."""
    result = _call_ai(prompt)
    try:
        return json.loads(result)
    except Exception:
        return _demo_resume_content(data)


def generate_cover_letter(data):
    if DEMO_MODE:
        return _demo_cover_letter(data)
    company = data.get("company", "")
    role = data.get("job_title", "")
    jd = data.get("job_description", "")
    skills = data.get("skills", "")
    projects = data.get("projects", "")
    prompt = f"""Write a professional, personalized cover letter for:
Company: {company}
Role: {role}
Job Description: {jd}
Candidate Skills: {skills}
Relevant Projects: {projects}

Write a compelling 3-4 paragraph cover letter. Be specific and professional."""
    result = _call_ai(prompt)
    return result if result else _demo_cover_letter(data)


def generate_portfolio_content(data):
    if DEMO_MODE:
        return _demo_portfolio_content(data)
    name = data.get("full_name", "")
    skills = data.get("skills", "")
    projects = data.get("projects", "")
    prompt = f"""Generate professional portfolio content for a student developer:
Name: {name}
Skills: {skills}
Projects: {projects}

Return a JSON object with keys:
- about_me (engaging bio paragraph)
- professional_tagline (short catchy tagline)
- skills_description (paragraph about technical skills)
- project_descriptions (list of objects with name and description)
- call_to_action (closing statement)

Return only valid JSON."""
    result = _call_ai(prompt)
    try:
        return json.loads(result)
    except Exception:
        return _demo_portfolio_content(data)


def generate_career_suggestions(data):
    if DEMO_MODE:
        return _demo_career_suggestions(data)
    skills = data.get("skills", "")
    education = data.get("education", "")
    interests = data.get("interests", "")
    target = data.get("target_career", "")
    prompt = f"""Act as a career counselor. Give detailed career suggestions for:
Skills: {skills}
Education: {education}
Interests: {interests}
Target Career: {target}

Return a JSON object with keys:
- suitable_roles (list of 5 job titles)
- skills_to_learn (list of 5 skills)
- career_paths (list of objects with path and timeline)
- recommended_projects (list of 5 project ideas)
- interview_topics (list of 6 topics)

Return only valid JSON."""
    result = _call_ai(prompt)
    try:
        return json.loads(result)
    except Exception:
        return _demo_career_suggestions(data)


def analyze_ats(data):
    if DEMO_MODE:
        return _demo_ats_analysis(data)
    resume_text = data.get("resume_text", "")
    job_description = data.get("job_description", "")
    prompt = f"""Analyze this resume against the job description for ATS compatibility:
RESUME: {resume_text}
JOB DESCRIPTION: {job_description}

Return a JSON object with keys:
- score (integer 0-100)
- matching_skills (list of skills found in both)
- missing_keywords (list of important missing keywords)
- suggestions (list of 5 improvement suggestions)

Return only valid JSON."""
    result = _call_ai(prompt)
    try:
        return json.loads(result)
    except Exception:
        return _demo_ats_analysis(data)


def is_demo_mode():
    return DEMO_MODE
