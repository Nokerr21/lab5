import math
import random
import copy
from cec2017.functions import f2
from cec2017.functions import f13
import numpy as np


def generate_starting_population(population_size, lower_bound, upper_bound, dimensionality):
    population = []
    for i in range(0, population_size):
        calculated_cords = np.random.uniform(lower_bound, upper_bound, size=dimensionality)
        population.append([calculated_cords, []])

    return population


def simulate_evolution(population, function):
    # population = generate_starting_population(population_size, upper_bound, dimensionality)
    assess_population(population, function)
    global_best_individual = find_best_individual(population)
    # print("best_individual: ", global_best_individual)
    current_iteration = 0
    while current_iteration <= EVOLUTION_ITERATIONS:
        # print("population", population)
        new_population = create_new_generation(population)
        assess_population(new_population, function)
        current_best_individual = find_best_individual(new_population)
        if current_best_individual[1] < global_best_individual[1]:
            global_best_individual = current_best_individual
        # print("Iteration: " + str(current_iteration) + ": " + str(global_best_individual))
        # print("current_population", new_population)
        population = new_population
        current_iteration += 1


def assess_population(population, function):
    for individual in population:
        individual[1] = function(individual[0])


def find_best_individual(population):
    population.sort(key=lambda x: x[1], reverse=False)
    return population[0]


def create_new_generation(population):
    new_population = tournament_selection(population)
    return mutate(new_population)


def tournament_selection(population):
    successors = []
    for i in range(0, len(population)):
        pretender1 = random.choice(population)
        pretender2 = random.choice(population)
        # print(population)
        print("Pretender1: ", pretender1)
        print("Pretender2: ", pretender2)
        # print(population)
        if pretender1[1] < pretender2[1]:
            successors.append(copy.deepcopy(pretender1))
        else:
            successors.append(copy.deepcopy(pretender2))
    # print(successors)
    return successors


def mutate(population):
    print("MUTATION_FACTOR", MUTATION_FACTOR)
    mutated_population = population.copy()
    for individual in mutated_population:
        mutation_rate = random.gauss(0, 1)
        individual[0] = individual[0] + (mutation_rate * MUTATION_FACTOR)
    return mutated_population


POPULATION_SIZE = 20
BUDGET = 100
DIMENSIONS = 10
UPPER_BOUND = 100
EVOLUTION_ITERATIONS = math.ceil(BUDGET / POPULATION_SIZE)
MUTATION_FACTOR = 2
starting_population = generate_starting_population(POPULATION_SIZE, -UPPER_BOUND, UPPER_BOUND, DIMENSIONS)
print(starting_population)
simulate_evolution(starting_population, f2)

# 6 linijka to selekcja turniejowa
# 7 linijka to mutacja
# 14 linijka to sukcesja generacyjna
