from model import Model
from element import Create, Process
import pandas as pd


def tasks_1_2():
    create = Create("CREATE")
    process = Process("PROCESSOR", max_workers=1, max_queue=1)

    create.next_elements = [process]
    model = Model([create, process])
    model.simulate(1000)


def tasks_3_4():
    process1_delay = [1.0, 5.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0]
    process2_delay = [1.0, 1.0, 5.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0]
    process3_delay = [1.0, 1.0, 1.0, 5.0, 1.0, 1.0, 1.0, 1.0, 1.0]
    process1_max_queue = [5, 5, 5, 5, 1, 5, 5, 5, 5]
    process2_max_queue = [5, 5, 5, 5, 5, 1, 5, 5, 5]
    process3_max_queue = [5, 5, 5, 5, 5, 5, 1, 5, 5]
    create_delay = [2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 5.0, 1.0]
    result = pd.DataFrame()

    for i in range(9):
        create = Create("CREATE", mean_delay=create_delay[i])
        process1 = Process("PROCESSOR_1", max_workers=1, max_queue=process1_max_queue[i], mean_delay=process1_delay[i])
        process2 = Process("PROCESSOR_2", max_workers=1, max_queue=process2_max_queue[i], mean_delay=process2_delay[i])
        process3 = Process("PROCESSOR_3", max_workers=1, max_queue=process3_max_queue[i], mean_delay=process3_delay[i])

        create.next_elements = [process1]
        process1.next_elements = [process2]
        process2.next_elements = [process3]

        model = Model([create, process1, process2, process3])
        model.simulate(1000)

        create_num = model.elements[0].processed
        process1_num = model.elements[1].processed
        process2_num = model.elements[2].processed
        process3_num = model.elements[3].processed
        process1_mean_queue = round(model.elements[1].mean_queue / model.elements[1].tcurr, 2)
        process2_mean_queue = round(model.elements[2].mean_queue / model.elements[2].tcurr, 2)
        process3_mean_queue = round(model.elements[3].mean_queue / model.elements[3].tcurr, 2)
        process1_failures = model.elements[1].failures
        process2_failures = model.elements[2].failures
        process3_failures = model.elements[3].failures
        process1_failure_probability = round(process1_failures / (process1_num + process1_failures), 2)
        process2_failure_probability = round(process2_failures / (process2_num + process2_failures), 2)
        process3_failure_probability = round(process3_failures / (process3_num + process3_failures), 2)

        data = {
            "create_num": [create_num],
            "process1_num": [process1_num],
            "process2_num": [process2_num],
            "process3_num": [process3_num],
            "process1_mean_queue": [process1_mean_queue],
            "process2_mean_queue": [process2_mean_queue],
            "process3_mean_queue": [process3_mean_queue],
            "process1_failure_probability": [process1_failure_probability],
            "process2_failure_probability": [process2_failure_probability],
            "process3_failure_probability": [process3_failure_probability]
        }

        result = pd.concat([result, pd.DataFrame(data)], ignore_index=True)

    result.to_csv("result.csv")



def tasks_5_6():
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
    # tasks_1_2()
    tasks_3_4()
    # tasks_5_6()
