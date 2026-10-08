import os
from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
from groq import Groq

app = Flask(__name__)
CORS(app)

API_KEY = "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"
client = Groq(api_key=API_KEY)

# Primary model with automatic fallback support
MODELS_TO_TRY = ["llama-3.1-8b-instant", "openai/gpt-oss-20b", "qwen/qwen3.6-27b"]

def query_groq_ai(system_prompt, user_prompt):
    """Tries primary model and falls back if not found."""
    last_error = None
    for model_name in MODELS_TO_TRY:
        try:
            completion = client.chat.completions.create(
                model=model_name,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.3,
                max_tokens=250
            )
            return completion.choices[0].message.content.strip()
        except Exception as e:
            last_error = e
            if "model_not_found" in str(e) or "404" in str(e):
                continue
            raise e
    raise last_error

@app.route("/")
def index():
    return send_from_directory(os.getcwd(), "index.html")

# Endpoint 1: Grievance / Concern Matcher
@app.route("/match-scheme", methods=["POST"])
def match_scheme():
    try:
        data = request.get_json(force=True) or {}
        issue = data.get("issue", "").strip()
        village = data.get("village", "Local Rural Cluster")
        lang = data.get("lang", "en")

        if not issue:
            return jsonify({"success": False, "error": "Please describe your concern first."}), 400

        lang_prompts = {
            "ta": "Respond strictly in Tamil (தமிழ்). Keep it structured with bullet points.",
            "hi": "Respond strictly in Hindi (हिन्दी). Keep it structured with bullet points.",
            "en": "Respond in English. Keep it structured with bullet points."
        }
        instruction = lang_prompts.get(lang, lang_prompts["en"])

        system_msg = (
            "You are an AI civic assistant for Earth & Hub.\n"
            "Map the citizen grievance to the appropriate government scheme (MGNREGS, PM-KISAN, Jal Jeevan Mission, TNEB, Smart Village Fund, etc.).\n"
            f"{instruction}\n"
            "Keep the response under 70 words."
        )
        user_msg = f"Location: {village}\nCitizen Grievance: {issue}"

        reply = query_groq_ai(system_msg, user_msg)
        return jsonify({"success": True, "result": reply})

    except Exception as e:
        print(f"Error in /match-scheme: {e}")
        return jsonify({"success": False, "error": str(e)}), 500


# Endpoint 2: Scholarship & Financial Aid Matcher
@app.route("/match-scholarship", methods=["POST"])
def match_scholarship():
    try:
        data = request.get_json(force=True) or {}
        marks = data.get("marks", "")
        income = data.get("income", "")
        lang = data.get("lang", "en")

        if not marks or not income:
            return jsonify({"success": False, "error": "Marks and income required."}), 400

        lang_prompts = {
            "ta": "Respond strictly in Tamil (தமிழ் script).",
            "hi": "Respond strictly in Hindi (हिन्दी script).",
            "en": "Respond in English."
        }
        instruction = lang_prompts.get(lang, lang_prompts["en"])

        system_msg = (
            "You are an AI scholarship and educational aid consultant.\n"
            "Recommend 2 matching government or CSR scholarships based on marks and income.\n"
            f"{instruction}\n"
            "Keep the response under 60 words."
        )
        user_msg = f"Student Marks: {marks}%\nAnnual Family Income: INR {income}"

        reply = query_groq_ai(system_msg, user_msg)
        return jsonify({"success": True, "result": reply})

    except Exception as e:
        print(f"Error in /match-scholarship: {e}")
        return jsonify({"success": False, "error": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)