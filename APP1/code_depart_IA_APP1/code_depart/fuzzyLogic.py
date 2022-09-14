import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import matplotlib.pyplot as plt
from Games2D import *

def createFuzzyController():
    # TODO: Create the fuzzy variables for inputs and outputs.
    # Defuzzification (defuzzify_method) methods for fuzzy variables:
    #    'centroid': Centroid of area
    #    'bisector': bisector of area
    #    'mom'     : mean of maximum
    #    'som'     : min of maximum
    #    'lom'     : max of maximum

    #in
    direction = ctrl.Antecedent(np.linspace(-1, 1, 1000), 'direction')
    up_p = ctrl.Antecedent(np.linspace(0, 100, 1000), 'up_p')
    down_p = ctrl.Antecedent(np.linspace(0, 100, 1000), 'down_p')
    left_p = ctrl.Antecedent(np.linspace(0, 100, 1000), 'left_p')
    right_p = ctrl.Antecedent(np.linspace(0, 100, 1000), 'right_p')


    #out
    move_x = ctrl.Consequent(np.linspace(-1, 1, 10), 'move_x', defuzzify_method='centroid')
    move_y = ctrl.Consequent(np.linspace(-1, 1, 10), 'move_y', defuzzify_method='centroid')

    # Accumulation (accumulation_method) methods for fuzzy variables:
    #    np.fmax
    #    np.multiply
    move_x.accumulation_method = np.fmax
    move_y.accumulation_method = np.fmax

    # TODO: Create membership functions
    #dir = ['up', 'down', 'left', 'right']
    #direction.automf(names=dir)
    direction['up'] = fuzz.trimf(direction.universe, [-1, -0.75, -0.5])
    direction['down'] = fuzz.trimf(direction.universe, [-0.5, -0.25, 0])
    direction['left'] = fuzz.trimf(direction.universe, [0, 0.25, 0.5])
    direction['right'] = fuzz.trimf(direction.universe, [0.5, 0.75, 1])

    up_p['leave'] = fuzz.trimf(up_p.universe, [0, 25, 50])
    up_p['go_to'] = fuzz.trimf(up_p.universe, [50, 75, 100])

    down_p['leave'] = fuzz.trimf(down_p.universe, [-10, -10, 0])
    down_p['go_to'] = fuzz.trimf(down_p.universe, [0, 10, 10])

    right_p['leave'] = fuzz.trimf(right_p.universe, [0, 25, 50])
    right_p['go_to'] = fuzz.trimf(right_p.universe, [25, 75, 100])

    left_p['leave'] = fuzz.trimf(left_p.universe, [0, 25, 50])
    left_p['go_to'] = fuzz.trimf(left_p.universe, [50, 75, 100])

    move_x['left'] = fuzz.trapmf(move_x.universe, [-1, -1, 0, 0])
    move_x['right'] = fuzz.trapmf(move_x.universe, [0, 0, 1, 1])
    move_y['up'] = fuzz.trapmf(move_x.universe, [-1, -1, 0, 0])
    move_y['down'] = fuzz.trapmf(move_x.universe, [0, 0, 1, 1])

    # TODO: Define the rules.
    rules = []
    #------------------------------------------------------------------------------------------------------------------#
    #-----------------------------------------------UP-----------------------------------------------------------------#
    #------------------------------------------------------------------------------------------------------------------#
    rules.append(ctrl.Rule(antecedent=(direction['up']),
                           consequent=(move_y['up'])))
    rules.append(ctrl.Rule(antecedent=(direction['up'] & up_p['go_to'] & left_p['go_to']),
                           consequent=(move_y['up'], move_x['left'])))
    rules.append(ctrl.Rule(antecedent=(direction['up'] & up_p['go_to'] & left_p['leave']),
                           consequent=(move_y['up'], move_x['right'])))
    rules.append(ctrl.Rule(antecedent=(direction['up'] & up_p['go_to'] & right_p['go_to']),
                           consequent=(move_y['up'], move_x['right'])))
    rules.append(ctrl.Rule(antecedent=(direction['up'] & up_p['go_to'] & right_p['leave']),
                           consequent=(move_y['up'], move_x['left'])))
    rules.append(ctrl.Rule(antecedent=(direction['up'] & up_p['leave'] & left_p['go_to']),
                           consequent=(move_x['left'])))
    rules.append(ctrl.Rule(antecedent=(direction['up'] & up_p['leave'] & left_p['leave']),
                           consequent=(move_x['right'])))
    rules.append(ctrl.Rule(antecedent=(direction['up'] & up_p['leave'] & right_p['go_to']),
                           consequent=(move_x['right'])))
    rules.append(ctrl.Rule(antecedent=(direction['up'] & up_p['leave'] & right_p['leave']),
                           consequent=(move_x['left'])))
    # -----------------------------------------------------------------------------------------------------------------#
    # -----------------------------------------------DOWN--------------------------------------------------------------#
    # -----------------------------------------------------------------------------------------------------------------#
    rules.append(ctrl.Rule(antecedent=(direction['down']),
                           consequent=(move_y['down'])))
    rules.append(ctrl.Rule(antecedent=(direction['down'] & down_p['go_to'] & left_p['go_to']),
                           consequent=(move_y['down'], move_x['left'])))
    rules.append(ctrl.Rule(antecedent=(direction['down'] & down_p['go_to'] & left_p['leave']),
                           consequent=(move_y['down'], move_x['right'])))
    rules.append(ctrl.Rule(antecedent=(direction['down'] & down_p['go_to'] & right_p['go_to']),
                           consequent=(move_y['dwon'], move_x['right'])))
    rules.append(ctrl.Rule(antecedent=(direction['down'] & down_p['go_to'] & right_p['leave']),
                           consequent=(move_y['down'], move_x['left'])))
    rules.append(ctrl.Rule(antecedent=(direction['down'] & down_p['leave'] & left_p['go_to']),
                           consequent=(move_x['left'])))
    rules.append(ctrl.Rule(antecedent=(direction['down'] & down_p['leave'] & left_p['leave']),
                           consequent=(move_x['right'])))
    rules.append(ctrl.Rule(antecedent=(direction['down'] & down_p['leave'] & right_p['go_to']),
                           consequent=(move_x['right'])))
    rules.append(ctrl.Rule(antecedent=(direction['down'] & down_p['leave'] & right_p['leave']),
                           consequent=(move_x['left'])))
    # -----------------------------------------------------------------------------------------------------------------#
    # -----------------------------------------------LEFT--------------------------------------------------------------#
    # -----------------------------------------------------------------------------------------------------------------#
    rules.append(ctrl.Rule(antecedent=(direction['left']),
                           consequent=(move_x['left'])))
    rules.append(ctrl.Rule(antecedent=(direction['left'] & left_p['go_to'] & down_p['go_to']),
                           consequent=(move_x['left'], move_y['down'])))
    rules.append(ctrl.Rule(antecedent=(direction['left'] & left_p['go_to'] & down_p['leave']),
                           consequent=(move_x['left'], move_y['up'])))
    rules.append(ctrl.Rule(antecedent=(direction['left'] & left_p['go_to'] & up_p['go_to']),
                           consequent=(move_x['left'], move_y['up'])))
    rules.append(ctrl.Rule(antecedent=(direction['left'] & left_p['go_to'] & up_p['leave']),
                           consequent=(move_x['left'], move_y['down'])))
    rules.append(ctrl.Rule(antecedent=(direction['left'] & left_p['leave'] & down_p['go_to']),
                           consequent=(move_y['down'])))
    rules.append(ctrl.Rule(antecedent=(direction['left'] & left_p['leave'] & down_p['leave']),
                           consequent=(move_y['up'])))
    rules.append(ctrl.Rule(antecedent=(direction['left'] & left_p['leave'] & up_p['go_to']),
                           consequent=(move_y['up'])))
    rules.append(ctrl.Rule(antecedent=(direction['left'] & left_p['leave'] & up_p['leave']),
                           consequent=(move_y['down'])))
    # -----------------------------------------------------------------------------------------------------------------#
    # -----------------------------------------------RIGHT-------------------------------------------------------------#
    # -----------------------------------------------------------------------------------------------------------------#
    rules.append(ctrl.Rule(antecedent=(direction['right']),
                           consequent=(move_x['right'])))
    rules.append(ctrl.Rule(antecedent=(direction['right'] & right_p['go_to'] & down_p['go_to']),
                           consequent=(move_x['right'], move_y['down'])))
    rules.append(ctrl.Rule(antecedent=(direction['right'] & right_p['go_to'] & down_p['leave']),
                           consequent=(move_x['right'], move_y['right'])))
    rules.append(ctrl.Rule(antecedent=(direction['right'] & right_p['go_to'] & up_p['go_to']),
                           consequent=(move_x['up'], move_y['up'])))
    rules.append(ctrl.Rule(antecedent=(direction['right'] & right_p['go_to'] & up_p['leave']),
                           consequent=(move_x['up'], move_y['down'])))
    rules.append(ctrl.Rule(antecedent=(direction['right'] & right_p['leave'] & down_p['go_to']),
                           consequent=(move_y['down'])))
    rules.append(ctrl.Rule(antecedent=(direction['right'] & right_p['leave'] & down_p['leave']),
                           consequent=(move_y['up'])))
    rules.append(ctrl.Rule(antecedent=(direction['right'] & right_p['leave'] & up_p['go_to']),
                           consequent=(move_y['up'])))
    rules.append(ctrl.Rule(antecedent=(direction['right'] & right_p['leave'] & up_p['leave']),
                           consequent=(move_y['down'])))

    for rule in rules:
        #somme ou somme ponderer possible
        rule.and_func = np.fmin
        rule.or_func = np.fmax


    #system
    system = ctrl.ControlSystem(rules)
    sim = ctrl.ControlSystemSimulation(system)
    return sim
