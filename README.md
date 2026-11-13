# Vendor_Management_Procurement_Portal
A modular Python and Streamlit web portal for vendor and procurement management. It uses persistent CSV storage to register and search suppliers, generate sequential purchase orders with automated cost calculations, enforce input validation, and visualize vendor-wise spending through interactive dashboard metrics and bar charts.
# Vendor Management & Procurement Portal

A modular Python and Streamlit application developed for **Programming for Business Lab (Assignment 3)** to manage supplier directories, automate purchase order (PO) creation, and visualize procurement spending.

## Team Members
* **[Your Name]** (`[Roll Number]`) — Backend Logic, CSV Persistence & Technical Report
* **[Partner's Name]** (`[Roll Number]`) — Streamlit UI Design, Frontend-Backend Integration & Notebook Testing

## Project Structure
* `backend.py` — Core functions for CSV I/O (`load_data`, `save_data`), authentication (`check_login`), vendor management (`add_vendor`, `search_vendors`), sequential PO creation (`create_purchase_order`), and spend calculation (`calculate_total_spending`).
* `front.py` — Interactive 7-page Streamlit dashboard (`Dashboard`, `Add Vendor`, `View Vendors`, `Search Vendor`, `Create Purchase Order`, `Purchase Orders`, `Reports`).
* `Vendor Management and Procurement Portal.ipynb` — Jupyter Notebook with modular code cells, CSV header normalization, and execution outputs.
* `vendors.csv` & `purchases.csv` — Persistent CSV data files.

## How to Run Locally
1. Clone or download this repository.
2. Open **Anaconda Prompt** (or terminal) inside the project folder.
3. Install dependencies:
   ```bash
   pip install streamlit pandas
