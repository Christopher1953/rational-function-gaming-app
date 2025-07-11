import streamlit as st
import time
import random
from utils.function_generator import RationalFunctionGenerator
from utils.graph_analyzer import GraphAnalyzer
from utils.scoring_system import ScoringSystem
from data.leaderboard import LeaderboardManager

class TimedChallenge:
    def __init__(self):
        self.function_generator = RationalFunctionGenerator()
        self.graph_analyzer = GraphAnalyzer()
        self.scoring_system = ScoringSystem()
        self.leaderboard_manager = LeaderboardManager()
        
        # Challenge configurations
        self.challenge_configs = {
            'sprint': {'duration': 60, 'questions': 10, 'name': '⚡ 1-Minute Sprint'},
            'marathon': {'duration': 300, 'questions': 25, 'name': '🏃 5-Minute Marathon'},
            'blitz': {'duration': 30, 'questions': 5, 'name': '💨 30-Second Blitz'}
        }
        
        # Initialize session state
        if 'timed_mode' not in st.session_state:
            st.session_state.timed_mode = None
        if 'timed_active' not in st.session_state:
            st.session_state.timed_active = False
        if 'timed_start_time' not in st.session_state:
            st.session_state.timed_start_time = None
        if 'timed_questions' not in st.session_state:
            st.session_state.timed_questions = []
        if 'timed_current_question' not in st.session_state:
            st.session_state.timed_current_question = 0
        if 'timed_answers' not in st.session_state:
            st.session_state.timed_answers = []
        if 'timed_scores' not in st.session_state:
            st.session_state.timed_scores = []
        if 'timed_finished' not in st.session_state:
            st.session_state.timed_finished = False
    
    def run(self):
        st.title("⏰ Timed Challenge")
        st.markdown("**Test your skills against the clock! Quick thinking and accuracy are key.**")
        
        if not st.session_state.timed_active and not st.session_state.timed_finished:
            self._show_challenge_selection()
        elif st.session_state.timed_active:
            self._run_active_challenge()
        elif st.session_state.timed_finished:
            self._show_results()
    
    def _show_challenge_selection(self):
        """Show challenge type selection screen"""
        st.subheader("🎯 Choose Your Challenge")
        
        # Challenge descriptions
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("### 💨 30-Second Blitz")
            st.write("Quick fire questions for speed demons!")
            st.metric("Duration", "30 seconds")
            st.metric("Questions", "5")
            st.metric("Difficulty", "Mixed")
            
            if st.button("Start Blitz", key="blitz", use_container_width=True):
                self._start_challenge('blitz')
        
        with col2:
            st.markdown("### ⚡ 1-Minute Sprint")
            st.write("Perfect balance of speed and accuracy!")
            st.metric("Duration", "1 minute")
            st.metric("Questions", "10")
            st.metric("Difficulty", "Progressive")
            
            if st.button("Start Sprint", key="sprint", use_container_width=True):
                self._start_challenge('sprint')
        
        with col3:
            st.markdown("### 🏃 5-Minute Marathon")
            st.write("Endurance test for rational function masters!")
            st.metric("Duration", "5 minutes")
            st.metric("Questions", "25")
            st.metric("Difficulty", "Challenging")
            
            if st.button("Start Marathon", key="marathon", use_container_width=True):
                self._start_challenge('marathon')
        
        st.divider()
        
        # Best times/scores
        st.subheader("🏆 Your Best Times")
        self._display_personal_bests()
        
        # Instructions
        st.subheader("📋 Instructions")
        st.markdown("""
        - Answer as many questions correctly as possible within the time limit
        - Each correct answer earns points based on difficulty and speed
        - Quick answers (under 5 seconds) earn bonus points
        - Consecutive correct answers create streak multipliers
        - The challenge ends when time runs out OR all questions are answered
        """)
    
    def _start_challenge(self, challenge_type):
        """Start a timed challenge"""
        config = self.challenge_configs[challenge_type]
        
        # Reset session state
        st.session_state.timed_mode = challenge_type
        st.session_state.timed_active = True
        st.session_state.timed_start_time = time.time()
        st.session_state.timed_current_question = 0
        st.session_state.timed_answers = []
        st.session_state.timed_scores = []
        st.session_state.timed_finished = False
        
        # Generate all questions at once
        st.session_state.timed_questions = []
        for i in range(config['questions']):
            # Progressive difficulty for some challenges
            if challenge_type == 'sprint':
                difficulty = min(5, (i // 2) + 1)
            elif challenge_type == 'marathon':
                difficulty = min(5, (i // 5) + 1)
            else:  # blitz
                difficulty = random.randint(1, 3)
            
            function_dict = self.function_generator.generate_function(difficulty)
            analysis = self.function_generator.analyze_function(function_dict)
            question_data = self.function_generator.generate_multiple_choice_question(
                function_dict, analysis, None  # Random question type
            )
            
            st.session_state.timed_questions.append({
                'function_dict': function_dict,
                'analysis': analysis,
                'question_data': question_data,
                'difficulty': difficulty
            })
        
        st.rerun()
    
    def _run_active_challenge(self):
        """Run the active timed challenge"""
        config = self.challenge_configs[st.session_state.timed_mode]
        
        # Calculate remaining time
        elapsed_time = time.time() - st.session_state.timed_start_time
        remaining_time = max(0, config['duration'] - elapsed_time)
        
        # Check if challenge should end
        if remaining_time <= 0 or st.session_state.timed_current_question >= len(st.session_state.timed_questions):
            self._end_challenge()
            return
        
        # Display timer and progress
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("⏰ Time Remaining", f"{remaining_time:.1f}s")
        
        with col2:
            progress = (st.session_state.timed_current_question + 1) / len(st.session_state.timed_questions)
            st.metric("📊 Progress", f"{st.session_state.timed_current_question + 1}/{len(st.session_state.timed_questions)}")
            st.progress(progress)
        
        with col3:
            current_score = sum(st.session_state.timed_scores)
            st.metric("🎯 Score", current_score)
        
        # Display current question
        current_q = st.session_state.timed_questions[st.session_state.timed_current_question]
        
        st.subheader(f"❓ Question {st.session_state.timed_current_question + 1}")
        
        # Show function (smaller to save space)
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.write(f"**Function:** f(x) = {current_q['function_dict']['function_str']}")
            st.write(f"**Question:** {current_q['question_data']['question']}")
            
            # Answer choices
            choices = current_q['question_data']['choices']
            
            # Use a form for immediate submission
            with st.form(f"question_{st.session_state.timed_current_question}"):
                selected_answer = st.radio(
                    "Your answer:",
                    options=choices,
                    key=f"timed_answer_{st.session_state.timed_current_question}"
                )
                
                submitted = st.form_submit_button("Submit Answer ⚡", use_container_width=True)
                
                if submitted:
                    self._process_answer(selected_answer)
        
        with col2:
            # Quick reference card
            st.markdown("### 🚀 Quick Tips")
            st.markdown("""
            - **VA**: Den = 0, Num ≠ 0
            - **HA**: Compare degrees
            - **X-int**: Num = 0, Den ≠ 0
            - **Holes**: Common factors
            """)
            
            # Show small graph if time allows
            if remaining_time > 10:  # Only show graph if more than 10 seconds left
                try:
                    fig = self.graph_analyzer.create_interactive_graph(
                        current_q['function_dict'],
                        current_q['analysis'],
                        x_range=(-5, 5),
                        y_range=(-5, 5)
                    )
                    fig.update_layout(height=300)
                    st.plotly_chart(fig, use_container_width=True)
                except:
                    st.info("Graph available after question")
        
        # Auto-refresh for timer
        time.sleep(0.1)
        st.rerun()
    
    def _process_answer(self, selected_answer):
        """Process the submitted answer"""
        current_q = st.session_state.timed_questions[st.session_state.timed_current_question]
        correct_answer = current_q['question_data']['correct_answer']
        
        # Calculate time for this question
        if st.session_state.timed_current_question == 0:
            question_start_time = st.session_state.timed_start_time
        else:
            # Estimate time based on total elapsed and questions answered
            total_elapsed = time.time() - st.session_state.timed_start_time
            avg_time_per_question = total_elapsed / (st.session_state.timed_current_question + 1)
            question_start_time = time.time() - avg_time_per_question
        
        time_taken = time.time() - question_start_time
        
        # Check correctness
        is_correct = selected_answer == correct_answer
        
        # Calculate score
        current_streak = len([ans for ans in st.session_state.timed_answers if ans['correct']]) if is_correct else 0
        
        score = self.scoring_system.calculate_score(
            is_correct=is_correct,
            difficulty_level=current_q['difficulty'],
            time_taken=time_taken,
            current_streak=current_streak
        ) if is_correct else 0
        
        # Store answer and score
        st.session_state.timed_answers.append({
            'question_index': st.session_state.timed_current_question,
            'user_answer': selected_answer,
            'correct_answer': correct_answer,
            'correct': is_correct,
            'time_taken': time_taken,
            'score': score
        })
        
        st.session_state.timed_scores.append(score)
        
        # Move to next question
        st.session_state.timed_current_question += 1
        
        # Check if challenge should end
        if st.session_state.timed_current_question >= len(st.session_state.timed_questions):
            self._end_challenge()
        else:
            st.rerun()
    
    def _end_challenge(self):
        """End the current challenge"""
        st.session_state.timed_active = False
        st.session_state.timed_finished = True
        
        # Calculate final statistics
        total_score = sum(st.session_state.timed_scores)
        total_time = time.time() - st.session_state.timed_start_time
        questions_answered = len(st.session_state.timed_answers)
        correct_answers = len([ans for ans in st.session_state.timed_answers if ans['correct']])
        
        # Update player statistics
        self.scoring_system.update_player_stats(
            st.session_state.player_name,
            is_correct=True,  # Overall performance metric
            difficulty_level=st.session_state.difficulty_level,
            time_taken=total_time,
            question_type='timed_challenge',
            score_earned=total_score
        )
        
        # Update leaderboard
        self.leaderboard_manager.update_player_score(
            st.session_state.player_name,
            total_score,
            st.session_state.difficulty_level,
            f'timed_{st.session_state.timed_mode}'
        )
        
        # Add to current session score
        st.session_state.current_score += total_score
        
        st.rerun()
    
    def _show_results(self):
        """Show challenge results"""
        config = self.challenge_configs[st.session_state.timed_mode]
        
        st.subheader(f"🏁 {config['name']} Complete!")
        
        # Calculate statistics
        total_score = sum(st.session_state.timed_scores)
        questions_answered = len(st.session_state.timed_answers)
        correct_answers = len([ans for ans in st.session_state.timed_answers if ans['correct']])
        accuracy = (correct_answers / max(questions_answered, 1)) * 100
        total_time = time.time() - st.session_state.timed_start_time if st.session_state.timed_start_time else config['duration']
        avg_time = total_time / max(questions_answered, 1)
        
        # Display key metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("🎯 Final Score", f"{total_score:,}")
        
        with col2:
            st.metric("✅ Accuracy", f"{accuracy:.1f}%")
        
        with col3:
            st.metric("⏱️ Avg Time/Question", f"{avg_time:.1f}s")
        
        with col4:
            st.metric("❓ Questions Answered", f"{questions_answered}/{len(st.session_state.timed_questions)}")
        
        # Performance analysis
        st.subheader("📊 Performance Analysis")
        
        if st.session_state.timed_answers:
            # Accuracy by question type
            question_types = {}
            for i, answer in enumerate(st.session_state.timed_answers):
                q = st.session_state.timed_questions[answer['question_index']]
                q_type = q['question_data']['question'].split()[0]  # First word as type indicator
                
                if q_type not in question_types:
                    question_types[q_type] = {'correct': 0, 'total': 0}
                
                question_types[q_type]['total'] += 1
                if answer['correct']:
                    question_types[q_type]['correct'] += 1
            
            # Display performance by type
            for q_type, stats in question_types.items():
                accuracy = (stats['correct'] / stats['total']) * 100
                st.write(f"**{q_type}:** {stats['correct']}/{stats['total']} ({accuracy:.1f}%)")
        
        # Detailed results
        with st.expander("📋 Detailed Results"):
            for i, answer in enumerate(st.session_state.timed_answers):
                q = st.session_state.timed_questions[answer['question_index']]
                status = "✅" if answer['correct'] else "❌"
                
                st.write(f"**Q{i+1}** {status} Score: {answer['score']} | Time: {answer['time_taken']:.1f}s")
                st.write(f"   Function: {q['function_dict']['function_str']}")
                st.write(f"   Your answer: {answer['user_answer']} | Correct: {answer['correct_answer']}")
                st.write("---")
        
        # Achievements and feedback
        if accuracy >= 90:
            st.success("🏆 Excellent performance! You're a rational function expert!")
            st.balloons()
        elif accuracy >= 75:
            st.success("🎉 Great job! You're getting the hang of this!")
        elif accuracy >= 50:
            st.info("👍 Good effort! Keep practicing to improve your accuracy.")
        else:
            st.info("📚 Don't worry! Practice makes perfect. Try the practice mode to build your skills.")
        
        # Action buttons
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("🔄 Try Again", use_container_width=True):
                # Reset for new challenge
                st.session_state.timed_mode = None
                st.session_state.timed_finished = False
                st.session_state.timed_questions = []
                st.session_state.timed_answers = []
                st.session_state.timed_scores = []
                st.rerun()
        
        with col2:
            if st.button("📚 Practice Mode", use_container_width=True):
                st.session_state.game_mode = "practice"
                st.rerun()
        
        with col3:
            if st.button("🏠 Home", use_container_width=True):
                st.session_state.game_mode = "home"
                st.rerun()
    
    def _display_personal_bests(self):
        """Display player's personal best times and scores"""
        player_stats = self.leaderboard_manager.get_player_stats(st.session_state.player_name)
        
        if player_stats:
            history = self.leaderboard_manager.get_player_history(st.session_state.player_name)
            
            # Filter timed challenges
            timed_games = [game for game in history if game['mode'].startswith('timed_')]
            
            if timed_games:
                # Best scores by challenge type
                best_scores = {}
                for game in timed_games:
                    mode = game['mode'].replace('timed_', '')
                    if mode not in best_scores or game['score'] > best_scores[mode]['score']:
                        best_scores[mode] = game
                
                col1, col2, col3 = st.columns(3)
                
                challenge_names = {
                    'blitz': '💨 Blitz',
                    'sprint': '⚡ Sprint', 
                    'marathon': '🏃 Marathon'
                }
                
                for i, (mode, game) in enumerate(best_scores.items()):
                    with [col1, col2, col3][i % 3]:
                        st.metric(
                            challenge_names.get(mode, mode.title()),
                            f"{game['score']:,} pts"
                        )
            else:
                st.info("No timed challenges completed yet. Start your first challenge above!")
        else:
            st.info("Complete your first challenge to see your best times!")
