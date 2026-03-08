import streamlit as st
import os
import sys

# Get project root directory
current_dir = os.path.dirname(__file__)
project_root = os.path.abspath(os.path.join(current_dir, "..", ".."))

sys.path.insert(0, project_root)

# Backend imports
from backend.resume_parser import extract_text, extract_email, extract_skills, extract_experience
from backend.database import insert_candidate, update_score, create_table
from backend.matcher import rank_candidates

# Create database table
create_table()

# Page config
st.set_page_config(page_title="Recruiter AI Agent", layout="wide")

st.title("Recruiter AI Agent - Resume Parser")

st.write("Upload a resume (PDF or DOCX) to extract skills and details.")

# ---------------------------------
# Resume Upload Section
# ---------------------------------

uploaded_file = st.file_uploader("Upload Resume", type=["pdf", "docx"])

if uploaded_file is not None:

    temp_folder = "temp_resume"
    os.makedirs(temp_folder, exist_ok=True)

    temp_path = os.path.join(temp_folder, uploaded_file.name)

    with open(temp_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    st.success("Resume uploaded successfully!")

    # Extract resume text
    text = extract_text(temp_path)

    # Extract candidate information
    email = extract_email(text)
    skills = extract_skills(text)
    experience = extract_experience(text)

    # Store candidate
    if email:
        insert_candidate(
            email,
            ",".join(skills),
            experience
        )

    st.subheader("Extracted Information")

    st.write("Email:", email)
    st.write("Experience:", experience, "years")

    st.subheader("Extracted Skills")

    if skills:
        for skill in skills:
            st.write("•", skill)
    else:
        st.write("No skills detected.")

    with st.expander("View Extracted Resume Text"):
        st.write(text)

# ---------------------------------
# Job Requirement Section
# ---------------------------------

st.header("Enter Job Requirements")

job_role = st.text_input("Job Role")

required_skills = st.text_input(
    "Required Skills (comma separated)"
)

required_exp = st.number_input(
    "Minimum Experience",
    min_value=0
)

skills_list = [
    skill.strip().lower()
    for skill in required_skills.split(",")
    if skill
]

# ---------------------------------
# Candidate Ranking Section
# ---------------------------------

st.subheader("Candidate Matching")

if st.button("Rank Candidates"):

    if not skills_list:
        st.warning("Please enter required skills.")

    else:

        results = rank_candidates(
            skills_list,
            required_exp
        )

        if results:

            # Update scores in database
            for candidate in results:
                update_score(
                    candidate["email"],
                    candidate["score"]
                )

            st.subheader("Candidate Dashboard")

            st.table(results)

        else:
            st.warning("No candidates found in database.")

# Run command
# streamlit run "frontend/Streamlit UI/app.py"