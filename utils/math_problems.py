import random
from data.math_problems import math_problems as mp

def load_math_problems(level_number):
    problems = [problem for problem in mp if problem["level"] == level_number]
    return problems

def get_random_problems(problems, count=2):
    return random.sample(problems, count)

def shuffle_answers(problem):
    answers = problem["answer_choices"][:]
    random.shuffle(answers)
    return answers