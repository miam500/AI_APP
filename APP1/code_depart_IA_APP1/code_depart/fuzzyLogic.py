import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import matplotlib.pyplot as plt
from Game2D import on_AI_input

def createFuzzyController():
    # TODO: Create the fuzzy variables for inputs and outputs.
    # Defuzzification (defuzzify_method) methods for fuzzy variables:
    #    'centroid': Centroid of area
    #    'bisector': bisector of area
    #    'mom'     : mean of maximum
    #    'som'     : min of maximum
    #    'lom'     : max of maximum
    direction = ctrl.Antecedent(np.linspace(-4, 4, 1000), 'direction')
    x_item = ctrl.Antecedent(np.linspace(-10, 10, 1000), 'x_item')
    y_item = ctrl.Antecedent(np.linspace(-10, 10, 1000), 'y_item')
    item = ctrl.Antecedent(np.linspace(-10, 10, 1000), 'item')
    #out
    move_x = ctrl.Consequent(np.linspace(-1, 1, 1000), 'move', defuzzify_method='centroid')
    move_y = ctrl.Consequent(np.linspace(-1, 1, 1000), 'move', defuzzify_method='centroid')

    # Accumulation (accumulation_method) methods for fuzzy variables:
    #    np.fmax
    #    np.multiply
    move_x.accumulation_method = np.fmax
    move_y.accumulation_method = np.fmax

    # TODO: Create membership functions
    dir = ['up', 'down', 'left', 'right']
    direction.automf(names=dir)
    #direction['up'] = fuzz.trapmf()
    #direction['down'] = fuzz.trapmf()
    #direction['left'] = fuzz.trapmf(direction.universe, [-4, -3, -0.8, 0])
    #direction['right'] = fuzz.trapmf(direction.universe, [0, 0.8, 3, 4])

    pos = ['en_haut', 'en_bas']
    y_item.automf(names=pos)
    pos = ['a_droite', 'a_gauche']
    x_item.automf(names=pos)
    things = ['O', 'M', 'C', 'T']
    item.automf(names=things)

    move = ['left', 'right']
    move_x.automf(names=move)
    move = ['up', 'down']
    move_y.automf(names=move)

    # TODO: Define the rules.
    rules = []
    rules.append(ctrl.Rule(antecedent=(direction['up'] & y_item['en_haut'] & x_item['a_gauche'] & item['T']),
                           consequent=(move_x['left'], move_y['up']) ))
    rules.append(ctrl.Rule(antecedent=(direction['up'] & y_item['en_haut'] & x_item['a_droite'] & item['T']),
                           consequent=(move_x['right'], move_y['up'])))

    rules.append(ctrl.Rule(antecedent=(direction['down'] & y_item['en_bas'] & x_item['a_gauche'] & item['T']),
                           consequent=(move_x['left'], move_y['down'])))
    rules.append(ctrl.Rule(antecedent=(direction['down'] & y_item['en_bas'] & x_item['a_droite'] & item['T']),
                           consequent=(move_x['right'], move_y['down'])))

    rules.append(ctrl.Rule(antecedent=(direction['left'] & y_item['en_bas'] & x_item['a_gauche'] & item['T']),
                           consequent=(move_x['left'], move_y['down'])))
    rules.append(ctrl.Rule(antecedent=(direction['left'] & y_item['en_bas'] & x_item['a_droite'] & item['T']),
                           consequent=(move_x['right'], move_y['down'])))

    rules.append(ctrl.Rule(antecedent=(direction['right'] & y_item['en_bas'] & x_item['a_gauche'] & item['T']),
                           consequent=(move_x['left'], move_y['down'])))
    rules.append(ctrl.Rule(antecedent=(direction['right'] & y_item['en_bas'] & x_item['a_droite'] & item['T']),
                           consequent=(move_x['right'], move_y['down'])))

    for rule in rules:
        rule.and_func = np.fmin
        rule.or_func = np.fmax


    #system
    system = ctrl.ControlSystem(rules)
    sim = ctrl.ControlSystemSimulation(system)
    return sim


