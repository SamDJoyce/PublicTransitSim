import os
import sys

import Events
from Loader import Loader
from Simulator import Simulator


class MainMenu:
    def __init__(self):
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
        print("3. Exit")
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
        vehicles = self.config.vehicles
        routes = self.config.routes
        sim = Simulator(vehicles, routes)
        for vehicle in sim.vehicles.values():
            sim.schedule_event(Events.StartService(0,vehicle))
        sim.run()


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
            print("\nExiting system. Goodbye.")
            sys.exit()
        else:
            print("\nInvalid selection. Please choose a valid option.")
            self.pause()

def main():
    menu = MainMenu()
    # Menu Loop
    while True:
        menu.clear_screen()
        menu.print_header()
        menu.print_main_menu()
        menu.choose()

if __name__ == "__main__":
    main()
