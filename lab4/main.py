from model import Model
from element import Create, Process
import pandas as pd
import numpy as np
import time


def linear_model(N):
    print("Linear model")
    df = pd.DataFrame(columns=["N", "Time"])

    for n in range(10, N + 1, 5):
        results = np.array([])

        for _ in range(5):
            create = Create("CREATE")
            processes = [Process(f"PROCESS_{i}") for i in range(n)]
            create.next_elements = [processes[0]]

            for i in range(n - 1):
                processes[i].next_elements = [processes[i + 1]]

            model = Model([create] + processes)
            start = time.time()
            model.simulate(1000)
            end = time.time()
            results = np.append(results, end - start)

        df.loc[n] = [n, results.mean()]
        print(f"N = {n} | time = {results.mean()}")

    df.to_csv("data/linear.csv", index=False)


def parallel_model(N):
    print("Parallel model")
    df = pd.DataFrame(columns=["N", "Time"])

    for n in range(10, N + 1, 5):
        results = np.array([])

        for _ in range(5):
            create = Create("CREATE")
            processes = [Process(f"PROCESS_{i}") for i in range(n)]

            # Split processes into 4 groups
            first_group = processes[:n // 4]
            second_group = processes[n // 4: n // 2]
            third_group = processes[n // 2: 3 * n // 4]
            fourth_group = processes[3 * n // 4:]

            create.next_elements = first_group
            
            for process in first_group:
                process.next_elements = second_group

            for process in second_group:
                process.next_elements = third_group

            for process in third_group:
                process.next_elements = fourth_group

            model = Model([create] + processes)
            start = time.time()
            model.simulate(1000)
            end = time.time()
            results = np.append(results, end - start)

        df.loc[n] = [n, results.mean()]
        print(f"N = {n} | time = {results.mean()}")

    df.to_csv("data/parallel.csv", index=False)


if __name__ == "__main__":
    linear_model(100)
    parallel_model(100)
