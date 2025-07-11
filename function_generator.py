import numpy as np
import sympy as sp
from sympy import symbols, factor, simplify, solve, limit, oo
import random

class RationalFunctionGenerator:
    def __init__(self):
        self.x = symbols('x')
        self.difficulty_configs = {
            1: {"max_degree": 2, "max_factors": 2, "holes_prob": 0.3},
            2: {"max_degree": 3, "max_factors": 3, "holes_prob": 0.4},
            3: {"max_degree": 4, "max_factors": 4, "holes_prob": 0.5},
            4: {"max_degree": 5, "max_factors": 5, "holes_prob": 0.6},
            5: {"max_degree": 6, "max_factors": 6, "holes_prob": 0.7}
        }
    
    def generate_function(self, difficulty=1):
        """Generate a rational function based on difficulty level"""
        config = self.difficulty_configs.get(difficulty, self.difficulty_configs[1])
        
        # Generate numerator and denominator
        numerator = self._generate_polynomial(config["max_degree"], config["max_factors"])
        denominator = self._generate_polynomial(config["max_degree"], config["max_factors"])
        
        # Ensure denominator is not zero
        while denominator == 0:
            denominator = self._generate_polynomial(config["max_degree"], config["max_factors"])
        
        # Add holes with certain probability
        if random.random() < config["holes_prob"]:
            hole_factor = self._generate_linear_factor()
            numerator *= hole_factor
            denominator *= hole_factor
        
        # Create the rational function
        function = numerator / denominator
        simplified = simplify(function)
        
        return {
            'function': simplified,
            'numerator': numerator,
            'denominator': denominator,
            'function_str': str(simplified),
            'latex': sp.latex(simplified)
        }
    
    def _generate_polynomial(self, max_degree, max_factors):
        """Generate a polynomial with given constraints"""
        degree = random.randint(1, max_degree)
        factors = random.randint(1, min(max_factors, degree))
        
        polynomial = 1
        for _ in range(factors):
            factor = self._generate_linear_factor()
            polynomial *= factor
        
        # Add remaining degree with coefficients
        remaining_degree = degree - factors
        if remaining_degree > 0:
            coeff = random.randint(-5, 5)
            if coeff == 0:
                coeff = 1
            polynomial *= coeff * (self.x ** remaining_degree)
        
        return polynomial
    
    def _generate_linear_factor(self):
        """Generate a linear factor like (x - a) or (x + a)"""
        a = random.randint(-5, 5)
        return self.x - a
    
    def analyze_function(self, function_dict):
        """Analyze a rational function for key characteristics"""
        func = function_dict['function']
        num = function_dict['numerator']
        den = function_dict['denominator']
        
        analysis = {}
        
        # Find vertical asymptotes
        den_roots = solve(den, self.x)
        num_roots = solve(num, self.x)
        
        # Vertical asymptotes are where denominator = 0 but numerator ≠ 0
        vertical_asymptotes = []
        holes = []
        
        for root in den_roots:
            if root.is_real:
                if root in num_roots:
                    holes.append(float(root))
                else:
                    vertical_asymptotes.append(float(root))
        
        analysis['vertical_asymptotes'] = vertical_asymptotes
        analysis['holes'] = holes
        
        # Find horizontal asymptotes
        analysis['horizontal_asymptote'] = self._find_horizontal_asymptote(num, den)
        
        # Find x-intercepts (where numerator = 0 and denominator ≠ 0)
        x_intercepts = []
        for root in num_roots:
            if root.is_real and root not in holes:
                x_intercepts.append(float(root))
        analysis['x_intercepts'] = x_intercepts
        
        # Find y-intercept
        try:
            y_intercept = float(func.subs(self.x, 0))
            analysis['y_intercept'] = y_intercept
        except:
            analysis['y_intercept'] = None
        
        return analysis
    
    def _find_horizontal_asymptote(self, num, den):
        """Find horizontal asymptote based on degrees of numerator and denominator"""
        try:
            # Get the limit as x approaches infinity
            limit_inf = limit(num/den, self.x, oo)
            
            if limit_inf.is_finite and limit_inf.is_real:
                return float(limit_inf)
            elif limit_inf == oo or limit_inf == -oo:
                return None  # No horizontal asymptote
            else:
                return 0  # Horizontal asymptote at y = 0
        except:
            return 0
    
    def generate_multiple_choice_question(self, function_dict, analysis, question_type):
        """Generate multiple choice questions about the function"""
        questions = {
            'vertical_asymptotes': self._generate_va_question,
            'horizontal_asymptote': self._generate_ha_question,
            'x_intercepts': self._generate_x_intercept_question,
            'holes': self._generate_holes_question
        }
        
        if question_type in questions:
            return questions[question_type](function_dict, analysis)
        else:
            return self._generate_random_question(function_dict, analysis)
    
    def _generate_va_question(self, function_dict, analysis):
        """Generate vertical asymptote question"""
        correct_answer = analysis['vertical_asymptotes']
        
        # Generate wrong answers
        wrong_answers = []
        for _ in range(3):
            wrong = random.randint(-5, 5)
            while wrong in correct_answer or wrong in wrong_answers:
                wrong = random.randint(-5, 5)
            wrong_answers.append([wrong])
        
        if not correct_answer:
            correct_answer = "None"
            wrong_answers = [[-1], [0], [1]]
        
        choices = [correct_answer] + wrong_answers
        random.shuffle(choices)
        
        return {
            'question': f"What are the vertical asymptotes of f(x) = {function_dict['function_str']}?",
            'choices': [str(choice) if choice != "None" else "None" for choice in choices],
            'correct_answer': str(correct_answer) if correct_answer != "None" else "None",
            'explanation': f"Vertical asymptotes occur where the denominator equals zero but the numerator doesn't."
        }
    
    def _generate_ha_question(self, function_dict, analysis):
        """Generate horizontal asymptote question"""
        correct_answer = analysis['horizontal_asymptote']
        
        wrong_answers = []
        if correct_answer is None:
            correct_answer = "None"
            wrong_answers = [0, 1, -1]
        else:
            for i in range(3):
                wrong = correct_answer + random.randint(-3, 3)
                while wrong == correct_answer or wrong in wrong_answers:
                    wrong = correct_answer + random.randint(-3, 3)
                wrong_answers.append(wrong)
        
        choices = [correct_answer] + wrong_answers
        random.shuffle(choices)
        
        return {
            'question': f"What is the horizontal asymptote of f(x) = {function_dict['function_str']}?",
            'choices': [str(choice) if choice != "None" else "None" for choice in choices],
            'correct_answer': str(correct_answer) if correct_answer != "None" else "None",
            'explanation': f"Horizontal asymptotes depend on the degrees of numerator and denominator."
        }
    
    def _generate_x_intercept_question(self, function_dict, analysis):
        """Generate x-intercept question"""
        correct_answer = analysis['x_intercepts']
        
        wrong_answers = []
        for _ in range(3):
            wrong = [random.randint(-5, 5)]
            while wrong == correct_answer or wrong in wrong_answers:
                wrong = [random.randint(-5, 5)]
            wrong_answers.append(wrong)
        
        if not correct_answer:
            correct_answer = "None"
            wrong_answers = [[-1], [0], [1]]
        
        choices = [correct_answer] + wrong_answers
        random.shuffle(choices)
        
        return {
            'question': f"What are the x-intercepts of f(x) = {function_dict['function_str']}?",
            'choices': [str(choice) if choice != "None" else "None" for choice in choices],
            'correct_answer': str(correct_answer) if correct_answer != "None" else "None",
            'explanation': f"X-intercepts occur where the numerator equals zero but the denominator doesn't."
        }
    
    def _generate_holes_question(self, function_dict, analysis):
        """Generate holes question"""
        correct_answer = analysis['holes']
        
        wrong_answers = []
        for _ in range(3):
            wrong = [random.randint(-5, 5)]
            while wrong == correct_answer or wrong in wrong_answers:
                wrong = [random.randint(-5, 5)]
            wrong_answers.append(wrong)
        
        if not correct_answer:
            correct_answer = "None"
            wrong_answers = [[-1], [0], [1]]
        
        choices = [correct_answer] + wrong_answers
        random.shuffle(choices)
        
        return {
            'question': f"Where are the holes in f(x) = {function_dict['function_str']}?",
            'choices': [str(choice) if choice != "None" else "None" for choice in choices],
            'correct_answer': str(correct_answer) if correct_answer != "None" else "None",
            'explanation': f"Holes occur where both numerator and denominator equal zero."
        }
    
    def _generate_random_question(self, function_dict, analysis):
        """Generate a random question type"""
        question_types = ['vertical_asymptotes', 'horizontal_asymptote', 'x_intercepts', 'holes']
        question_type = random.choice(question_types)
        return self.generate_multiple_choice_question(function_dict, analysis, question_type)
