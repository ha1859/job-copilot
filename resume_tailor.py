"""Suggest honest, job-specific rewrites of resume lines, then apply the ones you accept."""
import os
import re
import json
from datetime import date
from dotenv import load_dotenv
from anthropic import Anthropic

load_dotenv()
client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))


def tailor_resume(resume_text, job_posting):
    prompt = f"""Today's date is {date.today()}.

You are an expert resume writer helping a candidate tailor their resume to one specific job.

Rules you must follow:
- Only rephrase lines, change emphasis, or use the job's wording for experience the resume ALREADY shows.
- Never invent employers, titles, dates, numbers, tools, skills, or results. Keep every number exactly as written.
- Pick the 4 to 8 lines that would benefit most from tailoring. Skip lines that are already strong.
- The "original" value must be copied word for word from the resume.

Resume:
{resume_text}

Job posting:
{job_posting}

Respond with only a JSON object. No markdown, no code fences, no other text. Use this format:
{{"summary": "a tailored 2-3 sentence professional summary using only facts from the resume",
  "changes": [{{"original": "exact line from the resume", "suggested": "rewritten line", "reason": "why this helps for this job"}}],
  "keywords_to_emphasize": ["job keywords the resume truthfully supports"]}}"""

    response = client.messages.create(
        model="claude-sonnet-5-5",
        max_tokens=4000,
        messages=[{"role": "user", "content": prompt}],
    )

    text = ""
    for block in response.content:
        if block.type == "text":
            text = block.text

    start = text.find("{")
    end = text.rfind("}") + 1
    result = json.loads(text[start:end])

    # Keep only well-formed changes so the app never breaks on a bad item.
    changes = []
    for change in result.get("changes", []):
        if isinstance(change, dict) and change.get("original") and change.get("suggested"):
            changes.append(change)

    return {
        "summary": result.get("summary", ""),
        "changes": changes,
        "keywords_to_emphasize": result.get("keywords_to_emphasize", []),
    }


def apply_changes(resume_text, changes):
    """Swap each accepted original line for its suggestion.

    PDF text often breaks one bullet across several lines, so the match ignores
    differences in spaces and line breaks. Returns (new_text, number_applied).
    """
    new_text = resume_text
    applied = 0
    for change in changes:
        words = change["original"].split()
        if not words:
            continue
        pattern = r"\s+".join(re.escape(word) for word in words)
        new_text, count = re.subn(pattern, lambda m: change["suggested"], new_text, count=1)
        applied += count
    return new_text, applied
