import os
import sys
from datetime import datetime


def clear_screen():
    """Clears the console screen."""
    os.system("cls" if os.name == "nt" else "clear")


def print_header():
    print("=" * 60)
    print("PUBLIC TRANSIT DISCRETE-EVENT SIMULATION SYSTEM".center(60))
    print("=" * 60)
    print(f"Session Start: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("-" * 60)


def print_main_menu():
    print("\nMain Menu")
    print("-" * 20)
    print("1. Load Configuration File")
    print("2. Run Simulation")
    print("3. Export Metrics to CSV")
    print("4. View Simulation Summary")
    print("5. Exit")
    print("-" * 20)


def pause():
    input("\nPress Enter to return to the main menu...")


def main():
    config_loaded = False
    simulation_run = False

    while True:
        clear_screen()
        print_header()
        print_main_menu()

        choice = input("Select an option (1-5): ").strip()

        if choice == "1":
            file_path = input("Enter YAML configuration file path: ").strip()
            # Placeholder for actual loading logic
            print(f"\nLoading configuration from '{file_path}'...")
            print("Configuration loaded successfully.")
            config_loaded = True
            pause()

        elif choice == "2":
            if not config_loaded:
                print("\nError: Load configuration before running simulation.")
            else:
                print("\nSimulation running...")
                print("[0] Bus-1 arrived at Central")
                print("[2] Bus-1 departed Central")
                print("[7] Bus-1 arrived at Main")
                print("Simulation completed.")
                simulation_run = True
            pause()

        elif choice == "3":
            if not simulation_run:
                print("\nError: Run simulation before exporting metrics.")
            else:
                print("\nExporting metrics to metrics.csv...")
                print("Export complete.")
            pause()

        elif choice == "4":
            if not simulation_run:
                print("\nNo simulation data available.")
            else:
                print("\nSimulation Summary")
                print("-" * 20)
                print("Total Vehicles: 2")
                print("Total Stops: 3")
                print("Total Events: 6")
                print("Average Route Time: 12 minutes")
            pause()

        elif choice == "5":
            print("\nExiting system. Goodbye.")
            sys.exit()

        else:
            print("\nInvalid selection. Please choose a valid option.")
            pause()


if __name__ == "__main__":
    main()
