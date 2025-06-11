import google.generativeai as genai
import os

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def gemini_prompt(prompt_text):
    model = genai.GenerativeModel("gemini-2.0-flash")
    response = model.generate_content(prompt_text)
    return response.text

def get_subtopics_prompt(query):
    return f"""
The user wants to research: "{query}"

Break this topic down into 3-5 clear, researchable sub-questions or areas to explore.
Respond with a numbered list of sub-questions only.
"""

def summarize_web_content_prompt(sub_question, article_text):
    return f"""
The following is web content gathered while researching the question: "{sub_question}"

--- Start of Article ---
{article_text[:5000]}
--- End of Article ---

Write a concise summary (3–5 sentences) answering the question based on this article. Be objective and do not invent facts.
"""

def summarize_document_section_prompt(topic, document_text):
    return f"""
The user is researching: "{topic}"

The following content is from a document the user uploaded. Analyze it and extract any relevant information about the topic.

--- Document Content ---
{document_text[:5000]}
--- End of Document ---

Write a concise and factual summary of information in this document related to the topic.
"""
