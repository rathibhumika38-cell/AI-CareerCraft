import sqlite3
import os
import json
from datetime import datetime

DB_PATH = os.path.join(os.path.dirname(__file__), "careercraft.db")


def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.executescript("""
        CREATE TABLE IF NOT EXISTS resumes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            full_name TEXT NOT NULL,
            email TEXT,
            phone TEXT,
            location TEXT,
            career_objective TEXT,
            education TEXT,
            skills TEXT,
            certifications TEXT,
            projects TEXT,
            experience TEXT,
            achievements TEXT,
            languages TEXT,
            interests TEXT,
            linkedin TEXT,
            github TEXT,
            target_role TEXT,
            ai_content TEXT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        );

        CREATE TABLE IF NOT EXISTS cover_letters (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            company TEXT,
            job_title TEXT,
            job_description TEXT,
            skills TEXT,
            projects TEXT,
            generated_letter TEXT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        );

        CREATE TABLE IF NOT EXISTS portfolios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            full_name TEXT,
            skills TEXT,
            projects TEXT,
            ai_content TEXT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        );
    """)
    conn.commit()
    conn.close()


def save_resume(data, ai_content):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO resumes
        (full_name, email, phone, location, career_objective, education, skills,
         certifications, projects, experience, achievements, languages, interests,
         linkedin, github, target_role, ai_content, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        data.get("full_name", ""),
        data.get("email", ""),
        data.get("phone", ""),
        data.get("location", ""),
        data.get("career_objective", ""),
        data.get("education", ""),
        data.get("skills", ""),
        data.get("certifications", ""),
        data.get("projects", ""),
        data.get("experience", ""),
        data.get("achievements", ""),
        data.get("languages", ""),
        data.get("interests", ""),
        data.get("linkedin", ""),
        data.get("github", ""),
        data.get("target_role", ""),
        json.dumps(ai_content),
        datetime.now().isoformat()
    ))
    resume_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return resume_id


def get_resume(resume_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM resumes WHERE id = ?", (resume_id,))
    row = cursor.fetchone()
    conn.close()
    if row:
        result = dict(row)
        if result.get("ai_content"):
            try:
                result["ai_content"] = json.loads(result["ai_content"])
            except Exception:
                pass
        return result
    return None


def get_all_resumes():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, full_name, target_role, created_at FROM resumes ORDER BY created_at DESC")
    rows = cursor.fetchall()
    conn.close()
    return [dict(r) for r in rows]


def save_cover_letter(data, letter):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO cover_letters (company, job_title, job_description, skills, projects, generated_letter, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        data.get("company", ""),
        data.get("job_title", ""),
        data.get("job_description", ""),
        data.get("skills", ""),
        data.get("projects", ""),
        letter,
        datetime.now().isoformat()
    ))
    letter_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return letter_id


def save_portfolio(data, ai_content):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO portfolios (full_name, skills, projects, ai_content, created_at)
        VALUES (?, ?, ?, ?, ?)
    """, (
        data.get("full_name", ""),
        data.get("skills", ""),
        data.get("projects", ""),
        json.dumps(ai_content),
        datetime.now().isoformat()
    ))
    portfolio_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return portfolio_id
