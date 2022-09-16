import skfuzzy as fuzz
from skfuzzy import control as ctrl
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
    pos = ctrl.Antecedent(np.linspace(-15, 15, 1000), 'pos')
    obs = ctrl.Antecedent(np.linspace(-31, 20, 1000), 'obst')
    item = ctrl.Antecedent(np.linspace(-31, 20, 1000), 'item')
    #out
    move = ctrl.Consequent(np.linspace(-5, 5, 1000), 'move', defuzzify_method='centroid')

    # Accumulation (accumulation_method) methods for fuzzy variables:
    move.accumulation_method = np.fmax

    # TODO: Create membership functions
    pos['D'] = fuzz.trapmf(pos.universe, [-15, -15, -10, 0])
    pos['M'] = fuzz.trimf(pos.universe, [-5, 0, 5])
    pos['G'] = fuzz.trapmf(pos.universe, [0, 10, 15, 15])

    obs['rien'] = fuzz.trapmf(obs.universe, [-31, -31, -25, -20])
    obs['FD'] = fuzz.trapmf(obs.universe, [-21, -20, -15, -10])
    obs['MD'] = fuzz.trimf(obs.universe, [-12, -8, 0])
    obs['MG'] = fuzz.trimf(obs.universe, [0, 8, 12])
    obs['FG'] = fuzz.trapmf(obs.universe, [10, 13, 20, 20])

    item['rien'] = fuzz.trapmf(item.universe, [-31, -31, -25, -20])
    item['FD'] = fuzz.trapmf(item.universe, [-22, -20, -15, -10])
    item['MD'] = fuzz.trimf(item.universe, [-15, -10, 2])
    item['MG'] = fuzz.trimf(item.universe, [-2, 10, 15])
    item['FG'] = fuzz.trapmf(item.universe, [10, 15, 20, 20])

    direct = ['full_G', 'mid_G', 'mid_D', 'full_D']
    move.automf(names=direct)

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
    system = ctrl.ControlSystem(rules)
    sim = ctrl.ControlSystemSimulation(system)
    return sim

