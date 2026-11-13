import streamlit as st
import pandas as pd

from backend import (
    vendor_fields,
    purchase_fields,
    load_data,
    save_data,
    check_login,
    add_vendor,
    search_vendors,
    create_purchase_order,
    calculate_total_spending
)


# Here we set the Page or we simply Edit our Page layout:
st.set_page_config(
    page_title="Vendor Management Portal",
    page_icon="📦",
    layout="wide"
)


# Here we load our CSV Data:
try:

    vendors = load_data("vendors.csv", vendor_fields)

    purchases = load_data("purchases.csv", purchase_fields)

except (RuntimeError, ValueError) as error:

    st.error(str(error))

    st.stop()


# Here we create our Login Session:
if "logged_in" not in st.session_state:

    st.session_state.logged_in = False


# LOGIN PAGE
if not st.session_state.logged_in:

    st.title("Vendor Management Portal")

    st.subheader("Login to Your Account")

    with st.form("login_form"):

        username = st.text_input("Username")

        password = st.text_input("Password", type="password")

        login_button = st.form_submit_button("Login")

        if login_button:

            if check_login(username, password):

                st.session_state.logged_in = True

                st.rerun()

            else:

                st.error("Incorrect username or password.")

    st.info("Demo Login: admin / 230806")

    st.stop()


# SIDEBAR NAVIGATION
st.sidebar.title("Vendor Portal")

st.sidebar.write("Management System")

page = st.sidebar.radio(
    "Select a Page",
    [
        "Dashboard",
        "Add Vendor",
        "View Vendors",
        "Search Vendor",
        "Create Purchase Order",
        "Purchase Orders",
        "Reports"
    ]
)


# LOGOUT BUTTON
if st.sidebar.button("Log Out"):

    st.session_state.logged_in = False

    st.rerun()


# PAGE 1: DASHBOARD
if page == "Dashboard":

    st.title("Dashboard")

    st.write("Welcome to our Vendor Management Portal.")

    total_vendors = len(vendors)

    total_orders = len(purchases)

    total_spending = calculate_total_spending(purchases)

    col1, col2, col3 = st.columns(3)

    col1.metric("Total Vendors", total_vendors)

    col2.metric("Total Purchase Orders", total_orders)

    col3.metric("Total Spending", f"Rs. {total_spending:,.2f}")

    st.divider()

    st.subheader("Recent Purchase Orders")

    if purchases:

        recent_orders = purchases[-5:][::-1]

        st.dataframe(
            recent_orders,
            hide_index=True,
            use_container_width=True
        )

    else:

        st.info("No purchase orders available.")


# PAGE 2: ADD VENDOR
elif page == "Add Vendor":

    st.title("Add New Vendor")

    st.write("Enter the details of the new vendor.")

    with st.form("vendor_form", clear_on_submit=True):

        col1, col2 = st.columns(2)

        vendor_id = col1.text_input("Vendor ID")

        vendor_name = col2.text_input("Vendor Name")

        phone = col1.text_input("Phone Number")

        email = col2.text_input("Email Address")

        product = st.text_input("Product Supplied")

        submit = st.form_submit_button("Add Vendor")

    if submit:

        try:

            new_vendor = add_vendor(
                vendors,
                vendor_id,
                vendor_name,
                phone,
                email,
                product
            )

            vendors.append(new_vendor)

            save_data("vendors.csv", vendors, vendor_fields)

            st.success("Vendor added successfully!")

        except (ValueError, RuntimeError) as error:

            st.error(str(error))


# PAGE 3: VIEW VENDORS
elif page == "View Vendors":

    st.title("Registered Vendors")

    if vendors:

        st.dataframe(
            vendors,
            hide_index=True,
            use_container_width=True
        )

    else:

        st.info("No vendors registered yet.")


# PAGE 4: SEARCH VENDOR
elif page == "Search Vendor":

    st.title("Search Vendor")

    search_value = st.text_input("Enter Vendor ID or Vendor Name")

    if search_value.strip() != "":

        results = search_vendors(vendors, search_value)

        if results:

            st.success(str(len(results)) + " matching vendor(s) found.")

            st.dataframe(
                results,
                hide_index=True,
                use_container_width=True
            )

        else:

            st.warning("No matching vendor found.")


# PAGE 5: CREATE PURCHASE ORDER
elif page == "Create Purchase Order":

    st.title("Create Purchase Order")

    if not vendors:
        st.warning("Please register a vendor first.")

    else:
        vendor_options = {}

        for vendor in vendors:
            label = str(vendor["vendor_id"]) + " - " + str(vendor["vendor_name"])
            vendor_options[label] = vendor["vendor_id"]

        # Select Vendor
        selected_vendor = st.selectbox(
            "Select Vendor",
            list(vendor_options.keys())
        )

        selected_vendor_id = vendor_options[selected_vendor]

        # Get Selected Vendor Details
        selected_vendor_data = next(
            (
                v for v in vendors
                if str(v["vendor_id"]) == str(selected_vendor_id)
            ),
            None
        )

        # Get Vendor Products
        vendor_products = []

        if selected_vendor_data:
            raw_products = selected_vendor_data.get("product_supplied", "")

            if isinstance(raw_products, list):
                vendor_products = raw_products
            else:
                vendor_products = [
                    p.strip()
                    for p in str(raw_products).replace(";", ",").split(",")
                    if p.strip()
                ]

        # Purchase Order Form
        with st.form("purchase_form", clear_on_submit=True):

            if vendor_products:
                selected_product = st.selectbox(
                    "Select Product",
                    vendor_products
                )

                custom_product = st.text_input(
                    "Or Enter Another Product (Optional)"
                )

                product_name = (
                    custom_product.strip()
                    if custom_product.strip()
                    else selected_product
                )

            else:
                product_name = st.text_input("Product Name")

            quantity = st.number_input(
                "Quantity",
                min_value=1,
                value=1,
                step=1
            )

            unit_price = st.number_input(
                "Price Per Unit (Rs.)",
                min_value=0.01,
                value=100.0,
                step=100.0
            )

            submit = st.form_submit_button(
                "Create Purchase Order"
            )

        if submit:
            try:
                new_order = create_purchase_order(
                    vendors,
                    purchases,
                    selected_vendor_id,
                    product_name,
                    quantity,
                    unit_price
                )

                purchases.append(new_order)

                save_data(
                    "purchases.csv",
                    purchases,
                    purchase_fields
                )

                st.success("Purchase Order Created Successfully!")

                st.write("Order ID:", new_order["order_id"])
                st.write("Total Amount: Rs.", new_order["total_amount"])

            except (ValueError, RuntimeError) as error:
                st.error(str(error))
# PAGE 6: PURCHASE ORDERS
elif page == "Purchase Orders":

    st.title("All Purchase Orders")

    if purchases:

        st.dataframe(
            purchases,
            hide_index=True,
            use_container_width=True
        )

    else:

        st.info("No purchase orders available.")


# PAGE 7: REPORTS
elif page == "Reports":

    st.title("Procurement Reports")

    total_vendors = len(vendors)

    total_orders = len(purchases)

    total_spending = calculate_total_spending(purchases)

    col1, col2, col3 = st.columns(3)

    col1.metric("Total Vendors", total_vendors)

    col2.metric("Total Orders", total_orders)

    col3.metric("Total Spending", f"Rs. {total_spending:,.2f}")

    st.divider()

    st.subheader("Spending by Vendor")

    spending_by_vendor = {}

    for order in purchases:

        vendor_name = order["vendor_name"]

        amount = float(order["total_amount"])

        if vendor_name in spending_by_vendor:

            spending_by_vendor[vendor_name] += amount

        else:

            spending_by_vendor[vendor_name] = amount

    if spending_by_vendor:

        chart_data = pd.DataFrame.from_dict(
            spending_by_vendor,
            orient="index",
            columns=["Total Spending (Rs.)"]
        )

        st.bar_chart(chart_data)

    else:

        st.info("No purchase data available for reporting.")

