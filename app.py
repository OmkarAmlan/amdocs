from flask import Flask, render_template, jsonify, request
from guru import extract_text_from_pdf, analyze_resume_with_gpt, extract_improvement_areas, search_youtube_videos
import os

app = Flask(__name__)

# Mock data for jobs
JOBS = [
    {
        "companyName": "Tech Corp",
        "jobId": "1",
        "jobName": "Software Engineer",
        "ctc": "15 LPA",
        "jobDescriptionPdf": "/static/pdfs/job1.pdf",
    },
    {
        "companyName": "Innovate Inc",
        "jobId": "2",
        "jobName": "Data Scientist",
        "ctc": "20 LPA",
        "jobDescriptionPdf": "/static/pdfs/job2.pdf",
    },
]

# Mock data for network
NETWORK = {
    "nodes": [
        { "id": 1, "label": "Alice" },
        { "id": 2, "label": "Bob" },
        { "id": 3, "label": "Charlie" },
    ],
    "edges": [
        { "from": 1, "to": 2 },
        { "from": 2, "to": 3 },
    ],
}

# Configure upload folder
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

@app.route("/")
def home():
    return render_template("jobPosting.html")

@app.route("/api/jobs")
def get_jobs():
    return jsonify(JOBS)

@app.route("/api/network")
def get_network():
    return jsonify(NETWORK)

@app.route("/upskilling")
def upskilling():
    return render_template("upskilling.html")

@app.route("/analyze", methods=["POST"])
def analyze_resume():
    try:
        # Get uploaded files
        resume_file = request.files.get("resume")
        jd_file = request.files.get("job_description")
        
        if not resume_file or not jd_file:
            return jsonify({"error": "Both resume and job description files are required."}), 400
        
        # Save uploaded files
        resume_path = os.path.join(app.config["UPLOAD_FOLDER"], "resume.pdf")
        jd_path = os.path.join(app.config["UPLOAD_FOLDER"], "JD.pdf")
        resume_file.save(resume_path)
        jd_file.save(jd_path)
        
        # Extract text
        resume_text = extract_text_from_pdf(resume_path)
        job_description_text = extract_text_from_pdf(jd_path)
        
        # Create analysis prompt
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
        
        # Analyze resume
        improvements = analyze_resume_with_gpt(analysis_prompt)
        improvement_areas = extract_improvement_areas(improvements)
        
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
        
        # Search YouTube for relevant videos
        video_recommendations = {area: search_youtube_videos(area) for area in improvement_areas}

        return jsonify({
            "improvement_areas": improvement_areas,
            "video_recommendations": video_recommendations
        })
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)