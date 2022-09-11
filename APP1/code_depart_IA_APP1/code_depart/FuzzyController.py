import gym
import time
from cartpole import *
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import matplotlib.pyplot as plt
import numpy as np

def createFuzzyController():
    # TODO: Create the fuzzy variables for inputs and outputs.
    # Defuzzification (defuzzify_method) methods for fuzzy variables:
    #    'centroid': Centroid of area
    #    'bisector': bisector of area
    #    'mom'     : mean of maximum
    #    'som'     : min of maximum
    #    'lom'     : max of maximum
    # zone = ctrl.Antecedent(np.linspace(-1, 1, 1000), 'input1')
    # fall = ctrl.Antecedent(np.linspace(-1, 1, 1000), 'input2')
    # cons1 = ctrl.Consequent(np.linspace(-1, 1, 1000), 'output1', defuzzify_method='centroid')
    zone = ctrl.Antecedent(np.linspace(-1, 1, 1000), 'input1')
    # ant2 = ctrl.Antecedent(np.linspace(-1, 1, 1000), 'input2')
    fall = ctrl.Antecedent(np.linspace(-2, 2, 1000), 'input2')
    cons1 = ctrl.Consequent(np.linspace(-10, 10, 1000), 'output1', defuzzify_method='centroid')

    # Accumulation (accumulation_method) methods for fuzzy variables:
    #    np.fmax
    #    np.multiply
    cons1.accumulation_method = np.fmax

    # TODO: Create membership functions
    fall['neg'] = fuzz.trapmf(fall.universe, [-1*2, -0.5*2, -0.25*2, 0.1*2])
    fall['pos'] = fuzz.trapmf(fall.universe, [-0.1*2, 0.25*2, 0.5*2, 1*2])
    cons1['gauche'] = fuzz.trapmf(cons1.universe, [-10, -6, -2, 2])
    cons1['droite'] = fuzz.trapmf(cons1.universe, [-2, 2, 6, 10])
    # TODO: Define the rules.
    rules = []
    rules.append(ctrl.Rule(antecedent=(fall['neg']), consequent=cons1['gauche']))
    rules.append(ctrl.Rule(antecedent=(fall['pos']), consequent=cons1['droite']))

    # Conjunction (and_func) and disjunction (or_func) methods for rules:
    #     np.fmin
    #     np.fmax
    for rule in rules:
        rule.and_func = np.fmin
        rule.or_func = np.fmax

    system = ctrl.ControlSystem(rules)
    sim = ctrl.ControlSystemSimulation(system)
    return sim