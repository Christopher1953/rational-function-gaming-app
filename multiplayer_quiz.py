import streamlit as st
import time
import random
import json
from datetime import datetime, timedelta
from utils.function_generator import RationalFunctionGenerator
from utils.graph_analyzer import GraphAnalyzer
from utils.scoring_system import ScoringSystem
from data.leaderboard import LeaderboardManager

class MultiplayerQuiz:
    def __init__(self):
        self.function_generator = RationalFunctionGenerator()
        self.graph_analyzer = GraphAnalyzer()
        self.scoring_system = ScoringSystem()
        self.leaderboard_manager = LeaderboardManager()
        
        # Quiz room configurations
        self.room_configs = {
            'quick': {'duration': 120, 'questions': 8, 'name': '⚡ Quick Quiz (2 min)'},
            'standard': {'duration': 300, 'questions': 15, 'name': '📊 Standard Quiz (5 min)'},
            'expert': {'duration': 600, 'questions': 20, 'name': '🧠 Expert Quiz (10 min)'}
        }
        
        # Initialize session state for multiplayer
        self._initialize_session_state()
    
    def _initialize_session_state(self):
        """Initialize all session state variables for multiplayer mode"""
        defaults = {
            'mp_room_id': None,
            'mp_room_type': None,
            'mp_players': [],
            'mp_current_question': 0,
            'mp_questions': [],
            'mp_answers': {},
            'mp_scores': {},
            'mp_start_time': None,
            'mp_active': False,
            'mp_finished': False,
            'mp_player_answered': False,
            'mp_waiting_for_players': False,
            'mp_final_results': None
        }
        
        for key, default_value in defaults.items():
            if key not in st.session_state:
                st.session_state[key] = default_value
    
    def run(self):
        st.title("👥 Multiplayer Quiz")
        st.markdown("**Compete with other players in real-time! Who will be the rational function master?**")
        
        if not st.session_state.mp_room_id:
            self._show_room_selection()
        elif st.session_state.mp_waiting_for_players:
            self._show_waiting_room()
        elif st.session_state.mp_active:
            self._run_active_quiz()
        elif st.session_state.mp_finished:
            self._show_multiplayer_results()
    
    def _show_room_selection(self):
        """Show room creation/joining interface"""
        st.subheader("🚪 Join or Create a Quiz Room")
        
        tab1, tab2 = st.tabs(["🆕 Create Room", "🔗 Join Room"])
        
        with tab1:
            st.markdown("### Create a New Quiz Room")
            
            # Room type selection
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.markdown("#### ⚡ Quick Quiz")
                st.write("Perfect for a quick challenge!")
                st.metric("Duration", "2 minutes")
                st.metric("Questions", "8")
                
                if st.button("Create Quick Room", key="create_quick", use_container_width=True):
                    self._create_room('quick')
            
            with col2:
                st.markdown("#### 📊 Standard Quiz")
                st.write("Balanced challenge for most players")
                st.metric("Duration", "5 minutes")
                st.metric("Questions", "15")
                
                if st.button("Create Standard Room", key="create_standard", use_container_width=True):
                    self._create_room('standard')
            
            with col3:
                st.markdown("#### 🧠 Expert Quiz")
                st.write("For rational function masters!")
                st.metric("Duration", "10 minutes")
                st.metric("Questions", "20")
                
                if st.button("Create Expert Room", key="create_expert", use_container_width=True):
                    self._create_room('expert')
        
        with tab2:
            st.markdown("### Join an Existing Room")
            
            room_id = st.text_input("Enter Room ID:", placeholder="e.g., ROOM123")
            
            if st.button("Join Room", disabled=not room_id):
                self._join_room(room_id.upper())
            
            st.info("💡 Ask the room creator for the Room ID to join their quiz!")
        
        # Show active rooms (simulated)
        st.subheader("🔥 Recently Active Rooms")
        self._show_mock_active_rooms()
    
    def _create_room(self, room_type):
        """Create a new quiz room"""
        # Generate a unique room ID
        room_id = f"ROOM{random.randint(1000, 9999)}"
        
        st.session_state.mp_room_id = room_id
        st.session_state.mp_room_type = room_type
        st.session_state.mp_players = [st.session_state.player_name]
        st.session_state.mp_waiting_for_players = True
        
        # Generate questions for the room
        config = self.room_configs[room_type]
        self._generate_quiz_questions(config['questions'])
        
        st.success(f"🎉 Room created! Room ID: **{room_id}**")
        st.info("Share this Room ID with other players so they can join!")
        
        time.sleep(2)
        st.rerun()
    
    def _join_room(self, room_id):
        """Join an existing quiz room"""
        # Simulate joining a room (in a real app, this would check a database)
        mock_rooms = {
            "ROOM1234": {"type": "standard", "players": ["Alice", "Bob"]},
            "ROOM5678": {"type": "quick", "players": ["Charlie"]},
            "ROOM9999": {"type": "expert", "players": ["Expert1", "Expert2", "Expert3"]}
        }
        
        if room_id in mock_rooms:
            room_data = mock_rooms[room_id]
            
            if st.session_state.player_name not in room_data["players"]:
                st.session_state.mp_room_id = room_id
                st.session_state.mp_room_type = room_data["type"]
                st.session_state.mp_players = room_data["players"] + [st.session_state.player_name]
                st.session_state.mp_waiting_for_players = True
                
                # Generate questions
                config = self.room_configs[room_data["type"]]
                self._generate_quiz_questions(config['questions'])
                
                st.success(f"✅ Joined room {room_id}!")
                time.sleep(1)
                st.rerun()
            else:
                st.error("You're already in this room!")
        else:
            st.error("❌ Room not found. Please check the Room ID.")
    
    def _generate_quiz_questions(self, num_questions):
        """Generate questions for the multiplayer quiz"""
        st.session_state.mp_questions = []
        
        for i in range(num_questions):
            # Progressive difficulty
            if i < num_questions // 3:
                difficulty = random.randint(1, 2)
            elif i < (2 * num_questions) // 3:
                difficulty = random.randint(2, 4)
            else:
                difficulty = random.randint(3, 5)
            
            function_dict = self.function_generator.generate_function(difficulty)
            analysis = self.function_generator.analyze_function(function_dict)
            question_data = self.function_generator.generate_multiple_choice_question(
                function_dict, analysis, None
            )
            
            st.session_state.mp_questions.append({
                'function_dict': function_dict,
                'analysis': analysis,
                'question_data': question_data,
                'difficulty': difficulty,
                'number': i + 1
            })
    
    def _show_waiting_room(self):
        """Show waiting room before quiz starts"""
        config = self.room_configs[st.session_state.mp_room_type]
        
        st.subheader(f"🚪 Waiting Room - {config['name']}")
        
        # Room info
        col1, col2 = st.columns(2)
        
        with col1:
            st.info(f"**Room ID:** {st.session_state.mp_room_id}")
            st.metric("Quiz Duration", f"{config['duration']//60} minutes")
            st.metric("Total Questions", config['questions'])
        
        with col2:
            st.subheader("👥 Players in Room")
            for i, player in enumerate(st.session_state.mp_players):
                if player == st.session_state.player_name:
                    st.write(f"{i+1}. **{player} (You)** 👤")
                else:
                    st.write(f"{i+1}. {player}")
        
        # Start button for room creator (first player)
        if st.session_state.mp_players[0] == st.session_state.player_name:
            if len(st.session_state.mp_players) >= 2:
                if st.button("🚀 Start Quiz", use_container_width=True):
                    self._start_multiplayer_quiz()
            else:
                st.warning("⏳ Waiting for at least one more player to join...")
                
                # Allow single player start for demo
                if st.button("🤖 Start with AI Players", use_container_width=True):
                    self._add_ai_players()
                    self._start_multiplayer_quiz()
        else:
            st.info("⏳ Waiting for the room creator to start the quiz...")
        
        # Auto-refresh waiting room
        time.sleep(1)
        st.rerun()
    
    def _add_ai_players(self):
        """Add AI players for demo purposes"""
        ai_names = ["MathBot", "GraphGuru", "AsymptoteAce", "FunctionFinder"]
        num_ai = random.randint(1, 3)
        
        for i in range(num_ai):
            if len(st.session_state.mp_players) < 4:  # Max 4 players
                ai_name = random.choice(ai_names)
                if ai_name not in st.session_state.mp_players:
                    st.session_state.mp_players.append(ai_name)
    
    def _start_multiplayer_quiz(self):
        """Start the multiplayer quiz"""
        st.session_state.mp_waiting_for_players = False
        st.session_state.mp_active = True
        st.session_state.mp_start_time = time.time()
        st.session_state.mp_current_question = 0
        st.session_state.mp_player_answered = False
        
        # Initialize scores for all players
        st.session_state.mp_scores = {player: 0 for player in st.session_state.mp_players}
        st.session_state.mp_answers = {player: [] for player in st.session_state.mp_players}
        
        st.rerun()
    
    def _run_active_quiz(self):
        """Run the active multiplayer quiz"""
        config = self.room_configs[st.session_state.mp_room_type]
        
        # Calculate remaining time
        elapsed_time = time.time() - st.session_state.mp_start_time
        remaining_time = max(0, config['duration'] - elapsed_time)
        
        # Check if quiz should end
        if remaining_time <= 0 or st.session_state.mp_current_question >= len(st.session_state.mp_questions):
            self._end_multiplayer_quiz()
            return
        
        # Display quiz header
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("⏰ Time Left", f"{remaining_time:.0f}s")
        
        with col2:
            progress = (st.session_state.mp_current_question + 1) / len(st.session_state.mp_questions)
            st.metric("📊 Progress", f"{st.session_state.mp_current_question + 1}/{len(st.session_state.mp_questions)}")
            st.progress(progress)
        
        with col3:
            current_score = st.session_state.mp_scores.get(st.session_state.player_name, 0)
            st.metric("🎯 Your Score", current_score)
        
        # Show current leaderboard
        self._show_current_leaderboard()
        
        # Display current question
        if st.session_state.mp_current_question < len(st.session_state.mp_questions):
            current_q = st.session_state.mp_questions[st.session_state.mp_current_question]
            
            st.subheader(f"❓ Question {current_q['number']}")
            
            # Show function and question
            col1, col2 = st.columns([3, 1])
            
            with col1:
                st.write(f"**Function:** f(x) = {current_q['function_dict']['function_str']}")
                st.write(f"**Question:** {current_q['question_data']['question']}")
                
                if not st.session_state.mp_player_answered:
                    # Answer input
                    with st.form(f"mp_question_{st.session_state.mp_current_question}"):
                        choices = current_q['question_data']['choices']
                        selected_answer = st.radio(
                            "Your answer:",
                            options=choices,
                            key=f"mp_answer_{st.session_state.mp_current_question}"
                        )
                        
                        submitted = st.form_submit_button("Submit Answer ⚡", use_container_width=True)
                        
                        if submitted:
                            self._submit_multiplayer_answer(selected_answer, current_q)
                else:
                    st.success("✅ Answer submitted! Waiting for other players...")
                    
                    # Show what you answered
                    player_answers = st.session_state.mp_answers[st.session_state.player_name]
                    if player_answers:
                        last_answer = player_answers[-1]
                        st.info(f"Your answer: **{last_answer['user_answer']}**")
            
            with col2:
                # Show mini graph
                try:
                    fig = self.graph_analyzer.create_interactive_graph(
                        current_q['function_dict'],
                        current_q['analysis'],
                        x_range=(-5, 5),
                        y_range=(-5, 5)
                    )
                    fig.update_layout(height=300, margin=dict(l=20, r=20, t=30, b=20))
                    st.plotly_chart(fig, use_container_width=True)
                except:
                    st.info("Graph loading...")
        
        # Simulate other players answering
        self._simulate_ai_answers()
        
        # Auto advance when time is up or all answered
        if self._check_all_players_answered() or remaining_time <= 0:
            time.sleep(2)  # Brief pause to show results
            self._advance_to_next_question()
    
    def _submit_multiplayer_answer(self, selected_answer, current_q):
        """Submit answer for current player"""
        correct_answer = current_q['question_data']['correct_answer']
        is_correct = selected_answer == correct_answer
        
        # Calculate time taken for this question
        question_start_time = st.session_state.mp_start_time + (st.session_state.mp_current_question * 30)  # Estimate
        time_taken = max(1, time.time() - question_start_time)
        
        # Calculate score
        current_streak = len([ans for ans in st.session_state.mp_answers[st.session_state.player_name] if ans['correct']])
        score = self.scoring_system.calculate_score(
            is_correct=is_correct,
            difficulty_level=current_q['difficulty'],
            time_taken=time_taken,
            current_streak=current_streak
        ) if is_correct else 0
        
        # Store answer
        answer_data = {
            'question_number': st.session_state.mp_current_question,
            'user_answer': selected_answer,
            'correct_answer': correct_answer,
            'correct': is_correct,
            'time_taken': time_taken,
            'score': score
        }
        
        st.session_state.mp_answers[st.session_state.player_name].append(answer_data)
        st.session_state.mp_scores[st.session_state.player_name] += score
        st.session_state.mp_player_answered = True
        
        # Show immediate feedback
        if is_correct:
            st.success(f"🎉 Correct! +{score} points")
        else:
            st.error(f"❌ Incorrect. Correct answer: {correct_answer}")
        
        st.rerun()
    
    def _simulate_ai_answers(self):
        """Simulate AI players answering questions"""
        current_q = st.session_state.mp_questions[st.session_state.mp_current_question]
        
        for player in st.session_state.mp_players:
            if player == st.session_state.player_name:
                continue
            
            # Check if this AI player has already answered this question
            player_answers = st.session_state.mp_answers.get(player, [])
            already_answered = any(ans['question_number'] == st.session_state.mp_current_question for ans in player_answers)
            
            if not already_answered and random.random() < 0.3:  # 30% chance each refresh
                # AI answers with varying accuracy based on difficulty
                accuracy = max(0.4, 1.0 - (current_q['difficulty'] * 0.15))  # Harder questions = lower AI accuracy
                
                if random.random() < accuracy:
                    ai_answer = current_q['question_data']['correct_answer']
                    is_correct = True
                else:
                    wrong_choices = [choice for choice in current_q['question_data']['choices'] 
                                   if choice != current_q['question_data']['correct_answer']]
                    ai_answer = random.choice(wrong_choices)
                    is_correct = False
                
                # Calculate AI score
                ai_time = random.uniform(3, 15)  # AI takes 3-15 seconds
                ai_streak = len([ans for ans in player_answers if ans['correct']])
                ai_score = self.scoring_system.calculate_score(
                    is_correct=is_correct,
                    difficulty_level=current_q['difficulty'],
                    time_taken=ai_time,
                    current_streak=ai_streak
                ) if is_correct else 0
                
                # Store AI answer
                ai_answer_data = {
                    'question_number': st.session_state.mp_current_question,
                    'user_answer': ai_answer,
                    'correct_answer': current_q['question_data']['correct_answer'],
                    'correct': is_correct,
                    'time_taken': ai_time,
                    'score': ai_score
                }
                
                if player not in st.session_state.mp_answers:
                    st.session_state.mp_answers[player] = []
                
                st.session_state.mp_answers[player].append(ai_answer_data)
                st.session_state.mp_scores[player] += ai_score
    
    def _check_all_players_answered(self):
        """Check if all players have answered the current question"""
        for player in st.session_state.mp_players:
            player_answers = st.session_state.mp_answers.get(player, [])
            current_q_answered = any(ans['question_number'] == st.session_state.mp_current_question for ans in player_answers)
            if not current_q_answered:
                return False
        return True
    
    def _advance_to_next_question(self):
        """Advance to the next question"""
        st.session_state.mp_current_question += 1
        st.session_state.mp_player_answered = False
        
        if st.session_state.mp_current_question >= len(st.session_state.mp_questions):
            self._end_multiplayer_quiz()
        else:
            st.rerun()
    
    def _show_current_leaderboard(self):
        """Show current standings during the quiz"""
        with st.expander("🏆 Current Standings", expanded=False):
            # Sort players by score
            sorted_players = sorted(
                st.session_state.mp_scores.items(),
                key=lambda x: x[1],
                reverse=True
            )
            
            for i, (player, score) in enumerate(sorted_players):
                if player == st.session_state.player_name:
                    st.write(f"**{i+1}. {player} (You): {score} points** 👤")
                else:
                    st.write(f"{i+1}. {player}: {score} points")
    
    def _end_multiplayer_quiz(self):
        """End the multiplayer quiz"""
        st.session_state.mp_active = False
        st.session_state.mp_finished = True
        
        # Calculate final results
        final_results = []
        for player in st.session_state.mp_players:
            player_answers = st.session_state.mp_answers.get(player, [])
            total_score = st.session_state.mp_scores.get(player, 0)
            correct_count = len([ans for ans in player_answers if ans['correct']])
            
            final_results.append({
                'player': player,
                'score': total_score,
                'correct': correct_count,
                'total': len(player_answers),
                'accuracy': (correct_count / max(len(player_answers), 1)) * 100
            })
        
        # Sort by score
        final_results.sort(key=lambda x: x['score'], reverse=True)
        st.session_state.mp_final_results = final_results
        
        # Update personal stats and leaderboard
        player_total_score = st.session_state.mp_scores.get(st.session_state.player_name, 0)
        st.session_state.current_score += player_total_score
        
        self.leaderboard_manager.update_player_score(
            st.session_state.player_name,
            player_total_score,
            st.session_state.difficulty_level,
            f'multiplayer_{st.session_state.mp_room_type}'
        )
        
        st.rerun()
    
    def _show_multiplayer_results(self):
        """Show final multiplayer quiz results"""
        st.subheader(f"🏁 Quiz Complete - Room {st.session_state.mp_room_id}")
        
        config = self.room_configs[st.session_state.mp_room_type]
        st.write(f"**Quiz Type:** {config['name']}")
        
        # Final leaderboard
        st.subheader("🏆 Final Results")
        
        for i, result in enumerate(st.session_state.mp_final_results):
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
                if result['player'] == st.session_state.player_name:
                    st.markdown(f"**{result['player']} (You)**")
                else:
                    st.write(result['player'])
            
            with col3:
                st.write(f"{result['score']:,} pts")
            
            with col4:
                st.write(f"{result['correct']}/{result['total']} ({result['accuracy']:.1f}%)")
        
        # Personal performance summary
        player_result = next((r for r in st.session_state.mp_final_results if r['player'] == st.session_state.player_name), None)
        
        if player_result:
            st.subheader("📊 Your Performance")
            
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                placement = next(i for i, r in enumerate(st.session_state.mp_final_results) if r['player'] == st.session_state.player_name) + 1
                st.metric("🏆 Placement", f"{placement}/{len(st.session_state.mp_final_results)}")
            
            with col2:
                st.metric("🎯 Final Score", f"{player_result['score']:,}")
            
            with col3:
                st.metric("✅ Accuracy", f"{player_result['accuracy']:.1f}%")
            
            with col4:
                st.metric("❓ Answered", f"{player_result['total']}/{len(st.session_state.mp_questions)}")
        
        # Victory message
        if st.session_state.mp_final_results[0]['player'] == st.session_state.player_name:
            st.success("🎉 Congratulations! You won the quiz! 🏆")
            st.balloons()
        elif len(st.session_state.mp_final_results) > 1 and st.session_state.mp_final_results[1]['player'] == st.session_state.player_name:
            st.success("🥈 Great job! Second place! Keep it up!")
        elif len(st.session_state.mp_final_results) > 2 and st.session_state.mp_final_results[2]['player'] == st.session_state.player_name:
            st.success("🥉 Well done! Third place is still awesome!")
        else:
            st.info("Good effort! Practice more to improve your ranking!")
        
        # Action buttons
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("🔄 Play Again", use_container_width=True):
                self._reset_multiplayer_state()
                st.rerun()
        
        with col2:
            if st.button("📚 Practice Mode", use_container_width=True):
                st.session_state.game_mode = "practice"
                st.rerun()
        
        with col3:
            if st.button("🏠 Home", use_container_width=True):
                st.session_state.game_mode = "home"
                st.rerun()
    
    def _reset_multiplayer_state(self):
        """Reset multiplayer session state"""
        mp_keys = [key for key in st.session_state.keys() if key.startswith('mp_')]
        for key in mp_keys:
            del st.session_state[key]
        self._initialize_session_state()
    
    def _show_mock_active_rooms(self):
        """Show mock active rooms for demonstration"""
        mock_rooms = [
            {"id": "ROOM1234", "type": "Standard Quiz", "players": 3, "status": "Starting Soon"},
            {"id": "ROOM5678", "type": "Quick Quiz", "players": 2, "status": "In Progress"},
            {"id": "ROOM9999", "type": "Expert Quiz", "players": 4, "status": "Waiting for Players"}
        ]
        
        for room in mock_rooms:
            col1, col2, col3, col4 = st.columns([1, 2, 1, 1])
            
            with col1:
                st.write(f"**{room['id']}**")
            
            with col2:
                st.write(room['type'])
            
            with col3:
                st.write(f"{room['players']}/4 players")
            
            with col4:
                if room['status'] == "Waiting for Players":
                    if st.button("Join", key=f"join_{room['id']}", use_container_width=True):
                        self._join_room(room['id'])
                else:
                    st.write(room['status'])
