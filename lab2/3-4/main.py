from model import Model
from event_create import EventCreate
from event_process import EventProcess


def main():
    event_create = EventCreate(name="create", delay=2)
    event_process_1 = EventProcess(name="process1", delay=5, max_queue=5)
    event_process_2 = EventProcess(name="process2", delay=1, max_queue=5)
    event_process_3 = EventProcess(name="process3", delay=1, max_queue=5)

    event_create.set_next_element(event_process_1)
    event_process_1.set_next_element(event_process_2)
    event_process_2.set_next_element(event_process_3)

    model = Model(create_event=event_create, process_events=[event_process_1, event_process_2, event_process_3])
    model.simulate(1000)

if __name__ == "__main__":
    main()
