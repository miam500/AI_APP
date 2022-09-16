# Helper class for genetic algorithms
# Copyright (c) 2018, Audrey Corbeil Therrien, adapted from Simon Brodeur
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without modification,
# are permitted provided that the following conditions are met:
#
#  - Redistributions of source code must retain the above copyright notice,
#    this list of conditions and the following disclaimer.
#  - Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution.
#  - Neither the name of the copyright holder nor the names of its contributors
#    may be used to endorse or promote products derived from this software
#    without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED.
# IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT,
# INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT
# NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES LOSS OF USE, DATA,
# OR PROFITS OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY,
# WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

# Université de Sherbrooke
# Code for Artificial Intelligence module
# Adapted by Audrey Corbeil Therrien for Artificial Intelligence module
import numpy as np
from Constants import *

class tempclass:
    def __init__(self,parameters):
        self.attributes=parameters



class Genetic:
    num_params = 0
    pop_size = 0
    nbits = 0
    population = []

    def __init__(self, num_params, pop_size, nbits):
        # Input:
        # - NUMPARAMS, the number of parameters to optimize.
        # - POPSIZE, the population size.
        # - NBITS, the number of bits per indivual used for encoding.
        self.num_params = num_params
        self.pop_size = pop_size
        self.nbits = nbits
        self.fitness = np.zeros((self.pop_size, 1))
        self.fit_fun = np.zeros
        self.cvalues = np.zeros((self.pop_size, num_params))
        self.num_generations = 1
        self.mutation_prob = 0
        self.crossover_prob = 0
        self.bestIndividual = []
        self.bestIndividualFitness = -1e10
        self.maxFitnessRecord = np.zeros((self.num_generations,))
        self.overallMaxFitnessRecord = np.zeros((self.num_generations,))
        self.avgMaxFitnessRecord = np.zeros((self.num_generations,))
        self.current_gen = 0
        self.crossover_modulo = 0

    def init_pop(self):
        # Initialize the population as a matrix, where each individual is a binary string.
        self.population = np.random.randint(0, 2, size=(self.pop_size, self.num_params * self.nbits))


    def set_fit_fun(self, fun):
        # Set the fitness function
        self.fit_fun = fun

    def set_crossover_modulo(self, modulo):
        # Set the fitness function
        self.crossover_modulo = modulo

    def set_sim_parameters(self, num_generations, mutation_prob, crossover_prob):
        # set the simulation/evolution parameters to execute the optimization
        # initialize the result matrices
        self.num_generations = num_generations
        self.mutation_prob = mutation_prob
        self.crossover_prob = crossover_prob
        self.bestIndividual = np.zeros(self.num_params*self.nbits,)
        self.bestIndividualFitness = -1e10
        self.maxFitnessRecord = np.zeros((num_generations,))
        self.overallMaxFitnessRecord = np.zeros((num_generations,))
        self.avgMaxFitnessRecord = np.zeros((num_generations,))
        self.current_gen = 0

    def eval_fit(self):
        # Evaluate the fitness function
        # Record the best individual and average of the current generation
        self.fitness=[]
        for individual in self.cvalues:
            self.fitness.append(self.fit_fun.mock_fight(tempclass(individual*(2*MAX_ATTRIBUTE)-MAX_ATTRIBUTE))[1])

        if np.max(self.fitness) > self.bestIndividualFitness:
            #keep second best individual
            self.bestIndividualFitness = np.max(self.fitness)
            self.bestIndividual = self.population[self.fitness == np.max(self.fitness)][0]
        self.maxFitnessRecord[self.current_gen] = np.max(self.fitness)
        self.overallMaxFitnessRecord[self.current_gen] = self.bestIndividualFitness
        self.avgMaxFitnessRecord[self.current_gen] = np.mean(self.fitness)

        to_retain=int(len(self.population)*0.05)
        bestindices=np.argpartition(self.fitness,-to_retain)[-to_retain:]
        self.bestIndividuals=self.population[bestindices]



    def print_progress(self):
        # Prints the results of the current generation in the console
        print('Generation no.%d: best fitness is %f, average is %f' %
              (self.current_gen, self.maxFitnessRecord[self.current_gen],
               self.avgMaxFitnessRecord[self.current_gen]))
        print('Overall best fitness is %f' % self.bestIndividualFitness)

    def get_best_individual(self):
        # Prints the best individual for all of the simulated generations
        # TODO : Decode individual for better readability
        list=[]
        for atom in np.array_split(self.bestIndividual, self.num_params):
            list.append(bin2ufloat(atom,self.nbits)[0]*(2*MAX_ATTRIBUTE)-MAX_ATTRIBUTE)
        return list

    def encode_individuals(self):
        # Encode the population from a vector of continuous values to a binary string.
        for i,indiv in enumerate(self.cvalues):
            self.population[i]=ufloat2bin(indiv,self.nbits).flatten()


    def decode_individuals(self):
        # Decode an individual from a binary string to a vector of continuous values.
        for i, indiv in enumerate(self.population):

            atoms=np.array_split(indiv, self.num_params)

            for j in range(self.num_params):
                self.cvalues[i][j]=bin2ufloat(atoms[j],self.nbits)[0]

    def doSelection(self):
        # Select pairs of individuals from the population.

        self.encode_individuals()

        total=sum(self.fitness)
        wheel=[fit/total for fit in self.fitness]

        idx1 = np.random.choice(self.pop_size,int(self.pop_size/2),p=wheel)
        idx2 = np.random.choice(self.pop_size,int(self.pop_size/2), p=wheel)

        return [self.population[idx1, :], self.population[idx2, :]]

    def doCrossover(self, pairs):
        # Perform a crossover operation between two individuals, with a given probability and constraint on the cutting point.

        halfpop1 = pairs[0]
        halfpop2 = pairs[1]
        for index, (parent1,parent2) in enumerate(zip(halfpop1,halfpop2)):

            if np.random.rand() < self.crossover_prob:
                split=np.random.randint(0,self.num_params)*self.crossover_modulo
                halfpop1[index] = np.concatenate((parent1[:split], parent2[split:]))
                halfpop2[index] = np.concatenate((parent2[:split], parent1[split:]))

        return np.vstack((halfpop1, halfpop2))

    def doMutation(self):
        # Perform a mutation operation over the entire population.

        for index, indiv in enumerate(self.population):
            if np.random.rand() < self.mutation_prob:
                # flip the bit
                mut=np.random.randint(self.nbits*self.num_params)
                self.population[index][mut]=1 - indiv[mut]

        for i in range(len(self.bestIndividuals)):
            self.population[i]=self.bestIndividuals[i]

    def new_gen(self):
        # Perform a the pair selection, crossover and mutation and generate a new population for the next generation.
        pairs = self.doSelection()
        self.population = self.doCrossover(pairs)
        self.doMutation()
        self.current_gen += 1

def ufloat2bin(cvalue, nbits):
    # Convert floating point values into a binary vector
    if nbits > 64:
        raise Exception('Maximum number of bits limited to 64')
    ivalue = np.round(cvalue * (2**nbits - 1)).astype(np.uint64)
    bvalue = np.zeros((len(cvalue), nbits))

    # Overflow
    bvalue[ivalue > 2**nbits - 1] = np.ones((nbits,))

    # Underflow
    bvalue[ivalue < 0] = np.zeros((nbits,))

    bitmask = (2**np.arange(nbits)).astype(np.uint64)
    bvalue[np.logical_and(ivalue >= 0, ivalue <= 2**nbits - 1)] = (np.bitwise_and(np.tile(ivalue[:, np.newaxis], (1, nbits)), np.tile(bitmask[np.newaxis, :], (len(cvalue), 1))) != 0)
    return bvalue

def bin2ufloat(bvalue, nbits):
    # Convert a binary vector into floating point values
    if nbits > 64:
        raise Exception('Maximum number of bits limited to 64')
    ivalue = np.sum(bvalue * (2**np.arange(nbits)[np.newaxis, :]), axis=-1)
    cvalue = ivalue / (2**nbits - 1)
    return cvalue

def trainGA(monster):
    # Set parameters for GA
    numparams = 12
    nbits = 8
    popsize = 40

    # Init GA
    ga_sim = Genetic(numparams, popsize, nbits)
    ga_sim.init_pop()

    ga_sim.set_fit_fun(monster)

    numGenerations = 1000
    mutationProb = 0.01
    crossoverProb = 0.8
    ga_sim.set_sim_parameters(numGenerations, mutationProb, crossoverProb)
    ga_sim.set_crossover_modulo(nbits)

    while ga_sim.bestIndividualFitness<3.5 and ga_sim.current_gen!=numGenerations:
        ga_sim.decode_individuals()
        ga_sim.eval_fit()
        ga_sim.new_gen()
    print(ga_sim.current_gen)
    return ga_sim.get_best_individual()

def testGA(monster):
    # Set parameters for GA
    numparams = 12
    nbits = 8
    popsize = 40

    # Init GA
    ga_sim = Genetic(numparams, popsize, nbits)

    ga_sim.set_fit_fun(monster)

    numGenerations = 100
    mutationProb = 0.01
    crossoverProb = 0.8
    ga_sim.set_sim_parameters(numGenerations, mutationProb, crossoverProb)
    ga_sim.set_crossover_modulo(nbits)

    #Run fight simulation 100 times verify if it always converges
    import time
    start = time.time()
    num_gens=np.zeros(100000)
    for i in range(100000):
        ga_sim.init_pop()
        while ga_sim.bestIndividualFitness < 3.5 and ga_sim.current_gen != numGenerations:
            ga_sim.decode_individuals()
            ga_sim.eval_fit()
            ga_sim.new_gen()
        num_gens[i]=ga_sim.current_gen
    end = time.time()
    print('Max number of gens',num_gens.max())
    print("Time elapsed:", end - start)
    print()
