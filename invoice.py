import datetime

def generate_timestamp():
    """Return current date and time as formatted string."""
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def generate_sale_invoice(customer_name, cart, grand_total, vat, total_with_vat):
    """Create and save a sale invoice for the customer."""
    timestamp = generate_timestamp()
    safe_timestamp = timestamp.replace(" ", "_").replace(":", "-")
    safe_customer = customer_name.replace(" ", "_")
    invoice_filename = f"invoice_sale_{safe_customer}_{safe_timestamp}.txt"

    lines = []
    lines.append("=" * 65)
    lines.append("          MEDSTORE PVT. LTD.")
    lines.append("        Sales Invoice / VAT Bill")
    lines.append("=" * 65)
    lines.append(f"  Customer  : {customer_name}")
    lines.append(f"  Date/Time : {timestamp}")
    lines.append("-" * 65)
    lines.append(f"  {'Medicine':<22} {'Qty':<6} {'Unit':<10} {'T/S':>5} {'Disc':>9} {'Amount':>11}")
    lines.append("-" * 65)
    
    # Add each item to invoice
    for item in cart:
        unit_label = "strip(s)" if item["unit_type"] == "2" else "tablet(s)"
        disc_str = f"Rs.{item['discount_amount']:.2f}" if item["discount_amount"] > 0 else "-"
        lines.append(
            f"  {item['medicine_name']:<22} {item['quantity']:<6} {unit_label:<10} {item['tablets_per_strip']:>5} {disc_str:>9} Rs.{item['subtotal']:>8.2f}"
        )
        
    lines.append("-" * 65)
    lines.append(f"  {'Subtotal':<54} Rs.{grand_total:.2f}")
    lines.append(f"  {'VAT (13%)':<54} Rs.{vat:.2f}")
    lines.append("-" * 65)
    lines.append(f"  {'GRAND TOTAL':<54} Rs.{total_with_vat:.2f}")
    lines.append("=" * 65)
    lines.append("       Thank you for your purchase!")
    lines.append("=" * 65)

    # Print and save invoice
    print("\n")
    for line in lines:
        print(line)

    # Save to file
    with open(invoice_filename, "w") as f:
        for line in lines:
            f.write(line + "\n")

    print(f"\n[INFO] Invoice saved: {invoice_filename}")


def generate_restock_invoice(supplier_name, restock_items):
    """Create and save a restock invoice for supplier."""
    timestamp = generate_timestamp()
    safe_timestamp = timestamp.replace(" ", "_").replace(":", "-")
    safe_supplier = supplier_name.replace(" ", "_")
    invoice_filename = f"invoice_restock_{safe_supplier}_{safe_timestamp}.txt"

    with open(invoice_filename, "w") as f:
        f.write("=" * 55 + "\n")
        f.write("          MEDSTORE PVT. LTD.\n")
        f.write("        Restock Note / Purchase Bill\n")
        f.write("=" * 55 + "\n")
        f.write(f"Supplier Name : {supplier_name}\n")
        f.write(f"Date & Time   : {timestamp}\n")
        f.write("-" * 55 + "\n")
        f.write(f"{'Medicine':<22} {'Brand':<18} {'Qty (tabs)':>12}\n")
        f.write("-" * 55 + "\n")
        total_tablets = 0
        for item in restock_items:
            f.write(f"{item['name']:<22} {item['brand']:<18} {item['quantity']:>12}\n")
            total_tablets += item["quantity"]
        f.write("-" * 55 + "\n")
        f.write(f"{'Total Tablets Restocked':>36} {total_tablets:>12}\n")
        f.write("=" * 55 + "\n")
        f.write("     Stock updated in inventory file.\n")
        f.write("=" * 55 + "\n")

    print(f"\n[INFO] Restock note saved: {invoice_filename}")