import streamlit as st
import os
import json
import base64
import time

# -----------------------------
# PAGE CONFIG & SESSION STATE
# -----------------------------
st.set_page_config(
    page_title="⭐ Favorites Selector",
    page_icon="⭐",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# We use session state to remember to play the audio AFTER the page reloads!
if 'play_voice' not in st.session_state:
    st.session_state.play_voice = None

# -----------------------------
# HELPER FUNCTIONS
# -----------------------------
def get_img_as_base64(file_path):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(script_dir) 
    absolute_path = os.path.join(parent_dir, file_path)
    
    if not os.path.exists(absolute_path): return None
    with open(absolute_path, "rb") as f: data = f.read()
    encoded = base64.b64encode(data).decode()
    ext = absolute_path.split('.')[-1]
    return f"data:image/{ext};base64,{encoded}"

FAVS_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "favorites.json")

def load_favorites():
    default_data = {
        "taufiq": {"driver": "Max Verstappen", "team": "Red Bull"},
        "aleeya": {"driver": "Oscar Piastri", "team": "McLaren"}
    }
    if os.path.exists(FAVS_FILE):
        try:
            with open(FAVS_FILE, "r") as f:
                data = json.load(f)
                if "taufiq" not in data or "aleeya" not in data:
                    return default_data
                return data
        except:
            return default_data
    return default_data

def save_favorites(person, driver, team):
    data = load_favorites()
    data[person] = {"driver": driver, "team": team}
    with open(FAVS_FILE, "w") as f:
        json.dump(data, f)

# -----------------------------
# DATA, COLORS, & AUDIO
# -----------------------------
TEAM_HEX = {
    "Red Bull": "#3671C6",
    "Ferrari": "#E8002D",
    "Mercedes": "#27F4D2",
    "McLaren": "#FF8000",
    "Aston Martin": "#00A696",
    "None": "#8B949E"
}

# MAP DRIVERS TO THEIR MP3 FILES HERE
DRIVER_AUDIO = {
    "Max Verstappen": "pages/audio/max.mp3",
    "Lando Norris": "pages/audio/lando.mp3",
    "Oscar Piastri": "pages/audio/oscar.mp3",
}

DRIVERS_LIST = ["Max Verstappen", "Lando Norris", "Charles Leclerc", "Carlos Sainz", "Lewis Hamilton", "George Russell", "Oscar Piastri", "Fernando Alonso", "None"]
TEAMS_LIST = ["Red Bull", "McLaren", "Ferrari", "Mercedes", "Aston Martin", "None"]

current_favs = load_favorites()

# -----------------------------
# CUSTOM CSS
# -----------------------------
bg_base64 = get_img_as_base64("images/f1_logo.webp")

if bg_base64:
    app_bg = f'background: linear-gradient(rgba(10, 12, 16, 0.8), rgba(10, 12, 16, 0.95)), url("{bg_base64}") no-repeat center center fixed !important; background-size: cover !important;'
else:
    app_bg = 'background: linear-gradient(180deg, #0D1117 0%, #161B22 50%, #0D1117 100%);'

st.markdown(f"""
<style>
    .stApp {{ {app_bg} color: #E6EDF3; }}
    #MainMenu {{visibility: hidden;}} footer {{visibility: hidden;}} header {{visibility: hidden;}}
    .main-title {{ font-size: 52px; font-weight: 900; text-align: center; background: linear-gradient(135deg, #58A6FF 0%, #C9D1D9 50%, #FF6B6B 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; text-transform: uppercase; letter-spacing: 5px; margin-bottom: 5px; }}
    .subtitle {{ text-align: center; color: #8B949E; font-size: 18px; margin-bottom: 40px; letter-spacing: 2px; }}
    .modern-card {{ background: rgba(22, 27, 34, 0.4); backdrop-filter: blur(16px); -webkit-backdrop-filter: blur(16px); border: 1px solid rgba(255, 255, 255, 0.05); border-radius: 16px; padding: 40px 30px; text-align: center; transition: transform 0.3s cubic-bezier(0.1, 0.8, 0.2, 1), box-shadow 0.3s ease; margin-bottom: 20px; }}
    .modern-card:hover {{ transform: translateY(-5px); }}
    .profile-name {{ font-size: 20px; font-weight: 900; color: #8B949E; text-transform: uppercase; letter-spacing: 4px; margin-bottom: 30px; display: flex; align-items: center; justify-content: center; gap: 10px; }}
    .stats-grid {{ display: grid; grid-template-columns: 1fr; gap: 25px; }}
    .stat-box {{ background: rgba(13, 17, 23, 0.5); border-radius: 12px; padding: 20px; border: 1px solid rgba(255, 255, 255, 0.03); }}
    .stat-label {{ font-size: 11px; text-transform: uppercase; letter-spacing: 2px; color: #8B949E; margin-bottom: 8px; font-weight: 700; }}
    .stat-value {{ font-size: 24px; font-weight: 900; color: #FFFFFF; letter-spacing: 0.5px; }}
    div[data-testid="stSelectbox"] label {{ color: #E6EDF3 !important; font-weight: 700; letter-spacing: 1px; text-transform: uppercase; font-size: 12px !important; }}
    div[data-testid="stButton"] button {{ background: rgba(22, 27, 34, 0.8) !important; color: white !important; border: 1px solid rgba(255, 255, 255, 0.1) !important; font-weight: 800 !important; letter-spacing: 2px !important; text-transform: uppercase !important; border-radius: 8px !important; padding: 20px !important; transition: all 0.3s ease !important; }}
    div[data-testid="stButton"] button:hover {{ border-color: #58A6FF !important; box-shadow: 0 0 15px rgba(88, 166, 255, 0.3) !important; transform: scale(1.02) !important; }}
</style>
""", unsafe_allow_html=True)

# -----------------------------
# AUDIO PLAYER LOGIC
# -----------------------------
# If a voice is queued up to play, trigger it invisibly!
if st.session_state.play_voice:
    audio_path = DRIVER_AUDIO.get(st.session_state.play_voice)
    
    # We must construct the absolute path for Streamlit to find the file
    script_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(script_dir) 
    
    if audio_path:
        full_audio_path = os.path.join(parent_dir, audio_path)
        if os.path.exists(full_audio_path):
            # Render an invisible audio player that auto-plays
            st.audio(full_audio_path, format="audio/mpeg", autoplay=True)
            
    # Reset the state so it doesn't play every single time you click somewhere else
    st.session_state.play_voice = None

# -----------------------------
# RENDER APP
# -----------------------------
st.markdown('<div class="main-title">⭐ FAVORITES SELECTOR</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Choose your favorite driver & constructor</div>', unsafe_allow_html=True)

taufiq_color = TEAM_HEX.get(current_favs["taufiq"]["team"], TEAM_HEX["None"])
aleeya_color = TEAM_HEX.get(current_favs["aleeya"]["team"], TEAM_HEX["None"])

col1, col2 = st.columns(2)

with col1:
    st.markdown(f"""
    <div class="modern-card" style="border-top: 4px solid {taufiq_color}; box-shadow: 0 10px 30px -10px {taufiq_color}60;">
        <div class="profile-name"><span style="color: {taufiq_color};">⚡</span> TAUFIQ</div>
        <div class="stats-grid">
            <div class="stat-box"><div class="stat-label">Driver</div><div class="stat-value">{current_favs["taufiq"]["driver"]}</div></div>
            <div class="stat-box"><div class="stat-label">Constructor</div><div class="stat-value" style="color: {taufiq_color};">{current_favs["taufiq"]["team"]}</div></div>
        </div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="modern-card" style="border-top: 4px solid {aleeya_color}; box-shadow: 0 10px 30px -10px {aleeya_color}60;">
        <div class="profile-name"><span style="color: {aleeya_color};">⚡</span> ALEEYA</div>
        <div class="stats-grid">
            <div class="stat-box"><div class="stat-label">Driver</div><div class="stat-value">{current_favs["aleeya"]["driver"]}</div></div>
            <div class="stat-box"><div class="stat-label">Constructor</div><div class="stat-value" style="color: {aleeya_color};">{current_favs["aleeya"]["team"]}</div></div>
        </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

edit_col1, edit_col2 = st.columns(2)

with edit_col1:
    with st.expander("⚙️ EDIT TAUFIQ'S FAVORITES", expanded=False):
        t_d_idx = DRIVERS_LIST.index(current_favs["taufiq"]["driver"]) if current_favs["taufiq"]["driver"] in DRIVERS_LIST else 0
        t_t_idx = TEAMS_LIST.index(current_favs["taufiq"]["team"]) if current_favs["taufiq"]["team"] in TEAMS_LIST else 0
        
        new_t_driver = st.selectbox("Taufiq's Driver", DRIVERS_LIST, index=t_d_idx, key="t_d")
        new_t_team = st.selectbox("Taufiq's Constructor", TEAMS_LIST, index=t_t_idx, key="t_t")
        
        if st.button("💾 SAVE TAUFIQ", use_container_width=True):
            save_favorites("taufiq", new_t_driver, new_t_team)
            # Queue up the voice line to play on reload!
            st.session_state.play_voice = new_t_driver
            st.toast("Taufiq's favorites updated!", icon="🏁")
            time.sleep(0.5)
            st.rerun()

with edit_col2:
    with st.expander("⚙️ EDIT ALEEYA'S FAVORITES", expanded=False):
        a_d_idx = DRIVERS_LIST.index(current_favs["aleeya"]["driver"]) if current_favs["aleeya"]["driver"] in DRIVERS_LIST else 0
        a_t_idx = TEAMS_LIST.index(current_favs["aleeya"]["team"]) if current_favs["aleeya"]["team"] in TEAMS_LIST else 0
        
        new_a_driver = st.selectbox("Aleeya's Driver", DRIVERS_LIST, index=a_d_idx, key="a_d")
        new_a_team = st.selectbox("Aleeya's Constructor", TEAMS_LIST, index=a_t_idx, key="a_t")
        
        if st.button("💾 SAVE ALEEYA", use_container_width=True):
            save_favorites("aleeya", new_a_driver, new_a_team)
            # Queue up the voice line to play on reload!
            st.session_state.play_voice = new_a_driver
            st.toast("Aleeya's favorites updated!", icon="🏁")
            st.balloons()
            time.sleep(0.5)
            st.rerun()