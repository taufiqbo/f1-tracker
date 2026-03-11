import streamlit as st
import requests
import json
import os
import base64


def get_img_as_base64(file_path):
    """Reads a local image and converts it to base64 for CSS."""
    # Get the exact directory this script is living in
    script_dir = os.path.dirname(os.path.abspath(__file__))
    absolute_path = os.path.join(script_dir, file_path)
    
    if not os.path.exists(absolute_path):
        # This will show a red error on your page if the path is wrong
        st.error(f"⚠️ DEBUG: Could not find image at {absolute_path}") 
        return None
    
    with open(absolute_path, "rb") as f:
        data = f.read()
    
    encoded = base64.b64encode(data).decode()
    ext = absolute_path.split('.')[-1]
    return f"data:image/{ext};base64,{encoded}"

# Updated keys to match Ergast API standard IDs
DRIVER_BG_MAP = {
    "max_verstappen": "images/max_verstappen.webp",
    "norris": "images/lando_norris.webp",
    "piastri": "images/oscar_piastri.jpg",
    "leclerc": "images/charles_leclerc.webp",
    "sainz": "images/carlos_sainz.webp",
    "russell": "images/george_russell.jpg",
    "hamilton": "images/lewis_hamilton.jpg"

}


# Initialize session state FIRST
if "selected_driver" not in st.session_state:
    st.session_state.selected_driver = None

# PAGE CONFIG
st.set_page_config(
    page_title="🏆 Driver Championship",
    page_icon="🏁",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ... rest of your code ...

# -----------------------------
# CUSTOM CSS - MIDNIGHT RACER THEME
# -----------------------------
st.markdown("""
<style>
    /* Global Styles */
    .stApp {
        background: linear-gradient(180deg, #0D1117 0%, #161B22 50%, #0D1117 100%);
        color: #E6EDF3;
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Main Title */
    .main-title {
        font-size: 52px;
        font-weight: 900;
        text-align: center;
        background: linear-gradient(135deg, #58A6FF 0%, #C9D1D9 50%, #FF6B6B 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-transform: uppercase;
        letter-spacing: 5px;
        margin-bottom: 15px;
        filter: drop-shadow(0 0 20px rgba(88, 166, 255, 0.3));
        animation: titleShimmer 4s ease-in-out infinite;
    }
    
    @keyframes titleShimmer {
        0%, 100% { filter: drop-shadow(0 0 20px rgba(88, 166, 255, 0.3)); }
        50% { filter: drop-shadow(0 0 35px rgba(255, 107, 107, 0.4)); }
    }
    
    .subtitle {
        text-align: center;
        color: #8B949E;
        font-size: 17px;
        margin-bottom: 50px;
        font-weight: 400;
        letter-spacing: 2px;
    }
    
    /* Podium Section */
    .podium-container {
        display: flex;
        justify-content: center;
        align-items: flex-end;
        gap: 20px;
        margin: 40px 0 60px 0;
        padding: 0 20px;
    }
    
    .podium-position {
        text-align: center;
        transition: all 0.4s ease;
    }
    
    .podium-position:hover {
        transform: translateY(-10px);
    }
    
    /* First Place - Gold */
    .podium-first {
        order: 2;
    }
    
    .podium-first .podium-stand {
        background: linear-gradient(135deg, #FFD700 0%, #FFA500 100%);
        height: 180px;
        width: 200px;
        border-radius: 20px 20px 0 0;
        display: flex;
        align-items: center;
        justify-content: center;
        box-shadow: 0 15px 40px rgba(255, 215, 0, 0.5);
        border: 3px solid #FFD700;
    }
    
    .podium-first .position-number {
        font-size: 80px;
        font-weight: 900;
        color: #000000;
        text-shadow: 0 4px 8px rgba(0, 0, 0, 0.3);
    }
    
    /* Second Place - Silver */
    .podium-second {
        order: 1;
    }
    
    .podium-second .podium-stand {
        background: linear-gradient(135deg, #C0C0C0 0%, #A8A8A8 100%);
        height: 140px;
        width: 180px;
        border-radius: 20px 20px 0 0;
        display: flex;
        align-items: center;
        justify-content: center;
        box-shadow: 0 15px 40px rgba(192, 192, 192, 0.5);
        border: 3px solid #C0C0C0;
    }
    
    .podium-second .position-number {
        font-size: 70px;
        font-weight: 900;
        color: #000000;
        text-shadow: 0 4px 8px rgba(0, 0, 0, 0.3);
    }
    
    /* Third Place - Bronze */
    .podium-third {
        order: 3;
    }
    
    .podium-third .podium-stand {
        background: linear-gradient(135deg, #CD7F32 0%, #A0522D 100%);
        height: 100px;
        width: 180px;
        border-radius: 20px 20px 0 0;
        display: flex;
        align-items: center;
        justify-content: center;
        box-shadow: 0 15px 40px rgba(205, 127, 50, 0.5);
        border: 3px solid #CD7F32;
    }
    
    .podium-third .position-number {
        font-size: 60px;
        font-weight: 900;
        color: #FFFFFF;
        text-shadow: 0 4px 8px rgba(0, 0, 0, 0.5);
    }
    
    .podium-driver-info {
        margin-bottom: 15px;
    }
    
    .podium-driver-name {
        font-size: 20px;
        font-weight: 900;
        color: #E6EDF3;
        margin-bottom: 5px;
    }
    
    .podium-points {
        font-size: 24px;
        font-weight: 900;
        color: #FFA657;
        font-family: 'Courier New', monospace;
    }
    
    /* Driver Row - Enhanced */
    .driver-row {
        display: flex;
        align-items: center;
        padding: 20px 25px;
        margin-bottom: 15px;
        background: linear-gradient(135deg, #161B22 0%, #0D1117 100%);
        border-radius: 16px;
        border-left: 5px solid #58A6FF;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.3);
        position: relative;
        overflow: hidden;
    }
    
    .driver-row::before {
        content: '';
        position: absolute;
        left: 0;
        top: 0;
        bottom: 0;
        width: 0;
        background: linear-gradient(90deg, rgba(88, 166, 255, 0.1), transparent);
        transition: width 0.4s ease;
        border-radius: 16px 0 0 16px;
    }
    
    .driver-row:hover::before {
        width: 100%;
    }
    
    .driver-row:hover {
        background: linear-gradient(135deg, #1C2128 0%, #161B22 100%);
        transform: translateX(10px);
        box-shadow: 0 8px 24px rgba(88, 166, 255, 0.2);
        border-left-color: #FF6B6B;
    }
    
    .driver-position {
        font-size: 32px;
        font-weight: 900;
        color: #58A6FF;
        width: 70px;
        text-shadow: 0 2px 8px rgba(88, 166, 255, 0.4);
        position: relative;
        z-index: 1;
    }
    
    .driver-name {
        flex-grow: 1;
        position: relative;
        z-index: 1;
    }
    
    .driver-full-name {
        font-size: 22px;
        font-weight: 900;
        color: #E6EDF3;
        margin-bottom: 5px;
    }
    
    .driver-team {
        font-size: 14px;
        color: #8B949E;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    .driver-stats {
        display: flex;
        gap: 30px;
        align-items: center;
        position: relative;
        z-index: 1;
    }
    
    .stat-item {
        text-align: center;
    }
    
    .stat-label {
        font-size: 12px;
        color: #8B949E;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-bottom: 5px;
    }
    
    .stat-value {
        font-size: 24px;
        font-weight: 900;
        color: #FFA657;
        font-family: 'Courier New', monospace;
    }
    
    .points-bar {
        height: 6px;
        background: linear-gradient(90deg, #58A6FF 0%, #FF6B6B 100%);
        border-radius: 3px;
        margin-top: 12px;
        transition: all 0.8s cubic-bezier(0.4, 0, 0.2, 1);
        box-shadow: 0 2px 12px rgba(88, 166, 255, 0.4);
    }
    
    /* Favorite Highlight */
    .favorite-driver {
        background: linear-gradient(135deg, #1F6FEB 0%, #8B2B8B 50%, #C9184A 100%) !important;
        border-left-color: #FFD700 !important;
        box-shadow: 0 8px 32px rgba(31, 111, 235, 0.4) !important;
    }
    
    .favorite-driver .driver-full-name {
        color: #FFD700 !important;
        text-shadow: 0 0 20px rgba(255, 215, 0, 0.6);
    }
    
    .favorite-driver .driver-position {
        color: #FFD700 !important;
        text-shadow: 0 0 20px rgba(255, 215, 0, 0.6);
    }
    
    .favorite-driver .points-bar {
        background: linear-gradient(90deg, #FFD700 0%, #FFA500 100%) !important;
        box-shadow: 0 2px 16px rgba(255, 215, 0, 0.6) !important;
    }
    
    .favorite-badge {
        background: #FFD700;
        color: #000000;
        padding: 5px 15px;
        border-radius: 20px;
        font-size: 12px;
        font-weight: 900;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-left: 15px;
        animation: pulse 2s infinite;
    }
    
    @keyframes pulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.7; }
    }
    
    /* Top 3 Special Styling */
    .position-1 { border-left-color: #FFD700 !important; }
    .position-2 { border-left-color: #C0C0C0 !important; }
    .position-3 { border-left-color: #CD7F32 !important; }
    
    .position-1 .driver-position { color: #FFD700 !important; }
    .position-2 .driver-position { color: #C0C0C0 !important; }
    .position-3 .driver-position { color: #CD7F32 !important; }
    
    /* Info Banner */
    .info-banner {
        background: linear-gradient(135deg, #1C2128 0%, #0D1117 100%);
        border: 1px solid #30363D;
        border-left: 4px solid #58A6FF;
        padding: 20px 25px;
        border-radius: 12px;
        margin-bottom: 30px;
        display: flex;
        align-items: center;
        gap: 15px;
    }
    
    .info-icon {
        font-size: 32px;
        color: #58A6FF;
    }
    
    .info-text {
        color: #8B949E;
        font-size: 15px;
        line-height: 1.6;
    }
    
    /* Scrollbar */
    ::-webkit-scrollbar {
        width: 10px;
    }
    
    ::-webkit-scrollbar-track {
        background: #0D1117;
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(180deg, #58A6FF, #1F6FEB);
        border-radius: 5px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(180deg, #79C0FF, #58A6FF);
    }
            
</style>
""", unsafe_allow_html=True)

# -----------------------------
# API FUNCTIONS
# -----------------------------
@st.cache_data(ttl=300)
def get_driver_standings():
    """Fetch current driver standings"""
  # Try multiple API endpoints
    urls = [
        # 1. PRIMARY: Jolpi API for the LIVE current season
        "https://api.jolpi.ca/ergast/f1/current/driverStandings.json", 
        
        # 2. BACKUP: The old Ergast API
        "http://ergast.com/api/f1/current/driverStandings.json",
        
        # 3. LAST RESORT: 2025 data fallback (Upgraded from 2024!)
        "https://api.jolpi.ca/ergast/f1/2025/driverStandings.json"
    ]
    for url in urls:
        try:
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                data = response.json()
                standings_lists = data.get("MRData", {}).get("StandingsTable", {}).get("StandingsLists", [])
                
                if standings_lists and len(standings_lists) > 0:
                    drivers = standings_lists[0].get("DriverStandings", [])
                    return drivers
        except Exception as e:
            continue
    
    return []

def load_favorites():
    """Load saved favorites"""
    if os.path.exists("favorites.json"):
        try:
            with open("favorites.json", "r") as f:
                return json.load(f)
        except:
            pass
    return {"driver": None, "team": None}

def get_driver_profile(driver_id):
    """Fetch driver profile from cache or API"""
    try:
        # Try to load from local cache first
        json_path = "drivers_profiles.json"
        print(f"Looking for: {json_path}")  # DEBUG
        print(f"Driver ID: {driver_id}")    # DEBUG
        
        if os.path.exists(json_path):
            with open(json_path, "r") as f:
                profiles = json.load(f)
                print(f"Available profiles: {list(profiles.keys())}")  # DEBUG
                
                if driver_id.lower() in profiles:
                    return profiles[driver_id.lower()]
        
        # Fallback to API
        url = f"https://ergast.com/api/f1/drivers/{driver_id}.json"
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        data = response.json()
        
        if data.get("MRData", {}).get("DriverTable", {}).get("Drivers"):
            driver = data["MRData"]["DriverTable"]["Drivers"][0]
            return {
                "birth_date": driver.get("dateOfBirth", "N/A"),
                "nationality": driver.get("nationality", "N/A"),
                "height": driver.get("height", "N/A"),
                "code": driver.get("code", "N/A")
            }
        return None
    except Exception as e:
        print(f"Error: {e}")  # DEBUG
        return None



def display_driver_profile(standing):
    """Display detailed driver profile page"""
    
    col1, col2 = st.columns([1, 10])
    with col1:
        if st.button("🔙 BACK"):
            st.session_state.selected_driver = None
            st.rerun()
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # 1. Extract driver info
    position = standing.get("position", "-")
    driver = standing.get("Driver", {})
    given_name = driver.get("givenName", "")
    family_name = driver.get("familyName", "")
    driver_id = driver.get("driverId", "").lower().replace(" ", "_")
    driver_number = driver.get("permanentNumber", position) 
    
    constructor = standing.get("Constructors", [{}])[0]
    team_name = constructor.get("name", "Unknown")
    
    points = standing.get("points", "0")
    wins = standing.get("wins", "0")
    
    # 2. Get profile data and image
    profile = get_driver_profile(driver_id)
    bg_path = DRIVER_BG_MAP.get(driver_id)
    bg_base64 = get_img_as_base64(bg_path) if bg_path else ""

    # 3. Inject Glassmorphism CSS
    st.markdown(f"""
    <style>
        .stApp {{
            /* Changed to 'center top' and brightened the top gradient (0.3) so faces pop */
            background: linear-gradient(rgba(10, 12, 16, 0.3), rgba(10, 12, 16, 0.95)), url("{bg_base64}") no-repeat center top fixed !important;
            background-size: cover !important;
        }}
        .glass-panel {{
            background: rgba(22, 27, 34, 0.4);
            backdrop-filter: blur(16px);
            -webkit-backdrop-filter: blur(16px);
            border: 1px solid rgba(255, 255, 255, 0.08);
            border-radius: 20px;
            padding: 35px;
            box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.5);
            margin-bottom: 25px;
        }}
        .driver-header {{
            display: flex;
            align-items: center;
            gap: 25px;
            border-bottom: 1px solid rgba(255,255,255,0.1);
            padding-bottom: 25px;
            margin-bottom: 25px;
        }}
        .driver-num {{
            font-size: 90px;
            font-weight: 900;
            color: transparent;
            -webkit-text-stroke: 2px #E00400;
            line-height: 0.8;
            font-style: italic;
        }}
        .driver-name-block h1 {{
            font-size: 48px;
            font-weight: 900;
            margin: 0;
            color: #FFFFFF;
            line-height: 1.1;
            text-transform: uppercase;
            letter-spacing: 2px;
        }}
        .driver-name-block h3 {{
            font-size: 18px;
            color: #58A6FF;
            margin: 5px 0 0 0;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 3px;
        }}
        .stats-grid {{
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 20px;
        }}
        .stat-box {{
            background: rgba(0, 0, 0, 0.3);
            border-radius: 12px;
            padding: 20px;
            text-align: center;
            border: 1px solid rgba(255,255,255,0.03);
            transition: all 0.3s ease;
        }}
        .stat-box:hover {{
            transform: translateY(-5px);
            border-color: rgba(88, 166, 255, 0.4);
            background: rgba(0, 0, 0, 0.5);
        }}
        .stat-value {{ font-size: 42px; font-weight: 900; color: #FFFFFF; line-height: 1; }}
        .stat-label {{ font-size: 12px; color: #8B949E; text-transform: uppercase; letter-spacing: 1.5px; margin-top: 8px; }}
        .section-title {{
            color: #FFFFFF;
            font-size: 18px;
            letter-spacing: 2px;
            margin-bottom: 20px;
            border-bottom: 1px solid rgba(255,255,255,0.1);
            padding-bottom: 10px;
        }}
        .bio-text {{
            color: #C9D1D9;
            font-size: 16px;
            line-height: 1.8;
        }}
        .info-list {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 20px;
            margin-top: 30px;
        }}
        .info-item {{
            background: rgba(255,255,255,0.03);
            padding: 15px 20px;
            border-radius: 10px;
            border-left: 4px solid #58A6FF;
        }}
        .info-item .label {{ color: #8B949E; font-size: 11px; text-transform: uppercase; letter-spacing: 1px; display: block; margin-bottom: 4px;}}
        .info-item .val {{ color: #FFFFFF; font-size: 18px; font-weight: bold; }}
    </style>
    """, unsafe_allow_html=True)

    # 4. Handle missing profile data safely
    nationality = profile.get("nationality", "Unknown") if profile else "Unknown"
    height = profile.get("height", "Unknown") if profile else "Unknown"
    dob = profile.get("birth_date", "N/A") if profile else "N/A"
    bio = profile.get("bio", "No biography currently available for this driver.") if profile else "No biography currently available for this driver."

    # 5. Render HTML - ADDED margin-top: 40vh to push the UI down!
    html_content = f"""<div class="glass-panel" style="margin-top: 40vh;">
<div class="driver-header">
<div class="driver-num">{driver_number}</div>
<div class="driver-name-block">
<h1>{given_name} <span style="color: #58A6FF;">{family_name}</span></h1>
<h3>{team_name}</h3>
</div>
</div>
<div class="stats-grid">
<div class="stat-box">
<div class="stat-value" style="text-shadow: 0 0 15px rgba(88, 166, 255, 0.5);">{points}</div>
<div class="stat-label">Total Points</div>
</div>
<div class="stat-box">
<div class="stat-value" style="color: #3FB950; text-shadow: 0 0 15px rgba(63, 185, 80, 0.5);">{wins}</div>
<div class="stat-label">Season Wins</div>
</div>
<div class="stat-box">
<div class="stat-value" style="color: #FFA657; text-shadow: 0 0 15px rgba(255, 166, 87, 0.5);">P{position}</div>
<div class="stat-label">Championship</div>
</div>
<div class="stat-box">
<div class="stat-value" style="color: #C9184A; font-size: 28px; display: flex; align-items: center; justify-content: center; height: 42px;">{nationality}</div>
<div class="stat-label">Nationality</div>
</div>
</div>
</div>
<div class="glass-panel">
<div class="section-title">DRIVER BIOGRAPHY</div>
<div class="bio-text">{bio}</div>
<div class="info-list">
<div class="info-item">
<span class="label">Date of Birth</span>
<span class="val">{dob}</span>
</div>
<div class="info-item">
<span class="label">Height</span>
<span class="val">{height}</span>
</div>
</div>
</div>"""
    
    st.markdown(html_content, unsafe_allow_html=True)


# -----------------------------
# MAIN APP
# -----------------------------
def main():
    # Header
    st.markdown('<div class="main-title"> DRIVER CHAMPIONSHIP</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle">2026 Formula 1 World Championship Standings</div>', unsafe_allow_html=True)
    
    # Load favorites
    favorites = load_favorites()
    favorite_driver = favorites.get("driver", None)
    
    # Info banner
    if favorite_driver:
        info_html = f"""
<div class="info-banner">
    <div class="info-icon">⭐</div>
    <div class="info-text">
        Your favorite driver <strong>{favorite_driver}</strong> is highlighted below!
    </div>
</div>
"""
        st.markdown(info_html, unsafe_allow_html=True)
    
    # Fetch standings
    standings = get_driver_standings()
    
    if not standings:
        st.error("⚠️ Unable to fetch driver standings. Please try again later.")
        return
    
    # Podium Display (Top 3)
    if len(standings) >= 3:
        st.markdown("### 🏅 CHAMPIONSHIP PODIUM")
        
        top_3 = standings[:3]
        
        podium_html = '<div class="podium-container">'
        
        for i, standing in enumerate(top_3):
            driver = standing.get("Driver", {})
            given_name = driver.get("givenName", "")
            family_name = driver.get("familyName", "")
            full_name = f"{given_name} {family_name}"
            points = standing.get("points", "0")
            
            position_class = ["podium-first", "podium-second", "podium-third"][i]
            position_num = i + 1
            
            podium_html += f"""
<div class="podium-position {position_class}">
    <div class="podium-driver-info">
        <div class="podium-driver-name">{full_name}</div>
        <div class="podium-points">{points} PTS</div>
    </div>
    <div class="podium-stand">
        <div class="position-number">{position_num}</div>
    </div>
</div>
"""
        
        podium_html += '</div>'
        st.markdown(podium_html, unsafe_allow_html=True)
        # Full Standings
def display_driver_standings():
    """Display driver standings with clickable profiles"""
    
    # Header
    st.markdown('<div class="main-title"> DRIVER CHAMPIONSHIP</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle">2026 Formula 1 World Championship Standings</div>', unsafe_allow_html=True)
    
    # Load favorites
    favorites = load_favorites()
    favorite_driver = favorites.get("driver", None)
    
    # Info banner
    if favorite_driver:
        st.markdown(f"""
        <div class="info-banner">
            <div class="info-icon"></div>
            <div class="info-text">
                Your favorite driver <strong>{favorite_driver}</strong> is highlighted below!
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Fetch standings
    standings = get_driver_standings()
    
    if not standings:
        st.error("⚠️ Unable to fetch driver standings. Please try again later.")
        return
    
    # Podium Display (Top 3)
    if len(standings) >= 3:
        st.markdown("### 🏅 CHAMPIONSHIP PODIUM")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            driver = standings[1].get("Driver", {})
            full_name = f"{driver.get('givenName', '')} {driver.get('familyName', '')}"
            if st.button(f"🥈 {full_name}\n{standings[1].get('points', '0')} PTS", key="podium-2", use_container_width=True):
                st.session_state.selected_driver = standings[1]
                st.rerun()
        
        with col2:
            driver = standings[0].get("Driver", {})
            full_name = f"{driver.get('givenName', '')} {driver.get('familyName', '')}"
            if st.button(f"🥇 {full_name}\n{standings[0].get('points', '0')} PTS", key="podium-1", use_container_width=True):
                st.session_state.selected_driver = standings[0]
                st.rerun()
        
        with col3:
            driver = standings[2].get("Driver", {})
            full_name = f"{driver.get('givenName', '')} {driver.get('familyName', '')}"
            if st.button(f"🥉 {full_name}\n{standings[2].get('points', '0')} PTS", key="podium-3", use_container_width=True):
                st.session_state.selected_driver = standings[2]
                st.rerun()
    
    # Full Standings
    st.markdown("---")
    st.markdown("### 📊 FULL STANDINGS")
    
    max_points = float(standings[0].get("points", 1)) if standings else 1
    
    for idx, standing in enumerate(standings):
        position = standing.get("position", "-")
        driver = standing.get("Driver", {})
        given_name = driver.get("givenName", "")
        family_name = driver.get("familyName", "")
        full_name = f"{given_name} {family_name}"
        
        constructor = standing.get("Constructors", [{}])[0]
        team_name = constructor.get("name", "Unknown")
        
        points = standing.get("points", "0")
        wins = standing.get("wins", "0")
        
        # Check if favorite
        is_favorite = (favorite_driver and favorite_driver in full_name)
        favorite_class = "favorite-driver" if is_favorite else ""
        position_class = f"position-{position}" if str(position).isdigit() and int(position) <= 3 else ""
        
        # Calculate bar width
        bar_width = (float(points) / max_points) * 100
        favorite_badge = '<span class="favorite-badge">⭐ FAVORITE</span>' if is_favorite else ''
        
        # Clickable driver row
        if st.button(f"{full_name}", key=f"driver-{idx}", use_container_width=True):
            st.session_state.selected_driver = standing
            st.rerun()
        
        # HTML rendering
        driver_html = f"""
        <div class="driver-row {favorite_class} {position_class}">
            <div class="driver-position">{position}</div>
            <div class="driver-name">
                <div class="driver-full-name">{full_name} {favorite_badge}</div>
                <div class="driver-team">{team_name}</div>
                <div class="points-bar" style="width: {bar_width}%;"></div>
            </div>
            <div class="driver-stats">
                <div class="stat-item">
                    <div class="stat-label">Points</div>
                    <div class="stat-value">{points}</div>
                </div>
                <div class="stat-item">
                    <div class="stat-label">Wins</div>
                    <div class="stat-value">{wins}</div>
                </div>
            </div>
        </div>
        """
        st.markdown(driver_html, unsafe_allow_html=True)

# MAIN LOGIC
def main():
    if st.session_state.selected_driver is not None:
        display_driver_profile(st.session_state.selected_driver)
    else:
        display_driver_standings()

if __name__ == "__main__":
    main()