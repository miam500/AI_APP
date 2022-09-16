# Simple interactive dungeon crawler
# This code was written for the AI courses in computer engineering at Université de Sherbrooke
# Author : Audrey Corbeil Therrien
from FuzzyLogic import *

from Games2D import *

if __name__ == '__main__':
    # Niveau 0 - sans obstacle - 'assets/mazeMedium_0'
    # Niveau 1 - avec obstacles - 'assets/mazeMedium_1'
    # Niveau 2 - avec obstacles et ennemis - 'assets/mazeMedium_2'
    fuzzy_ctrl = createFuzzyController()
    theAPP = App('assets/mazeMedium_2', fuzzy_ctrl, tile_size)
    theAPP.on_execute()

