from math import exp
import random
import os
import psutil
import time

N = 8
T = 4000

def fitness(board):
    total_under_attack = 0
    # Count how many queens are in same index for horizontal collision
    for x1, y1 in enumerate(board):
        for x2, y2 in enumerate(board):
            if x1 != x2 and (y1 == y2 or abs(x1 - x2) == abs(y1 - y2)):
                total_under_attack = total_under_attack + 1
    return total_under_attack


def print_board(k, x):
    print("k = {}, {},  collision = {}".format(k, str(x), fitness(x)))


if __name__ == "__main__":
    t0 = time.time()

    board = [random.randint(0, N - 1) for _ in range(N)]

    k = 0
    temperature = T
    while True:
        k = k + 1
        temperature = T / float(k + 1)
        successor_board = board.copy()
        while successor_board == board:
            random_index = random.randint(0, N-1)
            random_value = random.randint(0, N-1)
            successor_board[random_index] = random_value
        diff = fitness(successor_board) - fitness(board)
        metropolis = exp(-diff / temperature)
        if diff < 0 or random.uniform(0, 1) < metropolis:
            board = successor_board
        if fitness(board) == 0:
            print('\nSolution Found:')
            print_board(k, board)
            break
        elif k % 100 == 0:
            print_board(k, board)

    process = psutil.Process(os.getpid())
    print("\nRam usage: {} bytes".format(process.memory_info().rss))
    print("Time: {} seconds".format(time.time()-t0))


0.057200+0.070531+0.133856+0.037510+0.043622