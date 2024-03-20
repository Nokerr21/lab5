import math
import random
import statistics
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
    assess_population(population, function)
    global_best_individual = find_best_individual(population)
    current_iteration = 0
    while current_iteration <= EVOLUTION_ITERATIONS:
        new_population = create_new_generation(population)
        assess_population(new_population, function)
        current_best_individual = find_best_individual(new_population)
        if current_best_individual[1] < global_best_individual[1]:
            global_best_individual = current_best_individual
        population = new_population
        current_iteration += 1
    return global_best_individual


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
        if pretender1[1] < pretender2[1]:
            successors.append(pretender1)
        else:
            successors.append(pretender2)
    return successors


def mutate(population):
    mutated_population = []
    for individual in population:
        mutation_rate = np.random.normal(0, 1, len(individual[0]))
        mutated_individual = individual[0] + (mutation_rate * SIGMA)

        for i in range(0, len(mutated_individual)):
            if mutated_individual[i] > UPPER_BOUND:
                mutated_individual[i] = UPPER_BOUND
            elif mutated_individual[i] < -UPPER_BOUND:
                mutated_individual[i] = -UPPER_BOUND

        mutated_population.append([mutated_individual, []])
    return mutated_population


def perform_simulation(population, function):
    results = []
    grades = []

    for i in range(0, 50):
        results.append(simulate_evolution(population, function))
    results.sort(key=lambda x: x[1], reverse=False)
    for result in results:
        grades.append(result[1])

    print("Min wynik: " + str(results[0][1]) + " osiągnięty dla: " + str(results[0][0]))
    print("Max wynik: " + str(results[-1][1]) + " osiągnięty dla: " + str(results[-1][0]))
    print("Średni wynik: ", sum(grades) / len(grades))
    print("Odchylenie standardowe: ", statistics.stdev(grades))

    print()
    print()


POPULATION_SIZE = 8
BUDGET = 50000
DIMENSIONS = 10
UPPER_BOUND = 100
EVOLUTION_ITERATIONS = math.ceil(BUDGET / POPULATION_SIZE)
SIGMA = 0.7
starting_population = generate_starting_population(POPULATION_SIZE, -UPPER_BOUND, UPPER_BOUND, DIMENSIONS)
perform_simulation(starting_population, f2)
perform_simulation(starting_population, f13)
