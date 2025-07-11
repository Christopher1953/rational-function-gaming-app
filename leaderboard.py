import pandas as pd
import streamlit as st
import json
import os
from datetime import datetime

class LeaderboardManager:
    def __init__(self, filename='leaderboard.json'):
        self.filename = filename
        self.leaderboard_data = self._load_leaderboard()
    
    def _load_leaderboard(self):
        """Load leaderboard data from file"""
        if os.path.exists(self.filename):
            try:
                with open(self.filename, 'r') as f:
                    return json.load(f)
            except:
                return {}
        return {}
    
    def _save_leaderboard(self):
        """Save leaderboard data to file"""
        try:
            with open(self.filename, 'w') as f:
                json.dump(self.leaderboard_data, f, indent=2)
        except:
            pass  # Silently fail if can't save
    
    def update_player_score(self, player_name, score, level, game_mode='general'):
        """Update a player's score in the leaderboard"""
        if player_name not in self.leaderboard_data:
            self.leaderboard_data[player_name] = {
                'total_score': 0,
                'games_played': 0,
                'best_score': 0,
                'max_level': 1,
                'last_played': None,
                'game_scores': []
            }
        
        player_data = self.leaderboard_data[player_name]
        
        # Update statistics
        player_data['total_score'] += score
        player_data['games_played'] += 1
        player_data['best_score'] = max(player_data['best_score'], score)
        player_data['max_level'] = max(player_data['max_level'], level)
        player_data['last_played'] = datetime.now().isoformat()
        
        # Add game score record
        game_record = {
            'score': score,
            'level': level,
            'mode': game_mode,
            'date': datetime.now().isoformat()
        }
        player_data['game_scores'].append(game_record)
        
        # Keep only last 50 game records to prevent file from growing too large
        if len(player_data['game_scores']) > 50:
            player_data['game_scores'] = player_data['game_scores'][-50:]
        
        self._save_leaderboard()
    
    def get_leaderboard(self, limit=None):
        """Get the current leaderboard as a pandas DataFrame"""
        if not self.leaderboard_data:
            return pd.DataFrame()
        
        # Convert to list of records
        records = []
        for player_name, data in self.leaderboard_data.items():
            records.append({
                'player_name': player_name,
                'total_score': data['total_score'],
                'games_played': data['games_played'],
                'best_score': data['best_score'],
                'max_level': data['max_level'],
                'avg_score': data['total_score'] / max(data['games_played'], 1),
                'last_played': data['last_played']
            })
        
        # Create DataFrame and sort by total score
        df = pd.DataFrame(records)
        df = df.sort_values('total_score', ascending=False).reset_index(drop=True)
        
        if limit:
            df = df.head(limit)
        
        return df
    
    def get_player_rank(self, player_name):
        """Get a player's current rank"""
        leaderboard = self.get_leaderboard()
        if leaderboard.empty:
            return None
        
        try:
            rank = leaderboard[leaderboard['player_name'] == player_name].index[0] + 1
            return rank
        except:
            return None
    
    def get_player_stats(self, player_name):
        """Get detailed statistics for a specific player"""
        if player_name not in self.leaderboard_data:
            return None
        
        data = self.leaderboard_data[player_name]
        
        # Calculate additional statistics
        stats = {
            'total_score': data['total_score'],
            'games_played': data['games_played'],
            'best_score': data['best_score'],
            'max_level': data['max_level'],
            'avg_score': data['total_score'] / max(data['games_played'], 1),
            'last_played': data['last_played']
        }
        
        # Recent performance (last 10 games)
        if data['game_scores']:
            recent_games = data['game_scores'][-10:]
            recent_scores = [game['score'] for game in recent_games]
            stats['recent_avg'] = sum(recent_scores) / len(recent_scores)
            stats['recent_best'] = max(recent_scores)
            stats['recent_games'] = len(recent_games)
        else:
            stats['recent_avg'] = 0
            stats['recent_best'] = 0
            stats['recent_games'] = 0
        
        return stats
    
    def get_top_players_by_category(self, category='total_score', limit=5):
        """Get top players by specific category"""
        leaderboard = self.get_leaderboard()
        if leaderboard.empty:
            return pd.DataFrame()
        
        if category in leaderboard.columns:
            return leaderboard.nlargest(limit, category)[['player_name', category]]
        return pd.DataFrame()
    
    def get_player_history(self, player_name, limit=20):
        """Get a player's game history"""
        if player_name not in self.leaderboard_data:
            return []
        
        game_scores = self.leaderboard_data[player_name]['game_scores']
        return game_scores[-limit:] if game_scores else []
    
    def reset_player_data(self, player_name):
        """Reset a specific player's data"""
        if player_name in self.leaderboard_data:
            del self.leaderboard_data[player_name]
            self._save_leaderboard()
    
    def get_leaderboard_summary(self):
        """Get summary statistics for the entire leaderboard"""
        if not self.leaderboard_data:
            return {
                'total_players': 0,
                'total_games': 0,
                'average_score': 0,
                'highest_score': 0,
                'most_active_player': None
            }
        
        total_players = len(self.leaderboard_data)
        total_games = sum(data['games_played'] for data in self.leaderboard_data.values())
        all_scores = [data['total_score'] for data in self.leaderboard_data.values()]
        average_score = sum(all_scores) / len(all_scores) if all_scores else 0
        highest_score = max(all_scores) if all_scores else 0
        
        # Find most active player
        most_active_player = max(
            self.leaderboard_data.items(),
            key=lambda x: x[1]['games_played']
        )[0] if self.leaderboard_data else None
        
        return {
            'total_players': total_players,
            'total_games': total_games,
            'average_score': average_score,
            'highest_score': highest_score,
            'most_active_player': most_active_player
        }
    
    def export_leaderboard_csv(self):
        """Export leaderboard to CSV format"""
        leaderboard = self.get_leaderboard()
        if not leaderboard.empty:
            return leaderboard.to_csv(index=False)
        return ""
