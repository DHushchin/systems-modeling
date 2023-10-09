from generator import Generator

class Model:
    def __init__(self, mean_create_delay, mean_process_delay, max_queue_size=None):
        """
        Initialize the model with mean create delay, mean process delay, and optional max queue size.

        Args:
            mean_create_delay (float): Mean time between request arrivals.
                It represents the average time between incoming requests.
            mean_process_delay (float): Mean time to process a request.
                It represents the average time it takes to process a request.
            max_queue_size (int, optional): Maximum queue size (default is None).
                It specifies the maximum number of requests that can be queued.
                If not provided (None), the queue size is considered infinite.
        """
        self.t_next_event = 0.0  # The time of the next event to be processed.
        self.t_curr = self.t_next_event  # The current simulation time.
        self.arrival_time = self.t_curr  # The time of the current request arrival.
        self.processing_completion_time = float('inf')  # The time of the current request processing completion.
        self.delay_create = mean_create_delay  # Mean time between request arrivals.
        self.delay_process = mean_process_delay  # Mean time to process a request.
        self.total_processing_time = 0.0  # Accumulator for total processing time.
        self.num_create = 0  # Number of requests created.
        self.num_process = 0  # Number of requests processed.
        self.failure = 0  # Number of requests that couldn't be queued due to max_queue limit.
        self.state = 0  # State of the system (0 for idle, 1 for busy).
        self.max_queue = max_queue_size if max_queue_size is not None else float('inf')
        # Maximum queue size (if provided), otherwise considered infinite.
        self.queue = 0  # Current number of requests in the queue.
        self.next_event = 0  # Type of the next event (0 for request arrival, 1 for request processing).


    def simulate(self, time_modeling):
        """
        Simulate the model for a specified duration.

        Args:
            time_modeling (float): The duration of the simulation in arbitrary time units.
        """
        while self.t_curr < time_modeling:
            self.t_next_event = self.arrival_time
            self.next_event = 0

            if self.processing_completion_time <= self.t_next_event:
                self.t_next_event = self.processing_completion_time
                self.next_event = 1

            self.t_curr = self.t_next_event

            if self.next_event == 0:
                self.event_create()
            else:
                self.event_process()

            self.print_info()

        self.print_statistic(time_modeling)


    def event_create(self):
        self.arrival_time = self.t_curr + self.get_delay_create()
        self.num_create += 1

        if self.state == 0:
            self.state = 1
            self.processing_completion_time = self.t_curr + self.get_delay_process()
        else:
            if self.queue < self.max_queue:
                self.queue += 1
            else:
                self.failure += 1


    def event_process(self):
        self.processing_completion_time = float('inf')
        self.state = 0

        if self.queue > 0:
            self.queue -= 1
            self.state = 1
            processing_time = self.get_delay_process()
            self.processing_completion_time = self.t_curr + processing_time
            self.total_processing_time += processing_time 

        self.num_process += 1

    def print_statistic(self, time_modeling):
        avg_load_time = self.total_processing_time / time_modeling
        print("numCreate = " + str(self.num_create) +
              " numProcess = " + str(self.num_process) +
              " failure = " + str(self.failure) +
              " avgProcessingTime = " + str(avg_load_time))

    def print_info(self):
        print("t = " + str(self.t_curr) +
              " state = " + str(self.state) +
              " queue = " + str(self.queue))

    def get_delay_create(self):
        return Generator.exp(self.delay_create)

    def get_delay_process(self):
        return Generator.exp(self.delay_process)
