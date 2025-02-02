import streamlit as st
from guru import extract_text_from_pdf, analyze_resume_with_gpt, extract_improvement_areas, search_youtube_videos
import os

# Configure upload folder
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Job description file paths for different industries
JD_FILE_PATHS = {
    "Software": "uploads/JD_software.pdf",
    "Analytics": "uploads/JD_analytics.pdf",
    "Semiconductor": "uploads/JD_semiconductor.pdf"
}

# Title and custom styling for the Streamlit app
st.set_page_config(page_title="Resume Analyzer", page_icon=":bar_chart:", layout="centered")

# Custom CSS for better styling
st.markdown("""
    <style>
    .title {
        font-size: 36px;
        font-weight: bold;
        color: #4CAF50;
        text-align: center;
    }
    .subheader {
        font-size: 24px;
        font-weight: 600;
        color: #333;
    }
    .section-title {
        font-size: 20px;
        font-weight: 600;
        color: #007BFF;
    }
    .video-card {
        background-color: #f1f1f1;
        border-radius: 5px;
        padding: 10px;
        margin: 10px 0;
    }
    .video-card:hover {
        background-color: #e0e0e0;
    }
    </style>
""", unsafe_allow_html=True)

# Header for the app
st.header("Resume Analysis & Upskilling Recommendations")

# Sidebar for navigation and file uploads
st.sidebar.header("Upload Your Documents")
resume_file = st.sidebar.file_uploader("Upload your resume (PDF format)", type="pdf")

# Show a message if resume is not uploaded
if not resume_file:
    st.sidebar.warning("Please upload your resume to begin the analysis.")
else:
    st.sidebar.success("Resume uploaded! Now you can start the analysis.")

# Processing the uploaded resume
if resume_file:
    with st.spinner('Analyzing your resume...'):
        # Save the uploaded resume
        resume_path = os.path.join(UPLOAD_FOLDER, "resume.pdf")
        with open(resume_path, "wb") as f:
            f.write(resume_file.getbuffer())
        
        # Select the job description category
        job_desciption_choice = st.selectbox(
            label="Select Target Job Description",
            options=["Software", "Analytics", "Semiconductor"]
        )

        # Fetch the job description based on selection
        job_description_file = JD_FILE_PATHS[job_desciption_choice]
        
        # Extract text from the uploaded resume and selected Job Description (JD)
        resume_text = extract_text_from_pdf(resume_path)
        job_description_text = extract_text_from_pdf(job_description_file)
        
        # Create analysis prompt for GPT
        analysis_prompt = f"""
        You are an AI that evaluates resumes based on job descriptions.
        
        Resume:
        {resume_text}
        
        Job Description:
        {job_description_text}
        
        Provide EXACTLY 3 specific areas for improvement.
        Prioritize technical skills first.
        Each area must be on a new line starting with '- IMPROVE: '
        """
        
        # Analyze the resume using GPT
        improvements = analyze_resume_with_gpt(analysis_prompt)
        improvement_areas = extract_improvement_areas(improvements)
        
        # If no improvement areas found, reanalyze
        if not improvement_areas:
            retry_prompt = f"""
            Reanalyze this resume and job description.
            List EXACTLY 3 areas for improvement, prioritizing technical skills first.
            Each area MUST start with '- IMPROVE: '
            
            Resume: {resume_text}
            Job Description: {job_description_text}
            """
            improvements = analyze_resume_with_gpt(retry_prompt)
            improvement_areas = extract_improvement_areas(improvements)
        
        # Search YouTube for relevant videos for each improvement area
        video_recommendations = {area: search_youtube_videos(area) for area in improvement_areas}
        
        # Display the improvement areas
        st.subheader("Areas for Improvement:")
        for area in improvement_areas:
            st.write(f"- {area}")
        
        # Display video recommendations
        st.subheader("Recommended YouTube Videos:")
        for area, videos in video_recommendations.items():
            st.write(f"**For '{area}':**")
            if isinstance(videos, list):  # Check if it's a list
                for video in videos:
                    st.success(video)
            else:
                st.write("No videos found.")
        
        # Success message after processing
        st.success("Resume analysis complete! Check out the improvement areas and video recommendations.")
