import gym
import time
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

    system = ctrl.ControlSystem(rules)
    sim = ctrl.ControlSystemSimulation(system)
    return sim


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