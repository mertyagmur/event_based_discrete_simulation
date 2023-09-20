import numpy as np
import pandas as pd
from numpy import random
import random as rn

class Toll_Booth:
    def __init__(self, mean_arrival_rate_r1, mean_arrival_rate_r2, mean_arrival_rate_r3, mean_service_rate):
        self.time = 0.0
        self.departure_time = 9999999  # Departure time of the next event
        self.num_in_queue = 0          # Number of cars in the queue
        self.cars_served = 0           # Number of cars that are served
        self.server_idle = True        # Status of the server
        self.departure_times = []      # List of departure times for all departure events
        self.service_times = []        # List of service times calculated for all cars
        self.interarrival_times_all = []        # List of all interarrival times from the cars of all 3 roads
        self.interarrival_times_r1 = []         # List of interarrival times from the cars of Road 1
        self.interarrival_times_r2 = []         # List of interarrival times from the cars of Road 2
        self.interarrival_times_r3 = []         # List of interarrival times from the cars of Road 3
        self.mean_arrival_rate_r1 = mean_arrival_rate_r1    # Mean arrival rate for Road 1 taken as input
        self.mean_arrival_rate_r2 = mean_arrival_rate_r2    # Mean arrival rate for Road 2 taken as input
        self.mean_arrival_rate_r3 = mean_arrival_rate_r3    # Mean arrival rate for Road 3 taken as input
        self.mean_service_rate = mean_service_rate                  # Mean service rate taken as input
        self.arrival_time = self.generate_interarrival_time()       # Arrival time of the next event
        self.arrival_times = [self.arrival_time]                    # List of arrival times for all arrival events
        self.event_counter = 0                              # Counter for all events                                      
        
    # Simulates the passing of time and generates new events
    def pass_time(self):
        self.event_counter += 1

        # Minimum of the arrival_time and departure_time is scheduled to be the next event
        next_event_time = min(self.arrival_time, self.departure_time) 
        self.time = next_event_time # Advance time to the next event
        
        if self.arrival_time < self.departure_time:
            self.arrival()
        else:
            self.service()

    # Simulates an arrival event
    def arrival(self):
        if self.num_in_queue == 0: # If the queue is empty and server is not idle
            if not self.server_idle:
                self.num_in_queue += 1 # Add one to the queue
                
                # Schedule next arrival event
                self.interarrival_time = self.generate_interarrival_time()
                self.arrival_time = self.time + self.interarrival_time
                self.arrival_times.append(self.arrival_time)

            elif self.server_idle: # If the queue is empty and server is idle

                # Schedule next departure event
                self.service_time = self.generate_service_time()
                self.departure_time = self.time + self.service_time
                self.departure_times.append(self.departure_time)

                # Schedule next arrival event
                self.interarrival_time = self.generate_interarrival_time()
                self.arrival_time = self.time + self.interarrival_time
                self.arrival_times.append(self.arrival_time)

                self.server_idle = False
        else: 
            self.num_in_queue += 1
            self.interarrival_time = self.generate_interarrival_time()
            self.arrival_time = self.time + self.interarrival_time
            self.arrival_times.append(self.arrival_time)

    # Simulates server
    def service(self):
        self.cars_served += 1
        if self.num_in_queue > 0: # If queue is not empty
            # Schedule next departure event
            self.service_time = self.generate_service_time()
            self.departure_time = self.time + self.service_time
            self.departure_times.append(self.departure_time)
            self.num_in_queue -= 1
        else:
            self.departure_time = 9999999 # Make sure the next event is an arrival event
            self.server_idle = True

    # Generates interarrival times to be used in arrival time calculation
    def generate_interarrival_time(self):

        # Select one out of 3 roads based on arrival rates given as weights
        selected_road = rn.choices(population=[1, 2, 3], weights=[self.mean_arrival_rate_r1, self.mean_arrival_rate_r2, self.mean_arrival_rate_r3], k=1)

        if selected_road[0] == 1:
            mean_arrival_rate = self.mean_arrival_rate_r1
            interarrival_times = self.interarrival_times_r1
        elif selected_road[0] == 2:
            mean_arrival_rate = self.mean_arrival_rate_r2
            interarrival_times = self.interarrival_times_r2
        elif selected_road[0] == 3:
            mean_arrival_rate = self.mean_arrival_rate_r3  
            interarrival_times = self.interarrival_times_r3  

        # Generate interarrival time
        mean_interarrival_time = 1.0 / mean_arrival_rate
        int_arr_time = random.exponential(scale=mean_interarrival_time, size=1)[0]
        interarrival_times.append(int_arr_time)
        self.interarrival_times_all.append(int_arr_time)
        return int_arr_time

    # Generates service times to be used in arrival time calculation
    def generate_service_time(self):
        mean_service_time = 1.0 / self.mean_service_rate
        service_time = random.exponential(scale=mean_service_time, size=1)[0]
        self.service_times.append(service_time)
        return service_time

def main():

    # Take user input
    mean_arrival_rate_r1 = int(input("Enter mean arrival rate for Road 1: "))
    mean_arrival_rate_r2 = int(input("Enter mean arrival rate for Road 2: "))
    mean_arrival_rate_r3 = int(input("Enter mean arrival rate for Road 3: "))
    mean_service_rate = int(input("Enter mean service rate: "))
    is_debug = input("Do you want to enter debug mode? (y/n)").lower().strip() == 'y'

    # Create simulation object
    sim = Toll_Booth(mean_arrival_rate_r1, mean_arrival_rate_r2, mean_arrival_rate_r3, mean_service_rate)

    # Run the simulation
    while sim.cars_served != 100000:
        sim.pass_time()

    # Print expected and simulated rates
    print(f"Expected mean arrival time of Road 1: {1.0 / mean_arrival_rate_r1}")
    print(f"Expected mean arrival time of Road 2: {1.0 / mean_arrival_rate_r2}")
    print(f"Expected mean arrival time of Road 3: {1.0 / mean_arrival_rate_r3}")
    print(f"Expected mean service time: {1.0 / mean_service_rate}\n")

    print(f"Simulated mean arrival time of Road 1: {sum(sim.interarrival_times_r1[1:])/len(sim.interarrival_times_r1)}")
    print(f"Simulated mean arrival time of Road 2: {sum(sim.interarrival_times_r2[1:])/len(sim.interarrival_times_r2)}")
    print(f"Simulated mean arrival time of Road 3: {sum(sim.interarrival_times_r3[1:])/len(sim.interarrival_times_r3)}")
    print(f"Simulated mean service time: {sum(sim.service_times)/len(sim.service_times)}\n")

    # Calculate queue and system wait times
    stats = list(zip(sim.interarrival_times_all, sim.arrival_times, sim.service_times, sim.departure_times))
    queue_wait_times = [unit1[3] - unit2[1] if unit2[1] < unit1[3] else 0.0 for unit1, unit2 in zip(stats[:-1], stats[1:])]
    queue_wait_times.insert(0,0)

    total_wait_times = [unit[3] - unit[1] for unit in stats]

    # Generate tabular data
    data = pd.DataFrame(list(zip(sim.interarrival_times_all, sim.arrival_times, sim.service_times, sim.departure_times, queue_wait_times, total_wait_times)), 
                    columns =["Interarrival Time", "Arrival Time", "Service Time", "Departure Time", "Queue Wait Time", "Total Wait Time"]) 

    # Print tabular data if debug mode is selected
    if is_debug:
        print(data)

    # Print results
    print(f"Average waiting time in queue: {sum(queue_wait_times)/sim.cars_served}")
    print(f"Average waiting time in system: {sum(total_wait_times)/sim.cars_served}")

    print((
        "Percentages: "
        f"Road1: {len(sim.interarrival_times_r1) / len(sim.arrival_times)* 100:.2f}% "
        f"Road2: {len(sim.interarrival_times_r2) / len(sim.arrival_times)* 100:.2f}% "
        f"Road3: {len(sim.interarrival_times_r3) / len(sim.arrival_times)* 100:.2f}% "
        ))

if __name__ == '__main__':
    main()