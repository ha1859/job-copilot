import streamlit as st
from resume_reader import get_resume_text
from job_matcher import match_job

st.set_page_config(page_title="Job Copilot", layout="wide")
st.title("Job Copilot")
st.caption("See how well your resume fits a job, and what's missing.")

left, right =  st.columns(2)
with left:
    resume_file = st.file_uploader("Your resume (PDF)", type="pdf")
with right:
    job_posting = st.text_area(
        "Job posting", 
        height=300,
        placeholder="Paste the full job posting here",
        )
if st.button("Score my fit", type="primary", use_container_width=True):
    if resume_file is None or not job_posting.strip():
        st.warning("Upload your resume and paste a job posting first.")
    else:

        with st.spinner("Comparing your resume to the job posting..."):
            resume_text = get_resume_text(resume_file)
            result = match_job(resume_text, job_posting)

            st.metric("Match Score", f"{result['score']}/100")
            st.progress(result['score']/100)

        matched_col, gaps_col = st.columns(2)
        with matched_col:
            st.subheader("What matches")
            for skill in result["matched_skills"]:
                st.markdown(f"- {skill}")

        with gaps_col:
            st.subheader("Gaps")
            for gap in result ["gaps"]:
                st.markdown(f"- {gap}")



