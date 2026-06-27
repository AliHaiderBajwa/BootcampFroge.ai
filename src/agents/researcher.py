import os
import re
import json
import google.generativeai as genai
from dotenv import load_dotenv


def research_projects(assessment: dict) -> list:
    load_dotenv()

    gemini_key = os.getenv("GEMINI_API_KEY")
    if not gemini_key:
        raise ValueError("GEMINI_API_KEY not found in .env")

    genai.configure(api_key=gemini_key)
    model = genai.GenerativeModel(model_name="gemini-1.5-flash")

    system_prompt = (
        "You are a coding curriculum researcher. "
        "Based on the assessment provided, find and return ONLY a raw JSON array "
        "with no markdown and no explanation. "
        "The array must contain exactly 8 project objects. "
        "Each project object must have these exact keys:\n"
        "    - title: short project name\n"
        "    - description: what the project does in one sentence\n"
        "    - skills_taught: list of 3-4 specific skills this project teaches\n"
        "    - difficulty: one of 'easy', 'medium', 'hard'\n"
        "    - estimated_hours: integer number of hours to complete\n"
        "    - why_this_project: one sentence explaining why it fits this user"
    )

    user_message = (
        f"Level: {assessment['level']}\n"
        f"Strong languages: {assessment['strong_languages']}\n"
        f"Weak areas: {assessment['weak_areas']}\n"
        f"Recommended stack: {assessment['recommended_stack']}\n"
        f"Assessment summary: {assessment['assessment_summary']}"
    )

    prompt = f"{system_prompt}\n\n{user_message}"

    try:
        response = model.generate_content(prompt)
        raw = response.text.strip()

        raw = re.sub(r"^```(?:json)?\s*", "", raw)
        raw = re.sub(r"\s*```$", "", raw)

        result = json.loads(raw)

        if not isinstance(result, list) or len(result) != 8:
            raise ValueError(
                f"Expected exactly 8 projects, got {len(result) if isinstance(result, list) else 'non-list'}"
            )

        print("Research complete. 8 projects found.")
        return result
    except (json.JSONDecodeError, KeyError, ValueError) as e:
        raise RuntimeError(f"Failed to parse research response: {e}")
