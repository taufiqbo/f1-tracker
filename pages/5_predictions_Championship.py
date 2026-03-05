import streamlit as st
import os
import json
import base64
import time

# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(
    page_title="🔮 Prediction Championship",
    page_icon="🔮",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# -----------------------------
# HELPER FUNCTIONS & DATA
# -----------------------------
def get_img_as_base64(file_path):
    """Reads a local image and converts it to base64 for CSS."""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Check inside the 'pages' folder first
    path1 = os.path.join(script_dir, file_path)
    # Check the main 'F1-PROJECT' root folder second
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

# Full grid of current drivers
DRIVERS = [
    "Select Driver...", "Max Verstappen", "Lando Norris", "Charles Leclerc", 
    "Carlos Sainz", "Lewis Hamilton", "George Russell", "Oscar Piastri", 
    "Fernando Alonso", "Lance Stroll", "Yuki Tsunoda", "Daniel Ricciardo", 
    "Alex Albon", "Logan Sargeant", "Esteban Ocon", "Pierre Gasly", 
    "Valtteri Bottas", "Zhou Guanyu", "Nico Hulkenberg", "Kevin Magnussen"
]

def load_predictions():
    # Create empty top 10 lists by default
    default_data = {
        "taufiq": ["Select Driver..."] * 10,
        "aleeya": ["Select Driver..."] * 10
    }
    if os.path.exists(PREDS_FILE):
        try:
            with open(PREDS_FILE, "r") as f:
                data = json.load(f)
                if "taufiq" not in data or "aleeya" not in data: return default_data
                return data
        except:
            return default_data
    return default_data

def save_predictions(taufiq_preds, aleeya_preds):
    with open(PREDS_FILE, "w") as f:
        json.dump({"taufiq": taufiq_preds, "aleeya": aleeya_preds}, f)

current_preds = load_predictions()

# -----------------------------
# CUSTOM CSS
# -----------------------------
bg_base64 = get_img_as_base64("images/start.avif")
app_bg = f'background: linear-gradient(rgba(10, 12, 16, 0.5), rgba(10, 12, 16, 0.95)), url("{bg_base64}") no-repeat center center fixed !important; background-size: cover !important;' if bg_base64 else 'background: #0D1117;'

st.markdown(f"""
<style>
    .stApp {{ {app_bg} color: #E6EDF3; }}
    #MainMenu {{visibility: hidden;}} footer {{visibility: hidden;}} header {{visibility: hidden;}}
    
    .main-title {{ font-size: 52px; font-weight: 900; text-align: center; background: linear-gradient(135deg, #58A6FF 0%, #C9D1D9 50%, #FF6B6B 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; text-transform: uppercase; letter-spacing: 5px; margin-bottom: 5px; }}
    .subtitle {{ text-align: center; color: #8B949E; font-size: 18px; margin-bottom: 40px; letter-spacing: 2px; }}
    
    .player-header {{ font-size: 28px; font-weight: 900; text-align: center; color: #FFFFFF; text-transform: uppercase; letter-spacing: 4px; padding: 15px; border-radius: 12px 12px 0 0; margin-bottom: 20px; }}
    .taufiq-header {{ background: linear-gradient(90deg, rgba(88,166,255,0.1), rgba(88,166,255,0.4), rgba(88,166,255,0.1)); border-bottom: 3px solid #58A6FF; }}
    .aleeya-header {{ background: linear-gradient(90deg, rgba(255,107,107,0.1), rgba(255,107,107,0.4), rgba(255,107,107,0.1)); border-bottom: 3px solid #FF6B6B; }}
    
    .glass-column {{ background: rgba(22, 27, 34, 0.5); backdrop-filter: blur(12px); border: 1px solid rgba(255,255,255,0.05); border-radius: 16px; padding: 20px; box-shadow: 0 10px 30px rgba(0,0,0,0.5); }}
    
    /* Position Number Styling */
    .pos-number {{ font-size: 20px; font-weight: 900; color: #8B949E; width: 40px; text-align: right; padding-right: 15px; display: flex; align-items: center; justify-content: flex-end; height: 100%; }}
    .pos-1 {{ color: #FFD700; text-shadow: 0 0 10px rgba(255,215,0,0.5); }} /* Gold */
    .pos-2 {{ color: #C0C0C0; text-shadow: 0 0 10px rgba(192,192,192,0.5); }} /* Silver */
    .pos-3 {{ color: #CD7F32; text-shadow: 0 0 10px rgba(205,127,50,0.5); }} /* Bronze */
    
    div[data-testid="stSelectbox"] label {{ display: none; }} /* Hide default labels */
    div[data-testid="stButton"] button {{ background: linear-gradient(135deg, #3FB950 0%, #2EA043 100%) !important; color: white !important; font-weight: 900 !important; letter-spacing: 2px !important; border-radius: 8px !important; padding: 25px !important; border: none !important; font-size: 18px !important; margin-top: 20px; }}
    div[data-testid="stButton"] button:hover {{ box-shadow: 0 0 20px rgba(63, 185, 80, 0.4) !important; transform: scale(1.01) !important; }}
</style>
""", unsafe_allow_html=True)

# -----------------------------
# RENDER APP
# -----------------------------
st.markdown('<div class="main-title">🔮 PREDICTION CHAMPIONSHIP</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Lock in our Top 10 before qualifying begins!</div>', unsafe_allow_html=True)

col1, spacer, col2 = st.columns([10, 1, 10])

# Lists to hold the live selections
taufiq_selections = []
aleeya_selections = []

with col1:
    st.markdown('<div class="glass-column">', unsafe_allow_html=True)
    st.markdown('<div class="player-header taufiq-header">🏎️ TAUFIQ</div>', unsafe_allow_html=True)
    
    for i in range(10):
        pos_class = f"pos-{i+1}" if i < 3 else ""
        row_c1, row_c2 = st.columns([1, 6])
        
        with row_c1:
            st.markdown(f'<div class="pos-number {pos_class}">P{i+1}</div>', unsafe_allow_html=True)
        with row_c2:
            # Find the index of the previously saved driver, default to 0 if not found
            saved_driver = current_preds["taufiq"][i]
            idx = DRIVERS.index(saved_driver) if saved_driver in DRIVERS else 0
            
            sel = st.selectbox(f"T_P{i}", DRIVERS, index=idx, key=f"t_{i}")
            taufiq_selections.append(sel)
            
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="glass-column">', unsafe_allow_html=True)
    st.markdown('<div class="player-header aleeya-header">🏎️ ALEEYA</div>', unsafe_allow_html=True)
    
    for i in range(10):
        pos_class = f"pos-{i+1}" if i < 3 else ""
        row_c1, row_c2 = st.columns([1, 6])
        
        with row_c1:
            st.markdown(f'<div class="pos-number {pos_class}">P{i+1}</div>', unsafe_allow_html=True)
        with row_c2:
            saved_driver = current_preds["aleeya"][i]
            idx = DRIVERS.index(saved_driver) if saved_driver in DRIVERS else 0
            
            sel = st.selectbox(f"A_P{i}", DRIVERS, index=idx, key=f"a_{i}")
            aleeya_selections.append(sel)
            
    st.markdown('</div>', unsafe_allow_html=True)

# Big Save Button at the bottom
if st.button("🏁 LOCK IN PREDICTIONS", use_container_width=True):
    save_predictions(taufiq_selections, aleeya_selections)
    st.toast("Predictions Locked!", icon="🔒")
    st.balloons()
    time.sleep(1)
    st.rerun()