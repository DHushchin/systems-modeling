from model import Model

def main():
    model = Model(mean_create_delay=0.5, mean_process_delay=1.0, max_queue_size=3)
    model.simulate(1000)

if __name__ == "__main__":
    main()
