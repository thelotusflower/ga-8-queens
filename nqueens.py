import random as rnd
import copy
from math import fabs

class Solver_8_queens:

    def __init__(self, cross_prob=0.4, mut_prob=0.3, pop_size=160):
        self.pop_size = pop_size
        self.cross_prob = cross_prob
        self.mut_prob = mut_prob


    def initial_population(self):
        rnd.seed()
        in_pop = []

        for i in range(self.pop_size):
            chrom = [[0]*8 for i in range(8)]
            in_pop.append(chrom)

        for chrom in in_pop:
            for el in chrom:
                i = rnd.randrange(0, 8)
                el[i] = 1

        return in_pop


    def if_hit(self, pos):
        queens = 0
        count = 0

        while count != 8:

            current = pos.pop(0)
            hit = False

            for i in range(len(pos)):
                if current[0] == pos[i][0] or current[1] == pos[i][1] \
                        or fabs(pos[i][0] - current[0]) == fabs(pos[i][1] - current[1]):
                    hit = True
                    break
            if not hit:
                queens += 1

            pos.append(current)
            count += 1
        return queens


    def find_queen_pos(self, chrom):
        positions = []

        positions.clear()
        fit_value = 0.01
        for i in range(8):
            for j in range(8):
                if chrom[i][j] == 1:
                    positions.append((i, j))

        return positions


    def fitness_function(self, pop):
        valued_chroms = []
        fit_value = 0.01
        count = 0

        for chrom in pop:
            positions = self.find_queen_pos(chrom)
            if len(positions) != 8:
                valued_chroms.append((count, 0.01))
                count += 1
                continue
            fit_value = self.if_hit(positions) + 0.1
            valued_chroms.append((count, fit_value))
            count += 1

        return valued_chroms


    def roulette(self, fit):
        rnd.seed()
        summ = 0
        mating_probs = []
        mating = []

        for value in fit:
            summ += value[1]

        prev_prob = 0.0

        for value in fit:
            prob = prev_prob + (value[1]/int(summ))
            prev_prob = prob
            mating_probs.append(prob)

        for i in range(int(self.pop_size*self.cross_prob)):
            thresh = rnd.random()
            for prob in mating_probs:
                if prob > thresh:
                    ind = mating_probs.index(prob)
                    mating.append(fit[ind][0])
                    break

        return mating


    def crossover(self, mates):
        rnd.seed()
        children = []

        while len(mates) > 0:
            child_1 = []
            child_2 = []
            num_1 = rnd.randrange(0, len(mates) - 1)
            num_2 = rnd.randrange(0, len(mates) - 1)

            if num_1 > num_2:
                parent_1 = mates.pop(num_1)
                parent_2 = mates.pop(num_2)
            elif len(mates) == 2:
                parent_1 = mates.pop(0)
                parent_2 = mates.pop(0)
            else:
                parent_2 = mates.pop(num_2)
                parent_1 = mates.pop(num_1)

            crossover_point = rnd.randrange(1, 8)

            child_1.extend(parent_1[0:crossover_point])
            child_1.extend(parent_2[crossover_point:])

            child_2.extend(parent_2[0:crossover_point])
            child_2.extend(parent_1[crossover_point:])

            children.append(child_1)
            children.append(child_2)
        return children


    def mutate(self, children):
        rnd.seed()

        for child in children:

            if rnd.random() < self.mut_prob:
                i = rnd.randrange(8)
                ind = child[i].index(1)
                child[i][ind] = 0
                j = rnd.randrange(8)
                child[i][j] = 1


    def reduction(self, fit):
        to_reduce = []
        for i in range(int(self.pop_size*self.cross_prob)):
            to_reduce.append(fit[i][0])
        return to_reduce


    def solve(self, min_fitness= 7, max_epochs=100):
        prev_pop = self.initial_population()
        epochs = 0
        max_fitness = 0

        while (max_fitness <= min_fitness) and (epochs < max_epochs):
            fitness = self.fitness_function(prev_pop)
            fitness.sort(key=lambda tup: tup[1])

            best_sol = fitness[len(fitness) - 1][0]
            max_fitness = fitness[len(fitness) - 1][1]
            mating = self.roulette(fitness)

            mating_chromes = []
            pop = copy.deepcopy(prev_pop)
            for chrom in mating:
                mating_chromes.append(pop[chrom])
            pop.clear()

            children = self.crossover(mating_chromes)
            self.mutate(children)
            fit = self.fitness_function(prev_pop)


            to_destroy = self.reduction(fitness)

            for el in to_destroy:
                prev_pop[el] = children.pop(0)

            epochs += 1

        visualization = ""
        for el in prev_pop[best_sol]:
            for num in el:
                if num == 1:
                    visualization += "Q"
                else:
                    visualization += "+"
            visualization += "\n" 
        
        return max_fitness, epochs, visualization
