import streamlit as st
import PyPDF2
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import re
from fpdf import FPDF
import time
import random

# --- Setup Page ---
st.set_page_config(page_title="AI Resume Analyzer Pro | Next-Gen Resume Intelligence", page_icon="⚡", layout="wide", initial_sidebar_state="expanded")

# --- Custom CSS (Cinematic SaaS) ---
def apply_custom_css():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;700;900&family=Space+Grotesk:wght@300;500;700;900&display=swap');
    
    /* Base Variables */
    :root {
        --bg-color: #030014;
        --card-bg: rgba(255, 255, 255, 0.03);
        --card-border: rgba(255, 255, 255, 0.08);
        --neon-blue: #00f0ff;
        --neon-purple: #8a2be2;
        --neon-pink: #ff007f;
        --text-primary: #ffffff;
        --text-secondary: #9ca3af;
    }

    * {
        font-family: 'Outfit', sans-serif;
    }

    /* 🌌 Cinematic Animated Background */
    .stApp {
        background-color: var(--bg-color);
        background-image: 
            radial-gradient(at 0% 0%, rgba(138, 43, 226, 0.15) 0px, transparent 50%),
            radial-gradient(at 100% 0%, rgba(0, 240, 255, 0.15) 0px, transparent 50%),
            radial-gradient(at 100% 100%, rgba(255, 0, 127, 0.15) 0px, transparent 50%),
            radial-gradient(at 0% 100%, rgba(138, 43, 226, 0.15) 0px, transparent 50%);
        background-attachment: fixed;
        color: var(--text-primary);
        overflow-x: hidden;
    }

    /* Floating Particles Overlay (Simulated via CSS) */
    .stApp::before {
        content: '';
        position: fixed;
        top: 0; left: 0; width: 200vw; height: 200vh;
        background: transparent url('https://www.transparenttextures.com/patterns/stardust.png');
        animation: drift 100s linear infinite;
        opacity: 0.3;
        z-index: -1;
        pointer-events: none;
    }

    @keyframes drift {
        0% { transform: translate(0, 0); }
        100% { transform: translate(-50vw, -50vh); }
    }

    /* 🧊 Premium Glassmorphism Cards */
    .glass-card {
        background: var(--card-bg);
        border: 1px solid var(--card-border);
        border-radius: 20px;
        padding: 2rem;
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        box-shadow: 0 4px 30px rgba(0, 0, 0, 0.5);
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        position: relative;
        overflow: hidden;
        margin-bottom: 2rem;
        z-index: 1;
    }
    
    /* Neon Glow on Hover */
    .glass-card:hover {
        transform: translateY(-8px) scale(1.02);
        border-color: rgba(0, 240, 255, 0.3);
        box-shadow: 0 15px 40px rgba(0, 240, 255, 0.1), 0 0 20px rgba(138, 43, 226, 0.1);
    }
    
    /* Card inner glow */
    .glass-card::after {
        content: '';
        position: absolute;
        top: 0; left: -100%;
        width: 50%; height: 100%;
        background: linear-gradient(to right, transparent, rgba(255,255,255,0.05), transparent);
        transform: skewX(-20deg);
        transition: 0.5s;
    }
    .glass-card:hover::after {
        left: 150%;
    }

    /* Headers & Typography */
    h1, h2, h3, h4 {
        font-family: 'Space Grotesk', sans-serif !important;
        font-weight: 700 !important;
        letter-spacing: -0.02em;
        color: #fff !important;
    }

    .hero-title {
        font-size: 5rem;
        font-weight: 900;
        font-family: 'Space Grotesk', sans-serif;
        text-align: center;
        background: linear-gradient(135deg, #fff 0%, #9ca3af 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.2rem;
        line-height: 1.1;
        animation: slideUpFade 1s ease-out forwards;
    }
    
    .hero-title span {
        background: linear-gradient(to right, var(--neon-blue), var(--neon-purple));
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-shadow: 0 0 40px rgba(0, 240, 255, 0.4);
    }

    .hero-subtitle {
        text-align: center;
        font-size: 1.5rem;
        color: var(--text-secondary);
        margin-bottom: 3rem;
        font-family: 'Space Grotesk', sans-serif;
        overflow: hidden;
        white-space: nowrap;
        margin-left: auto;
        margin-right: auto;
        animation: typing 3s steps(40, end), blink-caret .75s step-end infinite;
        border-right: .15em solid var(--neon-blue);
        max-width: fit-content;
    }

    @keyframes typing { from { width: 0 } to { width: 100% } }
    @keyframes blink-caret { from, to { border-color: transparent } 50% { border-color: var(--neon-blue) } }
    @keyframes slideUpFade { from { opacity: 0; transform: translateY(50px); } to { opacity: 1; transform: translateY(0); } }

    /* Custom Navbar */
    .custom-navbar {
        position: fixed;
        top: 0; left: 0; right: 0;
        height: 70px;
        background: rgba(3, 0, 20, 0.8);
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border-bottom: 1px solid rgba(255,255,255,0.05);
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 0 5%;
        z-index: 9999;
    }
    .nav-logo {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 1.5rem;
        font-weight: 800;
        color: #fff;
        text-decoration: none;
        display: flex;
        align-items: center;
        gap: 10px;
    }
    .nav-logo span { color: var(--neon-blue); }
    .nav-links { display: flex; gap: 30px; }
    .nav-link {
        color: var(--text-secondary);
        text-decoration: none;
        font-weight: 500;
        transition: 0.3s;
        font-size: 1rem;
    }
    .nav-link:hover { color: #fff; text-shadow: 0 0 10px var(--neon-blue); }

    /* Streamlit Overrides */
    div[data-testid="stFileUploader"] {
        background: var(--card-bg) !important;
        backdrop-filter: blur(20px);
        border-radius: 20px;
        border: 2px dashed rgba(0, 240, 255, 0.3);
        padding: 3rem;
        text-align: center;
        transition: 0.3s;
    }
    div[data-testid="stFileUploader"]:hover {
        border-color: var(--neon-blue);
        background: rgba(0, 240, 255, 0.05) !important;
    }
    
    section[data-testid="stSidebar"] {
        background-color: rgba(3, 0, 20, 0.95) !important;
        border-right: 1px solid rgba(255,255,255,0.05);
    }
    
    /* Metrics Override */
    div[data-testid="stMetricValue"] {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 3rem !important;
        font-weight: 800;
        background: linear-gradient(to right, #fff, #9ca3af);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    /* Custom Timeline */
    .timeline {
        border-left: 2px solid rgba(0, 240, 255, 0.3);
        padding-left: 20px;
        margin-left: 10px;
    }
    .timeline-item {
        position: relative;
        margin-bottom: 20px;
    }
    .timeline-item::before {
        content: '';
        position: absolute;
        left: -27px;
        top: 5px;
        width: 12px;
        height: 12px;
        border-radius: 50%;
        background: var(--neon-blue);
        box-shadow: 0 0 10px var(--neon-blue);
    }
    .timeline-date { color: var(--neon-purple); font-weight: 600; font-size: 0.9rem;}
    .timeline-content { background: rgba(255,255,255,0.02); padding: 15px; border-radius: 10px; margin-top: 5px; border: 1px solid rgba(255,255,255,0.05);}

    /* Hide default header */
    header[data-testid="stHeader"] { display: none; }
    
    /* Spacer for custom navbar */
    .navbar-spacer { height: 80px; }
    
    /* Fancy Download Button */
    .stDownloadButton button {
        background: linear-gradient(45deg, var(--neon-blue), var(--neon-purple)) !important;
        color: white !important;
        border: none !important;
        padding: 0.8rem 2rem !important;
        font-family: 'Space Grotesk', sans-serif !important;
        font-weight: 700 !important;
        border-radius: 30px !important;
        box-shadow: 0 10px 20px rgba(138, 43, 226, 0.3) !important;
        transition: 0.3s !important;
    }
    .stDownloadButton button:hover {
        transform: translateY(-3px) !important;
        box-shadow: 0 15px 30px rgba(0, 240, 255, 0.4) !important;
    }
    </style>
    
    <!-- Custom Sticky Navbar HTML -->
    <div class="custom-navbar">
        <div class="nav-logo">⚡ AI<span>Analyzer</span></div>
        <div class="nav-links">
            <a href="#" class="nav-link">Platform</a>
            <a href="#" class="nav-link">Intelligence</a>
            <a href="#" class="nav-link">Roadmap</a>
            <a href="#" class="nav-link" style="border: 1px solid var(--neon-blue); padding: 5px 15px; border-radius: 20px; color: var(--neon-blue);">Sign In</a>
        </div>
    </div>
    <div class="navbar-spacer"></div>
    """, unsafe_allow_html=True)

# --- Data Dictionaries & Logic ---
SKILL_CATEGORIES = {
    "Programming Languages": ["python", "java", "c++", "c", "c#", "javascript", "typescript", "ruby", "php", "go", "swift", "kotlin", "rust"],
    "AI & Data Science": ["machine learning", "deep learning", "nlp", "computer vision", "tensorflow", "pytorch", "scikit-learn", "keras", "pandas", "numpy", "matplotlib", "llm", "openai", "generative ai"],
    "Web Development": ["html", "css", "react", "node.js", "angular", "vue", "django", "flask", "fastapi", "spring boot", "express", "next.js", "tailwind"],
    "Databases & Cloud": ["sql", "mysql", "postgresql", "mongodb", "redis", "aws", "azure", "gcp", "docker", "kubernetes", "nosql", "terraform"],
    "Soft Skills": ["leadership", "communication", "teamwork", "problem solving", "agile", "scrum", "mentoring", "strategy"]
}

JOB_ROLES = {
    "AI/ML Engineer": ["machine learning", "python", "tensorflow", "pytorch", "deep learning", "nlp", "pandas", "numpy", "sql", "llm", "aws", "docker"],
    "Web Developer": ["html", "css", "javascript", "react", "node.js", "django", "sql", "git", "express", "vue", "next.js", "tailwind"],
    "Data Scientist": ["sql", "python", "pandas", "numpy", "machine learning", "scikit-learn", "tableau", "aws"],
    "Software Engineer": ["java", "python", "c++", "javascript", "sql", "git", "data structures", "aws", "docker", "kubernetes"],
    "DevOps Engineer": ["aws", "docker", "kubernetes", "linux", "jenkins", "ci/cd", "python", "terraform", "bash"]
}

ACTION_VERBS = ["managed", "led", "developed", "architected", "optimized", "increased", "decreased", "improved", "designed", "spearheaded", "orchestrated", "transformed", "engineered", "implemented"]

def extract_text_from_pdf(file):
    try:
        reader = PyPDF2.PdfReader(file)
        return "".join(page.extract_text() for page in reader.pages)
    except:
        return ""

def generate_pdf_report(score, ats_score, found_skills, top_roles):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(200, 10, txt="AI Resume Analyzer Pro - Resume Intelligence Report", ln=True, align='C')
    pdf.ln(10)
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(200, 10, txt=f"AI Readiness Score: {score}/100", ln=True)
    pdf.cell(200, 10, txt=f"ATS Compatibility: {ats_score}/100", ln=True)
    pdf.ln(5)
    pdf.cell(200, 10, txt="Skill Vectors Detected:", ln=True)
    pdf.set_font("Arial", '', 11)
    pdf.multi_cell(0, 10, txt=", ".join(found_skills) if found_skills else "None")
    pdf.ln(5)
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(200, 10, txt="Top Industry Matches:", ln=True)
    pdf.set_font("Arial", '', 11)
    for role, match in top_roles:
        pdf.multi_cell(0, 8, txt=f"- {role} ({match} core competencies matched)")
    return pdf.output(dest='S').encode('latin-1')

# --- Main App ---
def main():
    apply_custom_css()
    
    # Hero Section
    st.markdown("""
    <div style='margin-bottom: 4rem; margin-top: 2rem;'>
        <div class='hero-title'>Unlock Your <span>Career Potential</span></div>
        <div class='hero-subtitle'>Enterprise-grade AI resume analysis & career matching engine.</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar features
    with st.sidebar:
        st.markdown("<h2 style='text-align: center; color: var(--neon-blue); font-family: \"Space Grotesk\", sans-serif;'>AI Analyzer Core</h2>", unsafe_allow_html=True)
        st.markdown("---")
        st.markdown("""
        <div style='background: rgba(255,255,255,0.05); padding: 15px; border-radius: 10px; margin-bottom: 15px; border-left: 3px solid var(--neon-blue);'>
            <h4 style='margin-top:0; color: white;'>Live Systems</h4>
            <span style='color: #22c55e; font-weight: 600;'>● Engine Online</span>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("### 🧬 Analysis Modules")
        st.checkbox("ATS Simulation Check", value=True, disabled=True)
        st.checkbox("Neural Skill Matching", value=True, disabled=True)
        st.checkbox("Semantic Insight Engine", value=True, disabled=True)
        st.checkbox("Industry Readiness Map", value=True, disabled=True)
        
        st.markdown("---")
        st.markdown("### 💬 AI Assistant")
        st.info("Awaiting data input to generate tailored strategic insights.")

    # Upload Area
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        uploaded_file = st.file_uploader("Drop your PDF resume to initialize analysis", type=["pdf"])

    if uploaded_file:
        # Modern Processing Animation
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        for i in range(100):
            time.sleep(0.015)  # Simulate intense processing
            progress_bar.progress(i + 1)
            if i == 10: status_text.markdown("<p style='color: var(--neon-blue); text-align: center;'><i>Extracting semantic text layers...</i></p>", unsafe_allow_html=True)
            elif i == 40: status_text.markdown("<p style='color: var(--neon-purple); text-align: center;'><i>Running neural skill matching matrices...</i></p>", unsafe_allow_html=True)
            elif i == 70: status_text.markdown("<p style='color: var(--neon-pink); text-align: center;'><i>Calculating industry readiness vectors...</i></p>", unsafe_allow_html=True)
        
        progress_bar.empty()
        status_text.empty()
        
        text = extract_text_from_pdf(uploaded_file)
        if not text.strip():
            st.error("Failed to extract data. Ensure the PDF is text-based and not a scanned image.")
            return

        text_lower = text.lower()
        
        # --- Analysis Core ---
        found_skills = []
        categorized_skills = {cat: [] for cat in SKILL_CATEGORIES}
        unique_found_skills = set()
        
        for cat, skills in SKILL_CATEGORIES.items():
            for skill in skills:
                if re.search(r'\b' + re.escape(skill) + r'\b', text_lower):
                    if skill not in unique_found_skills:
                        unique_found_skills.add(skill)
                        found_skills.append(skill.title())
                        categorized_skills[cat].append(skill.title())
                        
        sections_to_look = ["education", "experience", "projects", "skills", "summary"]
        found_sections = [sec for sec in sections_to_look if sec in text_lower]
        ats_score = int((len(found_sections) / len(sections_to_look)) * 100)
        
        verbs_found = [verb for verb in ACTION_VERBS if re.search(r'\b' + verb + r'\b', text_lower)]
        
        base_score = min(len(found_skills) * 3, 50)
        section_score = (ats_score / 100) * 30
        action_score = min(len(verbs_found) * 5, 20)
        total_score = min(int(base_score + section_score + action_score), 100)

        role_matches = {}
        for role, r_skills in JOB_ROLES.items():
            match_count = sum(1 for s in r_skills if s in [fs.lower() for fs in found_skills])
            if match_count > 0:
                role_matches[role] = match_count
        top_roles = sorted(role_matches.items(), key=lambda x: x[1], reverse=True)[:3]
        
        # --- UI Phase 2: Dashboards ---
        st.markdown("<h2 style='text-align: center; margin-top: 3rem; margin-bottom: 3rem;'>Intelligence Report <span style='color: var(--neon-blue);'>Generated</span></h2>", unsafe_allow_html=True)
        
        # Top KPI row (Neon Guages)
        kpi_c1, kpi_c2, kpi_c3 = st.columns(3)
        
        with kpi_c1:
            st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
            fig1 = go.Figure(go.Indicator(
                mode = "gauge+number",
                value = total_score,
                title = {'text': "AI RESUME SCORE", 'font': {'color': 'white', 'family': 'Space Grotesk'}},
                gauge = {
                    'axis': {'range': [None, 100], 'tickwidth': 1, 'tickcolor': "white"},
                    'bar': {'color': "#00f0ff"},
                    'bgcolor': "rgba(255,255,255,0.05)",
                    'borderwidth': 2,
                    'bordercolor': "gray",
                    'steps': [
                        {'range': [0, 50], 'color': "rgba(255, 0, 127, 0.2)"},
                        {'range': [50, 80], 'color': "rgba(138, 43, 226, 0.2)"},
                        {'range': [80, 100], 'color': "rgba(0, 240, 255, 0.2)"}],
                }
            ))
            fig1.update_layout(paper_bgcolor="rgba(0,0,0,0)", font={'color': "white"}, height=250, margin=dict(l=10, r=10, t=40, b=10))
            st.plotly_chart(fig1, use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)
            
        with kpi_c2:
            st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
            fig2 = go.Figure(go.Indicator(
                mode = "gauge+number",
                value = ats_score,
                title = {'text': "ATS COMPATIBILITY", 'font': {'color': 'white', 'family': 'Space Grotesk'}},
                gauge = {
                    'axis': {'range': [None, 100], 'tickwidth': 1, 'tickcolor': "white"},
                    'bar': {'color': "#8a2be2"},
                    'bgcolor': "rgba(255,255,255,0.05)",
                    'borderwidth': 2,
                    'bordercolor': "gray"
                }
            ))
            fig2.update_layout(paper_bgcolor="rgba(0,0,0,0)", font={'color': "white"}, height=250, margin=dict(l=10, r=10, t=40, b=10))
            st.plotly_chart(fig2, use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)
            
        with kpi_c3:
            st.markdown("<div class='glass-card' style='text-align: center; height: 100%; display: flex; flex-direction: column; justify-content: center;'>", unsafe_allow_html=True)
            st.markdown("<h3 style='color: #9ca3af;'>Total Skill Vectors</h3>", unsafe_allow_html=True)
            st.markdown(f"<div style='font-size: 6rem; font-family: \"Space Grotesk\", sans-serif; font-weight: 900; color: #ff007f; text-shadow: 0 0 30px rgba(255,0,127,0.6); line-height: 1;'>{len(found_skills)}</div>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

        # Middle Section: Radar Chart & Match Engine
        col_L, col_R = st.columns([1.2, 1])
        
        with col_L:
            st.markdown("<div class='glass-card'><h3 style='margin-top: 0;'>🌐 Skill Density Radar</h3>", unsafe_allow_html=True)
            categories = list(categorized_skills.keys())
            values = [len(categorized_skills[cat]) for cat in categories]
            
            if categories and sum(values) > 0:
                categories_r = categories + [categories[0]]
                values_r = values + [values[0]]
                
                fig_radar = go.Figure(data=go.Scatterpolar(
                  r=values_r,
                  theta=categories_r,
                  fill='toself',
                  fillcolor='rgba(0, 240, 255, 0.2)',
                  line=dict(color='#00f0ff', width=3),
                  marker=dict(color='#00f0ff', size=8)
                ))
                fig_radar.update_layout(
                  polar=dict(
                    radialaxis=dict(visible=True, range=[0, max(values)+1], color='rgba(255,255,255,0.5)', gridcolor='rgba(255,255,255,0.1)', tickfont=dict(size=10)),
                    angularaxis=dict(color='white', gridcolor='rgba(255,255,255,0.2)', tickfont=dict(size=14, family='Outfit')),
                    bgcolor='rgba(0,0,0,0)'
                  ),
                  paper_bgcolor='rgba(0,0,0,0)',
                  font=dict(color='white'),
                  margin=dict(t=30, b=30, l=40, r=40),
                  height=400
                )
                st.plotly_chart(fig_radar, use_container_width=True)
            else:
                st.info("Insufficient skills detected to map density.")
            st.markdown("</div>", unsafe_allow_html=True)

        with col_R:
            st.markdown("<div class='glass-card'><h3 style='margin-top: 0;'>🎯 Industry Role Match</h3>", unsafe_allow_html=True)
            if top_roles:
                for role, match in top_roles:
                    max_skills = len(JOB_ROLES[role])
                    match_pct = min(int((match / max_skills) * 100), 100)
                    
                    st.markdown(f"**{role}**")
                    # Custom progress bar via HTML for neon styling
                    st.markdown(f"""
                        <div style='width: 100%; background: rgba(255,255,255,0.1); border-radius: 10px; height: 10px; margin-top: 5px; overflow: hidden;'>
                            <div style='width: {match_pct}%; background: linear-gradient(90deg, var(--neon-purple), var(--neon-blue)); height: 100%; box-shadow: 0 0 10px var(--neon-blue);'></div>
                        </div>
                        <p style='text-align: right; color: var(--neon-blue); font-size: 0.85rem; margin-top: 5px; font-weight: 600;'>{match_pct}% Match Readiness</p>
                    """, unsafe_allow_html=True)
            else:
                st.write("Insufficient data for role matching.")
            st.markdown("</div>", unsafe_allow_html=True)
            
            st.markdown("<div class='glass-card'><h3 style='margin-top: 0;'>🧠 Semantic Insights</h3>", unsafe_allow_html=True)
            if len(verbs_found) > 2:
                st.markdown(f"✅ <span style='color: #22c55e;'>Strong action language</span> detected ({len(verbs_found)} dynamic verbs).", unsafe_allow_html=True)
            else:
                st.markdown("⚠️ <span style='color: #eab308;'>Passive language detected.</span> Incorporate verbs like 'Architected' or 'Optimized'.", unsafe_allow_html=True)
                
            missing = [sec.title() for sec in sections_to_look if sec not in text_lower]
            if missing:
                st.markdown(f"❌ <span style='color: #ef4444;'>Missing critical structure:</span> {', '.join(missing)}.", unsafe_allow_html=True)
            else:
                st.markdown("✅ <span style='color: #22c55e;'>Structural integrity verified.</span>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

        # Bottom Section: Roadmap & Categories
        col_BL, col_BR = st.columns([1, 1])
        
        with col_BL:
            st.markdown("<div class='glass-card'><h3 style='margin-top: 0;'>🗺️ AI Career Roadmap</h3>", unsafe_allow_html=True)
            st.markdown("<p style='color: var(--text-secondary); margin-bottom: 20px;'>Projected progression based on current skill vectors.</p>", unsafe_allow_html=True)
            
            # Custom HTML Timeline
            timeline_html = f"""
            <div class="timeline">
                <div class="timeline-item">
                    <div class="timeline-date">Phase 1: Immediate Optimization</div>
                    <div class="timeline-content">Reinforce missing ATS sections. Add 2-3 specific metrics to your bullet points to quantify impact and activate neural matching.</div>
                </div>
                <div class="timeline-item">
                    <div class="timeline-date">Phase 2: Skill Augmentation</div>
                    <div class="timeline-content">Based on your primary {top_roles[0][0] if top_roles else 'Tech'} vector, acquire advanced competencies in Cloud Architecture or System Design.</div>
                </div>
                <div class="timeline-item">
                    <div class="timeline-date">Phase 3: Industry Domination</div>
                    <div class="timeline-content">Target Senior-level positions. Focus on architectural impact, cross-functional leadership, and strategic execution.</div>
                </div>
            </div>
            """
            st.markdown(timeline_html, unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

        with col_BR:
            st.markdown("<div class='glass-card'><h3 style='margin-top: 0;'>📦 Extracted Skill Vectors</h3>", unsafe_allow_html=True)
            for cat, skills in categorized_skills.items():
                if skills:
                    st.markdown(f"<p style='color: white; font-weight: 600; margin-bottom: 5px;'>{cat}</p>", unsafe_allow_html=True)
                    st.markdown(f"<div style='background: rgba(255,255,255,0.03); padding: 12px; border-radius: 12px; margin-bottom: 15px; border: 1px solid rgba(0,240,255,0.2); color: var(--neon-blue); font-size: 0.95rem; box-shadow: inset 0 0 10px rgba(0,0,0,0.5);'>{' • '.join(skills)}</div>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

        # Export Button
        st.markdown("<div style='display: flex; justify-content: center; margin: 4rem 0;'>", unsafe_allow_html=True)
        pdf_bytes = generate_pdf_report(total_score, ats_score, found_skills, top_roles)
        st.download_button(
            label="⚡ GENERATE INTELLIGENCE REPORT ⚡",
            data=pdf_bytes,
            file_name="ai_resume_report.pdf",
            mime="application/pdf",
        )
        st.markdown("</div>", unsafe_allow_html=True)

    # Footer
    st.markdown("""
        <div style='text-align: center; padding: 4rem 0 2rem 0; border-top: 1px solid rgba(255,255,255,0.05); margin-top: 5rem;'>
            <h2 style='font-family: "Space Grotesk", sans-serif; color: var(--text-primary); letter-spacing: 2px; margin-bottom: 0;'>AI <span style='color: var(--neon-blue);'>Analyzer Pro</span></h2>
            <p style='color: var(--text-secondary); margin-top: 10px;'>Made with love By Kranti</p>
            <div style='display: flex; justify-content: center; gap: 30px; margin-top: 30px;'>
                <a href="#" style='color: white; text-decoration: none; opacity: 0.5; transition: 0.3s; font-size: 1.1rem;' onmouseover="this.style.opacity='1'; this.style.color='var(--neon-blue)'" onmouseout="this.style.opacity='0.5'; this.style.color='white'">GitHub</a>
                <a href="#" style='color: white; text-decoration: none; opacity: 0.5; transition: 0.3s; font-size: 1.1rem;' onmouseover="this.style.opacity='1'; this.style.color='var(--neon-blue)'" onmouseout="this.style.opacity='0.5'; this.style.color='white'">LinkedIn</a>
                <a href="#" style='color: white; text-decoration: none; opacity: 0.5; transition: 0.3s; font-size: 1.1rem;' onmouseover="this.style.opacity='1'; this.style.color='var(--neon-blue)'" onmouseout="this.style.opacity='0.5'; this.style.color='white'">Platform</a>
            </div>
        </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
