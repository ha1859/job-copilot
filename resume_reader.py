import pdfplumber

# 1. Open "resume.pdf" with pdfplumber (use a "with" block)
with pdfplumber.open("resume.pdf") as pdf:
# 2. Make an empty list to hold each page's text
        pages_text = []
# 3. Loop through each page in pdf.pages
        for page in pdf.pages:
# 4. Get the page's text with page.extract_text() and add it to your list
                pages_text.append(page.extract_text() or "")
# 5. Join the list into one string with "\n".join(...)
        full_text = "\n".join(pages_text)
# 6. Print the result
        print(full_text)