<<<<<<< HEAD
import skfuzzy as fuzz
from skfuzzy import control as ctrl
from Games2D import *
=======
import gym
import time
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import matplotlib.pyplot as plt
import numpy as np
>>>>>>> c4c1e951ebdaf1764f93d970e8867dd75a8d89cd

def createFuzzyController():
    # TODO: Create the fuzzy variables for inputs and outputs.
    # Defuzzification (defuzzify_method) methods for fuzzy variables:
    #    'centroid': Centroid of area
    #    'bisector': bisector of area
    #    'mom'     : mean of maximum
    #    'som'     : min of maximum
    #    'lom'     : max of maximum
<<<<<<< HEAD

    #in
    pos = ctrl.Antecedent(np.linspace(-15, 15, 1000), 'pos')
    obs = ctrl.Antecedent(np.linspace(-31, 20, 1000), 'obst')
    item = ctrl.Antecedent(np.linspace(-31, 20, 1000), 'item')

    #out
    move = ctrl.Consequent(np.linspace(-13.5, 13.5, 1000), 'move', defuzzify_method='centroid')

    # Accumulation (accumulation_method) methods for fuzzy variables:
    #    np.fmax
    #    np.multiply
    move.accumulation_method = np.fmax

    # TODO: Create membership functions
    #pos['G'] = fuzz.trapmf(pos.universe, [10, 10, 15, 25])
    #pos['M'] = fuzz.trimf(pos.universe, [20, 25, 30])
    #pos['D'] = fuzz.trapmf(pos.universe, [25, 35, 40, 40])
    pos['D'] = fuzz.trapmf(pos.universe, [-15, -15, -10, 0])
    pos['M'] = fuzz.trimf(pos.universe, [-5, 0, 5])
    pos['G'] = fuzz.trapmf(pos.universe, [0, 10, 15, 15])

    #obs['rien'] = fuzz.trapmf(obs.universe, [-6, -6, 0, 5])
    #obs['FG'] = fuzz.trapmf(obs.universe, [4, 5, 12, 15])
    #obs['MG'] = fuzz.trimf(obs.universe, [10, 15, 25])
    #obs['MD'] = fuzz.trimf(obs.universe, [25, 35, 40])
    #obs['FD'] = fuzz.trapmf(obs.universe, [35, 38, 45, 45])
    obs['rien'] = fuzz.trapmf(obs.universe, [-31, -31, -25, -20])
    obs['FD'] = fuzz.trapmf(obs.universe, [-22, -20, -15, -10])
    obs['MD'] = fuzz.trimf(obs.universe, [-15, -10, 0])
    obs['MG'] = fuzz.trimf(obs.universe, [0, 10, 15])
    obs['FG'] = fuzz.trapmf(obs.universe, [10, 13, 20, 20])

    #item['rien'] = fuzz.trapmf(item.universe, [-6, -6, 0, 5])
    #item['FG'] = fuzz.trapmf(item.universe, [4, 5, 10, 15])
    #item['MG'] = fuzz.trimf(item.universe, [10, 15, 27])
    #item['MD'] = fuzz.trimf(item.universe, [23, 35, 40])
    #item['FD'] = fuzz.trapmf(item.universe, [35, 40, 45, 45])
    item['rien'] = fuzz.trapmf(item.universe, [-31, -31, -25, -20])
    item['FD'] = fuzz.trapmf(item.universe, [-22, -20, -15, -10])
    item['MD'] = fuzz.trimf(item.universe, [-15, -10, 2])
    item['MG'] = fuzz.trimf(item.universe, [-2, 10, 15])
    item['FG'] = fuzz.trapmf(item.universe, [10, 15, 20, 20])

    direct = ['full_G', 'mid_G', 'mid_D', 'full_D']
    move.automf(names=direct)
    #move['full_G'] = fuzz.trapmf(move.universe, [-14, -14, -8, -4])
    #move['mid_G'] = fuzz.trimf(move.universe, [-8, -4, 2])
    #move['mid_D'] = fuzz.trimf(move.universe, [-2, 4, 8])
    #move['full_D'] = fuzz.trapmf(move.universe, [4, 8, 14, 14])

    # TODO: Define the rules.
    rules = []
    #------------------------------------------------------------------------------------------------------------------#
    #-----------------------------------------------GAUCHE-------------------------------------------------------------#
    #------------------------------------------------------------------------------------------------------------------#
    rules.append(ctrl.Rule(antecedent=(pos['G']) & obs['rien'] & item['rien'],
                           consequent=(move['mid_D'])))

    rules.append(ctrl.Rule(antecedent=(pos['G']) & obs['FG'],
                           consequent=(move['full_D'])))
    rules.append(ctrl.Rule(antecedent=(pos['G']) & obs['MG'],
                           consequent=(move['full_D'])))
    rules.append(ctrl.Rule(antecedent=(pos['G']) & obs['MD'],
                           consequent=(move['mid_G'])))
    rules.append(ctrl.Rule(antecedent=(pos['G']) & obs['FD'],
                           consequent=(move['mid_G'])))

    rules.append(ctrl.Rule(antecedent=(pos['G']) & item['FG'],
                           consequent=(move['full_G'])))
    rules.append(ctrl.Rule(antecedent=(pos['G']) & item['MG'],
                           consequent=(move['mid_G'])))
    rules.append(ctrl.Rule(antecedent=(pos['G']) & item['MD'],
                           consequent=(move['full_D'])))
    rules.append(ctrl.Rule(antecedent=(pos['G']) & item['FD'],
                           consequent=(move['full_D'])))
    # -----------------------------------------------------------------------------------------------------------------#
    # -----------------------------------------------milieu------------------------------------------------------------#
    # -----------------------------------------------------------------------------------------------------------------#
    rules.append(ctrl.Rule(antecedent=(pos['M']) & obs['rien'] & item['rien'],
                           consequent=(move['mid_G'], move['mid_D'])))

    rules.append(ctrl.Rule(antecedent=(pos['M']) & obs['FG'],
                           consequent=(move['mid_D'])))
    rules.append(ctrl.Rule(antecedent=(pos['M']) & obs['MG'],
                           consequent=(move['full_D'])))
    rules.append(ctrl.Rule(antecedent=(pos['M']) & obs['MD'],
                           consequent=(move['full_G'])))
    rules.append(ctrl.Rule(antecedent=(pos['M']) & obs['FD'],
                           consequent=(move['mid_G'])))

    rules.append(ctrl.Rule(antecedent=(pos['M']) & item['FG'],
                           consequent=(move['full_G'])))
    rules.append(ctrl.Rule(antecedent=(pos['M']) & item['MG'],
                           consequent=(move['mid_G'])))
    rules.append(ctrl.Rule(antecedent=(pos['M']) & item['MD'],
                           consequent=(move['mid_D'])))
    rules.append(ctrl.Rule(antecedent=(pos['M']) & item['FD'],
                           consequent=(move['full_D'])))
    # -----------------------------------------------------------------------------------------------------------------#
    # -----------------------------------------------DROITE------------------------------------------------------------#
    # -----------------------------------------------------------------------------------------------------------------#
    rules.append(ctrl.Rule(antecedent=(pos['D']) & obs['rien'] & item['rien'],
                           consequent=(move['mid_G'])))

    rules.append(ctrl.Rule(antecedent=(pos['D']) & obs['FG'],
                           consequent=(move['mid_G'])))
    rules.append(ctrl.Rule(antecedent=(pos['D']) & obs['MG'],
                           consequent=(move['full_D'])))
    rules.append(ctrl.Rule(antecedent=(pos['D']) & obs['MD'],
                           consequent=(move['full_G'])))
    rules.append(ctrl.Rule(antecedent=(pos['D']) & obs['FD'],
                           consequent=(move['mid_G'])))

    rules.append(ctrl.Rule(antecedent=(pos['D']) & item['FG'],
                           consequent=(move['full_G'])))
    rules.append(ctrl.Rule(antecedent=(pos['D']) & item['MG'],
                           consequent=(move['full_G'])))
    rules.append(ctrl.Rule(antecedent=(pos['D']) & item['MD'],
                           consequent=(move['mid_D'])))
    rules.append(ctrl.Rule(antecedent=(pos['D']) & item['FD'],
                           consequent=(move['full_D'])))





    for rule in rules:
        #somme ou somme ponderer possible
        rule.and_func = np.fmin
        rule.or_func = np.fmax


    #system
=======

    # inputs
    vertical = ctrl.Antecedent(np.linspace(-150, 150, 10000), 'verticle')
    horizontal = ctrl.Antecedent(np.linspace(-150, 150, 10000), 'horizontal')

    # outputs
    vert_res = ctrl.Consequent(np.linspace(-1, 1, 100), 'vert_res', defuzzify_method='centroid')
    horiz_res = ctrl.Consequent(np.linspace(-1, 1, 100), 'horiz_res', defuzzify_method='centroid')


    # Accumulation (accumulation_method) methods for fuzzy variables:
    #    np.fmax
    #    np.multiply
    vert_res.accumulation_method = np.fmax
    horiz_res.accumulation_method = np.fmax

    # TODO: Create membership functions
    #zone['left'] = fuzz.trapmf(zone.universe, [-1, -1, -0.75, 0])
    #zone['center'] = fuzz.trapmf(zone.universe, [-0.5, -0.25, 0.25, 0.5])
    #zone['right'] = fuzz.trapmf(zone.universe, [0, 0.75, 1, 1])

    vertical['up'] = fuzz.trapmf(vertical.universe, [-150, -150, -100, 20])
    vertical['down'] = fuzz.trapmf(vertical.universe, [-20, 100, 150, 150])
    horizontal['left'] = fuzz.trapmf(horizontal.universe, [-150, -150, -100, 20])
    horizontal['right'] = fuzz.trapmf(horizontal.universe, [-20, 100, 150, 150])

    vert_res['up'] = fuzz.trimf(vert_res.universe, [-1, -1, 0.2])
    vert_res['down'] = fuzz.trimf(vert_res.universe, [-0.2, 1, 1])
    horiz_res['left'] = fuzz.trimf(horiz_res.universe, [-1, -1, 0.2])
    horiz_res['right'] = fuzz.trimf(horiz_res.universe, [-0.2, 1, 1])

    # TODO: Define the rules.
    rules = [ctrl.Rule(antecedent=vertical['up'], consequent=vert_res['up']),
             ctrl.Rule(antecedent=vertical['down'], consequent=vert_res['down']),
             ctrl.Rule(antecedent=horizontal['left'], consequent=horiz_res['left']),
             ctrl.Rule(antecedent=horizontal['right'], consequent=horiz_res['right'])]

    # Conjunction (and_func) and disjunction (or_func) methods for rules:
    #     np.fmin
    #     np.fmax
    for rule in rules:
        rule.and_func = np.fmin
        rule.or_func = np.fmax

>>>>>>> c4c1e951ebdaf1764f93d970e8867dd75a8d89cd
    system = ctrl.ControlSystem(rules)
    sim = ctrl.ControlSystemSimulation(system)
    return sim

<<<<<<< HEAD
=======

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # Create the environment and fuzzy controller
    env = CartPoleEnv("human")
    fuzz_ctrl = createFuzzyController()

    # Display rules
    print('------------------------ RULES ------------------------')
    for rule in fuzz_ctrl.ctrl.rules:
        print(rule)
    print('-------------------------------------------------------')

    # Display fuzzy variables
    for var in fuzz_ctrl.ctrl.fuzzy_variables:
        var.view()
    plt.show()

    VERBOSE = True

    for episode in range(10):
        print('Episode no.%d' % (episode))
        env.reset()

        isSuccess = True
        action = np.array([0.0], dtype=np.float32)
        for _ in range(100):
            env.render()
            time.sleep(0.01)

            # Execute the action
            observation, _, done, _ = env.step(action)
            if done:
                # End the episode
                isSuccess = False
                break

            # Select the next action based on the observation
            cartPosition, cartVelocity, poleAngle, poleVelocityAtTip = observation

            # TODO: set the input to the fuzzy system
            #fuzz_ctrl.input['zone'] = 0
            fuzz_ctrl.input['delta'] = poleVelocityAtTip

            fuzz_ctrl.compute()
            if VERBOSE:
                fuzz_ctrl.print_state()

            # TODO: get the output from the fuzzy system
            force = fuzz_ctrl.output['output1']

            action = np.array(force, dtype=np.float32).flatten()
>>>>>>> c4c1e951ebdaf1764f93d970e8867dd75a8d89cd
