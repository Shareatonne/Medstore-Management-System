import os
from inventory import load_inventory, display_inventory
from transactions import sell_medicine, restock_medicine, search_medicine, view_low_stock, add_medicine

INVENTORY_FILE = "inventory.txt"
    
def print_menu():
    """Display the main menu options."""
    print("\n" + "=" * 55)
    print("       MEDSTORE PVT. LTD. — MAIN MENU")
    print("=" * 55)
    print("  1. Display Inventory")
    print("  2. Sell Medicine")
    print("  3. Restock Medicine")
    print("  4. Search Medicine")
    print("  5. View Low Stock")
    print("  6. Add New Medicine")
    print("  0. Exit")
    print("=" * 55)


def main():
    """Main application loop."""
    # Load inventory at startup
    medicines_list = load_inventory(INVENTORY_FILE)

    while True:
        display_inventory(medicines_list)
        print_menu()
        choice = input("Enter your choice (1-6): ").strip()

        # Handle menu selections
        if choice == "1":
            display_inventory(medicines_list)

        elif choice == "2":
            sell_medicine(medicines_list, INVENTORY_FILE)
        elif choice == "3":
            restock_medicine(medicines_list, INVENTORY_FILE)
        elif choice == "4":
            search_medicine(medicines_list)
        elif choice == "5":
            view_low_stock(medicines_list)
        elif choice == "6":
            add_medicine(medicines_list, INVENTORY_FILE)
        elif choice == "0":
            print("\n[INFO] Exiting MedStore system. Goodbye!\n")
            break
        else:
            print("[ERROR] Invalid choice. Please enter a number between 1 and 6.")
        input("\nPress Enter to continue...")
        
if __name__ == "__main__":
    main()