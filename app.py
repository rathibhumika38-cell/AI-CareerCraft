import os
import sys

# Load .env if python-dotenv is available
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

from flask import Flask, render_template, request, jsonify, redirect, url_for

# Add project root to path for local imports
sys.path.insert(0, os.path.dirname(__file__))

from services.ai_service import (
    generate_resume_content,
    generate_cover_letter,
    generate_portfolio_content,
    generate_career_suggestions,
    analyze_ats,
    is_demo_mode,
)
from database.database import (
    init_db,
    save_resume,
    get_resume,
    get_all_resumes,
    save_cover_letter,
    save_portfolio,
)

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "careercraft-secret-2024")

# Initialize database on startup
with app.app_context():
    init_db()


# ─── PAGES ───────────────────────────────────────────────────────────────────

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/dashboard")
def dashboard():
    resumes = get_all_resumes()
    return render_template("dashboard.html", resumes=resumes, demo_mode=is_demo_mode())


@app.route("/resume")
def resume_page():
    return render_template("resume.html", demo_mode=is_demo_mode())


@app.route("/resume/<int:resume_id>")
def resume_view(resume_id):
    resume = get_resume(resume_id)
    if not resume:
        return redirect(url_for("resume_page"))
    return render_template("resume.html", resume=resume, demo_mode=is_demo_mode())


@app.route("/cover-letter")
def cover_letter_page():
    return render_template("cover_letter.html", demo_mode=is_demo_mode())


@app.route("/portfolio")
def portfolio_page():
    return render_template("portfolio.html", demo_mode=is_demo_mode())


@app.route("/ats-checker")
def ats_checker_page():
    return render_template("ats_checker.html", demo_mode=is_demo_mode())


# ─── API ENDPOINTS ────────────────────────────────────────────────────────────

@app.route("/api/generate-resume", methods=["POST"])
def api_generate_resume():
    try:
        data = request.get_json(force=True)
        if not data.get("full_name"):
            return jsonify({"error": "Full name is required"}), 400
        ai_content = generate_resume_content(data)
        resume_id = save_resume(data, ai_content)
        return jsonify({
            "success": True,
            "resume_id": resume_id,
            "ai_content": ai_content,
            "form_data": data,
            "demo_mode": is_demo_mode()
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/resume/<int:resume_id>", methods=["GET"])
def api_get_resume(resume_id):
    resume = get_resume(resume_id)
    if not resume:
        return jsonify({"error": "Resume not found"}), 404
    return jsonify(resume)


@app.route("/api/generate-cover-letter", methods=["POST"])
def api_generate_cover_letter():
    try:
        data = request.get_json(force=True)
        if not data.get("company") or not data.get("job_title"):
            return jsonify({"error": "Company and job title are required"}), 400
        letter = generate_cover_letter(data)
        letter_id = save_cover_letter(data, letter)
        return jsonify({
            "success": True,
            "letter_id": letter_id,
            "cover_letter": letter,
            "demo_mode": is_demo_mode()
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/generate-portfolio", methods=["POST"])
def api_generate_portfolio():
    try:
        data = request.get_json(force=True)
        if not data.get("full_name"):
            return jsonify({"error": "Full name is required"}), 400
        ai_content = generate_portfolio_content(data)
        portfolio_id = save_portfolio(data, ai_content)
        return jsonify({
            "success": True,
            "portfolio_id": portfolio_id,
            "ai_content": ai_content,
            "form_data": data,
            "demo_mode": is_demo_mode()
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/career-suggestions", methods=["POST"])
def api_career_suggestions():
    try:
        data = request.get_json(force=True)
        suggestions = generate_career_suggestions(data)
        return jsonify({
            "success": True,
            "suggestions": suggestions,
            "demo_mode": is_demo_mode()
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/ats-check", methods=["POST"])
def api_ats_check():
    try:
        data = request.get_json(force=True)
        if not data.get("job_description"):
            return jsonify({"error": "Job description is required"}), 400
        result = analyze_ats(data)
        return jsonify({
            "success": True,
            "result": result,
            "demo_mode": is_demo_mode()
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/status")
def api_status():
    return jsonify({
        "status": "running",
        "demo_mode": is_demo_mode(),
        "message": "AI CareerCraft is running in demo mode" if is_demo_mode() else "AI CareerCraft is running with live AI"
    })


# ─── MAIN ─────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("=" * 55)
    print("  AI CareerCraft – Resume & Portfolio Builder")
    print("=" * 55)
    if is_demo_mode():
        print("  Mode: DEMO (No OpenAI API key found)")
    else:
        print("  Mode: LIVE AI (OpenAI connected)")
    print("  Open: http://127.0.0.1:5000")
    print("=" * 55)
    app.run(debug=True, host="0.0.0.0", port=5000)
