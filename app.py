import streamlit as st
import PyPDF2
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet

# -------------------------------
# Page Config + UI Styling
# -------------------------------
st.set_page_config(page_title="AI Resume Analyzer", layout="wide")

st.markdown("""
<style>
.stApp {
    background: linear-gradient(to right, #1f4037, #99f2c8);
}
h1, h2, h3 {
    color: white;
}
</style>
""", unsafe_allow_html=True)

st.title("📄 AI Resume Analyzer")

# -------------------------------
# Job Role Selection
# -------------------------------
skills_data = {
    "Data Scientist": ["Python", "Machine Learning", "Deep Learning", "SQL", "Data Analysis"],
    "Web Developer": ["HTML", "CSS", "JavaScript", "React", "Node.js", "Docker"],
    "Java Developer": ["Java", "Spring", "SQL", "Hibernate", "Docker"],
    "Python Developer": ["Python", "Django", "Flask", "REST API", "SQL"],
    "Frontend Developer": ["HTML", "CSS", "JavaScript", "React", "Bootstrap"],
    "Backend Developer": ["Node.js", "Django", "Flask", "SQL", "API"],
    "Full Stack Developer": ["HTML", "CSS", "JavaScript", "React", "Node.js", "MongoDB"],
    "DevOps Engineer": ["AWS", "Docker", "Kubernetes", "CI/CD", "Linux"],
    "Android Developer": ["Java", "Kotlin", "Android Studio", "Firebase"],
    "Machine Learning Engineer": ["Python", "Machine Learning", "TensorFlow", "Scikit-learn"],
    "Cyber Security": ["Networking", "Linux", "Ethical Hacking", "Cryptography"],
    "Cloud Engineer": ["AWS", "Azure", "Docker", "Kubernetes"],
    "Data Analyst": ["Excel", "SQL", "Python", "Power BI", "Tableau"],
}

role = st.selectbox("🎯 Select Job Role", list(skills_data.keys()))
skills_list = skills_data[role]

# -------------------------------
# File Upload
# -------------------------------
uploaded_file = st.file_uploader("📤 Upload Resume (PDF)", type="pdf")

# -------------------------------
# Extract Text
# -------------------------------
def extract_text(file):
    pdf = PyPDF2.PdfReader(file)
    text = ""
    for page in pdf.pages:
        if page.extract_text():
            text += page.extract_text()
    return text

# -------------------------------
# Analyze Resume
# -------------------------------
def analyze(text):
    found = []
    for skill in skills_list:
        if skill.lower() in text.lower():
            found.append(skill)

    missing = list(set(skills_list) - set(found))
    score = int((len(found)/len(skills_list))*100)

    return found, missing, score

# -------------------------------
# AI Feedback (Strengths + Suggestions)
# -------------------------------
def generate_feedback(found, missing, score):
    strengths = []
    suggestions = []

    # Strengths
    if "Python" in found:
        strengths.append("Strong programming foundation with Python.")
    if "Machine Learning" in found:
        strengths.append("Good exposure to Machine Learning concepts.")
    if "AWS" in found or "Docker" in found:
        strengths.append("Strong knowledge of cloud and DevOps tools.")
    if score > 70:
        strengths.append("Well-balanced resume with relevant industry skills.")

    # Suggestions
    if "AWS" in missing:
        suggestions.append("Add AWS to demonstrate cloud expertise.")
    if "Docker" in missing:
        suggestions.append("Include Docker for deployment skills.")
    if "React" in missing:
        suggestions.append("Add React to improve frontend skills.")
    if score < 60:
        suggestions.append("Add more real-world projects with measurable impact.")
    suggestions.append("Include GitHub links for project verification.")

    return strengths, suggestions

# -------------------------------
# Create PDF Report
# -------------------------------
def create_pdf(strengths, suggestions, score):
    doc = SimpleDocTemplate("report.pdf")
    styles = getSampleStyleSheet()

    content = []

    content.append(Paragraph(f"Resume Score: {score}%", styles["Title"]))

    content.append(Paragraph("<b>Resume Strengths</b>", styles["Heading2"]))
    for s in strengths:
        content.append(Paragraph(s, styles["Normal"]))

    content.append(Paragraph("<b>Suggestions to Improve</b>", styles["Heading2"]))
    for s in suggestions:
        content.append(Paragraph(s, styles["Normal"]))

    doc.build(content)

# -------------------------------
# Buttons
# -------------------------------
col1, col2 = st.columns(2)

analyze_btn = col1.button("🔍 Analyze Resume")
reset_btn = col2.button("🔄 Reset")

# -------------------------------
# Main Logic
# -------------------------------
if analyze_btn and uploaded_file:

    text = extract_text(uploaded_file)
    found, missing, score = analyze(text)

    strengths, suggestions = generate_feedback(found, missing, score)

    st.success("Analysis Complete!")

    # Score
    st.subheader("📊 Resume Score")
    st.progress(score)
    st.write(f"### {score}%")

    # Skills
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("✅ Skills Found")
        for skill in found:
            st.write(f"✔ {skill}")

    with col2:
        st.subheader("❌ Missing Skills")
        for skill in missing:
            st.write(f"✘ {skill}")

    # Strengths
    st.subheader("💪 Resume Strengths")
    for s in strengths:
        st.write(f"✔ {s}")

    # Suggestions
    st.subheader("📉 Suggestions to Improve")
    for s in suggestions:
        st.write(f"➤ {s}")

    # PDF Download
    create_pdf(strengths, suggestions, score)

    with open("report.pdf", "rb") as file:
        st.download_button(
            label="📥 Download Feedback Report",
            data=file,
            file_name="resume_report.pdf",
            mime="application/pdf"
        )

# Reset
if reset_btn:
    st.experimental_rerun()