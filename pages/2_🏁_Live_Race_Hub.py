import streamlit as st
import requests
from datetime import datetime, timedelta
import pytz
import time
import base64
import os
from streamlit_autorefresh import st_autorefresh
# -----------------------------
# IMAGE HELPER FUNCTION
# -----------------------------
def get_img_as_base64(file_path):
    """Reads a local image and converts it to base64 for CSS."""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    absolute_path = os.path.join(script_dir, file_path)
    
    if not os.path.exists(absolute_path):
        return None
    
    with open(absolute_path, "rb") as f:
        data = f.read()
    
    encoded = base64.b64encode(data).decode()
    ext = absolute_path.split('.')[-1]
    return f"data:image/{ext};base64,{encoded}"
# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(
    page_title="🏁 F1 Live Race Hub",
    page_icon="🏎️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# -----------------------------
# CUSTOM CSS - SKY SPORTS F1 STYLE
# -----------------------------

# 1. Grab the background image
bg_base64 = get_img_as_base64("images/f1_logo.webp")

# Determine which background to use
if bg_base64:
    app_bg = f'background: linear-gradient(rgba(10, 12, 16, 0.4), rgba(10, 12, 16, 0.7)), url("{bg_base64}") no-repeat center center fixed !important; background-size: cover !important;'
else:
    app_bg = 'background: linear-gradient(180deg, #0D1117 0%, #161B22 50%, #0D1117 100%);'

# 2. Inject Dynamic Background (Using f-string just for this small part)
st.markdown(f"""
<style>
    .stApp {{
        {app_bg}
        color: #E6EDF3;
    }}
    background-size: cover !important;
</style>
""", unsafe_allow_html=True)

# 3. Inject Static CSS (Normal string - no f-string, so CSS brackets won't crash Python!)
st.markdown("""
<style>
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;} 
    header {visibility: hidden;}
    
    /* Main Title - Elegant Gradient */
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

    /* Countdown Banner - Sophisticated Red-Blue Gradient */
    .countdown-banner {
        background: linear-gradient(135deg, #1F6FEB 0%, #8B2B8B 50%, #C9184A 100%);
        padding: 45px;
        border-radius: 20px;
        text-align: center;
        margin-bottom: 40px;
        box-shadow: 0 20px 60px rgba(31, 111, 235, 0.3),
                    inset 0 1px 0 rgba(255, 255, 255, 0.1);
        border: 1px solid rgba(88, 166, 255, 0.2);
        position: relative;
        overflow: hidden;
    }

    .countdown-banner::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(circle, rgba(255,255,255,0.1) 0%, transparent 70%);
        animation: rotate 8s linear infinite;
    }

    @keyframes rotate {
        from { transform: rotate(0deg); }
        to { transform: rotate(360deg); }
    }

    .countdown-title {
        font-size: 19px;
        color: #58A6FF;
        text-transform: uppercase;
        letter-spacing: 3px;
        margin-bottom: 15px;
        font-weight: 700;
        position: relative;
        z-index: 1;
        text-shadow: 0 2px 10px rgba(0, 0, 0, 0.5);
    }

    .countdown-timer {
        font-size: 68px;
        font-weight: 900;
        color: #FFFFFF;
        font-family: 'Courier New', monospace;
        text-shadow: 0 0 40px rgba(255, 255, 255, 0.6),
                     0 5px 15px rgba(0, 0, 0, 0.8);
        position: relative;
        z-index: 1;
        letter-spacing: 8px;
    }

    /* Status Indicators - Modern Colors */
    .status-live {
        background: linear-gradient(135deg, #3FB950 0%, #2EA043 100%);
        color: #FFFFFF;
        padding: 18px 35px;
        border-radius: 12px;
        font-weight: 900;
        font-size: 22px;
        text-align: center;
        animation: livePulse 2s infinite;
        box-shadow: 0 10px 30px rgba(63, 185, 80, 0.4);
        border: 2px solid rgba(63, 185, 80, 0.5);
    }

    @keyframes livePulse {
        0%, 100% { 
            box-shadow: 0 10px 30px rgba(63, 185, 80, 0.4);
            transform: scale(1);
        }
        50% { 
            box-shadow: 0 15px 45px rgba(63, 185, 80, 0.6);
            transform: scale(1.02);
        }
    }

    .status-no-race {
        background: linear-gradient(135deg, #C9184A 0%, #8B1538 100%);
        color: #FFFFFF;
        padding: 18px 35px;
        border-radius: 12px;
        font-weight: 900;
        font-size: 22px;
        text-align: center;
        box-shadow: 0 10px 30px rgba(201, 24, 74, 0.3);
        border: 2px solid rgba(255, 107, 107, 0.3);
    }

    .status-weekend {
        background: linear-gradient(135deg, #FFA657 0%, #D29922 100%);
        color: #0D1117;
        padding: 18px 35px;
        border-radius: 12px;
        font-weight: 900;
        font-size: 22px;
        text-align: center;
        box-shadow: 0 10px 30px rgba(255, 166, 87, 0.4);
        border: 2px solid rgba(255, 166, 87, 0.5);
    }

    /* Info Cards - Premium Look */
    .info-card {
        background: linear-gradient(145deg, #161B22 0%, #0D1117 100%);
        border: 1px solid #30363D;
        border-radius: 18px;
        padding: 30px;
        margin-bottom: 25px;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.4);
        position: relative;
        overflow: hidden;
    }

    .info-card::after {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 2px;
        background: linear-gradient(90deg, 
            transparent 0%, 
            #58A6FF 50%, 
            transparent 100%);
        opacity: 0;
        transition: opacity 0.3s ease;
    }

    .info-card:hover {
        border-color: #58A6FF;
        box-shadow: 0 12px 48px rgba(88, 166, 255, 0.2);
        transform: translateY(-4px);
    }

    .info-card:hover::after {
        opacity: 1;
    }

    .card-title {
        font-size: 26px;
        font-weight: 900;
        background: linear-gradient(135deg, #58A6FF 0%, #FF6B6B 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-transform: uppercase;
        letter-spacing: 3px;
        margin-bottom: 25px;
        padding-bottom: 15px;
        position: relative;
    }

    .card-title::after {
        content: '';
        position: absolute;
        bottom: 0;
        left: 0;
        width: 80px;
        height: 3px;
        background: linear-gradient(90deg, #58A6FF 0%, #FF6B6B 100%);
        border-radius: 2px;
    }

    /* Info Rows - Refined */
    .info-row {
        display: flex;
        justify-content: space-between;
        padding: 14px 0;
        border-bottom: 1px solid rgba(48, 54, 61, 0.5);
        transition: all 0.3s ease;
    }

    .info-row:hover {
        padding-left: 12px;
        border-bottom-color: rgba(88, 166, 255, 0.3);
        background: rgba(88, 166, 255, 0.03);
        border-radius: 8px;
    }

    .info-row:last-child {
        border-bottom: none;
    }

    .info-label {
        color: #8B949E;
        font-size: 14px;
        text-transform: uppercase;
        letter-spacing: 1.5px;
        font-weight: 600;
    }

    .info-value {
        color: #E6EDF3;
        font-weight: 700;
        font-size: 16px;
    }

    /* Constructor Standings - Modern Design */
    .standings-row {
        display: flex;
        align-items: center;
        padding: 18px 20px;
        margin-bottom: 12px;
        background: linear-gradient(135deg, #161B22 0%, #0D1117 100%);
        border-radius: 14px;
        border-left: 4px solid #58A6FF;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.3);
        position: relative;
    }

    .standings-row::before {
        content: '';
        position: absolute;
        left: 0;
        top: 0;
        bottom: 0;
        width: 0;
        background: linear-gradient(90deg, rgba(88, 166, 255, 0.1), transparent);
        transition: width 0.4s ease;
        border-radius: 14px 0 0 14px;
    }

    .standings-row:hover::before {
        width: 100%;
    }

    .standings-row:hover {
        background: linear-gradient(135deg, #1C2128 0%, #161B22 100%);
        transform: translateX(8px);
        box-shadow: 0 8px 24px rgba(88, 166, 255, 0.2);
        border-left-color: #FF6B6B;
    }

    .standings-position {
        font-size: 26px;
        font-weight: 900;
        color: #58A6FF;
        width: 55px;
        text-shadow: 0 2px 8px rgba(88, 166, 255, 0.4);
        position: relative;
        z-index: 1;
    }

    .standings-team {
        flex-grow: 1;
        font-size: 19px;
        font-weight: 700;
        color: #E6EDF3;
        letter-spacing: 0.5px;
        position: relative;
        z-index: 1;
    }

    .standings-points {
        font-size: 26px;
        font-weight: 900;
        color: #FFA657;
        font-family: 'Courier New', monospace;
        text-shadow: 0 2px 8px rgba(255, 166, 87, 0.4);
        margin-right: 12px;
        position: relative;
        z-index: 1;
    }

    .points-bar {
        height: 6px;
        background: linear-gradient(90deg, #58A6FF 0%, #FF6B6B 100%);
        border-radius: 3px;
        margin-top: 10px;
        transition: all 0.8s cubic-bezier(0.4, 0, 0.2, 1);
        box-shadow: 0 2px 12px rgba(88, 166, 255, 0.4);
    }

    /* Ferrari Highlight - Special Treatment */
    .ferrari-highlight {
        background: linear-gradient(135deg, #8B1538 0%, #C9184A 50%, #8B1538 100%) !important;
        border-left-color: #FFA657 !important;
        box-shadow: 0 8px 32px rgba(201, 24, 74, 0.4) !important;
    }

    .ferrari-highlight .standings-team {
        color: #FFA657 !important;
        text-shadow: 0 0 20px rgba(255, 166, 87, 0.6);
    }

    .ferrari-highlight .standings-position {
        color: #FFA657 !important;
        text-shadow: 0 0 20px rgba(255, 166, 87, 0.6);
    }

    .ferrari-highlight .points-bar {
        background: linear-gradient(90deg, #FFA657 0%, #FFD700 100%) !important;
        box-shadow: 0 2px 16px rgba(255, 166, 87, 0.6) !important;
    }

    /* Scrollbar - Modern Blue */
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
@st.cache_data(ttl=300)  # Cache for 5 minutes
def get_next_race():
    """Fetch next race information from Ergast API"""
    url = "https://api.jolpi.ca/ergast/f1/current/next.json"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        races = data.get("MRData", {}).get("RaceTable", {}).get("Races", [])
        
        if not races:
            return None
        
        race = races[0]
        return {
            "name": race.get("raceName", "Unknown"),
            "date": race.get("date", "-"),
            "time": race.get("time", "00:00:00Z"),
            "circuit": race.get("Circuit", {}).get("circuitName", "Unknown"),
            "location": race.get("Circuit", {}).get("Location", {}),
            "round": race.get("round", "1")
        }
    except Exception as e:
        st.error(f"Error fetching race data: {e}")
        return None

@st.cache_data(ttl=300)
def get_constructor_standings():
    """Fetch current constructor standings"""
    
    # Try multiple API endpoints
  # Try multiple API endpoints
    urls = [
        # 1. PRIMARY: Jolpi API for the LIVE current season (This will pull 2026 data soon!)
        "https://api.jolpi.ca/ergast/f1/current/constructorStandings.json", 
        
        # 2. BACKUP: The old Ergast API
        "http://ergast.com/api/f1/current/constructorStandings.json",
        
        # 3. LAST RESORT: 2025 data fallback (Upgraded from 2024!)
        "https://api.jolpi.ca/ergast/f1/2025/constructorStandings.json"
    ]
    
    for url in urls:
        try:
            print(f"🔍 Trying: {url}")
            response = requests.get(url, timeout=10)
            print(f"📊 Status Code: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                
                # Debug: Print raw structure
                print(f"📦 Data Keys: {data.keys()}")
                
                standings_table = data.get("MRData", {}).get("StandingsTable", {})
                standings_lists = standings_table.get("StandingsLists", [])
                
                print(f"📋 Found {len(standings_lists)} standings lists")
                
                if standings_lists and len(standings_lists) > 0:
                    constructors = standings_lists[0].get("ConstructorStandings", [])
                    print(f"✅ SUCCESS! Found {len(constructors)} teams")
                    return constructors
                    
        except Exception as e:
            print(f"❌ Error with {url}: {e}")
            continue
    
    print("⚠️ All API attempts failed - returning empty list")
    return []




# -----------------------------
# HELPER FUNCTIONS
# -----------------------------
def get_race_status(race_datetime_utc):
    """Determine if race is live, upcoming, or race weekend"""
    now = datetime.now(pytz.UTC)
    race_end = race_datetime_utc + timedelta(hours=2)
    race_weekend_start = race_datetime_utc - timedelta(days=2)
    
    if race_datetime_utc <= now <= race_end:
        return "LIVE"
    elif race_weekend_start <= now < race_datetime_utc:
        return "RACE_WEEKEND"
    else:
        return "NO_RACE"

def calculate_countdown(target_datetime):
    """Calculate time remaining until race"""
    now = datetime.now(pytz.timezone("Asia/Kuala_Lumpur"))
    delta = target_datetime - now
    
    if delta.total_seconds() <= 0:
        return "00d 00h 00m"
    
    days = delta.days
    hours, remainder = divmod(delta.seconds, 3600)
    minutes, _ = divmod(remainder, 60)
    
    return f"{days:02d}d {hours:02d}h {minutes:02d}m"

# -----------------------------
# MAIN APP
# -----------------------------

def main():
    # Header
    st_autorefresh(interval=60000, key="f1_live_refresh")
    st.markdown('<div class="main-title">🏎️ F1 LIVE RACE HUB</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle">Real-time race tracking & constructor standings</div>', unsafe_allow_html=True)
    
    # Fetch data
    race_data = get_next_race()
    standings_data = get_constructor_standings()
    
    if not race_data:
        st.error("⚠️ Unable to fetch race information. Please try again later.")
        return
    
    # Parse race datetime
    utc = pytz.UTC
    local_tz = pytz.timezone("Asia/Kuala_Lumpur")
    uk_tz = pytz.timezone("Europe/London")
    race_datetime_utc = utc.localize(
        datetime.strptime(f"{race_data['date']} {race_data['time']}", "%Y-%m-%d %H:%M:%SZ")
    )
    race_datetime_local = race_datetime_utc.astimezone(local_tz)
    race_datetime_uk = race_datetime_utc.astimezone(uk_tz)
    
    # Determine race status
    race_status = get_race_status(race_datetime_utc)
    
    # Countdown Banner
# Determine race status
    race_status = get_race_status(race_datetime_utc)
    countdown = calculate_countdown(race_datetime_local)
    
    # Build the HTML block conditionally
    if race_status == "LIVE":
        status_html = '<div class="status-live">🏁 RACE IS LIVE RIGHT NOW!</div>'
        title = race_data["name"]
        timer_html = ""
    elif race_status == "RACE_WEEKEND":
        status_html = '<div class="status-weekend">🟡 RACE WEEKEND IN PROGRESS</div>'
        title = "LIGHTS OUT IN"
        timer_html = f'<div class="countdown-timer">{countdown}</div>'
    else:
        status_html = '<div class="status-no-race">🔴 NO RACE CURRENTLY HAPPENING</div>'
        title = "NEXT RACE IN"
        timer_html = f'<div class="countdown-timer">{countdown}</div>'

    # Single markdown injection
    st.markdown(f"""
    <div class="countdown-banner">
        {status_html}
        <div style="margin-top: 20px;">
            <div class="countdown-title">{title}</div>
            {timer_html}
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Two-column layout
    col1, col2 = st.columns([1, 1])
    
    # LEFT COLUMN - Race Information
    with col1:
        st.markdown('<div class="info-card">', unsafe_allow_html=True)
        st.markdown('<div class="card-title">📍 RACE INFORMATION</div>', unsafe_allow_html=True)
        
        st.markdown(f'''
        <div class="info-row">
            <span class="info-label">🏁 Race</span>
            <span class="info-value">{race_data["name"]}</span>
        </div>
        <div class="info-row">
            <span class="info-label">🏟️ Circuit</span>
            <span class="info-value">{race_data["circuit"]}</span>
        </div>
        <div class="info-row">
            <span class="info-label">🌍 Location</span>
            <span class="info-value">{race_data["location"].get("locality", "Unknown")}, {race_data["location"].get("country", "Unknown")}</span>
        </div>
        <div class="info-row">
            <span class="info-label">📅 Date</span>
            <span class="info-value">{race_datetime_local.strftime("%A, %d %B %Y")}</span>
        </div>
        <div class="info-row">
            <span class="info-label">⏰ Time (MYT)</span>
            <span class="info-value">{race_datetime_local.strftime("%I:%M %p")}</span>
        </div>
         <div class="info-row">
            <span class="info-label">GB Time (UK)</span>
            <span class="info-value">{race_datetime_uk.strftime("%I:%M %p %Z")}</span>
        </div>
        <div class="info-row">
            <span class="info-label">🔢 Round</span>
            <span class="info-value">Round {race_data["round"]}</span>
        </div>
        ''', unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # RIGHT COLUMN - Constructor Standings
    with col2:
        st.markdown('<div class="info-card">', unsafe_allow_html=True)
        st.markdown('<div class="card-title">🏆 CONSTRUCTOR STANDINGS</div>', unsafe_allow_html=True)
        
        if standings_data:
            max_points = float(standings_data[0].get("points", 1))
            
            for i, standing in enumerate(standings_data):  
                position = str(i + 1)  # Forces perfect numbering 1, 2, 3... 11
                constructor = standing.get("Constructor", {})
                team_name = constructor.get("name", "Unknown")
                points = standing.get("points", "0")
                
                # Highlight Ferrari
                is_ferrari = "Ferrari" in team_name
                row_class = "ferrari-highlight" if is_ferrari else ""
                
                # Calculate bar width
                bar_width = (float(points) / max_points) * 100
                
                st.markdown(f'''
                <div class="standings-row {row_class}">
                    <div class="standings-position">{position}</div>
                    <div style="flex-grow: 1;">
                        <div class="standings-team">{team_name}</div>
                        <div class="points-bar" style="width: {bar_width}%;"></div>
                    </div>
                    <div class="standings-points">{points}</div>
                </div>
                ''', unsafe_allow_html=True)
        else:
            st.warning("No standings data available")
        st.markdown('</div>', unsafe_allow_html=True)
  

if __name__ == "__main__":
    main()
