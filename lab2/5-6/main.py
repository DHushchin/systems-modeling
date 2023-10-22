from model import Model
from element import Create, Process


def main():
    create = Create("CREATE")
    MAX_QUEUE = 5

    process1 = Process("PROCESSOR_1", max_workers=2, max_queue=MAX_QUEUE)
    process2 = Process("PROCESSOR_2", max_workers=1, max_queue=MAX_QUEUE)
    process3 = Process("PROCESSOR_3", max_workers=1, max_queue=MAX_QUEUE)
    process4 = Process("PROCESSOR_4", max_workers=2, max_queue=MAX_QUEUE)

    create.next_elements = [process1]
    process1.next_elements = [process2, process3]
    process2.next_elements = [process4]
    process3.next_elements = [process4]

    model = Model([create, process1, process2, process3, process4])
    model.simulate(1000)

if __name__ == "__main__":
    main()
