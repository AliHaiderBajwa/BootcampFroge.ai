import os
import re
import json
import google.generativeai as genai
from dotenv import load_dotenv


def assess_user(user_input: dict) -> dict:
    load_dotenv()

    gemini_key = os.getenv("GEMINI_API_KEY")
    if not gemini_key:
        raise ValueError("GEMINI_API_KEY not found in .env")

    genai.configure(api_key=gemini_key)
    model = genai.GenerativeModel(model_name="gemini-1.5-flash")

    system_prompt = (
        "You are a senior coding mentor. "
        "Assess the user's current level and return ONLY a raw JSON object "
        "with no markdown and no explanation with these exact keys:\n"
        "    - level: one of 'beginner', 'intermediate', 'advanced'\n"
        "    - strong_languages: list of languages they know well\n"
        "    - weak_areas: list of specific gaps or weaknesses\n"
        "    - recommended_stack: the stack they should focus on given their goal\n"
        "    - assessment_summary: 2-3 sentences summarizing their profile"
    )

    user_message = (
        f"Languages: {user_input['languages']}\n"
        f"Experience years: {user_input['experience_years']}\n"
        f"Projects built: {user_input['projects_built']}\n"
        f"Goal: {user_input['goal']}\n"
        f"Hours per week: {user_input['hours_per_week']}\n"
        f"Timeline weeks: {user_input['timeline_weeks']}"
    )

    prompt = f"{system_prompt}\n\n{user_message}"

    try:
        response = model.generate_content(prompt)
        raw = response.text.strip()

        raw = re.sub(r"^```(?:json)?\s*", "", raw)
        raw = re.sub(r"\s*```$", "", raw)

        result = json.loads(raw)
        print(f"Assessment complete for: {user_input['goal']}")
        return result
    except (json.JSONDecodeError, KeyError) as e:
        raise RuntimeError(f"Failed to parse assessment response: {e}")
