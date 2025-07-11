import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import sympy as sp

class GraphAnalyzer:
    def __init__(self):
        self.x = sp.symbols('x')
    
    def create_interactive_graph(self, function_dict, analysis, x_range=(-10, 10), y_range=(-10, 10)):
        """Create an interactive Plotly graph of the rational function"""
        
        # Generate x values for plotting
        x_vals = np.linspace(x_range[0], x_range[1], 1000)
        
        # Convert sympy function to numpy-evaluable function
        func = function_dict['function']
        func_lambdified = sp.lambdify(self.x, func, 'numpy')
        
        # Calculate y values, handling asymptotes
        y_vals = []
        for x_val in x_vals:
            try:
                y_val = func_lambdified(x_val)
                # Handle very large values near asymptotes
                if abs(y_val) > 1000:
                    y_vals.append(np.nan)
                else:
                    y_vals.append(y_val)
            except:
                y_vals.append(np.nan)
        
        y_vals = np.array(y_vals)
        
        # Create the main plot
        fig = go.Figure()
        
        # Add the function curve
        fig.add_trace(go.Scatter(
            x=x_vals,
            y=y_vals,
            mode='lines',
            name=f'f(x) = {function_dict["function_str"]}',
            line=dict(color='blue', width=3),
            connectgaps=False
        ))
        
        # Add vertical asymptotes
        for va in analysis['vertical_asymptotes']:
            fig.add_vline(
                x=va,
                line_dash="dash",
                line_color="red",
                annotation_text=f"x = {va}",
                annotation_position="top"
            )
        
        # Add horizontal asymptote
        if analysis['horizontal_asymptote'] is not None:
            fig.add_hline(
                y=analysis['horizontal_asymptote'],
                line_dash="dash",
                line_color="green",
                annotation_text=f"y = {analysis['horizontal_asymptote']}",
                annotation_position="left"
            )
        
        # Add x-intercepts
        for x_int in analysis['x_intercepts']:
            fig.add_trace(go.Scatter(
                x=[x_int],
                y=[0],
                mode='markers',
                marker=dict(color='orange', size=10, symbol='circle'),
                name=f'x-intercept: ({x_int}, 0)',
                showlegend=True
            ))
        
        # Add y-intercept
        if analysis['y_intercept'] is not None:
            fig.add_trace(go.Scatter(
                x=[0],
                y=[analysis['y_intercept']],
                mode='markers',
                marker=dict(color='purple', size=10, symbol='square'),
                name=f'y-intercept: (0, {analysis["y_intercept"]:.2f})',
                showlegend=True
            ))
        
        # Add holes
        for hole_x in analysis['holes']:
            # Calculate y-value at hole by taking limit
            try:
                hole_y = float(sp.limit(function_dict['function'], self.x, hole_x))
                fig.add_trace(go.Scatter(
                    x=[hole_x],
                    y=[hole_y],
                    mode='markers',
                    marker=dict(color='red', size=10, symbol='circle-open', line=dict(width=2)),
                    name=f'Hole: ({hole_x}, {hole_y:.2f})',
                    showlegend=True
                ))
            except:
                pass
        
        # Update layout
        fig.update_layout(
            title=f'Graph of f(x) = {function_dict["function_str"]}',
            xaxis_title='x',
            yaxis_title='f(x)',
            xaxis=dict(range=x_range, zeroline=True, zerolinewidth=2, zerolinecolor='black'),
            yaxis=dict(range=y_range, zeroline=True, zerolinewidth=2, zerolinecolor='black'),
            showlegend=True,
            height=600,
            hovermode='x unified'
        )
        
        return fig
    
    def create_analysis_summary(self, analysis):
        """Create a formatted summary of the function analysis"""
        summary = {}
        
        # Vertical asymptotes
        if analysis['vertical_asymptotes']:
            va_list = [f"x = {va}" for va in analysis['vertical_asymptotes']]
            summary['Vertical Asymptotes'] = ", ".join(va_list)
        else:
            summary['Vertical Asymptotes'] = "None"
        
        # Horizontal asymptote
        if analysis['horizontal_asymptote'] is not None:
            summary['Horizontal Asymptote'] = f"y = {analysis['horizontal_asymptote']}"
        else:
            summary['Horizontal Asymptote'] = "None"
        
        # X-intercepts
        if analysis['x_intercepts']:
            x_int_list = [f"({x}, 0)" for x in analysis['x_intercepts']]
            summary['X-intercepts'] = ", ".join(x_int_list)
        else:
            summary['X-intercepts'] = "None"
        
        # Y-intercept
        if analysis['y_intercept'] is not None:
            summary['Y-intercept'] = f"(0, {analysis['y_intercept']:.2f})"
        else:
            summary['Y-intercept'] = "None"
        
        # Holes
        if analysis['holes']:
            hole_list = [f"x = {hole}" for hole in analysis['holes']]
            summary['Holes'] = ", ".join(hole_list)
        else:
            summary['Holes'] = "None"
        
        return summary
    
    def validate_user_answer(self, user_answer, correct_answer, tolerance=0.1):
        """Validate user's answer against correct answer with tolerance"""
        if user_answer is None or correct_answer is None:
            return user_answer == correct_answer
        
        if isinstance(correct_answer, list):
            if not isinstance(user_answer, list):
                return False
            
            if len(user_answer) != len(correct_answer):
                return False
            
            for ua, ca in zip(sorted(user_answer), sorted(correct_answer)):
                if abs(ua - ca) > tolerance:
                    return False
            return True
        
        if isinstance(correct_answer, (int, float)):
            try:
                return abs(float(user_answer) - float(correct_answer)) <= tolerance
            except:
                return False
        
        return str(user_answer).strip().lower() == str(correct_answer).strip().lower()
    
    def create_blank_graph(self, x_range=(-10, 10), y_range=(-10, 10)):
        """Create a blank coordinate plane for interactive exercises"""
        fig = go.Figure()
        
        # Add grid
        fig.update_layout(
            title='Interactive Coordinate Plane',
            xaxis_title='x',
            yaxis_title='y',
            xaxis=dict(
                range=x_range,
                zeroline=True,
                zerolinewidth=2,
                zerolinecolor='black',
                gridcolor='lightgray',
                showgrid=True
            ),
            yaxis=dict(
                range=y_range,
                zeroline=True,
                zerolinewidth=2,
                zerolinecolor='black',
                gridcolor='lightgray',
                showgrid=True
            ),
            height=600,
            showlegend=False
        )
        
        return fig
    
    def add_user_elements_to_graph(self, fig, user_elements):
        """Add user-drawn elements to the graph"""
        
        for element in user_elements:
            if element['type'] == 'vertical_asymptote':
                fig.add_vline(
                    x=element['x'],
                    line_dash="dash",
                    line_color="red",
                    annotation_text=f"VA: x = {element['x']}"
                )
            
            elif element['type'] == 'horizontal_asymptote':
                fig.add_hline(
                    y=element['y'],
                    line_dash="dash",
                    line_color="green",
                    annotation_text=f"HA: y = {element['y']}"
                )
            
            elif element['type'] == 'x_intercept':
                fig.add_trace(go.Scatter(
                    x=[element['x']],
                    y=[0],
                    mode='markers',
                    marker=dict(color='orange', size=10),
                    name=f"X-int: ({element['x']}, 0)"
                ))
            
            elif element['type'] == 'y_intercept':
                fig.add_trace(go.Scatter(
                    x=[0],
                    y=[element['y']],
                    mode='markers',
                    marker=dict(color='purple', size=10),
                    name=f"Y-int: (0, {element['y']})"
                ))
            
            elif element['type'] == 'hole':
                fig.add_trace(go.Scatter(
                    x=[element['x']],
                    y=[element['y']],
                    mode='markers',
                    marker=dict(color='red', size=10, symbol='circle-open'),
                    name=f"Hole: ({element['x']}, {element['y']})"
                ))
        
        return fig
