import streamlit as st
from openai import OpenAI
from anthropic import Anthropic
from github import Github
import os

# ==============================================================================
# 🎨 SHARP WEBSITE (Web Engine v1.0)
# ==============================================================================
# 1. INPUT: Natural Language Requirements.
# 2. OUTPUT: Single-File HTML5 with Embedded CSS/JS.
# 3. ACTION: Direct Commit to GitHub (Triggers Cloudflare Build).
# ==============================================================================

st.set_page_config(page_title="Sharp Architect", page_icon="🎨", layout="wide")

# --- CSS: BRANDING ---
st.markdown("""
<style>
    .stApp { background-color: #0e1117; color: #e0e0e0; }
    h1 { background: -webkit-linear-gradient(45deg, #bd00ff, #00e5ff); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
    .stTextArea textarea { background-color: #1c1c1c; color: #00e5ff; border: 1px solid #333; }
    div[data-testid="stButton"] button { border: 1px solid #bd00ff; color: #bd00ff; background: transparent; }
    div[data-testid="stButton"] button:hover { background: #bd00ff; color: #000; }
</style>
""", unsafe_allow_html=True)

# --- SECRETS & SETUP ---
try:
    ANTHROPIC_KEY = st.secrets["ANTHROPIC_API_KEY"]
    GITHUB_TOKEN = st.secrets["GITHUB_TOKEN"] # <--- NEW SECRET NEEDED
    REPO_NAME = "your-username/your-repo-name" # <--- UPDATE THIS
except:
    st.error("⚠️ Missing Secrets. Need ANTHROPIC_API_KEY and GITHUB_TOKEN.")
    st.stop()

anthropic = Anthropic(api_key=ANTHROPIC_KEY)

# --- THE ARCHITECT BRAIN ---
def generate_site(prompt, style_mode):
    system_prompt = f"""
    You are Sharp Architect, a world-class Frontend Engineer.
    
    GOAL: Build a single-file HTML landing page based on the user's request.
    
    DESIGN SYSTEM ({style_mode}):
    - If "Sharp-Neon": Use background #050505, Text #e0e0e0, Accents #00ff9d & #bd00ff. Monospace fonts.
    - If "Corporate-Clean": Use white/light-gray background, dark blue accents, sans-serif fonts.
    - Always use modern CSS (Flexbox/Grid), hover effects, and responsive design.
    
    RULES:
    1. Output ONLY valid HTML code. Start with <!DOCTYPE html>.
    2. Embed all CSS in <style> tags and JS in <script> tags.
    3. NO markdown blocks (```html). Just the raw code.
    4. Make it look expensive.
    """
    
    try:
        msg = anthropic.messages.create(
            model="claude-3-5-sonnet-latest",
            max_tokens=4000,
            system=system_prompt,
            messages=[{"role": "user", "content": prompt}]
        )
        return msg.content[0].text
    except Exception as e:
        return f"Error: {e}"

# --- THE GITHUB DEPLOYER ---
def deploy_to_github(html_content, commit_msg):
    try:
        g = Github(GITHUB_TOKEN)
        repo = g.get_repo(REPO_NAME)
        file_path = "index.html" # We are overwriting the homepage
        
        try:
            # Try to get existing file to update it
            contents = repo.get_contents(file_path)
            repo.update_file(file_path, commit_msg, html_content, contents.sha)
            return "✅ Updated index.html successfully!"
        except:
            # File doesn't exist, create it
            repo.create_file(file_path, commit_msg, html_content)
            return "✅ Created index.html successfully!"
            
    except Exception as e:
        return f"❌ Deployment Failed: {e}"

# --- UI LAYOUT ---
st.title("🎨 Sharp Architect")
st.caption("AI-Powered Static Site Generator")

col1, col2 = st.columns([1, 1])

with col1:
    st.markdown("### 1. Blueprint")
    style = st.selectbox("Design Language", ["Sharp-Neon", "Corporate-Clean", "Minimalist"])
    requirements = st.text_area("Site Requirements", height=200, 
        placeholder="Example: A landing page for an AI marketing agency. \n- Hero section with a glowing brain.\n- 3-column feature grid.\n- 'Book Demo' button.\n- Cyberpunk aesthetics.")
    
    generate_btn = st.button("🛠 Generate Code")

if generate_btn and requirements:
    with st.spinner("Architecting your vision..."):
        code = generate_site(requirements, style)
        st.session_state.generated_code = code
        st.success("Blueprint Generated!")

# --- PREVIEW & DEPLOY ---
if 'generated_code' in st.session_state:
    code = st.session_state.generated_code
    
    with col2:
        st.markdown("### 2. Live Preview")
        # Renders the HTML inside the Streamlit app!
        st.components.v1.html(code, height=600, scrolling=True)
    
    st.divider()
    st.markdown("### 3. Deployment")
    
    c_act1, c_act2 = st.columns(2)
    with c_act1:
        st.download_button("💾 Download HTML", code, "index.html", "text/html")
    with c_act2:
        if st.button("🚀 Push to Cloudflare (GitHub)"):
            with st.status("Deploying to Edge...", expanded=True):
                status = deploy_to_github(code, "Sharp Architect Update")
                st.write(status)
                if "✅" in status:
                    st.balloons()
