import os
from dotenv import load_dotenv
from anthropic import Anthropic
from resume_reader import get_resume_text

# 1. Load your .env file
load_dotenv()

# 2. Create the Claude client with your API key
client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
# 3. Get your resume text using your function (looks like we just call the function)
resume_text = get_resume_text("resume.pdf")
# 4. Send a message asking Claude to summarize your resume in 3 bullets
response = client.messages.create(
    model="claude-sonnet-5-5",
    max_tokens=1500,
    messages=[
        {"role": "user", "content": f"Summarize this resume in 3 bullet points:\n\n{resume_text}"}
    ],
)
# 5. Print Claude's reply
for block in response.content:
    if block.type == "text":
        print(block.text)