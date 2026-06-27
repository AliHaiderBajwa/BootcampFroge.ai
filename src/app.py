import streamlit as st

from src.agents.assessor import assess_user
from src.agents.researcher import research_projects
from src.agents.curriculum_builder import build_curriculum
from src.agents.reviewer import review_curriculum

st.set_page_config(page_title="Coding Bootcamp Builder", layout="centered")

st.title("Coding Bootcamp Builder")
st.caption("Build your personal coding bootcamp in seconds.")


if "results" not in st.session_state:
    st.session_state["results"] = None

with st.form("input_form"):
    languages = st.text_input("What languages or frameworks do you know?")
    experience_years = st.text_input("How long have you been coding?")
    projects_built = st.text_area("What have you built before? List any projects.")
    goal = st.text_input(
        "What is your goal?",
        placeholder="e.g. get a backend job, go freelance",
    )

    col1, col2 = st.columns(2)
    with col1:
        hours_per_week = st.number_input(
            "Hours available per week", min_value=1, max_value=40, value=10
        )
    with col2:
        timeline_raw = st.selectbox(
            "Timeline",
            ["4 weeks", "8 weeks", "12 weeks", "16 weeks"],
        )

    submitted = st.form_submit_button(
        "Build My Bootcamp", type="primary", use_container_width=True
    )

if submitted:
    if not all([languages, experience_years, projects_built, goal]):
        st.error("Please fill in all fields before building your bootcamp.")
        st.stop()

    timeline_weeks = int(timeline_raw.split()[0])

    user_input = {
        "languages": languages,
        "experience_years": experience_years,
        "projects_built": projects_built,
        "goal": goal,
        "hours_per_week": str(hours_per_week),
        "timeline_weeks": str(timeline_weeks),
    }

    try:
        with st.spinner("Assessing your current level..."):
            assessment = assess_user(user_input)

        with st.spinner("Researching the best projects for you..."):
            projects = research_projects(assessment)

        with st.spinner("Building your week-by-week curriculum..."):
            curriculum = build_curriculum(assessment, projects, timeline_weeks)

        with st.spinner("Adding mentorship checkpoints..."):
            reviewed = review_curriculum(curriculum, assessment)

        st.session_state["results"] = {
            "reviewed": reviewed,
            "stack_focus": curriculum["stack_focus"],
        }
        st.rerun()
    except Exception as e:
        st.error(f"Something went wrong: {e}")

results = st.session_state.get("results")
if results:
    reviewed = results["reviewed"]

    st.success(reviewed["overall_feedback"])
    st.info(
        f"Difficulty: {reviewed['difficulty_rating']} — "
        f"Stack: {results['stack_focus']}"
    )

    st.subheader("Your Week-by-Week Plan")
    for week in reviewed["weeks"]:
        with st.expander(f"Week {week['week_number']} — {week['theme']}"):
            st.markdown(f"**Project:** {week['project']}")
            st.markdown(f"**Deliverable:** {week['deliverable']}")
            st.markdown("**Goals:**")
            for goal_item in week["goals"]:
                st.markdown(f"- {goal_item}")
            st.markdown("**Resources:**")
            for resource in week["resources"]:
                st.markdown(f"- {resource}")
            st.warning(f"**Checkpoint:** {week['checkpoint']}")

    capstone = reviewed["final_project"]
    st.subheader("Final Capstone Project")
    st.markdown(f"**{capstone['title']}**")
    st.markdown(capstone["description"])
    st.markdown(f"**Estimated hours:** {capstone['estimated_hours']}")
    st.markdown("**Requirements:**")
    for i, req in enumerate(capstone["requirements"], 1):
        st.markdown(f"{i}. {req}")

    if st.button("Start Over"):
        st.session_state.clear()
        st.rerun()
