import streamlit as st
from anthropic import Anthropic
from github import Github
import time

# ==============================================================================
# 🎨 SHARP WEBSITE v2.2 (Cloudflare Fix + Model Update)
# ==============================================================================
# CHANGE LOG:
# - FIXED: Updated LLM model name to a current, valid version.
# - FIXED: Changed deployment path to 'public/index.html' for Cloudflare Pages.
# ==============================================================================
import streamlit as st
from anthropic import Anthropic
from github import Github
import time

# ==============================================================================
# 🎨 SHARP WEBSITE v2.2 (Cloudflare Fix + Model Update)
# ==============================================================================
# CHANGE LOG:
# - FIXED: Cleaned all non-printable characters (U+00A0) for Python compatibility.
# - FIXED: Updated LLM model name to a current, valid version.
# - FIXED: Changed deployment path to 'public/index.html' for Cloudflare Pages.
# ==============================================================================

st.set_page_config(page_title="Sharp Website | Sandbox", page_icon="🚧", layout="wide")

# --- CSS: STABILIZED UI ---
st.markdown("""
<style>
    .stApp { background-color: #0e1117; color: #e0e0e0; }
    h1 { color: #bd00ff !important; font-family: monospace; letter-spacing: -2px;}
    .stTextArea textarea, .stTextInput input { 
        background-color: #111; color: #00ff9d; border: 1px solid #333; font-family: monospace; 
    }
    .success-box { border: 1px solid #39ff14; background: rgba(57, 255, 20, 0.1); padding: 15px; border-radius: 5px; }
    .deploy-btn { border: 2px solid #bd00ff; color: #fff; }
</style>
""", unsafe_allow_html=True)

# --- SECRETS CHECK ---
if "ANTHROPIC_API_KEY" not in st.secrets or "GITHUB_TOKEN" not in st.secrets:
    st.error("🔒 SECRETS MISSING: Please add ANTHROPIC_API_KEY and GITHUB_TOKEN to secrets.toml")
    st.stop()

anthropic = Anthropic(api_key=st.secrets["ANTHROPIC_API_KEY"])
DEFAULT_REPO = "your-username/your-repo-name" # <--- UPDATE THIS IF YOU WANT

# --- FUNCTIONS ---
def architect_website(prompt, mode):
    system_prompt = f"""
    You are a Senior Frontend Architect. 
    TASK: Generate a single-file 'index.html' ready for production.
    STYLE MODE: {mode}
    REQUIREMENTS: HTML5, embedded CSS/JS, Responsive, High-End Aesthetic.
    OUTPUT: Raw code only.
    """
    try:
        msg = anthropic.messages.create(
            # FIXED: Updated model to a current, valid version
            model="claude-3-5-sonnet-20241022",
            max_tokens=4000,
            system=system_prompt,
            messages=[{"role": "user", "content": prompt}]
        )
        return msg.content[0].text
    except Exception as e:
        return f"Error: {e}"

def push_to_live(html_content, repo_name, commit_message, token):
    try:
        g = Github(token)
        # Verify repo access before trying to write
        try:
            repo = g.get_repo(repo_name)
        except:
            return False, f"Could not find repo: {repo_name}. Check spelling or Token permissions."

        # FIXED: File path now targets the 'public' folder for Cloudflare/SSG compatibility
        file_path = "public/index.html" 
        
        try:
            contents = repo.get_contents(file_path)
            repo.update_file(file_path, commit_message, html_content, contents.sha)
            return True, "Updated existing index.html"
        except:
            repo.create_file(file_path, commit_message, html_content)
            return True, "Created new index.html"
    except Exception as e:
        return False, str(e)

# --- UI LAYOUT ---
st.title("🚧 Sharp Website // Sandbox")

# SESSION STATE INIT
if 'sandbox_code' not in st.session_state: st.session_state.sandbox_code = ""

c1, c2 = st.columns([1, 1])

# === LEFT COLUMN: THE INPUTS (LOCKED IN FORM) ===
with c1:
    st.markdown("### 1. Blueprint")
    
    # WRAPPING IN FORM STOPs THE "GREY BUTTON" GLITCH
    with st.form("blueprint_form"):
        repo_target = st.text_input("Target Repo (username/repo)", value=DEFAULT_REPO)
        design_mode = st.selectbox("Design System", ["Neon Cyberpunk (Sharp)", "Minimal SaaS", "Luxury Dark", "Brutalist"])
        prompt = st.text_area("Client Requirements", height=250, placeholder="Describe the site...")
        
        # This button is the ONLY thing that triggers a reload now
        generate_pressed = st.form_submit_button("⚡ Generate Code")

    if generate_pressed:
        if not prompt:
            st.warning("Please enter requirements.")
        else:
            with st.spinner("Architecting..."):
                code = architect_website(prompt, design_mode)
                st.session_state.sandbox_code = code
                st.rerun() # Force refresh to show the result on the right

# === RIGHT COLUMN: PREVIEW & DEPLOY ===
with c2:
    if st.session_state.sandbox_code:
        st.markdown("### 2. Preview")
        st.components.v1.html(st.session_state.sandbox_code, height=450, scrolling=True)
        
        st.divider()
        st.markdown("### 3. Deploy")
        
        # This button is now STABLE because the inputs on the left are frozen
        deploy_btn = st.button("🚀 PUSH TO PRODUCTION", type="primary")
        
        if deploy_btn:
            token = st.secrets["GITHUB_TOKEN"]
            # Visual feedback that work is happening
            with st.status("Deploying to GitHub...", expanded=True) as status:
                st.write(" Authenticating...")
                success, msg = push_to_live(st.session_state.sandbox_code, repo_target, "Sharp AI Update", token)
                
                if success:
                    status.update(label="✅ Deployed!", state="complete", expanded=False)
                    st.balloons()
                    st.success(f"Live on {repo_target}. Cloudflare is building now (approx 30s).")
                else:
                    status.update(label="❌ Failed", state="error")
                    st.error(f"Error: {msg}")
st.set_page_config(page_title="Sharp Website | Sandbox", page_icon="🚧", layout="wide")

# --- CSS: STABILIZED UI ---
st.markdown("""
<style>
    .stApp { background-color: #0e1117; color: #e0e0e0; }
    h1 { color: #bd00ff !important; font-family: monospace; letter-spacing: -2px;}
    .stTextArea textarea, .stTextInput input { 
        background-color: #111; color: #00ff9d; border: 1px solid #333; font-family: monospace; 
    }
    .success-box { border: 1px solid #39ff14; background: rgba(57, 255, 20, 0.1); padding: 15px; border-radius: 5px; }
    .deploy-btn { border: 2px solid #bd00ff; color: #fff; }
</style>
""", unsafe_allow_html=True)

# --- SECRETS CHECK ---
if "ANTHROPIC_API_KEY" not in st.secrets or "GITHUB_TOKEN" not in st.secrets:
    st.error("🔒 SECRETS MISSING: Please add ANTHROPIC_API_KEY and GITHUB_TOKEN to secrets.toml")
    st.stop()

anthropic = Anthropic(api_key=st.secrets["ANTHROPIC_API_KEY"])
DEFAULT_REPO = "your-username/your-repo-name" # <--- UPDATE THIS IF YOU WANT

# --- FUNCTIONS ---
def architect_website(prompt, mode):
    system_prompt = f"""
    You are a Senior Frontend Architect. 
    TASK: Generate a single-file 'index.html' ready for production.
    STYLE MODE: {mode}
    REQUIREMENTS: HTML5, embedded CSS/JS, Responsive, High-End Aesthetic.
    OUTPUT: Raw code only.
    """
    try:
        msg = anthropic.messages.create(
            # --- CHANGED: Updated model to a current, valid version ---
            model="claude-3-5-sonnet-20241022",
            max_tokens=4000,
            system=system_prompt,
            messages=[{"role": "user", "content": prompt}]
        )
        return msg.content[0].text
    except Exception as e:
        return f"Error: {e}"

def push_to_live(html_content, repo_name, commit_message, token):
    try:
        g = Github(token)
        # Verify repo access before trying to write
        try:
            repo = g.get_repo(repo_name)
        except:
            return False, f"Could not find repo: {repo_name}. Check spelling or Token permissions."

        # --- CHANGED: File path now targets the 'public' folder for Cloudflare/SSG compatibility ---
        file_path = "public/index.html" 
        
        try:
            contents = repo.get_contents(file_path)
            repo.update_file(file_path, commit_message, html_content, contents.sha)
            return True, "Updated existing index.html"
        except:
            repo.create_file(file_path, commit_message, html_content)
            return True, "Created new index.html"
    except Exception as e:
        return False, str(e)

# --- UI LAYOUT ---
st.title("🚧 Sharp Website // Sandbox")

# SESSION STATE INIT
if 'sandbox_code' not in st.session_state: st.session_state.sandbox_code = ""

c1, c2 = st.columns([1, 1])

# === LEFT COLUMN: THE INPUTS (LOCKED IN FORM) ===
with c1:
    st.markdown("### 1. Blueprint")
    
    # WRAPPING IN FORM STOPs THE "GREY BUTTON" GLITCH
    with st.form("blueprint_form"):
        repo_target = st.text_input("Target Repo (username/repo)", value=DEFAULT_REPO)
        design_mode = st.selectbox("Design System", ["Neon Cyberpunk (Sharp)", "Minimal SaaS", "Luxury Dark", "Brutalist"])
        prompt = st.text_area("Client Requirements", height=250, placeholder="Describe the site...")
        
        # This button is the ONLY thing that triggers a reload now
        generate_pressed = st.form_submit_button("⚡ Generate Code")

    if generate_pressed:
        if not prompt:
            st.warning("Please enter requirements.")
        else:
            with st.spinner("Architecting..."):
                code = architect_website(prompt, design_mode)
                st.session_state.sandbox_code = code
                st.rerun() # Force refresh to show the result on the right

# === RIGHT COLUMN: PREVIEW & DEPLOY ===
with c2:
    if st.session_state.sandbox_code:
        st.markdown("### 2. Preview")
        st.components.v1.html(st.session_state.sandbox_code, height=450, scrolling=True)
        
        st.divider()
        st.markdown("### 3. Deploy")
        
        # This button is now STABLE because the inputs on the left are frozen
        deploy_btn = st.button("🚀 PUSH TO PRODUCTION", type="primary")
        
        if deploy_btn:
            token = st.secrets["GITHUB_TOKEN"]
            # Visual feedback that work is happening
            with st.status("Deploying to GitHub...", expanded=True) as status:
                st.write(" Authenticating...")
                success, msg = push_to_live(st.session_state.sandbox_code, repo_target, "Sharp AI Update", token)
                
                if success:
                    status.update(label="✅ Deployed!", state="complete", expanded=False)
                    st.balloons()
                    st.success(f"Live on {repo_target}. Cloudflare is building now (approx 30s).")
                else:
                    status.update(label="❌ Failed", state="error")
                    st.error(f"Error: {msg}")
