import os
import sys

import Events
from Loader import Loader
from Metrics import Metrics
from SimulationLog import SimulationLog
from Simulator import Simulator


class MainMenu:
    def __init__(self, sim: Simulator, metrics: Metrics):
        self.sim = sim
        self.metrics = metrics
        self.choice = None
        self.config_loaded = False
        self.simulation_run = False
        self.config = None

    def clear_screen(self):
        """
        Clear the console screen.
        """
        os.system("cls" if os.name == "nt" else "clear")


    def print_header(self):
        print("=" * 60)
        print("PUBLIC TRANSIT DISCRETE-EVENT SIMULATION SYSTEM".center(60))
        print("=" * 60)
        print("-" * 60)


    def print_main_menu(self):
        print("\nMain Menu")
        print("-" * 30)
        print("1. Load Configuration File")
        print("2. Run Simulation")
        print("3. View Simulation Logs")
        print("4. Exit")
        print("-" * 30)


    def pause(self):
        input("\nPress Enter to return to the main menu...")

    def load_config(self):
        """
        Load the configuration file.
        :return: true if the configuration file was successfully loaded.
        """
        file_path = input("Enter YAML configuration file path: ").strip()
        print(f"\nLoading configuration from '{file_path}'...")
        self.config = Loader(file_path)
        if self.config is None:
            print("Failed to load config file.")
            return False
        else:
            print("Configuration loaded successfully.")
            return True

    def run_simulation(self):
        """
        Run the simulation.
        """
        if self.config.vehicles is not None:
            self.sim.vehicles = self.config.vehicles
        else:
            raise TypeError("Vehicles not loaded.")
        if self.config.routes is not None:
            self.sim.route_queue = self.config.routes
        else:
            raise TypeError("Routes not loaded.")
        for vehicle in self.sim.vehicles.values():
            self.sim.schedule_event(Events.StartService(0,vehicle))
        self.sim.run()
        self.metrics.save_log(SimulationLog(
            self.sim.log, self.sim.vehicles, self.sim.completed_passengers
        ))

    def view_logs(self):
        self.clear_screen()
        i = 0
        # Print a list of saved logs
        for log in self.metrics.saved_logs:
            i += 1
            print(f"Log[{i}]")
        # Print the selected log
        while True:
            self.choice = input(f"\nSelect a log to view (1-{i})").strip()
            if self.choice.isdigit() and 0 < int(self.choice) <= i:
                self.metrics.print_all(i)
                break
            else:
                print("\nInvalid selection. Please choose a valid option.")

    def choose(self):
        self.choice = input("Select an option (1-3): ").strip()
        # Load config file
        if self.choice == "1":
            self.config_loaded = self.load_config()
            self.pause()
        # Run the simulation
        elif self.choice == "2":
            if not self.config_loaded:
                print("\nError: Load configuration before running simulation.")
                self.pause()
            else:
                self.run_simulation()
                self.pause()
        elif self.choice == "3":
            if self.metrics is None or len(self.metrics.saved_logs) == 0:
                print("\nError: No saved logs to display.")
                self.pause()
            else:
                self.view_logs()
                self.pause()
        elif self.choice == "4":
            print("\nExiting system. Goodbye.")
            sys.exit()
        else:
            print("\nInvalid selection. Please choose a valid option.")
            self.pause()

def main():
    sim = Simulator()
    metrics = Metrics()
    menu = MainMenu(sim, metrics)
    # Menu Loop
    while True:
        menu.clear_screen()
        menu.print_header()
        menu.print_main_menu()
        menu.choose()

if __name__ == "__main__":
    main()
