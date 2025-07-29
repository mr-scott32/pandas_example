from data_module import *

def main_menu():
    while True:
        print("\n=== Data Viewer Interface ===")
        print("1. View dataset")
        print("2. View visualisation")
        print("3. Exit")

        choice = input("Select an option (1-3): ").strip()

        if choice == '1':
            display_dataset_preview()
        elif choice == '2':
            compare_big_mac_and_cpi()
        elif choice == '3':
            print("Exiting program.")
            break
        else:
            print("Invalid selection. Please choose a number between 1 and 3.")

if __name__ == "__main__":
    main_menu()