import os
import gradio as gr
from groq import Groq

# 1. Setup Groq Client (Ensure 'GROQ_API_KEY' is set in Hugging Face Secrets)
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

# 2. Introduction & University List
MY_INTRO = """
# 🎓 University AI Consultant
**Developer:** Nisar Ahmad  
**Affiliation:** CUI Sahiwal Campus, Pakistan  
*Providing high-accuracy, real-time insights into Pakistan's top educational institutions.*
"""

UNI_LIST = """
### 🏛️ Universities Covered:
1. **COMSATS (CUI):** All campuses (Islamabad, Sahiwal, Lahore, etc.)
2. **UET:** All campuses (Lahore, Taxila, Peshawar, etc.)
3. **NUST:** All campuses (H-12, EME, MCS, etc.)
4. **FAST-NUCES:** All campuses (Chiniot-Faisalabad, Islamabad, Karachi, etc.)
5. **NUML:** All campuses.
6. **Medical Universities:** All HEC/PMC recognized medical institutions.

**Aspects Covered:** Admission criteria, Fee structures, Campus life, Ranking, and Department details.
"""

def get_university_info(user_query):
    if not user_query:
        return "Please enter a question about a university."
    
    try:
        system_prompt = (
            "You are a specialized AI assistant for Pakistani Universities. "
            "Provide the most accurate, advanced, and up-to-date information for COMSATS, UET, NUST, FAST, NUML, and Medical Universities. "
            "Use a professional tone. If you are unsure about a specific current date (like 2026 deadlines), "
            "advise the user to check the official portal while providing the most recent known data."
        )

        chat_completion = client.chat.completions.create(
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_query}
            ],
            model="llama-3.3-70b-versatile",
            temperature=0.3,
        )
        return chat_completion.choices[0].message.content
    except Exception as e:
        return f"Error: {str(e)}. Please ensure your Groq API Key is valid."

# 3. Custom CSS for Dark Mode & High Contrast
custom_css = """
body { background-color: #0f172a; color: #ffffff; }
.gradio-container { font-family: 'Inter', sans-serif !important; }
#intro-markdown { text-align: center; margin-bottom: 20px; color: #38bdf8; }
#uni-box { background: #1e293b; border-radius: 12px; padding: 20px; border: 1px solid #334155; color: #ffffff; }
.ans-box { font-size: 16px !important; color: #ffffff !important; background: #1e293b; padding: 15px; border-radius: 8px; border: 1px solid #334155; }
input, textarea { background-color: #1e293b !important; color: #ffffff !important; border: 1px solid #334155 !important; }
button { background-color: #2563eb !important; color: #ffffff !important; }
"""

# 4. Building the UI with gr.Blocks
with gr.Blocks(css=custom_css, theme=gr.themes.Soft()) as demo:
    with gr.Column(elem_id="main-container"):
        # Header Section
        gr.Markdown(MY_INTRO, elem_id="intro-markdown")
        
        with gr.Row():
            # Left Sidebar: University Info
            with gr.Column(scale=1, elem_id="uni-box"):
                gr.Markdown(UNI_LIST)
            
            # Right Side: AI Interaction
            with gr.Column(scale=2):
                query_input = gr.Textbox(
                    label="Ask anything about these universities",
                    placeholder="e.g., What is the aggregate for FAST Lahore CS 2026?",
                    lines=2
                )
                submit_btn = gr.Button("Get Advanced Information", variant="primary")
                output_display = gr.Markdown(label="AI Response", elem_classes="ans-box")

    # Linking function to UI
    submit_btn.click(fn=get_university_info, inputs=query_input, outputs=output_display)
    query_input.submit(fn=get_university_info, inputs=query_input, outputs=output_display)

if __name__ == "__main__":
    demo.launch()
