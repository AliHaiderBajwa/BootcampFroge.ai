import os
import re
import json
import google.generativeai as genai
from dotenv import load_dotenv


def review_curriculum(curriculum: dict, assessment: dict) -> dict:
    load_dotenv()

    gemini_key = os.getenv("GEMINI_API_KEY")
    if not gemini_key:
        raise ValueError("GEMINI_API_KEY not found in .env")

    genai.configure(api_key=gemini_key)
    model = genai.GenerativeModel(model_name="gemini-1.5-flash")

    system_prompt = (
        "You are a senior bootcamp mentor and curriculum reviewer. "
        "Review the curriculum and add mentorship checkpoints, then return "
        "ONLY a raw JSON object with no markdown and no explanation "
        "with these exact keys:\n"
        "    - overall_feedback: 2-3 sentences on the curriculum's strengths\n"
        "    - difficulty_rating: one of 'too easy', 'well balanced', 'too hard'\n"
        "    - weeks: the same weeks list from the curriculum but with one "
        "extra key added to each week object:\n"
        "      - checkpoint: a specific question or task the user must complete "
        "before moving to the next week. Must be concrete and testable, not vague. "
        "Example: 'Can you add user authentication to your app and explain how "
        "JWT tokens work?' not 'Review your progress.'\n"
        "    - final_project: a capstone project object with:\n"
        "      - title: name of the final project\n"
        "      - description: what to build in 3-4 sentences\n"
        "      - requirements: list of 5 specific technical requirements\n"
        "      - estimated_hours: integer"
    )

    weeks_summary = "\n".join(
        f"Week {w['week_number']} ({w['theme']}): {w['project']} - "
        f"Goals: {', '.join(w['goals'])}. Deliverable: {w['deliverable']}"
        for w in curriculum["weeks"]
    )

    user_message = (
        f"Assessment summary:\n{assessment['assessment_summary']}\n\n"
        f"Curriculum summary:\n"
        f"Total weeks: {curriculum['total_weeks']}\n"
        f"Weekly hours: {curriculum['weekly_hours']}\n"
        f"Stack focus: {curriculum['stack_focus']}\n\n"
        f"Weeks:\n{weeks_summary}"
    )

    prompt = f"{system_prompt}\n\n{user_message}"

    try:
        response = model.generate_content(prompt)
        raw = response.text.strip()

        raw = re.sub(r"^```(?:json)?\s*", "", raw)
        raw = re.sub(r"\s*```$", "", raw)

        result = json.loads(raw)

        if len(result["weeks"]) != len(curriculum["weeks"]):
            raise ValueError(
                f"Expected {len(curriculum['weeks'])} weeks, got {len(result['weeks'])}"
            )

        print("Review complete. Checkpoints added.")
        return result
    except (json.JSONDecodeError, KeyError, ValueError) as e:
        raise RuntimeError(f"Failed to parse review response: {e}")
