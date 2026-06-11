import os

def load_inventory(filename):
    """Load medicine data from inventory file and return as list of dictionaries."""
    medicines = []
    # Check if file exists
    if not os.path.exists(filename):
        print(f"[ERROR] Inventory file '{filename}' not found.")
        return medicines
    with open(filename, "r") as f:
        for line_number, line in enumerate(f, start=1):
            line = line.strip()
            # Skip empty lines
            if not line:
                continue
            parts = [p.strip() for p in line.split(",")]
            # Validate that line has 6 fields
            if len(parts) != 6:
                print(f"[WARNING] Skipping malformed line {line_number}: {line}")
                continue
            try:
                # Parse and convert fields to appropriate data types
                medicine = {
                    "name": parts[0],
                    "brand": parts[1],
                    "stock": int(parts[2]),
                    "price_per_tablet": float(parts[3]),
                    "price_per_strip": float(parts[4]),
                    "tablets_per_strip": int(parts[5]),
                }
                medicines.append(medicine)
            except ValueError:
                # Handle invalid numeric conversions
                print(f"[WARNING] Skipping line {line_number} with invalid numeric data.")
    return medicines

def save_inventory(filename, medicines):
    """Write medicines to file in CSV format."""
    with open(filename, "w") as f:
        for medicine in medicines:
            line = (
                f"{medicine['name']},"
                f"{medicine['brand']},"
                f"{medicine['stock']},"
                f"{medicine['price_per_tablet']},"
                f"{medicine['price_per_strip']},"
                f"{medicine['tablets_per_strip']}\n"
            )
            f.write(line)


def display_inventory(medicines):
    """Display all medicines in a formatted table."""
    # Print table header
    print("\n" + "=" * 110)
    print(" " * 35 + "MEDSTORE PVT. LTD. — INVENTORY")
    print("=" * 110)
    print(
        f"{'No.':<5} {'Medicine':<25} {'Brand':<22} {'Stock (tabs)':<14} "
        f"{'Price/Tab (Rs.)':<17} {'Price/Strip (Rs.)':<19} {'Tabs/Strip':<12}"
    )
    print("-" * 110)
    if not medicines:
        print(" " * 40 + "No medicines found in inventory.")
    # Display each medicine row
    for index, medicine in enumerate(medicines, start=1):
        # Show "OUT OF STOCK" if stock is zero or negative
        stock_display = f"{medicine['stock']}" if medicine['stock'] > 0 else "OUT OF STOCK"
        print(
            f"{index:<5} {medicine['name']:<25} {medicine['brand']:<22} {stock_display:<14} "
            f"{medicine['price_per_tablet']:<17.2f} {medicine['price_per_strip']:<19.2f} "
            f"{medicine['tablets_per_strip']:<12}"
        )
    print("=" * 110 + "\n")
