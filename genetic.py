#!/usr/bin/env python

import os
import psutil
import random
import time

N = 8
POPULATION = 100

maxFitness = 28


# Counting how many queens are under attack
def fitness(board):
    total_under_attack = 0
    # Count how many queens are in same index for horizontal collision
    for x1, y1 in enumerate(board):
        for x2, y2 in enumerate(board):
            if x1 != x2 and (y1 == y2 or abs(x1-x2) == abs(y1-y2)):
                total_under_attack = total_under_attack + 1
    return total_under_attack


def probability(board, fitness):
    return (28 - fitness(board)) / maxFitness


def random_pick(population, probabilities):
    total = sum(w for c, w in zip(population, probabilities))
    r = random.uniform(0, total)
    upto = 0
    for c, w in zip(population, probabilities):
        if upto + w >= r:
            return c
        upto += w


def crossover(x, y):
    c = random.randint(0, N - 1)
    return x[0:c] + y[c:N]


def mutate(x):
    c = random.randint(0, N - 1)
    m = random.randint(0, N - 1)
    x[c] = m
    return x


def genetic(population, fitness):
    mutation_probability = 0.2
    new_population = []
    probabilities = [probability(n, fitness) for n in population]
    for i in range(len(population)):
        x = random_pick(population, probabilities)
        y = random_pick(population, probabilities)
        child = crossover(x, y)
        if random.random() < mutation_probability:
            child = mutate(child)
        # print_individual(child)
        new_population.append(child)
        if fitness(child) == 0: break
    return new_population


def print_board(x):
    print("{},  collision = {}, probability = {:.6f}"
          .format(str(x), fitness(x), probability(x, fitness)))


if __name__ == "__main__":
    t0 = time.time()

    # Populate first generation
    population = [[random.randint(0, N - 1) for _ in range(N)] for _ in range(POPULATION)]

    i = 0
    while 0 not in [fitness(x) for x in population]:
        population = genetic(population, fitness)
        print("Min collision in generation {} = {}".format(i, min([fitness(n) for n in population])))
        i += 1

    print("Solved in Generation {}!".format(i - 1))
    for x in population:
        if fitness(x) == 28:
            print_board(x)

    process = psutil.Process(os.getpid())
    print("\nRam usage: {} bytes".format(process.memory_info().rss))
    print("Time: {} seconds".format(time.time()-t0))
