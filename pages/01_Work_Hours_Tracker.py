import streamlit as st
from datetime import datetime, date, time, timedelta
import plotly.graph_objects as go
import json
import os

# Page Config
st.set_page_config(page_title="Work Hours Tracker", page_icon="⏰", layout="centered")

# --- Persistence Logic ---
CONFIG_FILE = "tracker_config.json"

def load_config():
    """Load settings from a local JSON file."""
    default_config = {
        "in_time": "10:00",
        "tea_break": 0,
        "lunch_break": 17,
        "planned_exit": "19:00"
    }
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, 'r') as f:
                return {**default_config, **json.load(f)}
        except:
            return default_config
    return default_config

def save_config():
    """Save current session state to local JSON file."""
    config = {
        "in_time": st.session_state.in_time.strftime("%H:%M"),
        "tea_break": st.session_state.tea_break,
        "lunch_break": st.session_state.lunch_break,
        "planned_exit": st.session_state.planned_exit.strftime("%H:%M") if 'planned_exit' in st.session_state else "19:00"
    }
    with open(CONFIG_FILE, 'w') as f:
        json.dump(config, f)

# Load initial config
config = load_config()

# Convert string times back to time objects
try:
    init_in_time = datetime.strptime(config["in_time"], "%H:%M").time()
    init_exit_time = datetime.strptime(config["planned_exit"], "%H:%M").time()
except:
    init_in_time = time(10, 0)
    init_exit_time = time(19, 0)

# --- Custom Styling ---
st.markdown("""
    <style>
    .main { padding-top: 1rem; }
    .stTimeInput > label { font-size: 1.1rem; font-weight: bold; }
    div[data-testid="metric-container"] {
        background-color: #f0f2f6;
        padding: 10px;
        border-radius: 5px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
    }
    .date-subtext {
        font-size: 0.9rem;
        color: #555;
        margin-top: -10px;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("Work Hours Tracker")

# --- Inputs Section (Outside Fragment to allow interaction) ---
col1, col2 = st.columns(2)

with col1:
    st.subheader("Time Logs")
    
    in_time = st.time_input(
        "Office In Time", 
        value=init_in_time, 
        step=60, 
        key="in_time", 
        on_change=save_config
    )
    
    planned_exit_time = st.time_input(
        "Planned Exit Time", 
        value=init_exit_time, 
        step=60, 
        key="planned_exit",
        help="Used for projection calculations",
        on_change=save_config
    )

with col2:
    st.subheader("Breaks")
    
    tea_break_mins = st.slider(
        "Tea Break Duration", 
        min_value=0, max_value=90, 
        value=config["tea_break"], 
        format="%d min",
        key="tea_break",
        on_change=save_config
    )

    lunch_break_mins = st.slider(
        "Lunch Break Duration", 
        min_value=0, max_value=90, 
        value=config["lunch_break"], 
        format="%d min",
        key="lunch_break",
        on_change=save_config
    )

st.divider()

# --- Real-Time Fragment ---
# This decorator ensures only this function reruns every 1 second
@st.fragment(run_every=1)
def update_live_status():
    
    # --- 1. Header (Time & Date) ---
    now = datetime.now()
    
    # Create a nice header layout
    h_col1, h_col2 = st.columns([2, 1])
    
    with h_col1:
        st.write("Live Status Monitor")
    
    with h_col2:
        # Display Time (12hr format with seconds)
        time_str = now.strftime("%I:%M:%S %p")
        # Display Date (Day, DD Month YYYY)
        date_str = now.strftime("%A, %d %B %Y")
        
        st.metric(label="Current Time", value=time_str)
        st.caption(date_str)

    # --- 2. Calculations ---
    today = date.today()
    dt_in = datetime.combine(today, in_time)
    
    # Handle overnight logic if needed (simplified for same-day)
    if now < dt_in:
        gross_duration_seconds = 0
    else:
        gross_duration_seconds = (now - dt_in).total_seconds()

    gross_minutes = gross_duration_seconds / 60
    total_break_minutes = tea_break_mins + lunch_break_mins
    net_work_minutes = max(0, gross_minutes - total_break_minutes)
    net_work_hours = net_work_minutes / 60

    TARGET_HOURS = 8.0
    remaining_hours = TARGET_HOURS - net_work_hours
    
    # Calculate Target Exit DT
    target_exit_dt = dt_in + timedelta(minutes=total_break_minutes) + timedelta(hours=TARGET_HOURS)

    # --- 3. Visualization ---
    vis_col, stat_col = st.columns([1.5, 1])

    # Helper format
    def float_to_hm(hours_float):
        is_negative = hours_float < 0
        hours_float = abs(hours_float)
        h = int(hours_float)
        m = int((hours_float - h) * 60)
        s = int(((hours_float - h) * 60 - m) * 60)
        sign = "-" if is_negative else ""
        return f"{sign}{h}hr {m}min"

    with vis_col:
        fig = go.Figure(go.Indicator(
            mode = "gauge+number+delta",
            value = net_work_hours,
            domain = {'x': [0, 1], 'y': [0, 1]},
            title = {'text': "Live Net Hours", 'font': {'size': 20}},
            delta = {'reference': TARGET_HOURS, 'increasing': {'color': "green"}, 'decreasing': {'color': "red"}, 'suffix': " hr"},
            gauge = {
                'axis': {'range': [None, 12], 'tickwidth': 1, 'tickcolor': "darkblue"},
                'bar': {'color': "#2E86C1"},
                'bgcolor': "white",
                'borderwidth': 2,
                'bordercolor': "gray",
                'steps': [
                    {'range': [0, 6], 'color': '#EBDEF0'},
                    {'range': [6, 8], 'color': '#D4E6F1'},
                    {'range': [8, 12], 'color': '#D5F5E3'}
                ],
                'threshold': {
                    'line': {'color': "red", 'width': 4},
                    'thickness': 0.75,
                    'value': TARGET_HOURS
                }
            }
        ))
        fig.update_layout(height=300, margin=dict(l=20, r=20, t=30, b=20))
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

    with stat_col:
        st.subheader("Status")
        remaining_str = float_to_hm(remaining_hours)
        
        if remaining_hours > 0:
            st.error(f"**Remaining:** {remaining_str}")
            st.markdown(f"### {remaining_str} / 8hr")
            st.caption("Time remaining / Total")
        else:
            overtime = abs(remaining_hours)
            st.success(f"**Overtime:** {float_to_hm(overtime)}")
            st.markdown(f"### 0hr 0min / 8hr")
            st.caption("Target Reached!")

        st.divider()
        st.write("**You should leave at:**")
        st.subheader(f"{target_exit_dt.strftime('%I:%M %p')}")

# Call the fragment function
update_live_status()

# --- Static Projection Section (Outside loop) ---
# This updates only when inputs change, saving resources
with st.expander("See Detailed Breakdown & Projection"):
    # Re-calculate constants for static display
    total_break = tea_break_mins + lunch_break_mins
    today = date.today()
    dt_in = datetime.combine(today, in_time)
    dt_planned = datetime.combine(today, planned_exit_time)
    
    if dt_planned < dt_in: dt_planned += timedelta(days=1)
    
    proj_gross = (dt_planned - dt_in).total_seconds() / 60
    proj_net = (proj_gross - total_break) / 60
    proj_remain = 8.0 - proj_net
    
    def fmt(h): return f"{int(h)}hr {int((h-int(h))*60)}min"

    st.write(f"**Office In:** {dt_in.strftime('%I:%M %p')}")
    st.write(f"**Total Breaks:** {fmt(total_break/60)}")
    st.markdown("---")
    st.markdown(f"**Projection if leaving at {planned_exit_time.strftime('%I:%M %p')}:**")
    
    if proj_remain > 0:
        st.error(f"You will be short by: **{fmt(proj_remain)}**")
    else:
        st.success(f"You will have overtime: **{fmt(abs(proj_remain))}**")
