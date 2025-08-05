import streamlit as st
import fitz  # PyMuPDF
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import tempfile

# Title
st.title("🔍 MatchMyResume - Resume vs Job Description Matcher")

# File uploader for PDF resume
uploaded_resume = st.file_uploader("📄 Upload your Resume (PDF only)", type=["pdf"])

# Text area for job description
job_description = st.text_area("📝 Paste the Job Description here")

# Function to extract text from PDF
def extract_text_from_pdf(pdf_file):
    text = ""
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
        tmp_file.write(pdf_file.read())
        tmp_file_path = tmp_file.name

    doc = fitz.open(tmp_file_path)
    for page in doc:
        text += page.get_text()
    doc.close()
    return text

# Function to calculate similarity
def calculate_similarity(text1, text2):
    vectorizer = TfidfVectorizer()
    tfidf = vectorizer.fit_transform([text1, text2])
    similarity_score = cosine_similarity(tfidf[0:1], tfidf[1:2])[0][0]
    return round(similarity_score * 100, 2)  # Percentage

# When button is clicked
if st.button("🎯 Match Now"):
    if uploaded_resume and job_description.strip() != "":
        resume_text = extract_text_from_pdf(uploaded_resume)
        score = calculate_similarity(resume_text, job_description)

        st.subheader("✅ Match Result")
        st.markdown(f"**Similarity Score:** {score}%")

        if score > 75:
            st.success("🎉 Great match! Your resume is highly relevant to the job.")
        elif score > 50:
            st.warning("⚠️ Moderate match. Consider updating your resume with relevant keywords.")
        else:
            st.error("❌ Low match. Try tailoring your resume better to the job description.")
    else:
        st.error("Please upload a resume and paste a job description.")
