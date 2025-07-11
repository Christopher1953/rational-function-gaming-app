import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime
import json
import os

# Import custom modules
from utils.function_generator import RationalFunctionGenerator
from utils.graph_analyzer import GraphAnalyzer
from utils.scoring_system import ScoringSystem
from data.leaderboard import LeaderboardManager
from game_modes.practice_mode import PracticeMode
from game_modes.timed_challenge import TimedChallenge
from game_modes.multiplayer_quiz import MultiplayerQuiz

# Page configuration
st.set_page_config(
    page_title="Rational Function Gaming App",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
if 'player_name' not in st.session_state:
    st.session_state.player_name = ""
if 'current_score' not in st.session_state:
    st.session_state.current_score = 0
if 'game_mode' not in st.session_state:
    st.session_state.game_mode = "home"
if 'achievements' not in st.session_state:
    st.session_state.achievements = []
if 'difficulty_level' not in st.session_state:
    st.session_state.difficulty_level = 1

# Initialize managers
leaderboard_manager = LeaderboardManager()
scoring_system = ScoringSystem()

def main():
    # Sidebar for navigation
    with st.sidebar:
        st.title("🎮 Rational Function Games")
        
        # Player name input
        if not st.session_state.player_name:
            st.session_state.player_name = st.text_input(
                "Enter your name to start playing:",
                placeholder="Your name here..."
            )
            if st.session_state.player_name:
                st.success(f"Welcome, {st.session_state.player_name}! 🎉")
                st.rerun()
        else:
            st.success(f"Welcome back, {st.session_state.player_name}! 🎉")
            if st.button("Change Player"):
                st.session_state.player_name = ""
                st.session_state.current_score = 0
                st.rerun()
        
        st.divider()
        
        # Navigation menu
        if st.session_state.player_name:
            st.subheader("🎯 Game Modes")
            
            if st.button("🏠 Home", use_container_width=True):
                st.session_state.game_mode = "home"
                st.rerun()
            
            if st.button("📚 Practice Mode", use_container_width=True):
                st.session_state.game_mode = "practice"
                st.rerun()
            
            if st.button("⏰ Timed Challenge", use_container_width=True):
                st.session_state.game_mode = "timed"
                st.rerun()
            
            if st.button("👥 Multiplayer Quiz", use_container_width=True):
                st.session_state.game_mode = "multiplayer"
                st.rerun()
            
            if st.button("🏆 Leaderboard", use_container_width=True):
                st.session_state.game_mode = "leaderboard"
                st.rerun()
            
            st.divider()
            
            # Player stats
            st.subheader("📊 Your Stats")
            st.metric("Current Score", st.session_state.current_score)
            st.metric("Difficulty Level", st.session_state.difficulty_level)
            
            if st.session_state.achievements:
                st.subheader("🏅 Achievements")
                for achievement in st.session_state.achievements:
                    st.write(f"• {achievement}")

    # Main content area
    if not st.session_state.player_name:
        show_welcome_screen()
    elif st.session_state.game_mode == "home":
        show_home_screen()
    elif st.session_state.game_mode == "practice":
        show_practice_mode()
    elif st.session_state.game_mode == "timed":
        show_timed_challenge()
    elif st.session_state.game_mode == "multiplayer":
        show_multiplayer_quiz()
    elif st.session_state.game_mode == "leaderboard":
        show_leaderboard()

def show_welcome_screen():
    st.title("🎮 Welcome to Rational Function Gaming!")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("""
        ## 📊 Master Rational Functions Through Gaming!
        
        Welcome to the most engaging way to learn rational function graphing! This app combines the excitement of gaming with the fundamentals of precalculus.
        
        ### 🎯 What You'll Learn:
        - **Horizontal & Vertical Asymptotes** - Understand limits and behavior
        - **Holes in Functions** - Identify removable discontinuities
        - **X & Y Intercepts** - Find where functions cross axes
        - **End Behavior** - Analyze function limits at infinity
        
        ### 🎮 Game Modes Available:
        - **Practice Mode**: Learn at your own pace with hints
        - **Timed Challenge**: Race against the clock!
        - **Multiplayer Quiz**: Compete with other players
        
        ### 🏆 Features:
        - Interactive graph plotting and analysis
        - Real-time feedback and scoring
        - Achievement system and leaderboards
        - Progressive difficulty levels
        
        **Enter your name in the sidebar to start your mathematical adventure!**
        """)

def show_home_screen():
    st.title(f"🎮 Welcome, {st.session_state.player_name}!")
    
    # Quick stats overview
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("🎯 Current Score", st.session_state.current_score)
    
    with col2:
        st.metric("📈 Difficulty Level", st.session_state.difficulty_level)
    
    with col3:
        leaderboard_data = leaderboard_manager.get_leaderboard()
        if not leaderboard_data.empty:
            player_rank = leaderboard_manager.get_player_rank(st.session_state.player_name)
            st.metric("🏆 Your Rank", f"#{player_rank}" if player_rank else "Unranked")
        else:
            st.metric("🏆 Your Rank", "Unranked")
    
    with col4:
        st.metric("🏅 Achievements", len(st.session_state.achievements))
    
    st.divider()
    
    # Game mode selection with visual cards
    st.subheader("🎮 Choose Your Game Mode")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("### 📚 Practice Mode")
        st.write("Learn rational functions at your own pace with helpful hints and detailed explanations.")
        if st.button("Start Practice", key="practice_btn", use_container_width=True):
            st.session_state.game_mode = "practice"
            st.rerun()
    
    with col2:
        st.markdown("### ⏰ Timed Challenge")
        st.write("Test your skills against the clock! Quick thinking and accuracy are key.")
        if st.button("Start Challenge", key="timed_btn", use_container_width=True):
            st.session_state.game_mode = "timed"
            st.rerun()
    
    with col3:
        st.markdown("### 👥 Multiplayer Quiz")
        st.write("Compete with other players in real-time! Who will be the rational function master?")
        if st.button("Join Quiz", key="multiplayer_btn", use_container_width=True):
            st.session_state.game_mode = "multiplayer"
            st.rerun()
    
    st.divider()
    
    # Recent achievements or tips
    st.subheader("💡 Learning Tips")
    tips = [
        "🎯 Look for common factors in numerator and denominator to find holes",
        "📈 Vertical asymptotes occur where the denominator equals zero (and numerator doesn't)",
        "📊 Horizontal asymptotes depend on the degrees of numerator and denominator",
        "🔍 X-intercepts happen when the numerator equals zero (and denominator doesn't)",
        "📌 Y-intercepts are found by substituting x = 0"
    ]
    
    tip_index = len(st.session_state.player_name) % len(tips)
    st.info(tips[tip_index])

def show_practice_mode():
    practice_mode = PracticeMode()
    practice_mode.run()

def show_timed_challenge():
    timed_challenge = TimedChallenge()
    timed_challenge.run()

def show_multiplayer_quiz():
    multiplayer_quiz = MultiplayerQuiz()
    multiplayer_quiz.run()

def show_leaderboard():
    st.title("🏆 Leaderboard")
    
    leaderboard_data = leaderboard_manager.get_leaderboard()
    
    if leaderboard_data.empty:
        st.info("No scores recorded yet. Be the first to play and set a record! 🚀")
        return
    
    # Display top 10 players
    st.subheader("🥇 Top Players")
    
    for i, (_, row) in enumerate(leaderboard_data.head(10).iterrows()):
        col1, col2, col3, col4 = st.columns([0.5, 2, 1, 1])
        
        with col1:
            if i == 0:
                st.write("🥇")
            elif i == 1:
                st.write("🥈")
            elif i == 2:
                st.write("🥉")
            else:
                st.write(f"{i+1}.")
        
        with col2:
            if row['player_name'] == st.session_state.player_name:
                st.markdown(f"**{row['player_name']} (You)**")
            else:
                st.write(row['player_name'])
        
        with col3:
            st.write(f"{row['total_score']:,}")
        
        with col4:
            st.write(f"Level {row['max_level']}")
    
    st.divider()
    
    # Player's personal stats
    player_stats = leaderboard_manager.get_player_stats(st.session_state.player_name)
    if player_stats:
        st.subheader(f"📊 {st.session_state.player_name}'s Statistics")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Games Played", player_stats['games_played'])
        
        with col2:
            st.metric("Average Score", f"{player_stats['avg_score']:.1f}")
        
        with col3:
            st.metric("Best Score", player_stats['best_score'])

if __name__ == "__main__":
    main()
