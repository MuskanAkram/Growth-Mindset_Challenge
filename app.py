import streamlit as st
from dotenv import load_dotenv
import requests
import os
import random
import time
import json

# Load environment variables
load_dotenv()
# Custom CSS with enhanced space theme
st.markdown("""
   
""", unsafe_allow_html=True)

# Hugging Face API setup
API_URL = "https://api-inference.huggingface.co/models/facebook/opt-350m"  # Using a more reliable model
headers = {"Authorization": f"Bearer HUGGINGFACE_API_KEY=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 "}

def query_huggingface(payload):
    try:
        # Simplify payload
        if isinstance(payload, dict):
            text = payload.get('inputs', '')
        else:
            text = str(payload)
            
        simple_payload = {
            "inputs": text,
            "options": {
                "wait_for_model": True
            }
        }
        
        # Make API request
        response = requests.post(API_URL, headers=headers, json=simple_payload)
        
        # Handle different response cases
        if response.status_code == 200:
            result = response.json()
            if isinstance(result, list) and result:
                return result[0].get('generated_text', '')
            return get_fallback_response(text)
            
        elif response.status_code == 503:
            st.warning("Model is loading... Please try again in a few seconds.")
            time.sleep(5)  # Wait for model to load
            return get_fallback_response(text)
            
        else:
            st.error(f"API Error: Status code {response.status_code}")
            return get_fallback_response(text)
            
    except Exception as e:
        st.error(f"Error: {str(e)}")
        return get_fallback_response(text)

def test_api_connection():
    try:
        test_response = query_huggingface("Generate a short motivational message")
        if test_response and not test_response.startswith("API Error"):
            return True, "API connection successful!"
        return False, "API connection failed"
    except Exception as e:
        return False, f"Connection Error: {str(e)}"

# Add this at the start of your app to test the connection
with st.sidebar:
    if st.button("🔄 Test API Connection"):
        with st.spinner("Testing API connection..."):
            is_connected, message = test_api_connection()
            if is_connected:
                st.success(message)
            else:
                st.error(message)

def get_fallback_response(prompt):
    responses = {
        "mission": [
            "Embark on a journey of continuous learning and growth.",
            "Push beyond your current limits and explore new possibilities.",
            "Transform challenges into opportunities for advancement."
        ],
        "challenge": [
            "Break down your mission into daily explorations.",
            "Track your progress like a space mission - one milestone at a time.",
            "Maintain mission logs to document your growth journey."
        ],
        "motivation": [
            "The universe of possibilities awaits your exploration.",
            "Every small step is a leap toward your greater potential.",
            "Your growth journey is as vast as space itself."
        ]
    }
    
    if "mission" in prompt.lower():
        return random.choice(responses["mission"])
    elif "challenge" in prompt.lower():
        return random.choice(responses["challenge"])
    else:
        return random.choice(responses["motivation"])

# Sidebar for Explorer Profile
with st.sidebar:
    st.title("🚀 Mission Control")
    if 'explorer_name' not in st.session_state:
        st.session_state.explorer_name = st.text_input("Enter Explorer Name:", "Space Pioneer")
    
    st.subheader("Mission Stats")
    if 'missions_completed' not in st.session_state:
        st.session_state.missions_completed = 0
    
    st.metric("Missions Launched", st.session_state.missions_completed)
    
    # Achievement ranks
    st.subheader("Explorer Rank")
    ranks = {
        5: "🛸 Cosmic Rookie",
        10: "✨ Star Navigator",
        20: "🌌 Galaxy Pioneer",
        30: "⭐ Universal Master"
    }
    
    current_rank = max([level for level in ranks.keys() 
                       if st.session_state.missions_completed >= level] or [0])
    
    if current_rank > 0:
        st.markdown(f"<div class='achievement-badge'>{ranks[current_rank]}</div>", 
                   unsafe_allow_html=True)

# Main Mission Control
st.title("🚀 Growth Mindset Explorer")
st.write(f"Welcome, Explorer {st.session_state.explorer_name}! Ready for your next mission?")

# Mission Planning
with st.container():
    st.header("🎯 Launch New Mission")
    mission = st.text_area("What's your next growth mission?", 
                          placeholder="Example: Master the art of public speaking...")
    
    if st.button("Initialize Mission Plan"):
        if mission:
            with st.spinner("Calculating mission parameters..."):
                # Get AI responses
                refined_mission = query_huggingface({"inputs": f"Refine this growth mission: {mission}"})
                strategy = query_huggingface({"inputs": f"Create a 30-day strategy for: {mission}"})
                cosmic_wisdom = query_huggingface({"inputs": "Share cosmic wisdom about growth and exploration"})
                
                # Display mission briefing
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown("<div class='mission-card'>", unsafe_allow_html=True)
                    st.subheader("🎯 Mission Objectives")
                    st.write(refined_mission)
                    st.markdown("</div>", unsafe_allow_html=True)
                
                with col2:
                    st.markdown("<div class='mission-card'>", unsafe_allow_html=True)
                    st.subheader("📅 30-Day Flight Plan")
                    st.write(strategy)
                    st.markdown("</div>", unsafe_allow_html=True)
                
                st.markdown("<div class='quote-box'>", unsafe_allow_html=True)
                st.write(f"💫 *{cosmic_wisdom}*")
                st.markdown("</div>", unsafe_allow_html=True)
                
                st.session_state.missions_completed += 1
        else:
            st.warning("Please define your mission objectives!")

# Mission Progress Tracking
if 'mission_progress' not in st.session_state:
    st.session_state.mission_progress = [False] * 30

st.header("📊 Mission Progress")

# Create an interactive space journey tracker
progress_cols = st.columns(10)
for i in range(30):
    col_index = i % 10
    with progress_cols[col_index]:
        milestone_class = "progress-milestone milestone-active" if st.session_state.mission_progress[i] else "progress-milestone"
        st.markdown(f"<div class='{milestone_class}'>", unsafe_allow_html=True)
        day_complete = st.checkbox(f"D{i+1}", value=st.session_state.mission_progress[i], key=f"day_{i}")
        st.markdown("</div>", unsafe_allow_html=True)
        if day_complete != st.session_state.mission_progress[i]:
            st.session_state.mission_progress[i] = day_complete
            st.rerun()

# Progress visualization
completed = sum(st.session_state.mission_progress)
progress_percentage = (completed / 30) * 100

st.progress(progress_percentage / 100)
st.write(f"🌟 Mission Progress: {completed}/30 milestones achieved! ({progress_percentage:.1f}%)")

# Mission Status
if progress_percentage == 100:
    st.balloons()
    st.success("🌟 Mission Accomplished! You've reached all milestones!")
elif progress_percentage >= 75:
    st.info("🚀 Final approach initiated! Keep pushing forward!")
elif progress_percentage >= 50:
    st.info("💫 Halfway through your journey! Stay on course!")
elif progress_percentage >= 25:
    st.info("✨ Liftoff successful! Maintain trajectory!")
else:
    st.info("🛸 Pre-launch sequence initiated! Ready for takeoff!")

# Cosmic Tips
st.header("💫 Cosmic Wisdom")
cosmic_tips = [
    "The universe rewards those who dare to grow.",
    "Every challenge is a new star to reach for.",
    "Your potential is as limitless as space itself.",
    "Navigate through difficulties like a skilled astronaut.",
    "Each small step contributes to your cosmic journey.",
    "Embrace the unknown - that's where growth happens.",
    "Your mindset is your spacecraft through challenges.",
    "Chart your own course among the stars.",
    "Learn from every meteor and milestone.",
    "Your growth journey is writing constellations in the sky."
]
st.info(random.choice(cosmic_tips))

# Footer
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: rgba(255,255,255,0.7);'>"
    "Exploring the infinite possibilities of growth 🌌"
    "</div>", 
    unsafe_allow_html=True
)