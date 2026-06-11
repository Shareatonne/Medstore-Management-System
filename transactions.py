# from inventory import save_inventory, display_inventory
# from invoice import generate_sale_invoice, generate_restock_invoice

# STRIP_DISCOUNT_THRESHOLD = 2  # Min strips for discount
# STRIP_DISCOUNT_RATE = 0.05    # 5% discount rate


# def get_integer_input(prompt):
#     """Get validated positive integer input from user."""
#     while True:
#         value = input(prompt).strip()
#         # Validate positive integer
#         if value.isdigit() and int(value) > 0:
#             return int(value)
#         print("[ERROR] Please enter a valid positive integer.")


# def get_nonempty_input(prompt):
#     """Get non-empty text input from user."""
#     while True:
#         value = input(prompt).strip()
#         if value:
#             return value
#         print("[ERROR] This field cannot be empty.")


# def find_medicine(medicines, name, brand):
#     """Search for medicine by name and brand (case-insensitive)."""
#     for medicine in medicines:
#         if medicine["name"].lower() == name.lower() and medicine["brand"].lower() == brand.lower():
#             return medicine
#     return None


# def sell_medicine(medicines, filename):
#     """Process medicine sales, update inventory, and generate invoice."""
#     print("\n" + "=" * 55)
#     print("               SELL MEDICINE")
#     print("=" * 55)

#     customer_name = get_nonempty_input("Enter customer name: ")
#     cart = []  # Items in current sale
#     grand_total = 0.0

#     # Keep adding items until user finishes
#     while True:
#         print("\n-- Add item to cart --")
#         choice = get_integer_input("Enter medicine number: ")

#         # Validate medicine number
#         if choice < 1 or choice > len(medicines):
#             print("[ERROR] Invalid medicine number. Please try again.")
#             continue
    
#         medicine = medicines[choice - 1]
        
#         # Check stock availability
#         if medicine["stock"] == 0:
#             print(f"[ERROR] '{medicine['name']}' ({medicine['brand']}) is out of stock.")
#             continue

#         print(f"  Available stock : {medicine['stock']} tablets")
#         print(f"  Price per tablet: Rs. {medicine['price_per_tablet']:.2f}")
#         print(f"  Price per strip : Rs. {medicine['price_per_strip']:.2f} ({medicine['tablets_per_strip']} tabs/strip)")
#         print("  Unit type: 1 = Tablets  |  2 = Strips")

#         while True:
#             unit_type = input("Enter unit type (1 or 2): ").strip()
#             if unit_type in ("1", "2"):
#                 break
#             print("[ERROR] Enter 1 for tablets or 2 for strips.")

#         quantity = get_integer_input("Enter quantity: ")
#         discount_amount = 0.0

#         # Calculate price by unit type
#         if unit_type == "1":  # Tablets
#             if medicine["stock"] < quantity:
#                 print(f"[ERROR] Insufficient stock. Only {medicine['stock']} tablet(s) available.")
#                 continue
#             medicine["stock"] -= quantity
#             subtotal = quantity * medicine["price_per_tablet"]
            
#             # Apply bulk discount if tablet quantity equals or exceeds the strip threshold
#             if quantity >= (STRIP_DISCOUNT_THRESHOLD * medicine["tablets_per_strip"]):
#                 discount_amount = subtotal * STRIP_DISCOUNT_RATE
#                 subtotal -= discount_amount
#                 print(f"  [DISCOUNT] 5% bulk tablet discount applied: -Rs. {discount_amount:.2f}")

#         else:  # Strips
#             strips_requested = quantity
#             tablets_needed = strips_requested * medicine["tablets_per_strip"]
#             if medicine["stock"] < tablets_needed:
#                 available_strips = medicine["stock"] // medicine["tablets_per_strip"]
#                 print(f"[ERROR] Insufficient stock. Only {available_strips} strip(s) available.")
#                 continue
#             medicine["stock"] -= tablets_needed
#             subtotal = strips_requested * medicine["price_per_strip"]
#             # Apply bulk discount for strips
#             if strips_requested >= STRIP_DISCOUNT_THRESHOLD:
#                 discount_amount = subtotal * STRIP_DISCOUNT_RATE
#                 subtotal -= discount_amount
#                 print(f"  [DISCOUNT] 5% strip discount applied: -Rs. {discount_amount:.2f}")

#         grand_total += subtotal
#         cart.append({
#             "medicine_name": medicine["name"],
#             "brand": medicine["brand"],
#             "quantity": quantity,
#             "unit_type": unit_type,
#             "discount_amount": discount_amount,
#             "subtotal": subtotal,
#             "tablets_per_strip": medicine["tablets_per_strip"],
#         })

#         print(f"  Subtotal: Rs. {subtotal:.2f}")
#         print(f"  Running total: Rs. {grand_total:.2f}")

#         another = input("\nAdd another medicine? (yes/no): ").strip().lower()
#         if another != "yes":
#             break

#     # Finalize sale if items were added
#     if cart:
#         vat = grand_total * 0.13
#         total_with_vat = grand_total + vat
        
#         print("\n" + "=" * 55)
#         print(f"  Subtotal         : Rs. {grand_total:.2f}")
#         print(f"  VAT (13%)        : Rs. {vat:.2f}")
#         print("-" * 55)
#         print(f"  GRAND TOTAL      : Rs. {total_with_vat:.2f}")
#         print("=" * 55)
        
#         save_inventory(filename, medicines)
#         generate_sale_invoice(customer_name, cart, grand_total, vat, total_with_vat)
#         print("[SUCCESS] Sale completed and inventory updated.")


# def restock_medicine(medicines, filename):
#     """Handle restocking of medicines and addition of new medicines."""
#     print("\n" + "=" * 55)
#     print("              RESTOCK MEDICINE")
#     print("=" * 55)

#     supplier_name = get_nonempty_input("Enter supplier / vendor name: ")
#     restock_items = []  # Items being restocked

#     # Keep adding restock items
#     while True:
#         print("\n-- Add restock item --")
#         name = get_nonempty_input("Medicine name (or 'done' to finish): ")
#         if name.lower() == "done":
#             if not restock_items:
#                 print("[INFO] No items added. Restock cancelled.")
#             break

#         brand = get_nonempty_input("Brand name: ")
#         medicine = find_medicine(medicines, name, brand)

#         if medicine is None:
#             print(f"[ERROR] Medicine '{name}' by '{brand}' not found in inventory.")
#             add_new = input("Add as a new medicine? (yes/no): ").strip().lower()
#             if add_new == "yes":
#                 try:
#                     price_per_tablet = float(get_nonempty_input("Price per tablet (Rs.): "))
#                     price_per_strip = float(get_nonempty_input("Price per strip (Rs.): "))
#                     tablets_per_strip = get_integer_input("Tablets per strip: ")
#                     quantity = get_integer_input("Quantity to add (in tablets): ")
#                     new_medicine = {
#                         "name": name,
#                         "brand": brand,
#                         "stock": quantity,
#                         "price_per_tablet": price_per_tablet,
#                         "price_per_strip": price_per_strip,
#                         "tablets_per_strip": tablets_per_strip,
#                     }
#                     medicines.append(new_medicine)
#                     restock_items.append({"name": name, "brand": brand, "quantity": quantity})
#                     print(f"[INFO] New medicine '{name}' ({brand}) added with {quantity} tablets.")
#                 except ValueError:
#                     print("[ERROR] Invalid input. Medicine not added.")
#             continue

#         quantity = get_integer_input("Enter quantity to restock (in tablets): ")
#         medicine["stock"] += quantity
#         restock_items.append({"name": medicine["name"], "brand": medicine["brand"], "quantity": quantity})
#         print(f"[INFO] Restocked {quantity} tablet(s) of '{medicine['name']}' ({medicine['brand']}). New stock: {medicine['stock']}")

#         another = input("\nRestock another medicine? (yes/no): ").strip().lower()
#         if another != "yes":
#             break

#     if restock_items:
#         save_inventory(filename, medicines)
#         generate_restock_invoice(supplier_name, restock_items)
#         print("[SUCCESS] Restock completed and inventory updated.")


# def search_medicine(medicines):
#     """Search for medicines by name or brand."""
#     print("\n" + "=" * 55)
#     print("              SEARCH MEDICINE")
#     print("=" * 55)
#     keyword = get_nonempty_input("Enter medicine name or brand to search: ").lower()
#     # Filter medicines by keyword
#     results = [
#         m for m in medicines
#         if keyword in m["name"].lower() or keyword in m["brand"].lower()
#     ]
#     # Display results or info message
#     if results:
#         display_inventory(results)
#     else:
#         print(f"[INFO] No medicines found matching '{keyword}'.")


# def view_low_stock(medicines):
#     """Displays all medicines that have less than 50 tablets remaining in stock."""
    
#     # Filter medicines with stock below 50
#     low = [m for m in medicines if m["stock"] < 50]
    
#     if low:
#         print("\n[INFO] The following medicines are running low:")
#         display_inventory(low)
#     else:
#         print("\n[INFO] All medicines have sufficient stock.")


# def add_medicine(medicines, filename):
#     """Adds a new medicine to the inventory after taking input from the user."""
    
#     print("\n" + "=" * 55)
#     print("             ADD NEW MEDICINE")
#     print("=" * 55)
    
#     # Get medicine details from user
#     name = get_nonempty_input("Enter medicine name: ")
#     brand = get_nonempty_input("Enter brand name: ")
    
#     # Check if medicine already exists
#     if find_medicine(medicines, name, brand):
#         print(f"[ERROR] '{name}' by '{brand}' already exists in inventory.")
#         return
    
#     stock = get_integer_input("Enter opening stock (in tablets): ")
#     price_per_tablet = float(get_nonempty_input("Enter price per tablet (Rs.): "))
#     price_per_strip = float(get_nonempty_input("Enter price per strip (Rs.): "))
#     tablets_per_strip = get_integer_input("Enter tablets per strip: ")
    
#     # Build the new medicine dictionary
#     new_medicine = {
#         "name": name,
#         "brand": brand,
#         "stock": stock,
#         "price_per_tablet": price_per_tablet,
#         "price_per_strip": price_per_strip,
#         "tablets_per_strip": tablets_per_strip,
#     }
    
#     # Add to list and save
#     medicines.append(new_medicine)
#     save_inventory(filename, medicines)
#     print(f"\n[SUCCESS] '{name}' ({brand}) added to inventory successfully.")


from inventory import save_inventory, display_inventory
from invoice import generate_sale_invoice, generate_restock_invoice

STRIP_DISCOUNT_THRESHOLD = 2  # Min strips for discount
STRIP_DISCOUNT_RATE = 0.05    # 5% discount rate


def get_integer_input(prompt):
    """Get validated positive integer input from user."""
    while True:
        value = input(prompt).strip()
        # Validate positive integer
        if value.isdigit() and int(value) > 0:
            return int(value)
        print("[ERROR] Please enter a valid positive integer.")


def get_nonempty_input(prompt):
    """Get non-empty text input from user."""
    while True:
        value = input(prompt).strip()
        if value:
            return value
        print("[ERROR] This field cannot be empty.")


def find_medicine(medicines, name, brand):
    """Search for medicine by name and brand (case-insensitive)."""
    for medicine in medicines:
        if medicine["name"].lower() == name.lower() and medicine["brand"].lower() == brand.lower():
            return medicine
    return None


def sell_medicine(medicines, filename):
    """Process medicine sales, update inventory, and generate invoice."""
    print("\n" + "=" * 55)
    print("               SELL MEDICINE")
    print("=" * 55)

    customer_name = get_nonempty_input("Enter customer name: ")
    cart = []  # Items in current sale
    grand_total = 0.0

    # Keep adding items until user finishes
    while True:
        print("\n-- Add item to cart --")
        choice = get_integer_input("Enter medicine number: ")

        # Validate medicine number
        if choice < 1 or choice > len(medicines):
            print("[ERROR] Invalid medicine number. Please try again.")
            continue
    
        medicine = medicines[choice - 1]
        
        # Check stock availability
        if medicine["stock"] == 0:
            print(f"[ERROR] '{medicine['name']}' ({medicine['brand']}) is out of stock.")
            continue

        print(f"  Available stock : {medicine['stock']} tablets")
        print(f"  Price per tablet: Rs. {medicine['price_per_tablet']:.2f}")
        print(f"  Price per strip : Rs. {medicine['price_per_strip']:.2f} ({medicine['tablets_per_strip']} tabs/strip)")
        print("  Unit type: 1 = Tablets  |  2 = Strips")

        while True:
            unit_type = input("Enter unit type (1 or 2): ").strip()
            if unit_type in ("1", "2"):
                break
            print("[ERROR] Enter 1 for tablets or 2 for strips.")

        quantity = get_integer_input("Enter quantity: ")
        discount_amount = 0.0

        # Calculate price by unit type
        if unit_type == "1":  # Tablets
            if medicine["stock"] < quantity:
                print(f"[ERROR] Insufficient stock. Only {medicine['stock']} tablet(s) available.")
                continue
            medicine["stock"] -= quantity
            subtotal = quantity * medicine["price_per_tablet"]
            # Apply bulk discount when quantity meets or exceeds 2 full strips' worth of tablets
            tablet_discount_threshold = medicine["tablets_per_strip"] * STRIP_DISCOUNT_THRESHOLD
            if quantity >= tablet_discount_threshold:
                discount_amount = subtotal * STRIP_DISCOUNT_RATE
                subtotal -= discount_amount
                print(f"  [DISCOUNT] 5% tablet discount applied: -Rs. {discount_amount:.2f}")

        else:  # Strips
            strips_requested = quantity
            tablets_needed = strips_requested * medicine["tablets_per_strip"]
            if medicine["stock"] < tablets_needed:
                available_strips = medicine["stock"] // medicine["tablets_per_strip"]
                print(f"[ERROR] Insufficient stock. Only {available_strips} strip(s) available.")
                continue
            medicine["stock"] -= tablets_needed
            subtotal = strips_requested * medicine["price_per_strip"]
            # Apply bulk discount for strips
            if strips_requested >= STRIP_DISCOUNT_THRESHOLD:
                discount_amount = subtotal * STRIP_DISCOUNT_RATE
                subtotal -= discount_amount
                print(f"  [DISCOUNT] 5% strip discount applied: -Rs. {discount_amount:.2f}")

        grand_total += subtotal
        cart.append({
            "medicine_name": medicine["name"],
            "brand": medicine["brand"],
            "quantity": quantity,
            "unit_type": unit_type,
            "tablets_per_strip": medicine["tablets_per_strip"],
            "discount_amount": discount_amount,
            "subtotal": subtotal,
        })

        print(f"  Subtotal: Rs. {subtotal:.2f}")
        print(f"  Running total: Rs. {grand_total:.2f}")

        another = input("\nAdd another medicine? (yes/no): ").strip().lower()
        if another != "yes":
            break

    # Finalize sale if items were added
    if cart:
        vat = grand_total * 0.13
        total_with_vat = grand_total + vat
        
        print("\n" + "=" * 55)
        print(f"  Subtotal         : Rs. {grand_total:.2f}")
        print(f"  VAT (13%)        : Rs. {vat:.2f}")
        print("-" * 55)
        print(f"  GRAND TOTAL      : Rs. {total_with_vat:.2f}")
        print("=" * 55)
        
        save_inventory(filename, medicines)
        generate_sale_invoice(customer_name, cart, grand_total, vat, total_with_vat)
        print("[SUCCESS] Sale completed and inventory updated.")


def restock_medicine(medicines, filename):
    """Handle restocking of medicines and addition of new medicines."""
    print("\n" + "=" * 55)
    print("              RESTOCK MEDICINE")
    print("=" * 55)

    supplier_name = get_nonempty_input("Enter supplier / vendor name: ")
    restock_items = []  # Items being restocked

    # Keep adding restock items
    while True:
        print("\n-- Add restock item --")
        name = get_nonempty_input("Medicine name (or 'done' to finish): ")
        if name.lower() == "done":
            if not restock_items:
                print("[INFO] No items added. Restock cancelled.")
            break

        brand = get_nonempty_input("Brand name: ")
        medicine = find_medicine(medicines, name, brand)

        if medicine is None:
            print(f"[ERROR] Medicine '{name}' by '{brand}' not found in inventory.")
            add_new = input("Add as a new medicine? (yes/no): ").strip().lower()
            if add_new == "yes":
                try:
                    price_per_tablet = float(get_nonempty_input("Price per tablet (Rs.): "))
                    price_per_strip = float(get_nonempty_input("Price per strip (Rs.): "))
                    tablets_per_strip = get_integer_input("Tablets per strip: ")
                    quantity = get_integer_input("Quantity to add (in tablets): ")
                    new_medicine = {
                        "name": name,
                        "brand": brand,
                        "stock": quantity,
                        "price_per_tablet": price_per_tablet,
                        "price_per_strip": price_per_strip,
                        "tablets_per_strip": tablets_per_strip,
                    }
                    medicines.append(new_medicine)
                    restock_items.append({"name": name, "brand": brand, "quantity": quantity})
                    print(f"[INFO] New medicine '{name}' ({brand}) added with {quantity} tablets.")
                except ValueError:
                    print("[ERROR] Invalid input. Medicine not added.")
            continue

        quantity = get_integer_input("Enter quantity to restock (in tablets): ")
        medicine["stock"] += quantity
        restock_items.append({"name": medicine["name"], "brand": medicine["brand"], "quantity": quantity})
        print(f"[INFO] Restocked {quantity} tablet(s) of '{medicine['name']}' ({medicine['brand']}). New stock: {medicine['stock']}")

        another = input("\nRestock another medicine? (yes/no): ").strip().lower()
        if another != "yes":
            break

    if restock_items:
        save_inventory(filename, medicines)
        generate_restock_invoice(supplier_name, restock_items)
        print("[SUCCESS] Restock completed and inventory updated.")


def search_medicine(medicines):
    """Search for medicines by name or brand."""
    print("\n" + "=" * 55)
    print("              SEARCH MEDICINE")
    print("=" * 55)
    keyword = get_nonempty_input("Enter medicine name or brand to search: ").lower()
    # Filter medicines by keyword
    results = [
        m for m in medicines
        if keyword in m["name"].lower() or keyword in m["brand"].lower()
    ]
    # Display results or info message
    if results:
        display_inventory(results)
    else:
        print(f"[INFO] No medicines found matching '{keyword}'.")

def view_low_stock(medicines):
    """Displays all medicines that have less than 50 tablets remaining in stock."""
    
    # Filter medicines with stock below 50
    low = [m for m in medicines if m["stock"] < 50]
    
    if low:
        print("\n[INFO] The following medicines are running low:")
        display_inventory(low)
    else:
        print("\n[INFO] All medicines have sufficient stock.")

def add_medicine(medicines, filename):
    """Adds a new medicine to the inventory after taking input from the user."""
    
    print("\n" + "=" * 55)
    print("             ADD NEW MEDICINE")
    print("=" * 55)
    
    # Get medicine details from user
    name = get_nonempty_input("Enter medicine name: ")
    brand = get_nonempty_input("Enter brand name: ")
    
    # Check if medicine already exists
    if find_medicine(medicines, name, brand):
        print(f"[ERROR] '{name}' by '{brand}' already exists in inventory.")
        return
    
    stock = get_integer_input("Enter opening stock (in tablets): ")
    price_per_tablet = float(get_nonempty_input("Enter price per tablet (Rs.): "))
    price_per_strip = float(get_nonempty_input("Enter price per strip (Rs.): "))
    tablets_per_strip = get_integer_input("Enter tablets per strip: ")
    
    # Build the new medicine dictionary
    new_medicine = {
        "name": name,
        "brand": brand,
        "stock": stock,
        "price_per_tablet": price_per_tablet,
        "price_per_strip": price_per_strip,
        "tablets_per_strip": tablets_per_strip,
    }
    
    # Add to list and save
    medicines.append(new_medicine)
    save_inventory(filename, medicines)
    print(f"\n[SUCCESS] '{name}' ({brand}) added to inventory successfully.")