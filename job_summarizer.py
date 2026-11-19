import os # allows python to access files & whatnot from my mac
import json # allows python to read and write json files
from dotenv import load_dotenv # this is where we load our API key from the .env file
from anthropic import Anthropic # allows us to use claude's API

load_dotenv() # load the .env file

client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY")) # create a client to talk to claude

def summarize_job(job_posting):
    prompt = f"""You are an experienced technical recruiter. I want you to analyze the following job posting and summarize the information as concisely and as simply as you can.

Job Posting:
{job_posting}

Respond with only a JSON object. No markdown, no code fences, no other text. Use this format:
{{"company": "", "role": "", "location": "", "salary": "", "required_skills": [], "nice_to_have": []}}

If something isn't in the posting, use "Not listed".

"""
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
    with open("job_posting.txt") as f:
        job_posting = f.read()

    result = summarize_job(job_posting)

    print(f"Company: {result['company']}", f"Role: {result['role']}")
    print (f"Location: {result['location']}", f"Salary: {result['salary']}")
    print("\nRequired Skills:")
    for skill in result["required_skills"]:
        print(f"- {skill}")
    print("\nNice to Have:")
    for skill in result["nice_to_have"]:
        print(f"- {skill}")


