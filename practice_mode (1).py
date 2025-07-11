import streamlit as st
import time
import random
from utils.function_generator import RationalFunctionGenerator
from utils.graph_analyzer import GraphAnalyzer
from utils.scoring_system import ScoringSystem
from data.leaderboard import LeaderboardManager

class PracticeMode:
    def __init__(self):
        self.function_generator = RationalFunctionGenerator()
        self.graph_analyzer = GraphAnalyzer()
        self.scoring_system = ScoringSystem()
        self.leaderboard_manager = LeaderboardManager()
        
        # Initialize session state for practice mode
        if 'practice_question' not in st.session_state:
            st.session_state.practice_question = None
        if 'practice_answer_submitted' not in st.session_state:
            st.session_state.practice_answer_submitted = False
        if 'practice_streak' not in st.session_state:
            st.session_state.practice_streak = 0
        if 'practice_questions_answered' not in st.session_state:
            st.session_state.practice_questions_answered = 0
        if 'practice_start_time' not in st.session_state:
            st.session_state.practice_start_time = None
    
    def run(self):
        st.title("📚 Practice Mode")
        st.markdown("**Learn rational functions at your own pace with helpful hints and explanations.**")
        
        # Settings panel
        with st.sidebar:
            st.subheader("⚙️ Practice Settings")
            
            # Difficulty selection
            difficulty = st.selectbox(
                "Difficulty Level",
                options=[1, 2, 3, 4, 5],
                index=st.session_state.difficulty_level - 1,
                format_func=lambda x: f"Level {x} {'⭐' * x}"
            )
            
            if difficulty != st.session_state.difficulty_level:
                st.session_state.difficulty_level = difficulty
                st.session_state.practice_question = None  # Reset question
            
            # Question type selection
            question_types = [
                "Random",
                "Vertical Asymptotes",
                "Horizontal Asymptotes", 
                "X-intercepts",
                "Holes"
            ]
            
            selected_type = st.selectbox(
                "Focus on:",
                options=question_types
            )
            
            st.divider()
            
            # Practice stats
            st.subheader("📊 Practice Stats")
            st.metric("Questions Answered", st.session_state.practice_questions_answered)
            st.metric("Current Streak", st.session_state.practice_streak)
            
            if st.button("Reset Practice Stats"):
                st.session_state.practice_questions_answered = 0
                st.session_state.practice_streak = 0
                st.session_state.practice_question = None
                st.rerun()
        
        # Main practice area
        col1, col2 = st.columns([2, 1])
        
        with col1:
            # Generate or display current question
            if st.session_state.practice_question is None:
                self._generate_new_question(difficulty, selected_type)
            
            if st.session_state.practice_question:
                self._display_question()
        
        with col2:
            self._display_help_panel()
        
        # Answer section
        if st.session_state.practice_question and not st.session_state.practice_answer_submitted:
            self._handle_answer_input()
        
        # Results and next question
        if st.session_state.practice_answer_submitted:
            self._display_results()
    
    def _generate_new_question(self, difficulty, question_type):
        """Generate a new practice question"""
        function_dict = self.function_generator.generate_function(difficulty)
        analysis = self.function_generator.analyze_function(function_dict)
        
        # Determine question type
        if question_type == "Random":
            q_type = random.choice(['vertical_asymptotes', 'horizontal_asymptote', 'x_intercepts', 'holes'])
        else:
            type_mapping = {
                "Vertical Asymptotes": "vertical_asymptotes",
                "Horizontal Asymptotes": "horizontal_asymptote",
                "X-intercepts": "x_intercepts",
                "Holes": "holes"
            }
            q_type = type_mapping.get(question_type, 'vertical_asymptotes')
        
        question_data = self.function_generator.generate_multiple_choice_question(
            function_dict, analysis, q_type
        )
        
        st.session_state.practice_question = {
            'function_dict': function_dict,
            'analysis': analysis,
            'question_data': question_data,
            'question_type': q_type,
            'difficulty': difficulty
        }
        st.session_state.practice_answer_submitted = False
        st.session_state.practice_start_time = time.time()
    
    def _display_question(self):
        """Display the current practice question"""
        question = st.session_state.practice_question
        
        # Display function
        st.subheader("📊 Function to Analyze")
        st.latex(f"f(x) = {question['function_dict']['latex']}")
        
        # Display interactive graph
        fig = self.graph_analyzer.create_interactive_graph(
            question['function_dict'],
            question['analysis']
        )
        if fig is not None:
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("📊 Graph visualization temporarily unavailable. Focus on the function equation above.")
        
        # Display question
        st.subheader("❓ Question")
        st.write(question['question_data']['question'])
    
    def _handle_answer_input(self):
        """Handle answer input and submission"""
        question = st.session_state.practice_question
        
        st.subheader("✏️ Your Answer")
        
        # Multiple choice interface
        choices = question['question_data']['choices']
        
        with st.form("practice_answer_form"):
            selected_answer = st.radio(
                "Select your answer:",
                options=choices,
                key="practice_selected_answer"
            )
            
            col1, col2, col3 = st.columns([1, 1, 1])
            
            with col1:
                submitted = st.form_submit_button("Submit Answer", use_container_width=True)
            
            with col2:
                hint_requested = st.form_submit_button("💡 Need a Hint?", use_container_width=True)
            
            with col3:
                show_solution = st.form_submit_button("📖 Show Solution", use_container_width=True)
            
            if hint_requested:
                self._show_hint()
            
            if show_solution:
                self._show_complete_solution()
            
            if submitted:
                st.session_state.practice_user_answer = selected_answer
                st.session_state.practice_answer_submitted = True
                st.rerun()
    
    def _show_hint(self):
        """Show a helpful hint for the current question"""
        question = st.session_state.practice_question
        q_type = question['question_type']
        
        hints = {
            'vertical_asymptotes': "💡 **Hint:** Vertical asymptotes occur where the denominator equals zero, but the numerator doesn't. Factor both numerator and denominator first!",
            'horizontal_asymptote': "💡 **Hint:** Compare the degrees of the numerator and denominator. If denominator degree > numerator degree, HA is y=0. If equal, HA is the ratio of leading coefficients.",
            'x_intercepts': "💡 **Hint:** X-intercepts occur where the numerator equals zero (and the denominator doesn't). Set the numerator equal to zero and solve!",
            'holes': "💡 **Hint:** Holes occur where both numerator and denominator have a common factor. Factor both and look for factors that cancel out!"
        }
        
        st.info(hints.get(q_type, "💡 **Hint:** Analyze the function step by step. Factor first, then look for patterns!"))
    
    def _show_complete_solution(self):
        """Show the complete solution with step-by-step explanation"""
        question = st.session_state.practice_question
        analysis = question['analysis']
        
        st.success("📖 **Complete Solution:**")
        
        # Show the analysis summary
        summary = self.graph_analyzer.create_analysis_summary(analysis)
        
        for key, value in summary.items():
            st.write(f"**{key}:** {value}")
        
        # Provide detailed explanation
        st.markdown("### 📝 Step-by-Step Process:")
        
        st.markdown("""
        1. **Factor** both numerator and denominator completely
        2. **Identify common factors** - these create holes
        3. **Find vertical asymptotes** - where denominator = 0 (after canceling)
        4. **Find horizontal asymptotes** - compare degrees of num/den
        5. **Find x-intercepts** - where numerator = 0 (after canceling)
        6. **Find y-intercept** - substitute x = 0
        """)
    
    def _display_results(self):
        """Display results after answer submission"""
        question = st.session_state.practice_question
        user_answer = st.session_state.practice_user_answer
        correct_answer = question['question_data']['correct_answer']
        
        # Calculate time taken
        time_taken = time.time() - st.session_state.practice_start_time if st.session_state.practice_start_time else 0
        
        # Check if answer is correct
        is_correct = user_answer == correct_answer
        
        # Update statistics
        st.session_state.practice_questions_answered += 1
        
        if is_correct:
            st.session_state.practice_streak += 1
            # Calculate score
            score = self.scoring_system.calculate_score(
                is_correct=True,
                difficulty_level=question['difficulty'],
                time_taken=time_taken,
                current_streak=st.session_state.practice_streak,
                question_type=question['question_type']
            )
            st.session_state.current_score += score
            
            # Update player statistics
            self.scoring_system.update_player_stats(
                st.session_state.player_name,
                is_correct=True,
                difficulty_level=question['difficulty'],
                time_taken=time_taken,
                question_type=question['question_type'],
                score_earned=score
            )
            
            st.success(f"🎉 Correct! Well done! (+{score} points)")
            st.balloons()
            
        else:
            st.session_state.practice_streak = 0
            st.error(f"❌ Incorrect. The correct answer is: **{correct_answer}**")
            
            # Still update stats for incorrect answer
            self.scoring_system.update_player_stats(
                st.session_state.player_name,
                is_correct=False,
                difficulty_level=question['difficulty'],
                time_taken=time_taken,
                question_type=question['question_type'],
                score_earned=0
            )
        
        # Show explanation
        st.info(f"📝 **Explanation:** {question['question_data']['explanation']}")
        
        # Show time taken
        st.metric("⏱️ Time Taken", f"{time_taken:.1f} seconds")
        
        # Next question button
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("➡️ Next Question", use_container_width=True):
                st.session_state.practice_question = None
                st.session_state.practice_answer_submitted = False
                st.rerun()
        
        with col2:
            if st.button("🏠 Back to Home", use_container_width=True):
                # Update leaderboard before leaving
                self.leaderboard_manager.update_player_score(
                    st.session_state.player_name,
                    st.session_state.current_score,
                    st.session_state.difficulty_level,
                    'practice'
                )
                st.session_state.game_mode = "home"
                st.rerun()
    
    def _display_help_panel(self):
        """Display helpful information and tips"""
        st.subheader("🆘 Help & Tips")
        
        # Current difficulty info
        difficulty = st.session_state.difficulty_level
        st.info(f"**Current Level:** {difficulty} {'⭐' * difficulty}")
        
        # Level description
        level_descriptions = {
            1: "Basic rational functions with simple factors",
            2: "Moderate complexity with multiple factors",
            3: "Advanced functions with higher degrees",
            4: "Complex functions with multiple asymptotes",
            5: "Expert level with challenging compositions"
        }
        
        st.write(f"**Level {difficulty}:** {level_descriptions.get(difficulty, 'Unknown level')}")
        
        st.divider()
        
        # Quick reference
        st.subheader("📚 Quick Reference")
        
        with st.expander("🔍 Finding Vertical Asymptotes"):
            st.markdown("""
            1. Factor numerator and denominator
            2. Cancel common factors (these create holes)
            3. Set remaining denominator = 0
            4. Solve for x values
            """)
        
        with st.expander("📈 Finding Horizontal Asymptotes"):
            st.markdown("""
            - If degree(den) > degree(num): HA at y = 0
            - If degree(den) = degree(num): HA at y = ratio of leading coefficients
            - If degree(den) < degree(num): No horizontal asymptote
            """)
        
        with st.expander("🎯 Finding Intercepts"):
            st.markdown("""
            **X-intercepts:** Set numerator = 0, solve for x
            **Y-intercept:** Substitute x = 0 into function
            """)
        
        with st.expander("🕳️ Finding Holes"):
            st.markdown("""
            1. Factor numerator and denominator
            2. Look for common factors
            3. Cancel common factors
            4. Holes occur at x-values that make common factors = 0
            """)
