import streamlit as st
import pandas as pd
from google import genai

# ==========================================
# PAGE CONFIGURATION
# ==========================================
# Sets the browser tab title, icon, and layout width.
st.set_page_config(page_title="ThinkLoop", page_icon="🧠", layout="centered")

GOOGLE_API_KEY = st.secrets["GOOGLE_API_KEY"]
# ==========================================
# SYSTEM PROMPT (THE "BRAIN")
# ==========================================
# This dictates the AI's persona, boundaries, and output format.
# (Make sure your FULL master prompt is pasted between these quotes!)
SYSTEM_PROMPT = """
You are ThinkLoop, a compassionate, grounded, and deeply empathetic sounding board. 
Your purpose is to help the user find emotional clarity and practical steps forward, but you must do so with warmth, heart, and a conversational "human" tone.

Do not sound like a clinical robot, a medical dictionary, or a cold AI. Sound like a wise, deeply caring mentor who listens first, validates their very human feelings, and then gently guides them toward clarity. 
Never judge, and always remind them that their feelings are valid and normal. 

OUTPUT FORMAT:
(Please use these exact headings, but fill them with warm, conversational, and supportive text. Speak directly to the user using "you".)

🌱 A Moment to Breathe:
(Start by deeply validating their emotional state. Acknowledge how hard or heavy things feel right now. Make them feel heard and safe.)

🔍 Gently Unpacking This:
(Point out the psychological signals or patterns you see, but use kind, understandable terms. E.g., instead of "Cognitive Distortion," say "It looks like your brain is trying to protect you by assuming the worst...")

💡 A Perspective Shift:
(Offer a gentle reframe. What does this situation likely mean when we step back and look at it with a clear, calm mind?)

✅ Gentle Steps Forward (What to do):
(Provide emotionally stable, supportive actions they can take to care for themselves right now.)

⏸️ What to Pause On (What to avoid):
(List impulsive reactions or thought spirals to avoid, but frame them protectively. E.g., "Try to pause on sending that text while your nervous system is on high alert.")

🎯 The Next Small Step:
(Give them ONE tiny, incredibly easy, and manageable action they can take right this second to feel just 1% better.)
"""

# ==========================================
# SIDEBAR NAVIGATION & USER CONTEXT
# ==========================================
st.sidebar.title("🧭 Navigation")
st.sidebar.markdown("Welcome to the control panel.")

# Optional user context to personalize the session
user_name = st.sidebar.text_input("Enter your name (optional):")
if user_name:
    st.sidebar.success(f"Ready to focus, {user_name}.")

# ==========================================
# MAIN INTERFACE (FRONTEND)
# ==========================================
st.title("🧠 ThinkLoop")
st.markdown("*Clarity over comfort. Evidence over assumption.*")

# Text area for user to input their thoughts/messages
user_input = st.text_area("Paste your message, letter, or thought here:", height=200)

# ==========================================
# AI ANALYSIS LOGIC (BACKEND)
# ==========================================
# Trigger analysis only when the button is clicked
if st.button("Analyze"):
    if not user_input:
        st.warning("Please enter some text first.")
    else:
        with st.spinner("Analyzing patterns..."):
            try:
                # 1. Connect to the GenAI Client
                client = genai.Client(api_key=GOOGLE_API_KEY)
                
                # 2. Combine instructions with user's specific input
                full_prompt = f"{SYSTEM_PROMPT}\n\nUSER INPUT:\n{user_input}"
                
                # 3. Call the Gemini 2.5 Flash model
                response = client.models.generate_content(
                    model='gemini-2.5-flash',
                    contents=full_prompt,
                )
                
                # 4. Display the result
                st.subheader("Analysis")
                st.write(response.text)
                
            except Exception as e:
                st.error(f"An error occurred: {e}")

# ==========================================
# DATA DASHBOARD (BOTTOM SECTION)
# ==========================================
st.markdown("---")
st.subheader("📊 Your Emotional Insights") 

# Instruction box for intensity metrics
st.info("""
**How to measure Intensity (1-10):**
* **1-3 (Low):** A passing feeling. Manageable.
* **4-7 (Moderate):** Distracting. Needs some attention.
* **8-10 (High):** Overwhelming. Requires immediate grounding exercises.
""")

# Split the bottom section into two equal columns
col1, col2 = st.columns(2)

# --- Column 1: Real EV Data ---
with col1:
    st.markdown("##### 🚗 Live EV Data")
    
    # Load the real dataset
    df_ev = pd.read_csv("ev_data.csv")
    
    # 1. Get a list of all unique car brands in the dataset
    car_brands = df_ev['Make'].dropna().unique()
    
    # 2. Create the interactive dropdown menu
    selected_brand = st.selectbox("Select an EV Brand:", car_brands)
    
    # 3. Filter the dataset to ONLY show rows matching the selected brand
    filtered_data = df_ev[df_ev['Make'] == selected_brand]
    
    # 4. Display the newly filtered data
    st.dataframe(filtered_data.head(50), use_container_width=True)
#Visuals added
    st.markdown("##### 📊 Top 10 EV Brands")
    
    # 1. Count how many vehicles each brand has and take the top 10
    top_brands = df_ev['Make'].value_counts().head(10)
    
    # 2. Tell Streamlit to draw a bar chart!
    st.bar_chart(top_brands)

# --- Column 2: Habit Tracker ---
with col2:
    st.markdown("##### 🛠️ Habit Tracker")
    habit_data = {
        "🌟 Good Habits": ["Daily 10-min journaling", "Pause before texting", "Fact-checking", "Deep breathing"],
        "🛑 Habits to Avoid": ["Doomscrolling at night", "Assuming motives", "Over-caffeinating", "Rushing responses"]
    }
    df_habits = pd.DataFrame(habit_data)
    st.dataframe(df_habits, use_container_width=True)