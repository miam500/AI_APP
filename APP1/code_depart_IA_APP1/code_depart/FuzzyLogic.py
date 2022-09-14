# import numpy as np
# import skfuzzy as fuzz
# from skfuzzy import control as ctrl
# import matplotlib.pyplot as plt
# from Games2D import *
#
#
# def createFuzzyController():
#     # TODO: Create the fuzzy variables for inputs and outputs.
#     # Defuzzification (defuzzify_method) methods for fuzzy variables:
#     #    'centroid': Centroid of area
#     #    'bisector': bisector of area
#     #    'mom'     : mean of maximum
#     #    'som'     : min of maximum
#     #    'lom'     : max of maximum
#     #in
#     direction = ctrl.Antecedent(np.linspace(-1, 1, 1000), 'direction')
#     v_item = ctrl.Antecedent(np.linspace(-1, 1, 1000), 'v_item')
#     a_item = ctrl.Antecedent(np.linspace(-1, 1, 1000), 'a_item')
#     v_ob = ctrl.Antecedent(np.linspace(-30, 30, 1000), 'v_ob')
#     a_ob = ctrl.Antecedent(np.linspace(-1, 1, 1000), 'a_ob')
#
#     #out
#     move_x = ctrl.Consequent(np.linspace(-1, 1, 10), 'move_x', defuzzify_method='centroid')
#     move_y = ctrl.Consequent(np.linspace(-1, 1, 10), 'move_y', defuzzify_method='centroid')
#     # Accumulation (accumulation_method) methods for fuzzy variables:
#     #    np.fmax
#     #    np.multiply
#     move_x.accumulation_method = np.fmax
#     move_y.accumulation_method = np.fmax
#     # TODO: Create membership functions
#     #dir = ['up', 'down', 'left', 'right']
#     #direction.automf(names=dir)
#     direction['up'] = fuzz.trimf(direction.universe, [-1, -0.75, -0.5])
#     direction['down'] = fuzz.trimf(direction.universe, [-0.5, -0.25, 0])
#     direction['left'] = fuzz.trimf(direction.universe, [0, 0.25, 0.5])
#     direction['right'] = fuzz.trimf(direction.universe, [0.5, 0.75, 1])
#     x_ob['left'] = fuzz.trapmf(x_ob.universe, [-30, -30, -10, 0])
#     x_ob['right'] = fuzz.trapmf(x_ob.universe, [0, 10, 30, 30])
#     move_x['left'] = fuzz.trapmf(move_x.universe, [-1, -1, 0, 0])
#     move_x['right'] = fuzz.trapmf(move_x.universe, [0, 0, 1, 1])
#     move_y['up'] = fuzz.trapmf(move_x.universe, [-1, -1, 0, 0])
#     move_y['down'] = fuzz.trapmf(move_x.universe, [0, 0, 1, 1])
#     # TODO: Define the rules.
#     rules = []
#     #-----------------------------------------------------------------------------------------------#
#     rules.append(ctrl.Rule(antecedent=(direction['up']),
#                            consequent=(move_x['left'], move_y['up'])))
#     rules.append(ctrl.Rule(antecedent=(direction['down']),
#                            consequent=(move_x['left'], move_y['down'])))
#     rules.append(ctrl.Rule(antecedent=(direction['left']),
#                            consequent=(move_x['left'], move_y['down'])))
#     rules.append(ctrl.Rule(antecedent=(direction['right']),
#                            consequent=(move_x['right'], move_y['up'])))
#     # -----------------------------------------------------------------------------------------------#
#     rules.append(ctrl.Rule(antecedent=(direction['up'] & x_ob['left']),
#                            consequent=(move_x['right'], move_y['up'])))
#     rules.append(ctrl.Rule(antecedent=(direction['down'] & x_ob['left']),
#                            consequent=(move_x['right'], move_y['down'])))
#     rules.append(ctrl.Rule(antecedent=(direction['left'] & x_ob['left']),
#                            consequent=(move_x['left'], move_y['down'])))
#     rules.append(ctrl.Rule(antecedent=(direction['right'] & x_ob['left']),
#                            consequent=(move_x['right'], move_y['up'])))
#     rules.append(ctrl.Rule(antecedent=(direction['up'] & x_ob['right']),
#                            consequent=(move_x['left'], move_y['up'])))
#     rules.append(ctrl.Rule(antecedent=(direction['down'] & x_ob['right']),
#                            consequent=(move_x['left'], move_y['down'])))
#     rules.append(ctrl.Rule(antecedent=(direction['left'] & x_ob['right']),
#                            consequent=(move_x['left'], move_y['down'])))
#     rules.append(ctrl.Rule(antecedent=(direction['right'] & x_ob['right']),
#                            consequent=(move_x['right'], move_y['up'])))
#
#     for rule in rules:
#         rule.and_func = np.fmin
#         rule.or_func = np.fmax
#
#     #system
#     system = ctrl.ControlSystem(rules)
#     sim = ctrl.ControlSystemSimulation(system)
#     return sim

import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import matplotlib.pyplot as plt
from Games2D import *


def createFuzzyController():
    # TODO: Create the fuzzy variables for inputs and outputs.
    # Defuzzification (defuzzify_method) methods for fuzzy variables:
    # 'centroid': Centroid of area
    # 'bisector': bisector of area
    # 'mom' : mean of maximum
    # 'som' : min of maximum
    # 'lom' : max of maximum
    #in
    direction = ctrl.Antecedent(np.linspace(-1, 1, 1000), 'direction')
    up_p = ctrl.Antecedent(np.linspace(0, 170, 1000), 'up_p')
    down_p = ctrl.Antecedent(np.linspace(0, 170, 1000), 'down_p')
    left_p = ctrl.Antecedent(np.linspace(0, 170, 1000), 'left_p')
    right_p = ctrl.Antecedent(np.linspace(0, 170, 1000), 'right_p')
    #out
    move_x = ctrl.Consequent(np.linspace(-1, 1, 10), 'move_x', defuzzify_method='centroid')
    move_y = ctrl.Consequent(np.linspace(-1, 1, 10), 'move_y', defuzzify_method='centroid')
    # Accumulation (accumulation_method) methods for fuzzy variables:
    # np.fmax
    # np.multiply
    move_x.accumulation_method = np.fmax
    move_y.accumulation_method = np.fmax
    # TODO: Create membership functions
    #dir = ['up', 'down', 'left', 'right']
    #direction.automf(names=dir)
    #direction['up'] = fuzz.trimf(direction.universe, [-1, -0.75, -0.5])
    #direction['down'] = fuzz.trimf(direction.universe, [-0.5, -0.25, 0])
    #direction['left'] = fuzz.trimf(direction.universe, [0, 0.25, 0.5])
    #direction['right'] = fuzz.trimf(direction.universe, [0.5, 0.75, 1])
    up_p['leave'] = fuzz.trapmf(up_p.universe, [0, 0, 20, 25])
    up_p['go_to'] = fuzz.trapmf(up_p.universe, [0, 80, 170, 170])
    down_p['leave'] = fuzz.trapmf(down_p.universe, [0, 0, 20, 25])
    down_p['go_to'] = fuzz.trapmf(down_p.universe, [0, 80, 170, 170])
    right_p['leave'] = fuzz.trapmf(right_p.universe, [0, 0, 20, 25])
    right_p['go_to'] = fuzz.trapmf(right_p.universe, [0, 80, 170, 170])
    left_p['leave'] = fuzz.trapmf(left_p.universe, [0, 0, 20, 25])
    left_p['go_to'] = fuzz.trapmf(left_p.universe, [0, 80, 170, 170])
    move_x['left'] = fuzz.trimf(move_x.universe, [-1, -1, 0])
    move_x['right'] = fuzz.trimf(move_x.universe, [0, 1, 1])
    move_y['up'] = fuzz.trimf(move_x.universe, [-1, -1, 0])
    move_y['down'] = fuzz.trimf(move_x.universe, [0, 1, 1])
    # TODO: Define the rules.

    rules = []
    #------------------------------------------------------------------------------------------------------------------#
    #-----------------------------------------------go_to--------------------------------------------------------------#
    #------------------------------------------------------------------------------------------------------------------#
    rules.append(ctrl.Rule(antecedent=(up_p['go_to']), consequent=(move_y['up'])))
    rules.append(ctrl.Rule(antecedent=(down_p['go_to']), consequent=(move_y['down'])))
    rules.append(ctrl.Rule(antecedent=(left_p['go_to']), consequent=(move_x['left'])))
    rules.append(ctrl.Rule(antecedent=(right_p['go_to']), consequent=(move_x['right'])))
    # -----------------------------------------------------------------------------------------------------------------#
    # -----------------------------------------------LEAVE-------------------------------------------------------------#
    # -----------------------------------------------------------------------------------------------------------------#
    rules.append(ctrl.Rule(antecedent=(up_p['leave']), consequent=(move_y['down'])))
    rules.append(ctrl.Rule(antecedent=(down_p['leave']), consequent=(move_y['up'])))
    rules.append(ctrl.Rule(antecedent=(left_p['leave']), consequent=(move_x['right'])))
    rules.append(ctrl.Rule(antecedent=(right_p['leave']), consequent=(move_x['left'])))
    # -----------------------------------------------------------------------------------------------------------------#
    # -----------------------------------------------down+x-------------------------------------------------------------#
    # -----------------------------------------------------------------------------------------------------------------#
    rules.append(ctrl.Rule(antecedent=(down_p['leave'] & left_p['leave']), consequent=(move_y['up'], move_x['right'])))
    rules.append(ctrl.Rule(antecedent=(down_p['go_to'] & left_p['leave']), consequent=(move_y['down'], move_x['right'])))
    rules.append(ctrl.Rule(antecedent=(down_p['leave']), consequent=(move_x['left'])))

    for rule in rules:
    #somme ou somme ponderer possible
        rule.and_func = np.fmin
        rule.or_func = np.fmax
    #system
    system = ctrl.ControlSystem(rules)
    sim = ctrl.ControlSystemSimulation(system)
    return sim
