import streamlit as st
from st_supabase_connection import SupabaseConnection

# --- Page Configuration ---
st.set_page_config(
        page_title="GunitaTawanan 2025",
        page_icon="☀️",
        layout="wide",
        initial_sidebar_state="expanded",
)

# --- Fun Header Banner ---
st.markdown("""
<div style='background: linear-gradient(90deg, #f9d423 0%, #ff4e50 100%); padding: 2rem 1rem; border-radius: 1.5rem; text-align: center; margin-bottom: 2rem;'>
    <h1 style='color: #fff; font-size: 3rem; margin-bottom: 0.5rem;'>GunitaTawanan 2025 🥳☀️</h1>
    <h3 style='color: #fff; font-weight: 400;'>Your Ultimate Chill Reunion 🏖️</h3>
</div>
""", unsafe_allow_html=True)

# --- Supabase Connection ---
# The st.connection will securely load credentials from .streamlit/secrets.toml
try:
    conn = st.connection("supabase", type=SupabaseConnection)
except Exception:
    st.error("Connection to Supabase failed. Please check your `.streamlit/secrets.toml` file.")
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


st.info("🗓️ **August 30–31, 2025** | 📍 **New Era Association | One Spatial Iloilo**")
st.markdown("""
<div style='background: #fffbe7; border-radius: 1rem; padding: 1rem; margin-bottom: 1.5rem; border: 2px dashed #f9d423;'>
<span style='font-size: 1.2rem;'>
🎉 <b>Get ready for a weekend of good vibes, laughter, and making new memories!</b> 🤩<br>
<span style='color: #ff4e50;'>Bring your best tawa and chill lang energy!</span>
</span>
</div>
""", unsafe_allow_html=True)


# --- Registration Form ---
st.header("🎟️ Confirm Your Attendance")
st.markdown("""
<span style='font-size: 1.1rem;'>We can't wait to see you!<br>Enter your name and email to confirm you're coming. ✨</span>
""", unsafe_allow_html=True)

with st.form("attendance_form"):
    email = st.text_input("📧 Your Email Address")
    name = st.text_input("🙋‍♀️ Your Name")
    submitted = st.form_submit_button("I'm Coming! 🎉")

    if submitted:
        if email and name:
            if add_attendee(name, email):
                st.success("Attendance confirmed! We'll see you there. 🥳")
                st.balloons()
                st.toast("Welcome to the reunion! 🎈", icon="🎉")
                # Clear cache and rerun to update the sidebar list
                st.cache_data.clear()
                st.rerun()
            else:
                st.error("Something went wrong. Please try again.")
        else:
            st.error("Please provide both your name and email. 🥺")

st.markdown("---")

# --- Attendees Dashboard ---
attendee_list = get_attendees()
num_attendees = len(attendee_list)

st.markdown("""
<div style='background: #f9d42322; border-radius: 1rem; padding: 1.2rem; margin-bottom: 1.5rem; border: 2px solid #f9d423;'>
<h3 style='margin-bottom:0.5em;'>👥 Attendees Dashboard</h3>
</div>
""", unsafe_allow_html=True)

cols = st.columns([1, 2, 2])
cols[0].metric("Total Attending", num_attendees, delta=None, help="Number of confirmed attendees")
if num_attendees > 0:
    cols[1].progress(num_attendees/30, text=f"{num_attendees}/30 slots filled")
    cols[2].markdown(
        "<div style='font-size:1.2em;'>" +
        " ".join(["🧑‍🤝‍🧑" for _ in range(min(num_attendees, 10))]) +
        (f" +{num_attendees-10} more" if num_attendees > 10 else "") +
        "</div>", unsafe_allow_html=True)
else:
    cols[1].info("No one has confirmed yet.")
    cols[2].markdown(":(")

# --- Beautiful Itinerary Section ---
st.markdown("""
<div style='background: linear-gradient(90deg, #f9d423 0%, #ff4e50 100%); padding: 1rem; border-radius: 1rem; margin-top: 2rem; margin-bottom: 1rem;'>
  <h2 style='color: #fff; margin: 0;'>🗓️ Itinerary – August 30–31, 2025</h2>
  <h4 style='color: #fff; margin: 0;'>New Era Association | One Spatial Iloilo</h4>
</div>
""", unsafe_allow_html=True)

with st.expander("Day 1: August 30, 2025 (Saturday) 🌞", expanded=True):
    st.markdown("""
    <ul>
    <li><b>🛬 2:00 PM – Arrival & Check-in</b><br>
    Registration at lobby<br>Welcome drinks 🥤<br>Room assignment & quick orientation 🗝️</li>
    <li><b>🧳 2:30 PM – Settling In & Free Time</b><br>
    Unpack, settle, take photos 📸, vibe check</li>
    <li><b>🎤 3:30 PM – Opening Program</b><br>
    Welcome remarks<br>Light icebreaker (e.g., “Find Someone Who…”)<br>Reminders: just chill, respect everyone’s comfort</li>
    <li><b>🍪 4:30 PM – Merienda & Chill Catch-up</b><br>
    Snacks and drinks<br>Catch-up conversations (no forced grouping, just mingle as you want)<br>Playlist plays in the background 🎶</li>
    <li><b>🎲 5:30 PM – Gentle Group Activity (Optional)</b><br>
    One group activity: e.g., “Guess the Throwback Photo”<br><i>(Totally optional—join or just watch/laugh along!)</i></li>
    <li><b>🛏️ 6:00 PM – Free Time / Room Prep</b><br>
    Relax, get ready for dinner, pajama/loungewear if you want</li>
    <li><b>🍽️ 7:00 PM – Dinner</b><br>
    Buy or order dinner. Feel free to choose whatever cuisine that suits your palate!<br>Long-table setup for shared stories, laughter</li>
    <li><b>💬 8:00 PM – Debrief & Reflection Night</b><br>
    <u>Structured, Heartfelt Conversation:</u><br>
    Debriefing Session:<br>
    How’s everyone really doing?<br>
    Memorable moments—personal, career, life updates<br>
    What we miss, what we look forward to as a group<br>
    Open mic for anything (big or small!)<br>
    Gentle facilitation, but zero pressure—just a safe, open space<br>
    <u>Parallel Zone:</u><br>
    If you need to bedrot, nap, or doomscroll in a corner—go ahead!<br>
    Bring out board games, cards, or just vibe with your gadgets 🎮</li>
    <li><b>🌙 10:00 PM – Open Socials</b><br>
    Pajama/lounge hangout<br>Movie or music (optional) 🎬<br>“Tambay” corners—small groups, or just scrolling, laughing at memes, or sharing reels<br>Late night snacks for whoever’s still up 🍫</li>
    <li><b>😴 12:00 MN – Wind Down</b><br>
    Quiet hours begin for those sleeping, but “barkada” room always open for late-night convos</li>
    </ul>
    """, unsafe_allow_html=True)

with st.expander("Day 2: August 31, 2025 (Sunday) 🌅", expanded=False):
    st.markdown("""
    <ul>
    <li><b>🌅 7:00 AM – Chill Wake-up & Breakfast</b><br>
    Self-serve breakfast, coffee ☕, and chill conversations</li>
    <li><b>🧘‍♂️ 8:00 AM – Light Morning Activity (Optional)</b><br>
    Stretching, walk, or just tambay by the pool/garden<br><i>(Totally optional—sleep in if you want!)</i></li>
    <li><b>🏊 9:30 AM – Free Time</b><br>
    Swim, pack up, photos, last-minute chika</li>
    <li><b>🥞 10:30 AM – Brunch & Closing</b><br>
    Group brunch<br>“Letter to Future Self” (optional)<br>Feedback and suggestions for next time<br>Final group picture, thank yous, and send-offs</li>
    <li><b>🚗 12:00 NN – Checkout / Departure</b></li>
    </ul>
    """, unsafe_allow_html=True)

# --- Sidebar ---
with st.sidebar:
        st.markdown("""
        <div style='background: linear-gradient(90deg, #f9d423 0%, #ff4e50 100%); padding: 1rem; border-radius: 1rem; margin-bottom: 1rem;'>
            <h2 style='color: #fff; margin: 0;'>Who's Coming? 🎉</h2>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("**Attendees:**")
        attendee_list = get_attendees()
        if attendee_list:
                st.markdown(
                        "<ul style='padding-left: 1.2em;'>" +
                        "".join([f"<li style='font-size:1.1em; margin-bottom:0.3em;'>✨ <b>{name}</b></li>" for name in attendee_list]) +
                        "</ul>", unsafe_allow_html=True)
        else:
                st.write("No one has confirmed yet. Be the first! ✨")
        st.markdown("---")
        st.markdown("""
        <div style='background: #fffbe7; border-radius: 1rem; padding: 1rem; border: 2px dashed #f9d423;'>
        <b>Reminders:</b><br>
        <ul>
            <li>Bring essentials, themed attire, food contributions, and your best tawa or “chill lang” energy 😂</li>
            <li>This is a safe, no-pressure, “be yourself” reunion—rest if you want, join the fun if you want! 💖</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)