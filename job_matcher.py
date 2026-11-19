import os
import json
from dotenv import load_dotenv
from anthropic import Anthropic
from resume_reader import get_resume_text
from datetime import date

load_dotenv()
client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

def match_job(resume_text, job_posting):

    prompt = f"""Today's date is {date.today()}. You are an experienced technical recruiter. Compare the resume to the job posting and judge honestly how well the candidate fits. Only count skills and experience the resume clearly shows.

Resume:
{resume_text}

Job posting:
{job_posting}

Respond with only a JSON object. No markdown, no code fences, no other text. Use this format:
{{"score": 0-100, "matched_skills": ["skills from the job posting the resume clearly shows"], "gaps": ["requirements in the job posting the resume doesn't show"]}}"""

    response = client.messages.create(
        model="claude-sonnet-5-5",
        max_tokens=1500,
        messages=[{"role": "user", "content": prompt}],
    )

    text = ""
    for block in response.content:
        if block.type == "text":
            text = block.text

    start = text.find("{")
    end = text.rfind("}") + 1 

    result = json.loads(text[start:end])
    return result

if __name__ == "__main__":
    resume_text = get_resume_text("resume.pdf")

    with open("job_posting.txt") as f:
        job_posting = f.read()

    result = match_job(resume_text, job_posting)

    print(f"Match score: {result['score']}/100")

    print("\nMatched skills:")
    for skill in result["matched_skills"]:
        print(f"- {skill}")

    print("\nGaps:")
    for gap in result["gaps"]:
        print(f"- {gap}")

