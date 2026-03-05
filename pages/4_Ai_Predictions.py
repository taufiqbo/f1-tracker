import streamlit as st
import pandas as pd
import joblib
import os
import base64

def get_img_as_base64(file_path):
    """Reads a local image and converts it to base64 for CSS."""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    absolute_path = os.path.join(script_dir, file_path)
    if not os.path.exists(absolute_path): return None
    with open(absolute_path, "rb") as f: data = f.read()
    encoded = base64.b64encode(data).decode()
    ext = absolute_path.split('.')[-1]
    return f"data:image/{ext};base64,{encoded}"



# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(
    page_title="🤖 AI Prediction",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# -----------------------------
# AI MODEL INTEGRATION
# -----------------------------
TEAM_COLORS = {
    "Red Bull": "linear-gradient(90deg, #001A30 0%, #3671C6 100%)",
    "Ferrari": "linear-gradient(90deg, #8B0000 0%, #E8002D 100%)",
    "Mercedes": "linear-gradient(90deg, #00A19B 0%, #27F4D2 100%)",
    "McLaren": "linear-gradient(90deg, #FF4500 0%, #FF8000 100%)",
    "Aston Martin": "linear-gradient(90deg, #006F62 0%, #004F46 100%)"
}

# Solid hex colors for typography
TEAM_HEX = {
    "Red Bull": "#58A6FF",
    "Ferrari": "#FF4B4B",
    "Mercedes": "#00D2BE",
    "McLaren": "#FF8000",
    "Aston Martin": "#006F62"
}

# Load the trained model
current_dir = os.path.dirname(os.path.abspath(__file__))
model_path = os.path.join(current_dir, 'f1_winner_model.pkl')

try:
    model = joblib.load(model_path)
    model_loaded = True
except FileNotFoundError:
    model_loaded = False

# -----------------------------
# CUSTOM CSS - PREMIUM UI
# -----------------------------
# -----------------------------
# CUSTOM CSS - PREMIUM UI
# -----------------------------

# 1. Grab the background image (You can change this to "images/ai_wallpaper.jpg" if you download a new one)
bg_base64 = get_img_as_base64("images/start.avif")

if bg_base64:
    app_bg = f'background: linear-gradient(rgba(10, 12, 16, 0.6), rgba(10, 12, 16, 0.85)), url("{bg_base64}") no-repeat center center fixed !important; background-size: cover !important;'
else:
    app_bg = 'background: linear-gradient(180deg, #0D1117 0%, #161B22 50%, #0D1117 100%);'

# 2. Inject Dynamic Background (Using f-string)
st.markdown(f"""
<style>
    /* Global Styles */
    .stApp {{
        {app_bg}
        color: #E6EDF3;
    }}
</style>
""", unsafe_allow_html=True)

# 3. Inject Static CSS (Normal string to prevent Python crashes)
st.markdown("""
<style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    .main-title {
        font-size: 52px;
        font-weight: 900;
        text-align: center;
        background: linear-gradient(135deg, #58A6FF 0%, #C9D1D9 50%, #FF6B6B 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-transform: uppercase;
        letter-spacing: 5px;
        margin-bottom: 5px;
    }
    
    .subtitle {
        text-align: center;
        color: #8B949E;
        font-size: 18px;
        margin-bottom: 30px;
        letter-spacing: 2px;
    }
    
    /* Sleek Number Inputs */
    div[data-testid="stNumberInputContainer"] {
        background-color: #0D1117 !important;
        border: 1px solid #30363D !important;
        border-radius: 8px !important;
        transition: all 0.3s ease;
    }
    
    div[data-testid="stNumberInputContainer"]:focus-within {
        border-color: #58A6FF !important;
        box-shadow: 0 0 10px rgba(88, 166, 255, 0.3) !important;
    }

    /* Make Input Labels Look Like Tech Dashboards */
    .stNumberInput label {
        color: #8B949E !important;
        font-size: 11px !important;
        text-transform: uppercase !important;
        letter-spacing: 1px !important;
        font-weight: 600 !important;
    }
    
    /* Results Glass Panel */
    .glass-panel {
        background: linear-gradient(145deg, rgba(22, 27, 34, 0.8), rgba(13, 17, 23, 0.9));
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-top: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 24px;
        padding: 40px;
        box-shadow: 0 15px 35px rgba(0, 0, 0, 0.6);
        max-width: 900px;
        margin: 30px auto;
    }
    
    .panel-header {
        display: flex;
        justify-content: center;
        align-items: center;
        border-bottom: 1px solid rgba(48, 54, 61, 0.5);
        padding-bottom: 25px;
        margin-bottom: 35px;
    }
    
    .race-name {
        font-size: 24px;
        font-weight: 900;
        color: #FFFFFF;
        text-transform: uppercase;
        letter-spacing: 4px;
        display: flex;
        align-items: center;
        gap: 10px;
    }
    
    .pred-row {
        display: flex;
        align-items: center;
        margin-bottom: 28px;
        padding: 10px;
        border-radius: 12px;
        transition: background 0.3s ease;
    }
    
    .pred-row:hover {
        background: rgba(255, 255, 255, 0.03);
    }
    
    .pred-rank {
        font-size: 28px;
        font-weight: 900;
        color: #30363D;
        width: 50px;
    }
    
    /* Make the #1 rank pop out */
    .rank-1 { color: #58A6FF; text-shadow: 0 0 15px rgba(88, 166, 255, 0.4); }
    .rank-2 { color: #C9D1D9; }
    .rank-3 { color: #8B949E; }
    
    .pred-info {
        width: 220px;
    }
    
    .pred-name {
        font-size: 19px;
        font-weight: 800;
        color: #FFFFFF;
        margin-bottom: 2px;
        letter-spacing: 0.5px;
    }
    
    .pred-team {
        font-size: 11px;
        color: #8B949E;
        text-transform: uppercase;
        letter-spacing: 2px;
        font-weight: 600;
    }
    
    .bar-track {
        flex-grow: 1;
        height: 12px;
        background: rgba(0, 0, 0, 0.6);
        border-radius: 20px;
        margin: 0 30px;
        overflow: hidden;
        border: 1px solid rgba(255,255,255,0.03);
        box-shadow: inset 0 2px 4px rgba(0,0,0,0.5);
    }
    
    .bar-fill {
        height: 100%;
        border-radius: 20px;
        transition: width 1.2s cubic-bezier(0.2, 0.8, 0.2, 1);
        box-shadow: 0 0 15px rgba(255,255,255,0.2);
    }
    
    .pred-value {
        font-size: 24px;
        font-weight: 900;
        color: #FFFFFF;
        width: 70px;
        text-align: right;
        font-family: 'Courier New', monospace;
    }
</style>
""", unsafe_allow_html=True)

# -----------------------------
# RENDER APP
# -----------------------------
st.markdown('<div class="main-title">🤖 AI RACE PREDICTION</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Interactive Sandbox - Test the ML Model</div>', unsafe_allow_html=True)

if not model_loaded:
    st.error("⚠️ Model file 'f1_winner_model.pkl' not found.")
else:
    # --- INTERACTIVE CONTROL PANEL ---
    with st.expander(" OPEN CONTROL PANEL", expanded=True):
        st.markdown("<p style='text-align: center; color: #8B949E; margin-bottom: 20px;'>Adjust starting grid and championship points to recalculate live win probabilities.</p>", unsafe_allow_html=True)
        
        # Base templates for drivers
        driver_templates = [
            {"name": "Max Verstappen", "team": "Red Bull", "def_grid": 1, "def_pts": 437, "def_cpts": 589},
            {"name": "Lando Norris", "team": "McLaren", "def_grid": 2, "def_pts": 374, "def_cpts": 666},
            {"name": "Charles Leclerc", "team": "Ferrari", "def_grid": 3, "def_pts": 292, "def_cpts": 652},
            {"name": "Oscar Piastri", "team": "McLaren", "def_grid": 4, "def_pts": 292, "def_cpts": 666},
            {"name": "Lewis Hamilton", "team": "Mercedes", "def_grid": 5, "def_pts": 190, "def_cpts": 382},
            {"name": "Carlos Sainz", "team": "Ferrari", "def_grid": 6, "def_pts": 200, "def_cpts": 652}
        ]
        
        upcoming_race_data = []
        cols = st.columns(6)
        
        # Create input widgets for each driver inside stylized containers
        for i, col in enumerate(cols):
            with col:
                # Using Streamlit's native border container for a "Control Module" look
                with st.container(border=True):
                    team = driver_templates[i]['team']
                    team_color = TEAM_HEX.get(team, "#FFFFFF")
                    
                    st.markdown(f"<div style='text-align: center; font-size: 16px; font-weight: 800; color: white; margin-bottom: 2px;'>{driver_templates[i]['name']}</div>", unsafe_allow_html=True)
                    st.markdown(f"<div style='text-align: center; font-size: 10px; font-weight: 700; color: {team_color}; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 15px;'>{team}</div>", unsafe_allow_html=True)
                    
                    grid_val = st.number_input("Grid Start", min_value=1, max_value=20, value=driver_templates[i]['def_grid'], key=f"grid_{i}")
                    d_pts = st.number_input("Driver Pts", min_value=0, max_value=600, value=driver_templates[i]['def_pts'], key=f"dpts_{i}")
                    c_pts = st.number_input("Team Pts", min_value=0, max_value=1000, value=driver_templates[i]['def_cpts'], key=f"cpts_{i}")
                    
                    upcoming_race_data.append({
                        "name": driver_templates[i]['name'],
                        "team": driver_templates[i]['team'],
                        "grid": grid_val,
                        "driver_points": d_pts,
                        "constructor_points": c_pts
                    })

    # --- ML PREDICTION LOGIC ---
    df_predict = pd.DataFrame(upcoming_race_data)[['grid', 'driver_points', 'constructor_points']]
    probabilities = model.predict_proba(df_predict)

    predictions = []
    for idx, driver in enumerate(upcoming_race_data):
        raw_prob = probabilities[idx][1] * 100
        display_prob = int(raw_prob * 2.5) if (raw_prob * 2.5) < 95 else 95 
        
        predictions.append({
            "name": driver["name"],
            "team": driver["team"],
            "prob": display_prob
        })

    predictions = sorted(predictions, key=lambda x: x['prob'], reverse=True)

    # --- RENDER RESULTS PANEL ---
    html_content = """<div class="glass-panel">
    <div class="panel-header">
    <div class="race-name"> SIMULATED RACE OUTCOME</div>
    </div>
    """

    for idx, driver in enumerate(predictions):
        rank = idx + 1
        name = driver["name"]
        team = driver["team"]
        prob = driver["prob"]
        
        bar_color = TEAM_COLORS.get(team, "linear-gradient(90deg, #30363D 0%, #8B949E 100%)")
        
        # Add special CSS classes to top 3 ranks
        rank_class = f"rank-{rank}" if rank <= 3 else ""
        
        html_content += f"""<div class="pred-row">
    <div class="pred-rank {rank_class}">#{rank}</div>
    <div class="pred-info">
    <div class="pred-name">{name}</div>
    <div class="pred-team">{team}</div>
    </div>
    <div class="bar-track">
    <div class="bar-fill" style="width: {prob}%; background: {bar_color};"></div>
    </div>
    <div class="pred-value">{prob}%</div>
    </div>
    """
        
    html_content += "</div>"
    st.markdown(html_content, unsafe_allow_html=True)