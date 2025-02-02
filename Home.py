import streamlit as st

# Set the page configuration
st.set_page_config(page_title="CoPilot, your carrer automated and optimized", page_icon=":chart_with_upwards_trend:", layout="centered")

# Display the title and introduction
st.title("Welcome to the Copilot!")
st.write("Your career automated, and optimized")

# Display an introductory image
st.image("https://images.pexels.com/photos/3182767/pexels-photo-3182767.jpeg", caption="Connect, Learn, Grow", use_container_width=True)

st.write("""
    This application offers two key functionalities:
    1. **User Connections**: Visualize and connect with professionals in your field.
    2. **Resume Suggestions**: Get AI-powered feedback on your resume with actionable improvements.
    
    Our goal is to help you grow your professional network and improve your job application materials to land your next big opportunity.
""")
