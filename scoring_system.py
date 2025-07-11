import streamlit as st
from datetime import datetime, timedelta
import json

class ScoringSystem:
    def __init__(self):
        self.base_points = {
            'correct_answer': 100,
            'quick_answer': 50,  # Bonus for answering quickly
            'streak_bonus': 25,  # Bonus for consecutive correct answers
            'difficulty_multiplier': {1: 1.0, 2: 1.2, 3: 1.5, 4: 1.8, 5: 2.0}
        }
        
        self.achievements = {
            'first_correct': {'name': '🎯 First Success!', 'description': 'Got your first answer correct', 'points': 50},
            'speed_demon': {'name': '⚡ Speed Demon', 'description': 'Answered 5 questions in under 5 seconds each', 'points': 200},
            'perfectionist': {'name': '💯 Perfectionist', 'description': 'Got 10 questions correct in a row', 'points': 500},
            'asymptote_master': {'name': '📈 Asymptote Master', 'description': 'Correctly identified 20 asymptotes', 'points': 300},
            'intercept_hunter': {'name': '🎯 Intercept Hunter', 'description': 'Found 15 intercepts correctly', 'points': 250},
            'hole_finder': {'name': '🕳️ Hole Finder', 'description': 'Identified 10 holes correctly', 'points': 200},
            'level_up': {'name': '📈 Level Up!', 'description': 'Reached a new difficulty level', 'points': 100}
        }
    
    def calculate_score(self, is_correct, difficulty_level, time_taken, current_streak, question_type=None):
        """Calculate score for a single question"""
        if not is_correct:
            return 0
        
        score = self.base_points['correct_answer']
        
        # Apply difficulty multiplier
        multiplier = self.base_points['difficulty_multiplier'].get(difficulty_level, 1.0)
        score *= multiplier
        
        # Quick answer bonus (under 5 seconds)
        if time_taken < 5:
            score += self.base_points['quick_answer']
        
        # Streak bonus
        if current_streak >= 3:
            streak_bonus = min(current_streak - 2, 10) * self.base_points['streak_bonus']
            score += streak_bonus
        
        return int(score)
    
    def check_achievements(self, player_stats):
        """Check for new achievements based on player statistics"""
        new_achievements = []
        
        # First correct answer
        if player_stats.get('total_correct', 0) == 1 and 'first_correct' not in player_stats.get('earned_achievements', []):
            new_achievements.append('first_correct')
        
        # Speed demon - 5 quick answers
        if player_stats.get('quick_answers', 0) >= 5 and 'speed_demon' not in player_stats.get('earned_achievements', []):
            new_achievements.append('speed_demon')
        
        # Perfectionist - 10 in a row
        if player_stats.get('max_streak', 0) >= 10 and 'perfectionist' not in player_stats.get('earned_achievements', []):
            new_achievements.append('perfectionist')
        
        # Asymptote master
        if player_stats.get('asymptotes_correct', 0) >= 20 and 'asymptote_master' not in player_stats.get('earned_achievements', []):
            new_achievements.append('asymptote_master')
        
        # Intercept hunter
        if player_stats.get('intercepts_correct', 0) >= 15 and 'intercept_hunter' not in player_stats.get('earned_achievements', []):
            new_achievements.append('intercept_hunter')
        
        # Hole finder
        if player_stats.get('holes_correct', 0) >= 10 and 'hole_finder' not in player_stats.get('earned_achievements', []):
            new_achievements.append('hole_finder')
        
        # Level up
        current_level = player_stats.get('current_level', 1)
        max_earned_level = player_stats.get('max_earned_level', 0)
        if current_level > max_earned_level:
            new_achievements.append('level_up')
            player_stats['max_earned_level'] = current_level
        
        return new_achievements
    
    def award_achievement(self, achievement_key):
        """Award an achievement to the player"""
        if achievement_key in self.achievements:
            achievement = self.achievements[achievement_key]
            
            # Add to session state achievements if not already there
            if achievement['name'] not in st.session_state.achievements:
                st.session_state.achievements.append(achievement['name'])
                st.session_state.current_score += achievement['points']
                return achievement
        
        return None
    
    def get_level_requirements(self, level):
        """Get the score requirements for reaching a specific level"""
        base_requirement = 1000
        return base_requirement * (level ** 1.5)
    
    def calculate_level_from_score(self, total_score):
        """Calculate the player's level based on their total score"""
        level = 1
        while total_score >= self.get_level_requirements(level + 1):
            level += 1
        return min(level, 5)  # Cap at level 5
    
    def get_progress_to_next_level(self, total_score, current_level):
        """Get progress percentage to next level"""
        if current_level >= 5:
            return 100  # Max level reached
        
        current_requirement = self.get_level_requirements(current_level)
        next_requirement = self.get_level_requirements(current_level + 1)
        
        progress = (total_score - current_requirement) / (next_requirement - current_requirement)
        return max(0, min(100, progress * 100))
    
    def update_player_stats(self, player_name, is_correct, difficulty_level, time_taken, question_type, score_earned):
        """Update comprehensive player statistics"""
        # Initialize session state stats if not exists
        if 'player_stats' not in st.session_state:
            st.session_state.player_stats = {}
        
        if player_name not in st.session_state.player_stats:
            st.session_state.player_stats[player_name] = {
                'total_questions': 0,
                'total_correct': 0,
                'total_score': 0,
                'total_time': 0,
                'quick_answers': 0,
                'current_streak': 0,
                'max_streak': 0,
                'current_level': 1,
                'max_earned_level': 0,
                'questions_by_type': {},
                'correct_by_type': {},
                'asymptotes_correct': 0,
                'intercepts_correct': 0,
                'holes_correct': 0,
                'earned_achievements': []
            }
        
        stats = st.session_state.player_stats[player_name]
        
        # Update basic stats
        stats['total_questions'] += 1
        stats['total_time'] += time_taken
        stats['total_score'] += score_earned
        
        if is_correct:
            stats['total_correct'] += 1
            stats['current_streak'] += 1
            stats['max_streak'] = max(stats['max_streak'], stats['current_streak'])
            
            if time_taken < 5:
                stats['quick_answers'] += 1
            
            # Update question type specific stats
            if question_type:
                if 'asymptote' in question_type.lower():
                    stats['asymptotes_correct'] += 1
                elif 'intercept' in question_type.lower():
                    stats['intercepts_correct'] += 1
                elif 'hole' in question_type.lower():
                    stats['holes_correct'] += 1
        else:
            stats['current_streak'] = 0
        
        # Update question type tracking
        if question_type:
            stats['questions_by_type'][question_type] = stats['questions_by_type'].get(question_type, 0) + 1
            if is_correct:
                stats['correct_by_type'][question_type] = stats['correct_by_type'].get(question_type, 0) + 1
        
        # Update level
        stats['current_level'] = self.calculate_level_from_score(stats['total_score'])
        
        # Check for achievements
        new_achievements = self.check_achievements(stats)
        for achievement_key in new_achievements:
            if achievement_key not in stats['earned_achievements']:
                stats['earned_achievements'].append(achievement_key)
                awarded = self.award_achievement(achievement_key)
                if awarded:
                    st.success(f"🏆 Achievement Unlocked: {awarded['name']}! (+{awarded['points']} points)")
        
        return stats
    
    def get_performance_analytics(self, player_name):
        """Get detailed performance analytics for a player"""
        if 'player_stats' not in st.session_state or player_name not in st.session_state.player_stats:
            return None
        
        stats = st.session_state.player_stats[player_name]
        
        analytics = {
            'accuracy': (stats['total_correct'] / max(stats['total_questions'], 1)) * 100,
            'avg_time': stats['total_time'] / max(stats['total_questions'], 1),
            'points_per_question': stats['total_score'] / max(stats['total_questions'], 1),
            'streak_efficiency': (stats['max_streak'] / max(stats['total_questions'], 1)) * 100,
            'quick_answer_rate': (stats['quick_answers'] / max(stats['total_correct'], 1)) * 100
        }
        
        # Question type performance
        type_performance = {}
        for q_type in stats['questions_by_type']:
            total = stats['questions_by_type'][q_type]
            correct = stats['correct_by_type'].get(q_type, 0)
            type_performance[q_type] = {
                'total': total,
                'correct': correct,
                'accuracy': (correct / total) * 100 if total > 0 else 0
            }
        
        analytics['type_performance'] = type_performance
        
        return analytics
