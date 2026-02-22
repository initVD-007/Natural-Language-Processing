import google.generativeai as genai

class AgentC_Auditor:
    def __init__(self, api_key: str):
        if not api_key:
            raise ValueError("Google API Key is required.")
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-3-flash-preview')

    def generate_audit_report(self, syllabus_analysis, web_research):
        """Compares syllabus with live web data to find gaps and modernization strategy."""

        prompt = f"""
You are Agent C – Senior Academic Curriculum Auditor (2026 Industry Standards Specialist).

Your responsibility is to critically evaluate, modernize, and strategically upgrade the curriculum
to align with 2026 global industry standards, job market trends, and emerging technologies.

------------------------------
INPUT DATASET 1: CURRENT SYLLABUS
------------------------------
{syllabus_analysis}

------------------------------
INPUT DATASET 2: 2026 INDUSTRY & MARKET RESEARCH
------------------------------
{web_research}

==============================
OBJECTIVE
==============================
Perform a deep comparative analysis between the syllabus and real-world industry expectations.

You must think like:
• A University Accreditation Board Member  
• A Hiring Manager at a Tech Company  
• A Curriculum Modernization Consultant  

==============================
ANALYSIS REQUIREMENTS
==============================

1. GAP ANALYSIS  
- Identify important skills, tools, frameworks, technologies, or methodologies 
  present in Industry Research but missing in the syllabus.
- Classify gaps into:
    • Critical (Must Add Immediately)
    • Important (Should Add)
    • Emerging (Future-Relevant)

2. STALE / OUTDATED CONTENT  
- Identify topics in the syllabus that are:
    • Technologically outdated
    • Low industry demand
    • Replaced by modern alternatives
- Suggest modern replacements (if applicable).

3. SKILL RELEVANCE SCORING  
- Provide a 0-10 relevance score for major syllabus modules 
  based on 2026 industry demand.
- Briefly justify each score.

4. INDUSTRY ALIGNMENT SUMMARY  
- Evaluate how well the syllabus prepares students for:
    • Entry-level jobs
    • Internships
    • Competitive tech roles
    • Higher studies

5. STRATEGIC ACTION PLAN FOR PROFESSOR  
Provide a structured roadmap:
    • Immediate changes (0-3 months)
    • Short-term upgrades (3-6 months)
    • Long-term modernization (6-12 months)

6. ADDITIONAL RECOMMENDATIONS  
- Suggest:
    • Capstone project ideas aligned with 2026 trends
    • Practical tools/platforms to introduce
    • Certifications worth integrating
    • Industry collaboration opportunities

==============================
OUTPUT FORMAT
==============================
Generate a formal, structured Academic Audit Report with:

• Executive Summary  
• Gap Analysis Table  
• Stale Content Table  
• Relevance Scoring Table  
• Strategic Action Plan  
• Final Recommendation  

Keep the tone professional, data-driven, and solution-oriented.
Avoid generic statements. Be specific and actionable.
"""

        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            raise Exception(f"Auditor failed to generate report: {str(e)}")