import pypdf
from pptx import Presentation
import google.generativeai as genai
import os
from dotenv import load_dotenv
import re

load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

class AgentA_Parser:
    def extract_text(self, uploaded_file):
        """Extracts text from PDF or PPTX bytes."""
        extension = uploaded_file.name.split('.')[-1].lower()
        text = ""
        
        if extension == "pdf":
            reader = pypdf.PdfReader(uploaded_file)
            for page in reader.pages:
                text += page.extract_text() or ""
        elif extension in ["pptx", "ppt"]:
            prs = Presentation(uploaded_file)
            for slide in prs.slides:
                for shape in slide.shapes:
                    if hasattr(shape, "text"):
                        text += shape.text + " "
        return text

    def analyze_content(self, raw_text):
        """Uses LLM to deeply analyze document structure and generate research queries."""
        model = genai.GenerativeModel('gemini-3-flash-preview')
        
        prompt = f"""
You are Agent A (The Intelligent Parser).

Your role is to deeply analyze the provided educational document.
The content may belong to any domain (e.g., Mathematics, Finance, Artificial Intelligence, Computer Science, etc.).

Perform the following tasks carefully and concisely:

1. MAIN SUBJECT
   - Identify the single primary subject of the document.
   - Provide a one-line clear definition of that subject.

2. CORE TOPICS
   - Extract the top 5 most important core topics discussed.
   - For each topic:
       • Provide a short explanation (1–2 sentences).
       • Mention why it is important in the context of the document.

3. 2026 UPDATE SEARCH QUERIES
   - Generate 3 highly specific and research-focused search queries.
   - Each query must:
       • Include the year "2026"
       • Be designed to find recent advancements, updates, or new research
       • Be clear, targeted, and suitable for academic or technical search engines

Output Format (strictly follow this structure):

MAIN SUBJECT:
<subject name>
<one-line definition>

CORE TOPICS:
1. <Topic Name>
   - Explanation:
   - Importance:

2. <Topic Name>
   - Explanation:
   - Importance:

3. <Topic Name>
   - Explanation:
   - Importance:

4. <Topic Name>
   - Explanation:
   - Importance:

5. <Topic Name>
   - Explanation:
   - Importance:

SEARCH QUERIES FOR 2026 UPDATES:
1. "<query 1>"
2. "<query 2>"
3. "<query 3>"

DOCUMENT TEXT:
{raw_text[:15000]}
"""
        response = model.generate_content(prompt)
        return response.text
    def get_search_queries(self, report_text):
        """Extracts the 3 queries from the LLM report using Regex."""
        queries = re.findall(r'"([^"]*2026[^"]*)"', report_text)

        # return only first 3 found
        return queries[:3]
