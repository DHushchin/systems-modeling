from model import Model
from element import Create, Process
import pandas as pd


def task_1():
    create = Create("CREATE")
    process1 = Process("PROCESSOR 1", max_workers=1, max_queue=1)
    process2 = Process("PROCESSOR 2", max_workers=1, max_queue=1)
    process3 = Process("PROCESSOR 3", max_workers=1, max_queue=1)
    process4 = Process("PROCESSOR 4", max_workers=1, max_queue=1)
    process5 = Process("PROCESSOR 5", max_workers=1, max_queue=1)
    process6 = Process("PROCESSOR 6", max_workers=1, max_queue=1)

    create.next_elements = [process1]
    process1.set_next_elements([process2, process3, process4], priorities=[1, 2, 2], blocked=[False, True, False])
    process2.set_next_elements([process5, process6], probabilities=[0.2, 0.8], blocked=[False, False])
    process3.set_next_elements([process5, process6], probabilities=[0.2, 0.8], blocked=[False, False])
    process4.set_next_elements([process5, process6], probabilities=[0.2, 0.8], blocked=[False, False])

    model = Model([create, process1, process2, process3, process4, process5, process6])
    model.simulate(10000)


if __name__ == "__main__":
    task_1()
