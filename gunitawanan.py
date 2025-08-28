import streamlit as st
from st_supabase_connection import SupabaseConnection
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from datetime import datetime

# --- Page Configuration ---
st.set_page_config(
    page_title="GunitaTawanan 2025",
    page_icon="☀️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# --- Custom CSS for better styling ---
st.markdown("""
<style>
.main-header {
    text-align: center;
    padding: 2rem 0;
}
.event-info {
    text-align: center;
    padding: 1rem;
    margin: 1rem 0;
}
.attendee-card {
    padding: 0.5rem;
    margin: 0.25rem;
    border-radius: 10px;
    text-align: center;
    font-weight: bold;
}
</style>
""", unsafe_allow_html=True)

# --- Fun Header Banner ---
st.markdown('<div class="main-header">', unsafe_allow_html=True)
col1, col2, col3 = st.columns([1, 3, 1])
with col2:
    st.title("🥳 GunitaTawanan 2025 ☀️")
    st.subheader("Your Ultimate Chill Reunion 🏖️")
st.markdown('</div>', unsafe_allow_html=True)

# --- Supabase Connection ---
try:
    conn = st.connection("supabase", type=SupabaseConnection)
except Exception:
    st.error("🚫 Connection to Supabase failed. Please check your `.streamlit/secrets.toml` file.")
    st.stop()

# --- Functions to Interact with Supabase ---
@st.cache_data(ttl=600)
def get_attendees():
    """Fetches all names from the attendees table. Caches the result."""
    try:
        rows = conn.table("attendees").select("Name").execute()
        attendee_names = [record.get("Name") for record in rows.data if record.get("Name")]
        return attendee_names
    except Exception as e:
        st.error(f"Failed to fetch attendee list: {e}")
        return []

def add_attendee(name, email):
    """Inserts a new attendee into the database."""
    try:
        conn.table("attendees").insert({"Name": name, "Email": email}).execute()
        return True
    except Exception as e:
        st.error(f"Failed to add attendee: {e}")
        return False

# --- Event Info Section ---
st.info("🗓️ **August 30–31, 2025** | 📍 **New Era Association | One Spatial Iloilo**")

# Create attractive info box
with st.container():
    st.success("🎉 **Get ready for a weekend of good vibes, laughter, and making new memories!** 🤩")
    st.markdown("**Bring your best tawa and chill lang energy!** 🌟")

st.divider()

# --- Registration Form ---
st.header("🎟️ Confirm Your Attendance")
st.write("We can't wait to see you! Enter your details to confirm you're coming. ✨")

col1, col2 = st.columns(2)
with col1:
    with st.form("attendance_form"):
        email = st.text_input("📧 Your Email Address", placeholder="your.email@example.com")
        name = st.text_input("🙋‍♀️ Your Name", placeholder="Your full name")
        submitted = st.form_submit_button("I'm Coming! 🎉", use_container_width=True, type="primary")

        if submitted:
            if email and name:
                if add_attendee(name, email):
                    st.success("🎊 Attendance confirmed! We'll see you there!")
                    st.balloons()
                    st.cache_data.clear()
                    st.rerun()
                else:
                    st.error("Something went wrong. Please try again.")
            else:
                st.error("Please provide both your name and email. 🥺")

# --- Attendees Dashboard ---
attendee_list = get_attendees()
num_attendees = len(attendee_list)
max_participants = 10

with col2:
    st.subheader("👥 Registration Status")
    
    # Progress metrics
    col_metric1, col_metric2 = st.columns(2)
    with col_metric1:
        st.metric("Confirmed", num_attendees, help="Number of confirmed attendees")
    with col_metric2:
        remaining = max_participants - num_attendees
        st.metric("Slots Left", remaining, delta=-1 if remaining < max_participants else 0)
    
    # Progress bar
    progress_percentage = min(num_attendees / max_participants, 1.0)
    st.progress(progress_percentage, text=f"{num_attendees}/{max_participants} slots filled")
    
    if num_attendees >= max_participants:
        st.warning("🎉 Event is now full! Contact organizers for waitlist.")
    elif num_attendees > max_participants * 0.8:
        st.warning("⚡ Only a few spots left!")

st.divider()

# --- Visualization Section ---
if num_attendees > 0:
    st.subheader("📊 Fun Attendance Visualizations")
    
    viz_col1, viz_col2 = st.columns(2)
    
    with viz_col1:
        st.write("**Registration Timeline**")
        # Create a simple timeline chart
        timeline_data = pd.DataFrame({
            'Day': list(range(1, num_attendees + 1)),
            'Cumulative Attendees': list(range(1, num_attendees + 1)),
            'Names': attendee_list
        })
        
        fig_timeline = px.line(timeline_data, x='Day', y='Cumulative Attendees',
                              title="Registration Growth",
                              markers=True, hover_data=['Names'])
        fig_timeline.update_layout(height=300, showlegend=False)
        st.plotly_chart(fig_timeline, use_container_width=True)
    
    with viz_col2:
        st.write("**Attendance Gauge**")
        # Create a gauge chart
        fig_gauge = go.Figure(go.Indicator(
            mode = "gauge+number+delta",
            value = num_attendees,
            domain = {'x': [0, 1], 'y': [0, 1]},
            title = {'text': "Confirmed Attendees"},
            delta = {'reference': max_participants},
            gauge = {
                'axis': {'range': [None, max_participants]},
                'bar': {'color': "orange"},
                'steps': [
                    {'range': [0, max_participants//2], 'color': "lightgray"},
                    {'range': [max_participants//2, max_participants], 'color': "gray"}
                ],
                'threshold': {
                    'line': {'color': "red", 'width': 4},
                    'thickness': 0.75,
                    'value': max_participants
                }
            }
        ))
        fig_gauge.update_layout(height=300)
        st.plotly_chart(fig_gauge, use_container_width=True)

    # Attendee name visualization
    st.write("**Who's Coming? 🎉**")
    name_cols = st.columns(min(5, num_attendees))
    for i, name in enumerate(attendee_list):
        with name_cols[i % 5]:
            st.success(f"✨ **{name}**")

else:
    st.info("🎯 Be the first to register and see your name here!")

st.divider()

# --- Itinerary Section ---
st.header("🗓️ Event Itinerary")
st.subheader("📍 New Era Association | One Spatial Iloilo")

# Day 1 Tab
with st.expander("🌞 Day 1: August 30, 2025 (Saturday)", expanded=True):
    day1_schedule = [
        ("🛬 2:00 PM", "Arrival & Check-in", "Registration, welcome drinks, room assignment & orientation"),
        ("🧳 2:30 PM", "Settling In & Free Time", "Unpack, settle, photo ops, vibe check"),
        ("🎤 3:30 PM", "Opening Program", "Welcome remarks, icebreaker activities"),
        ("🍪 4:30 PM", "Merienda & Chill Catch-up", "Snacks, drinks, and casual conversations"),
        ("🎲 5:30 PM", "Group Activity (Optional)", "Throwback photo guessing game"),
        ("🛏️ 6:00 PM", "Free Time / Room Prep", "Relax and prepare for dinner"),
        ("🍽️ 7:00 PM", "Dinner", "Order your favorite cuisine, shared dining experience"),
        ("💬 8:00 PM", "Debrief & Reflection", "Heartfelt conversations and life updates"),
        ("🌙 10:00 PM", "Open Socials", "Pajama hangout, movies, games, or chill time"),
        ("😴 12:00 MN", "Wind Down", "Quiet hours begin, optional late-night conversations")
    ]
    
    for time, activity, description in day1_schedule:
        with st.container():
            col_time, col_content = st.columns([1, 4])
            with col_time:
                st.write(f"**{time}**")
            with col_content:
                st.write(f"**{activity}**")
                st.caption(description)

# Day 2 Tab
with st.expander("🌅 Day 2: August 31, 2025 (Sunday)", expanded=False):
    day2_schedule = [
        ("🌅 7:00 AM", "Chill Wake-up & Breakfast", "Self-serve breakfast and morning coffee"),
        ("🧘‍♂️ 8:00 AM", "Morning Activity (Optional)", "Stretching, walks, or pool relaxation"),
        ("🏊 9:30 AM", "Free Time", "Swimming, packing, photos, final conversations"),
        ("🥞 10:30 AM", "Brunch & Closing", "Group brunch, future letters, group photos"),
        ("🚗 12:00 NN", "Checkout / Departure", "Final goodbyes and safe travels")
    ]
    
    for time, activity, description in day2_schedule:
        with st.container():
            col_time, col_content = st.columns([1, 4])
            with col_time:
                st.write(f"**{time}**")
            with col_content:
                st.write(f"**{activity}**")
                st.caption(description)

# --- Sidebar ---
with st.sidebar:
    st.header("🎉 Reunion Central")
    
    # Attendees list
    st.subheader("Who's Coming?")
    if attendee_list:
        for i, name in enumerate(attendee_list, 1):
            st.write(f"{i}. ✨ **{name}**")
        
        # Fun stats
        st.divider()
        st.metric("Total Excitement Level", "🔥" * min(num_attendees, 5))
    else:
        st.write("No one has confirmed yet. Be the first! ✨")
    
    st.divider()
    
    # Reminders section
    st.subheader("📋 Important Reminders")
    with st.container():
        st.info("""
        **What to Bring:**
        - Essentials & toiletries
        - Themed attire
        - Food contributions
        - Your best energy! 😂
        """)
        
        st.success("""
        **Reunion Vibes:**
        - Safe, no-pressure environment
        - Be yourself completely
        - Rest when you want
        - Join the fun when you feel like it! 💖
        """)
    
    # Contact info
    st.divider()
    st.subheader("📞 Need Help?")
    st.write("Contact the organizers if you have any questions!")

# --- Footer ---
st.divider()
st.markdown(
    """
    <div style='text-align: center; padding: 2rem; color: gray;'>
        Made with ❤️ for GunitaTawanan 2025 • Let's make memories together! 🌟
    </div>
    """, 
    unsafe_allow_html=True
)