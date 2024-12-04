import random
from data.math_problems import math_problems as mp

def load_math_problems(level):
    problems = []
    for problem in mp:
        if problem["level"] == level:
            problems.append(problem)
    return problems

def get_random_problems(problems, count=10):
    if count > len(problems):
        count = len(problems)
    return random.sample(problems, count)