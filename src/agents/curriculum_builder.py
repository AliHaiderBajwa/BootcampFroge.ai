import os
import re
import json
import google.generativeai as genai
from dotenv import load_dotenv


def build_curriculum(assessment: dict, projects: list, timeline_weeks: int) -> dict:
    load_dotenv()

    gemini_key = os.getenv("GEMINI_API_KEY")
    if not gemini_key:
        raise ValueError("GEMINI_API_KEY not found in .env")

    genai.configure(api_key=gemini_key)
    model = genai.GenerativeModel(model_name="gemini-1.5-flash")

    system_prompt = (
        "You are a coding bootcamp curriculum designer. "
        "Using the assessment and project list provided, build a structured "
        "week-by-week curriculum and return ONLY a raw JSON object "
        "with no markdown and no explanation with these exact keys:\n"
        "    - total_weeks: integer\n"
        "    - weekly_hours: integer\n"
        "    - stack_focus: string\n"
        "    - weeks: a list of week objects, each containing:\n"
        "      - week_number: integer\n"
        "      - theme: short title for the week\n"
        "      - project: the project title assigned to this week\n"
        "      - goals: list of 3 specific learning goals for this week\n"
        "      - deliverable: exactly what the user should have built by end of week\n"
        "      - resources: list of 2-3 specific resource names or types to use"
    )

    projects_summary = "\n".join(
        f"- {p['title']}: {p['description']}" for p in projects
    )

    user_message = (
        f"Assessment summary:\n{assessment['assessment_summary']}\n\n"
        f"Projects:\n{projects_summary}\n\n"
        f"Timeline: {timeline_weeks} weeks"
    )

    prompt = f"{system_prompt}\n\n{user_message}"

    try:
        response = model.generate_content(prompt)
        raw = response.text.strip()

        raw = re.sub(r"^```(?:json)?\s*", "", raw)
        raw = re.sub(r"\s*```$", "", raw)

        result = json.loads(raw)

        if len(result["weeks"]) != timeline_weeks:
            raise ValueError(
                f"Expected {timeline_weeks} weeks, got {len(result['weeks'])}"
            )

        print(f"Curriculum built. {timeline_weeks} weeks planned.")
        return result
    except (json.JSONDecodeError, KeyError, ValueError) as e:
        raise RuntimeError(f"Failed to parse curriculum response: {e}")
