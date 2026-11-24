import os
import streamlit as st

st.set_page_config(page_title="Job Copilot", layout="wide")


# ---------- Secrets ----------
# Locally, keys come from .env. When deployed, they come from Streamlit secrets.
# Copy any deployed secrets into environment variables BEFORE importing the
# modules that create the Claude client.
def load_deployed_secrets():
    try:
        for key in ("ANTHROPIC_API_KEY", "APP_PASSWORD"):
            if key in st.secrets and not os.getenv(key):
                os.environ[key] = str(st.secrets[key])
    except Exception:
        pass  # no secrets file locally, which is fine


load_deployed_secrets()

from resume_reader import get_resume_text  # noqa: E402
from job_matcher import match_job  # noqa: E402
from job_summarizer import summarize_job  # noqa: E402
from resume_tailor import tailor_resume, apply_changes  # noqa: E402
import tracker  # noqa: E402


# ---------- Styles ----------
st.markdown(
    """
    <style>
    .block-container {padding-top: 2rem; max-width: 1200px;}
    .hero h1 {font-size: 2.4rem; margin-bottom: 0;}
    .hero p {color: #6B7280; font-size: 1.05rem; margin-top: 0.25rem;}
    .score {font-size: 3.5rem; font-weight: 800; line-height: 1;}
    .score-label {color: #6B7280; font-size: 0.9rem; text-transform: uppercase; letter-spacing: 0.05em;}
    .chip {display: inline-block; padding: 0.2rem 0.65rem; margin: 0.15rem; border-radius: 999px;
           background: #EEF2FF; color: #3730A3; font-size: 0.85rem;}
    .before {color: #6B7280; text-decoration: line-through;}
    .after {color: #065F46; font-weight: 500;}
    </style>
    """,
    unsafe_allow_html=True,
)


# ---------- Optional password (for the public demo) ----------
password = os.getenv("APP_PASSWORD")
if password and not st.session_state.get("unlocked"):
    st.title("Job Copilot")
    entered = st.text_input("Enter the demo password", type="password")
    if entered == password:
        st.session_state.unlocked = True
        st.rerun()
    elif entered:
        st.error("Wrong password.")
    st.stop()


# ---------- Helpers ----------
def score_color(score):
    if score >= 75:
        return "#059669"  # green
    if score >= 50:
        return "#D97706"  # amber
    return "#DC2626"  # red


def show_score(label, score):
    st.markdown(
        f"<div class='score-label'>{label}</div>"
        f"<div class='score' style='color:{score_color(score)}'>{score}<span style='font-size:1.5rem;color:#9CA3AF'>/100</span></div>",
        unsafe_allow_html=True,
    )
    st.progress(max(0, min(score, 100)) / 100)


def chips(items):
    if items:
        st.markdown("".join(f"<span class='chip'>{item}</span>" for item in items),
                    unsafe_allow_html=True)


def run_safely(message, fn, *args):
    """Run an AI call with a spinner, and show a friendly error if it fails."""
    try:
        with st.spinner(message):
            return fn(*args)
    except Exception as error:
        st.error(f"Something went wrong: {error}")
        return None


def clear_results():
    """When the job posting changes, old results no longer apply."""
    for key in ("match", "summary", "tailor", "tailored"):
        st.session_state.pop(key, None)


# ---------- Sidebar: resume ----------
with st.sidebar:
    st.header("Your resume")
    uploaded = st.file_uploader("Upload a PDF", type="pdf")
    if uploaded is not None and st.session_state.get("resume_name") != uploaded.name:
        st.session_state.resume_text = get_resume_text(uploaded)
        st.session_state.resume_name = uploaded.name
        clear_results()

    resume_text = st.session_state.get("resume_text", "")
    if resume_text:
        st.success(f"Loaded {st.session_state.resume_name} ({len(resume_text.split())} words)")
    else:
        st.info("Upload your resume to get started.")

    st.divider()
    st.caption("Job Copilot never invents experience. Every resume change is a suggestion you approve.")


# ---------- Header ----------
st.markdown(
    "<div class='hero'><h1>Job Copilot</h1>"
    "<p>See how well you fit a job, tailor your resume honestly, and track every application.</p></div>",
    unsafe_allow_html=True,
)

job_posting = st.text_area(
    "Job posting",
    height=200,
    placeholder="Paste the full job posting here",
    key="job_posting",
    on_change=clear_results,
)

match_tab, summary_tab, tailor_tab, tracker_tab = st.tabs(
    ["Match", "Job summary", "Tailor resume", "Tracker"]
)

ready = bool(resume_text) and bool(job_posting.strip())


# ---------- Tab 1: Match ----------
with match_tab:
    if st.button("Score my fit", type="primary", use_container_width=True):
        if not ready:
            st.warning("Upload your resume and paste a job posting first.")
        else:
            st.session_state.match = run_safely(
                "Comparing your resume to the job...", match_job, resume_text, job_posting
            )

    result = st.session_state.get("match")
    if result:
        show_score("Match score", result["score"])
        matched_col, gaps_col = st.columns(2)
        with matched_col:
            with st.container(border=True):
                st.subheader("What matches")
                for skill in result["matched_skills"]:
                    st.markdown(f"- {skill}")
        with gaps_col:
            with st.container(border=True):
                st.subheader("Gaps")
                for gap in result["gaps"]:
                    st.markdown(f"- {gap}")
        st.caption("Next: open **Tailor resume** to close the gaps you truthfully can.")


# ---------- Tab 2: Job summary ----------
with summary_tab:
    if st.button("Summarize this job", type="primary", use_container_width=True):
        if not job_posting.strip():
            st.warning("Paste a job posting first.")
        else:
            st.session_state.summary = run_safely(
                "Reading the job posting...", summarize_job, job_posting
            )

    summary = st.session_state.get("summary")
    if summary:
        st.subheader(f"{summary['company']} - {summary['role']}")
        loc_col, pay_col = st.columns(2)
        loc_col.metric("Location", summary["location"])
        pay_col.metric("Salary", summary["salary"])
        req_col, nice_col = st.columns(2)
        with req_col:
            with st.container(border=True):
                st.markdown("**Required skills**")
                chips(summary["required_skills"])
        with nice_col:
            with st.container(border=True):
                st.markdown("**Nice to have**")
                chips(summary["nice_to_have"])


# ---------- Tab 3: Tailor resume ----------
with tailor_tab:
    st.markdown(
        "Claude suggests rewrites of lines already on your resume, using this job's language. "
        "It can't add experience you don't have. Uncheck any change you don't want."
    )
    if st.button("Suggest changes", type="primary", use_container_width=True):
        if not ready:
            st.warning("Upload your resume and paste a job posting first.")
        else:
            st.session_state.pop("tailored", None)
            st.session_state.tailor = run_safely(
                "Finding lines to tailor...", tailor_resume, resume_text, job_posting
            )

    tailor = st.session_state.get("tailor")
    if tailor:
        with st.container(border=True):
            st.markdown("**Suggested summary**")
            st.write(tailor["summary"])
            st.markdown("**Keywords to emphasize**")
            chips(tailor["keywords_to_emphasize"])

        accepted = []
        for i, change in enumerate(tailor["changes"]):
            with st.container(border=True):
                keep = st.checkbox("Use this change", value=True, key=f"accept_{i}")
                st.markdown(f"<div class='before'>{change['original']}</div>", unsafe_allow_html=True)
                st.markdown(f"<div class='after'>{change['suggested']}</div>", unsafe_allow_html=True)
                if change.get("reason"):
                    st.caption(change["reason"])
                if keep:
                    accepted.append(change)

        label = "change" if len(accepted) == 1 else "changes"
        if st.button(f"Build tailored resume ({len(accepted)} {label})", use_container_width=True):
            new_text, applied = apply_changes(resume_text, accepted)
            before = st.session_state.get("match") or run_safely(
                "Scoring your original resume...", match_job, resume_text, job_posting
            )
            after = run_safely("Scoring your tailored resume...", match_job, new_text, job_posting)
            if before and after:
                st.session_state.match = before
                st.session_state.tailored = {
                    "text": new_text,
                    "applied": applied,
                    "requested": len(accepted),
                    "before": before["score"],
                    "after": after["score"],
                }

    tailored = st.session_state.get("tailored")
    if tailored:
        st.divider()
        before_col, after_col = st.columns(2)
        with before_col:
            show_score("Before", tailored["before"])
        with after_col:
            show_score("After", tailored["after"])
        if tailored["applied"] < tailored["requested"]:
            st.info(
                f"Applied {tailored['applied']} of {tailored['requested']} changes. "
                "Some lines couldn't be matched exactly, so copy those by hand."
            )
        st.text_area("Tailored resume text", tailored["text"], height=300)
        st.download_button("Download as .txt", tailored["text"], file_name="tailored_resume.txt",
                           use_container_width=True)
        st.caption("Paste these lines into your real resume file and keep your original formatting.")


# ---------- Tab 4: Tracker ----------
with tracker_tab:
    summary = st.session_state.get("summary") or {}
    match = st.session_state.get("match") or {}
    tailored = st.session_state.get("tailored") or {}

    with st.expander("Save this job to your tracker", expanded=bool(job_posting.strip())):
        with st.form("save_job", clear_on_submit=True):
            c1, c2, c3 = st.columns([2, 2, 1])
            company = c1.text_input("Company", value=summary.get("company", ""))
            role = c2.text_input("Role", value=summary.get("role", ""))
            status = c3.selectbox("Status", tracker.STATUSES, index=1)
            notes = st.text_area("Notes", height=80)
            st.caption("Tip: run Job summary first to fill in the company and role.")
            if st.form_submit_button("Save", type="primary"):
                try:
                    tracker.add_application(
                        company, role, status,
                        score=tailored.get("after") or match.get("score"),
                        notes=notes,
                        tailored_resume=tailored.get("text", ""),
                        job_posting=job_posting,
                    )
                    st.success(f"Saved {company}.")
                except ValueError as error:
                    st.error(str(error))

    applications = tracker.list_applications()
    if not applications:
        st.info("No applications yet. Save your first one above.")
    else:
        counts = st.columns(len(tracker.STATUSES))
        for col, name in zip(counts, tracker.STATUSES):
            col.metric(name, sum(1 for a in applications if a["status"] == name))

        for app in applications:
            score = f" | score {app['score']}" if app["score"] is not None else ""
            with st.expander(f"{app['company']} - {app['role'] or 'Role'} | {app['status']}{score}"):
                st.caption(f"Added {app['date_added']}")
                c1, c2 = st.columns([1, 3])
                new_status = c1.selectbox("Status", tracker.STATUSES,
                                          index=tracker.STATUSES.index(app["status"]),
                                          key=f"status_{app['id']}")
                new_notes = c2.text_area("Notes", app["notes"], key=f"notes_{app['id']}", height=80)
                b1, b2 = st.columns(2)
                if b1.button("Save changes", key=f"save_{app['id']}", use_container_width=True):
                    tracker.update_application(app["id"], new_status, new_notes)
                    st.rerun()
                if b2.button("Delete", key=f"delete_{app['id']}", use_container_width=True):
                    tracker.delete_application(app["id"])
                    st.rerun()
                if app["tailored_resume"]:
                    st.text_area("Tailored resume used", app["tailored_resume"], height=200,
                                 key=f"resume_{app['id']}", disabled=True)
