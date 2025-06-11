import streamlit as st
from dotenv import load_dotenv
from gemini_tools import (
    get_subtopics_prompt,
    summarize_web_content_prompt,
    summarize_document_section_prompt,
    gemini_prompt
)
from search_tools import get_web_results, scrape_text_from_url
from doc_tools import extract_text_from_pdf, save_report_as_pdf, save_report_as_docx
import os
import tempfile

load_dotenv()

st.set_page_config(page_title="Gemini Research Agent", layout="centered")
st.title("📚 LLM-Powered Research Agent")

query = st.text_input("Enter a research topic:")
document = st.file_uploader("Upload a document (PDF) (Optional)", type=["pdf"])

if st.button("Run Agent") and query:
    with st.spinner("Analyzing topic and documents..."):
        subtopics_prompt = get_subtopics_prompt(query)
        subtopics = gemini_prompt(subtopics_prompt).split("\n")

        full_report = f"## Research Report on: {query}\n"

        for sub in subtopics:
            if not sub.strip():
                continue
            st.markdown(f"#### 🔍 Researching: {sub}")
            web_content = ""
            results = get_web_results(sub)
            for link in results[:2]:
                scraped = scrape_text_from_url(link)
                if scraped:
                    web_content += scraped[:3000] + "\n"

            summary = gemini_prompt(summarize_web_content_prompt(sub, web_content))
            full_report += f"\n### {sub}\n{summary}\n"

        if document:
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
                tmp.write(document.read())
                doc_text = extract_text_from_pdf(tmp.name)
                doc_summary = gemini_prompt(summarize_document_section_prompt(query, doc_text))
                full_report += f"\n### 📄 Document Insights\n{doc_summary}\n"

        st.markdown("---")
        st.subheader("📝 Final Research Report")
        st.markdown(full_report)
        st.download_button("📥 Download Report (Markdown)", full_report, file_name="research_report.md")

        pdf_path = save_report_as_pdf(full_report)
        with open(pdf_path, "rb") as pdf_file:
            st.download_button("📄 Download PDF", pdf_file, file_name="research_report.pdf")

        docx_path = save_report_as_docx(full_report)
        with open(docx_path, "rb") as docx_file:
            st.download_button("📝 Download Word Doc", docx_file, file_name="research_report.docx")