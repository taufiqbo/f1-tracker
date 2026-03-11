import streamlit as st

# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(
    page_title="📖 F1 Technical Guide",
    page_icon="🏎️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -----------------------------
# CUSTOM CSS
# -----------------------------
st.markdown("""
<style>
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
        margin-bottom: 5px;
    }
    .subtitle {
        text-align: center;
        color: #8B949E;
        font-size: 17px;
        margin-bottom: 40px;
        font-weight: 400;
        letter-spacing: 2px;
    }
    
    /* Tab Styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 24px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        white-space: pre-wrap;
        background-color: transparent;
        border-radius: 4px 4px 0px 0px;
        gap: 1px;
        padding-top: 10px;
        padding-bottom: 10px;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown('<div class="main-title">🏎️ THE F1 TECHNICAL PRIMER</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">VIP Access: Engineering, Strategy, and the Rulebook</div>', unsafe_allow_html=True)

# -----------------------------
# INTERACTIVE TABS (Now with 4 tabs!)
# -----------------------------
tab1, tab2, tab3, tab4 = st.tabs(["⚙️ The 2026 Machinery", "🚩 The Language of the Track", "🏎️ Rules of Engagement", "🛞 Tires & Pit Strategy"])

# TAB 1: MACHINERY
with tab1:
    st.header("The 'Agile Hybrid' Era")
    st.markdown("""
    In 2026, the FIA (Formula 1's governing body) introduced the biggest regulation overhaul in the sport's history to make the cars lighter, safer, and more competitive. Formula 1 isn't just about driving fast; it is a high-speed chess match governed by strict physics and complex engineering.

    * **The 50/50 Power Unit:** The cars are powered by a highly complex hybrid system. For 2026, the power output is split evenly: 50% comes from a traditional Internal Combustion Engine (ICE) and 50% comes from massive electrical batteries. The electrical power has been tripled (from 120kW to 350kW). Plus, they now run on 100% sustainable fuels.
    * **Smaller & Nimbler:** To improve overtaking on tight tracks, the 2026 cars have been put on a diet. The wheelbase is 200mm shorter, the cars are 100mm narrower, and the minimum weight has dropped to 768kg.
    * **Active Aerodynamics (The Game Changer):** The old Drag Reduction System (DRS) is dead. Now, all cars feature "Active Aero" where both the front and rear wings physically change shape during the lap.
        * **Z-Mode (Cornering):** The wing flaps stay closed, pushing the car into the ground to provide maximum grip and downforce.
        * **X-Mode (Straights):** The wing flaps flatten out to completely shed drag, giving the car a massive top-speed boost on the straights.
    * **Manual Override (Push-to-Pass):** Instead of DRS, drivers now get a tactical "Overtake Mode". If a driver is within one second of the car ahead, they are granted a short, manual burst of extra battery power to attempt a pass.
    """)

# TAB 2: FLAGS
with tab2:
    st.header("Race Control Flag System")
    st.markdown("""
    Because the cars are too loud and fast for normal communication, race control uses a strict flag system to issue immediate orders to the drivers. Ignoring these is a guaranteed penalty.

    * 🟢 **Green Flag:** The track is clear. Racing conditions are normal.
    * 🟡 **Yellow Flag (Single):** Hazard ahead (like debris or a spun car). Drivers must reduce speed and overtaking is strictly prohibited.
    * 🟡🟡 **Yellow Flag (Double):** Severe hazard, often meaning marshals are physically working on the track. Drivers must slow down significantly and be prepared to come to a complete stop.
    * 🔴 **Red Flag:** The session is immediately suspended due to a severe crash or extreme weather (like a flooded track). All cars must safely return to the pit lane.
    * 🔵 **Blue Flag:** During the race, this is shown to a slow driver at the back of the pack who is about to be "lapped" by the race leaders. The slow driver must yield the racing line and let the faster car pass immediately.
    * 🏁 **Black & White Diagonal Flag:** The F1 equivalent of a soccer "Yellow Card." It is a final warning issued to a specific driver for unsportsmanlike behavior or breaking track limits.
    * 🟠 **Black & Orange Circle (The "Meatball" Flag):** A specific car has sustained mechanical damage that is too dangerous to keep driving (e.g., a broken front wing dragging on the floor). That driver must return to the pits immediately for repairs.
    * 🏴 **Black Flag:** Immediate disqualification. The driver has committed a severe rule breach, their race is over, and they must return to the garage.
    """)

# TAB 3: RULES
with tab3:
    st.header("Track Limits & Overtaking")
    st.markdown("""
    F1 is non-contact. You cannot just bump people out of the way. There are strict geometries to how a driver is allowed to race.

    * **Track Limits:** The race track is defined by the solid white lines painted on the edges. At least *one* part of the car's tire must remain in contact with the white line at all times. If all four wheels cross entirely over the white line, it is an illegal advantage. During the race, a driver gets three "strikes" for exceeding track limits. On the fourth strike, they are hit with a 5-second time penalty.
    * **Defending a Position:** If a driver is defending against an attacker on a straight, they are only allowed to make *one* defensive steering move. "Weaving" back and forth to block the car behind is highly illegal. Furthermore, moving under braking (changing direction after you have slammed on the brakes for a corner) is strictly prohibited as it causes catastrophic crashes.
    * **The Apex Rule (Who owns the corner?):** When two cars dive into a corner side-by-side, the stewards look at the "apex" (the innermost geometric point of the turn).
        * If the attacking car is on the *inside*, their front wheels must be at least level with the defending car's side mirrors to be legally entitled to space.
        * If the attacking car is trying the much harder pass on the *outside*, their front wheels must be completely ahead of the defending car's front wheels.
        * Divebombing (braking dangerously late just to force the other car off the road) is penalized.
    """)

# TAB 4: TIRES & STRATEGY
with tab4:
    st.header("The Chess Match: Tires & Pit Strategy")
    st.markdown("""
    Formula 1 cars do not refuel during a race. The only reason they stop in the pit lane is to change tires. Because tires physically melt and degrade as they are driven to their absolute limit, managing them is the most important strategic element of the race.

    ### The Pirelli Compounds
    F1 uses "slick" tires (completely smooth with no treads) to maximize the surface area touching the track. Pirelli brings three compounds to every dry race:
    * 🔴 **Soft (Red):** The fastest tire. It provides massive, instant grip, but it degrades ("falls off a cliff") very quickly. Used mostly for Qualifying or late-race sprints.
    * 🟡 **Medium (Yellow):** The balanced tire. A perfect mix of speed and durability, often used as the primary race tire.
    * ⚪ **Hard (White):** The slowest tire, but the most durable. Used for doing very long stints on the track to avoid making extra pit stops.
    * 🟢 **Intermediates (Green) / 🔵 Wets (Blue):** These are the only tires with treads. Used only when it rains to displace standing water and prevent hydroplaning.

    ### The Golden Rule
    In a dry race, **every driver is legally required to make at least one pit stop and use at least TWO different tire compounds.** (For example: starting on Mediums and switching to Hards). If it rains and they use Green or Blue tires, this rule is instantly canceled.

    ### Strategy 101: The Undercut
    Imagine Car A is stuck closely behind Car B, but cannot physically overtake them on the track because the dirty air is too turbulent. 
    * **The Move:** Car A dives into the pits *first* to get fresh, fast tires. Car B stays out on their old, slow tires.
    * **The Trap:** When Car A comes out of the pits, they drive the fastest lap of their life on the fresh rubber. By the time Car B pits on the very next lap, Car A is going so fast that they fly right past Car B while Car B is exiting the pit lane. Car A has successfully "undercut" their rival.
    
    ### Strategy 101: The Overcut
    The exact opposite. Car A stays out longer on older tires, banking on the fact that they have "saved" their rubber better than Car B. When Car B pits early, they might get stuck in traffic behind slower cars. Car A uses "clean air" to build a massive time gap, pitting later and coming out safely ahead of Car B.
    """)