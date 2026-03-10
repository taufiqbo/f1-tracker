import streamlit as st
import os
import json
import base64

# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(
    page_title="🏆 Championship Scoreboard",
    page_icon="🏆",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# -----------------------------
# HELPER FUNCTIONS & DATA
# -----------------------------
def get_img_as_base64(file_path):
    """Reads a local image and converts it to base64 for CSS."""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    path1 = os.path.join(script_dir, file_path)
    path2 = os.path.join(os.path.dirname(script_dir), file_path)
    
    if os.path.exists(path1):
        absolute_path = path1
    elif os.path.exists(path2):
        absolute_path = path2
    else:
        return None
        
    with open(absolute_path, "rb") as f: data = f.read()
    return f"data:image/{absolute_path.split('.')[-1]};base64,{base64.b64encode(data).decode()}"

PREDS_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "predictions.json")

DRIVERS = [
    "Select Driver...", 
    "Max Verstappen", "Lando Norris", "Charles Leclerc", "Carlos Sainz", 
    "Lewis Hamilton", "George Russell", "Oscar Piastri", "Fernando Alonso", 
    "Lance Stroll", "Yuki Tsunoda", "Alex Albon", "Esteban Ocon", 
    "Pierre Gasly", "Nico Hulkenberg", "Kevin Magnussen", "Liam Lawson", 
    "Kimi Antonelli", "Oliver Bearman", "Jack Doohan", "Gabriel Bortoleto", 
    "Franco Colapinto", "Isack Hadjar", "Arvid Lindblad"
]

def load_predictions():
    default_data = {"taufiq": ["Select Driver..."] * 10, "aleeya": ["Select Driver..."] * 10}
    if os.path.exists(PREDS_FILE):
        try:
            with open(PREDS_FILE, "r") as f:
                data = json.load(f)
                if "taufiq" not in data or "aleeya" not in data: return default_data
                return data
        except:
            return default_data
    return default_data

# The Custom Scoring Engine
def calculate_score(predictions, actual_results):
    score = 0
    breakdown = []
    
    for i in range(10):
        pred = predictions[i]
        actual = actual_results[i]
        
        if pred == "Select Driver..." or actual == "Select Driver...":
            breakdown.append({"pos": i+1, "status": "missed", "text": "No Prediction / No Result"})
            continue
            
        if pred == actual:
            # Custom Point System applied here
            if i == 0: pts = 25
            elif i == 1: pts = 18
            elif i == 2: pts = 15
            else: pts = 1
            
            score += pts
            breakdown.append({"pos": i+1, "status": "correct", "text": f"✅ Correct! {pred} (+{pts})"})
        else:
            breakdown.append({"pos": i+1, "status": "wrong", "text": f"❌ Guessed {pred}"})
            
    return score, breakdown

# -----------------------------
# CUSTOM CSS
# -----------------------------
bg_base64 = get_img_as_base64("images/f1_logo.webp")

app_bg = f'background: linear-gradient(rgba(10, 12, 16, 0.5), rgba(10, 12, 16, 0.7)), url("{bg_base64}") no-repeat center center fixed !important; background-size: cover !important;' if bg_base64 else 'background: #0D1117;'

st.markdown(f"""
<style>
    .stApp {{ {app_bg} color: #E6EDF3; }}
    #MainMenu {{visibility: hidden;}} footer {{visibility: hidden;}} header {{visibility: hidden;}}
    
    .main-title {{ font-size: 52px; font-weight: 900; text-align: center; background: linear-gradient(135deg, #FFD700 0%, #FFA500 50%, #FF4500 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; text-transform: uppercase; letter-spacing: 5px; margin-bottom: 5px; }}
    .subtitle {{ text-align: center; color: #8B949E; font-size: 18px; margin-bottom: 20px; letter-spacing: 2px; }}
    
    .score-card {{ background: rgba(22, 27, 34, 0.6); backdrop-filter: blur(16px); border-radius: 20px; padding: 40px; text-align: center; box-shadow: 0 15px 35px rgba(0,0,0,0.6); border: 1px solid rgba(255,255,255,0.05); transition: transform 0.3s ease; }}
    .score-card:hover {{ transform: translateY(-5px); }}
    
    .score-name {{ font-size: 32px; font-weight: 900; text-transform: uppercase; letter-spacing: 4px; margin-bottom: 10px; }}
    .score-number {{ font-size: 80px; font-weight: 900; line-height: 1; text-shadow: 0 10px 20px rgba(0,0,0,0.5); }}
    
    .winner-glow {{ border: 2px solid #FFD700 !important; box-shadow: 0 0 30px rgba(255,215,0,0.3) !important; }}
    .winner-text {{ color: #FFD700; }}
    
    .breakdown-row {{ display: flex; align-items: center; padding: 12px; border-bottom: 1px solid rgba(255,255,255,0.05); }}
    .bd-pos {{ width: 40px; font-weight: 900; color: #8B949E; }}
    .bd-text {{ flex-grow: 1; text-align: left; font-size: 14px; font-weight: 600; }}
    .correct {{ color: #3FB950; }}
    .wrong {{ color: #F85149; opacity: 0.7; }}
    
    div[data-testid="stSelectbox"] label {{ display: none; }}
    
    /* Sleek Back Button Styling */
    div[data-testid="stButton"] button {{
        background: rgba(22, 27, 34, 0.8) !important;
        color: #8B949E !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        font-weight: 700 !important;
        border-radius: 8px !important;
        padding: 15px !important;
        transition: all 0.3s ease !important;
    }}
    div[data-testid="stButton"] button:hover {{
        border-color: #58A6FF !important;
        color: #FFFFFF !important;
        box-shadow: 0 0 15px rgba(88, 166, 255, 0.3) !important;
    }}
</style>
""", unsafe_allow_html=True)

# -----------------------------
# RENDER APP
# -----------------------------
current_preds = load_predictions()

# --- THE NEW BACK BUTTON ---
btn_col, _ = st.columns([2, 10])
with btn_col:
    if st.button("BACK TO PREDICTIONS", use_container_width=True):
        st.switch_page("pages/5_predictions_Championship.py")

st.markdown('<div class="main-title">CHAMPIONSHIP SCOREBOARD</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Enter the official race results to calculate the winner!</div>', unsafe_allow_html=True)

# 1. ACTUAL RESULTS INPUT
with st.expander("🏁 ENTER OFFICIAL RACE RESULTS", expanded=True):
    st.write("Wait for the race to finish, then select the real Top 10 here:")
    actual_results = []
    
    col_a, col_b = st.columns(2)
    for i in range(10):
        target_col = col_a if i < 5 else col_b
        with target_col:
            # OVERLAP FIX: Margin bottom is now positive 5px
            st.markdown(f"<div style='color: #8B949E; font-weight: bold; font-size: 12px; margin-bottom: 5px;'>POSITION {i+1}</div>", unsafe_allow_html=True)
            sel = st.selectbox(f"Actual_P{i}", DRIVERS, key=f"actual_{i}")
            actual_results.append(sel)

# 2. CALCULATE SCORES
taufiq_score, taufiq_breakdown = calculate_score(current_preds["taufiq"], actual_results)
aleeya_score, aleeya_breakdown = calculate_score(current_preds["aleeya"], actual_results)

st.markdown("<br><hr style='border-color: rgba(255,255,255,0.1);'><br>", unsafe_allow_html=True)

# 3. DISPLAY HEAD-TO-HEAD
score_col1, score_col2 = st.columns(2)

t_winner_class = "winner-glow" if taufiq_score > aleeya_score and taufiq_score > 0 else ""
t_text_class = "winner-text" if taufiq_score > aleeya_score and taufiq_score > 0 else "text-white"

a_winner_class = "winner-glow" if aleeya_score > taufiq_score and aleeya_score > 0 else ""
a_text_class = "winner-text" if aleeya_score > taufiq_score and aleeya_score > 0 else "text-white"

with score_col1:
    st.markdown(f"""
    <div class="score-card {t_winner_class}" style="border-top: 5px solid #58A6FF;">
        <div class="score-name" style="color: #58A6FF;">TAUFIQ</div>
        <div class="score-number {t_text_class}">{taufiq_score}</div>
        <div style="color: #8B949E; font-weight: 700; letter-spacing: 2px; margin-top: 5px;">POINTS</div>
    </div>
    """, unsafe_allow_html=True)
    
    with st.expander("View Taufiq's Breakdown"):
        for item in taufiq_breakdown:
            st.markdown(f'<div class="breakdown-row"><div class="bd-pos">P{item["pos"]}</div><div class="bd-text {item["status"]}">{item["text"]}</div></div>', unsafe_allow_html=True)

with score_col2:
    st.markdown(f"""
    <div class="score-card {a_winner_class}" style="border-top: 5px solid #FF6B6B;">
        <div class="score-name" style="color: #FF6B6B;">ALEEYA</div>
        <div class="score-number {a_text_class}">{aleeya_score}</div>
        <div style="color: #8B949E; font-weight: 700; letter-spacing: 2px; margin-top: 5px;">POINTS</div>
    </div>
    """, unsafe_allow_html=True)
    
    with st.expander(" View Aleeya's Breakdown"):
        for item in aleeya_breakdown:
            st.markdown(f'<div class="breakdown-row"><div class="bd-pos">P{item["pos"]}</div><div class="bd-text {item["status"]}">{item["text"]}</div></div>', unsafe_allow_html=True)

# Crown the winner
st.markdown("<br>", unsafe_allow_html=True)
if any(r != "Select Driver..." for r in actual_results):
    if taufiq_score > aleeya_score:
        st.success("TAUFIQ IS CURRENTLY IN THE LEAD!")
    elif aleeya_score > taufiq_score:
        st.success("ALEEYA IS CURRENTLY IN THE LEAD!")
    else:
        st.info(" IT'S A DEAD HEAT TIE!")