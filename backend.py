import csv
import csv


# Column names for vendor CSV file
vendor_fields = [
    "vendor_id",
    "vendor_name",
    "phone",
    "email",
    "product_supplied"
]


# Column names for purchase CSV file
purchase_fields = [
    "order_id",
    "vendor_id",
    "vendor_name",
    "product_name",
    "quantity",
    "unit_price",
    "total_amount"
]


# Function to save data in a CSV file
def save_data(filename, data, fieldnames):

    file = None

    try:
        file = open(filename, "w", newline="", encoding="utf-8")

        writer = csv.DictWriter(file, fieldnames=fieldnames)

        writer.writeheader()

        writer.writerows(data)

    except (OSError, csv.Error, UnicodeError) as error:
        raise RuntimeError("Error saving file: " + str(error))

    finally:
        if file is not None:
            file.close()


# Function to load data from a CSV file
def load_data(filename, fieldnames):

    file = None

    try:
        file = open(filename, "r", newline="", encoding="utf-8")

        reader = csv.DictReader(file)

        if reader.fieldnames != fieldnames:
            raise ValueError("CSV column names are incorrect: " + filename)

        data = list(reader)

        return data

    except FileNotFoundError:

        save_data(filename, [], fieldnames)

        return []

    except (OSError, csv.Error, UnicodeError) as error:
        raise RuntimeError("Error reading file: " + str(error))

    finally:
        if file is not None:
            file.close()


# Function to check login details
def check_login(username, password):

    if username == "admin" and password == "230806":
        return True

    return False


# Function to add a new vendor
def add_vendor(vendors, vendor_id, vendor_name, phone, email, product_supplied):

    vendor_id = vendor_id.strip().upper()
    vendor_name = vendor_name.strip()
    phone = phone.strip()
    email = email.strip()
    product_supplied = product_supplied.strip()

    # Check empty fields
    if vendor_id == "" or vendor_name == "" or phone == "" or email == "" or product_supplied == "":
        raise ValueError("Please fill in all the fields.")

    # Check whether vendor ID already exists
    for vendor in vendors:

        if vendor["vendor_id"] == vendor_id:
            raise ValueError("This Vendor ID already exists.")

    # Create a new vendor
    new_vendor = {
        "vendor_id": vendor_id,
        "vendor_name": vendor_name,
        "phone": phone,
        "email": email,
        "product_supplied": product_supplied
    }

    return new_vendor


# Function to search for a vendor
def search_vendors(vendors, search_value):

    search_value = search_value.strip().lower()

    results = []

    for vendor in vendors:

        if search_value in vendor["vendor_id"].lower() or search_value in vendor["vendor_name"].lower():

            results.append(vendor)

    return results


# Function to create a purchase order
def create_purchase_order(vendors, purchases, vendor_id, product_name, quantity, unit_price):

    vendor_id = vendor_id.strip().upper()
    product_name = product_name.strip()

    selected_vendor = None

    # Find the selected vendor
    for vendor in vendors:

        if vendor["vendor_id"] == vendor_id:

            selected_vendor = vendor

            break

    if selected_vendor is None:
        raise ValueError("Vendor not found.")

    if product_name == "":
        raise ValueError("Please enter a product name.")

    # Convert quantity and price into numbers
    try:
        quantity = int(quantity)

        unit_price = float(unit_price)

    except (ValueError, TypeError):
        raise ValueError("Please enter valid quantity and price.")

    if quantity <= 0:
        raise ValueError("Quantity must be greater than zero.")

    if unit_price <= 0:
        raise ValueError("Price must be greater than zero.")

    # Generate a unique purchase order ID
    next_number = 1

    while True:

        order_id = "PO" + str(next_number).zfill(3)

        order_found = False

        for order in purchases:

            if order["order_id"] == order_id:

                order_found = True

                break

        if order_found == False:
            break

        next_number = next_number + 1

    # Calculate total amount
    total_amount = quantity * unit_price

    # Create purchase order
    new_order = {
        "order_id": order_id,
        "vendor_id": selected_vendor["vendor_id"],
        "vendor_name": selected_vendor["vendor_name"],
        "product_name": product_name,
        "quantity": str(quantity),
        "unit_price": str(round(unit_price, 2)),
        "total_amount": str(round(total_amount, 2))
    }

    return new_order


# Function to calculate total spending
def calculate_total_spending(purchases):

    total_spending = 0

    for order in purchases:

        total_spending = total_spending + float(order["total_amount"])

    return total_spending