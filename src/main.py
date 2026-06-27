import os
import sys
from dotenv import load_dotenv

from src.agents.assessor import assess_user
from src.agents.researcher import research_projects
from src.agents.curriculum_builder import build_curriculum
from src.agents.reviewer import review_curriculum


def main():
    load_dotenv()

    gemini_key = os.getenv("GEMINI_API_KEY")
    if not gemini_key:
        raise EnvironmentError("ERROR: GEMINI_API_KEY not found in .env file")

    test_user = {
        "languages": "Python, basic HTML/CSS",
        "experience_years": "1 year",
        "projects_built": "a todo app, a weather app",
        "goal": "get a junior backend developer job",
        "hours_per_week": "15",
        "timeline_weeks": "8",
    }

    try:
        assessment = assess_user(test_user)
        print("Assessment result:", assessment)

        projects = research_projects(assessment)
        print(f"Projects found: {len(projects)}")

        timeline_weeks = int(test_user["timeline_weeks"])
        curriculum = build_curriculum(assessment, projects, timeline_weeks)
        print(f"Weeks built: {len(curriculum['weeks'])}")

        reviewed = review_curriculum(curriculum, assessment)
        print(f"Overall feedback: {reviewed['overall_feedback']}")
        print(f"Difficulty rating: {reviewed['difficulty_rating']}")

        print("\nPipeline complete.")
    except Exception as e:
        print(f"Pipeline error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
