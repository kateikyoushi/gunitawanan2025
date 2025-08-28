import streamlit as st
from st_supabase_connection import SupabaseConnection

# --- Page Configuration ---
st.set_page_config(
    page_title="GunitaTawanan 2025",
    page_icon="☀️",
    layout="wide",
    initial_sidebar_state="expanded"
)

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
        rows = conn.query(table="attendees", columns=["Name"]).execute()
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

# --- Header and Introduction ---
st.title("GunitaTawanan 2025 🥳")
st.subheader("Your Ultimate Chill Reunion 🏖️")
st.markdown("---")
st.info("🗓️ **August 30–31, 2025** |📍 **New Era Association | One Spatial Iloilo**")
st.markdown("### Get ready for a weekend of good vibes, laughter, and making new memories! 🤩")

# --- Registration Form ---
st.header("🎟️ Confirm Your Attendance")
st.markdown("We can't wait to see you! Please enter your name and email to confirm you're coming. ✨")

with st.form("attendance_form"):
    email = st.text_input("📧 Your Email Address")
    name = st.text_input("🙋‍♀️ Your Name")
    submitted = st.form_submit_button("I'm Coming! 🎉")

    if submitted:
        if email and name:
            if add_attendee(name, email):
                st.success("Attendance confirmed! We'll see you there. 🥳")
                st.balloons()
                # Clear cache and rerun to update the sidebar list
                st.cache_data.clear()
                st.rerun()
            else:
                st.error("Something went wrong. Please try again.")
        else:
            st.error("Please provide both your name and email. 🥺")

st.markdown("---")

# --- Itinerary Section ---
st.header("📜 The Itinerary")
st.markdown("Here's a look at what we have in store. Everything is totally optional—just come, be yourself, and have fun! 😊")
st.markdown("### 🗓️ Day 1: August 30, 2025 (Saturday)")
st.markdown("A day for reconnection, good food, and deep conversations. 💬")
st.markdown("---")
st.markdown("#### ⏰ 2:00 PM – Arrival & Check-in")
st.markdown("Registration at lobby, welcome drinks, room assignment & quick orientation.")
st.markdown("#### ⏰ 2:30 PM – Settling In & Free Time")
st.markdown("Unpack, settle, take photos, vibe check. 📸")
st.markdown("#### ⏰ 3:30 PM – Opening Program")
st.markdown("Welcome remarks, light icebreaker (e.g., “Find Someone Who…”), and reminders.")
st.markdown("#### ⏰ 4:30 PM – Merienda & Chill Catch-up")
st.markdown("Snacks and drinks, catch-up conversations, playlist plays in the background. 🎶")
st.markdown("#### ⏰ 5:30 PM – Gentle Group Activity (Optional)")
st.markdown("One group activity: e.g., “Guess the Throwback Photo” (Totally optional—join or just watch/laugh along!).")
st.markdown("#### ⏰ 6:00 PM – Free Time / Room Prep")
st.markdown("Relax, get ready for dinner, pajama/loungewear if you want. 👕")
st.markdown("#### ⏰ 7:00 PM – Dinner")
st.markdown("Menu: Rice, Pork Sinigang, Beef with Broccoli. Long-table setup for shared stories, laughter. 🍲")
st.markdown("#### ⏰ 8:00 PM – Debrief & Reflection Night")
st.markdown("Structured, heartfelt conversation about how everyone is really doing. Safe and open space. Also includes a Parallel Zone for those who want to rest, play games, or just doomscroll. 🛋️")
st.markdown("#### ⏰ 10:00 PM – Open Socials")
st.markdown("Pajama/lounge hangout, movie or music (optional), “Tambay” corners, late-night snacks. 🍿")
st.markdown("#### ⏰ 12:00 MN – Wind Down")
st.markdown("Quiet hours begin for those sleeping, but “barkada” room always open for late-night convos. 🤫")
st.markdown("---")
st.markdown("### 🗓️ Day 2: August 31, 2025 (Sunday)")
st.markdown("A morning of farewells, good food, and final stories. 🫶")
st.markdown("---")
st.markdown("#### ⏰ 7:00 AM – Chill Wake-up & Breakfast")
st.markdown("Self-serve breakfast, coffee, and chill conversations. ☕️")
st.markdown("#### ⏰ 8:00 AM – Light Morning Activity (Optional)")
st.markdown("Stretching, walk, or just tambay by the pool/garden (Totally optional—sleep in if you want!). 🧘‍♀️")
st.markdown("#### 9:30 AM – Free Time")
st.markdown("Swim, pack up, photos, last-minute chika. 📸")
st.markdown("#### 10:30 AM – Brunch & Closing")
st.markdown("Group brunch, “Letter to Future Self” (optional), feedback, and final group picture. 🫂")
st.markdown("#### 12:00 NN – Checkout / Departure")
st.markdown("Safe travels, everyone! 🚗")
st.markdown("---")

# --- Sidebar ---
with st.sidebar:
    st.header("Who's Coming? 🎉")
    st.markdown("---")
    st.markdown("**Attendees:**")
    
    attendee_list = get_attendees()
    if attendee_list:
        for name in attendee_list:
            st.write(f"✨ {name}")
    else:
        st.write("No one has confirmed yet. Be the first! ✨")
    
    st.markdown("---")
    st.markdown("""
    **Reminders:**
    - Bring essentials, themed attire, food contributions, and your best tawa or “chill lang” energy 😂
    - This is a safe, no-pressure, “be yourself” reunion—rest if you want, join the fun if you want! 💖
    """)