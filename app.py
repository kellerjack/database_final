import sqlite3
from datetime import datetime

DB_FILE = 'ecommerce.db'

def connect_db():
    return sqlite3.connect(DB_FILE)

def view_products():
    with connect_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT product_id, name, price, stock FROM Product")
        products = cursor.fetchall()
        print("\n--- Available Products ---")
        for pid, name, price, stock in products:
            print(f"ID: {pid} | {name} | ${price:.2f} | Stock: {stock}")

def add_product():
    name = input("Product name: ")
    price = float(input("Price: "))
    quantity = int(input("Stock quantity: "))
    with connect_db() as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO Product (name, price, stock) VALUES (?, ?, ?)", 
                       (name, price, quantity))
        conn.commit()
        print("Product added!")

def make_purchase():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    try:
        customer_id = int(input("Enter customer ID: "))
        card_id_input = input("Enter card ID (leave blank if not using one): ")
        card_id = int(card_id_input) if card_id_input else None

        cursor.execute("""
            INSERT INTO Purchase (Customer_ID, Card_ID)
            VALUES (?, ?)
        """, (customer_id, card_id))
        purchase_id = cursor.lastrowid

        while True:
            product_id = int(input("Enter product ID to purchase (or 0 to finish): "))
            if product_id == 0:
                break
            quantity = int(input("Enter quantity: "))

            cursor.execute("SELECT price, stock FROM Product WHERE product_id = ?", (product_id,))
            result = cursor.fetchone()
            if not result:
                print("Product not found.")
                continue
            price, stock = result
            if quantity > stock:
                print(f"Not enough stock. Available: {stock}")
                continue

            cursor.execute("""
                INSERT INTO PurchaseItem (Purchase_ID, product_id, Quantity, Price)
                VALUES (?, ?, ?, ?)
            """, (purchase_id, product_id, quantity, price))

            cursor.execute(
                "UPDATE Product SET stock = stock - ? WHERE product_id = ?",
                (quantity, product_id)
            )

        conn.commit()
        print("Purchase completed.")
    except Exception as e:
        conn.rollback()
        print("Error during purchase:", e)
    finally:
        conn.close()


def view_purchases():
    with connect_db() as conn:
        cursor = conn.cursor()
        cursor.execute("""
        SELECT
            Customer.Customer_ID,
            Customer.Name AS CustomerName,
            Product.Product_ID,
            Product.Name AS ProductName,
            PurchaseItem.Quantity,
            Product.Price,
            (PurchaseItem.Quantity * Product.Price) AS TotalCost
        FROM
            Customer
        JOIN Purchase ON Customer.Customer_ID = Purchase.Customer_ID
        JOIN PurchaseItem ON Purchase.Purchase_ID = PurchaseItem.Purchase_ID
        JOIN Product ON PurchaseItem.Product_ID = Product.Product_ID
        ORDER BY
            Customer.Customer_ID, Purchase.Purchase_ID;
        """)

        rows = cursor.fetchall()
        for row in rows:
            customer_id, customer_name, product_id, product_name, quantity, price, total = row
            print(f"Customer {customer_id} ({customer_name}) bought {quantity} x {product_name} (Product ID: {product_id}) at ${price:.2f} each. Total: ${total:.2f}")

import sqlite3

import sqlite3

def edit_product():
    print("\n=== Edit Product ===")
    try:
        conn = sqlite3.connect("ecommerce.db")
        cursor = conn.cursor()

        product_id = int(input("Enter the ID of the product to edit: "))
        cursor.execute("SELECT * FROM Product WHERE product_id = ?", (product_id,))
        product = cursor.fetchone()

        if product is None:
            print("No product found with that ID.")
            return

        print(f"Current Name: {product[1]}")
        print(f"Current Price: {product[2]}")
        print(f"Current Stock: {product[3]}")

        new_name = input("Enter new name (or press Enter to keep current): ")
        new_price_input = input("Enter new price (or press Enter to keep current): ")
        new_stock_input = input("Enter new stock (or press Enter to keep current): ")

        new_name = new_name if new_name else product[1]
        new_price = float(new_price_input) if new_price_input else product[2]
        new_stock = int(new_stock_input) if new_stock_input else product[3]

        cursor.execute("""
            UPDATE Product
            SET name = ?, price = ?, stock = ?
            WHERE product_id = ?
        """, (new_name, new_price, new_stock, product_id))

        conn.commit()
        print("Product updated successfully.")

    except Exception as e:
        print(f"Error editing product: {e}")
    finally:
        conn.close()

def edit_customer_account():
    print("\n=== Edit Customer Account ===")
    try:
        conn = sqlite3.connect("ecommerce.db")
        cursor = conn.cursor()

        customer_id = int(input("Enter your customer ID: "))

        # Check if the customer exists
        cursor.execute("SELECT * FROM Customer WHERE customer_id = ?", (customer_id,))
        customer = cursor.fetchone()

        if customer is None:
            print("No customer found with that ID.")
            return

        print(f"Current Name: {customer[1]}")
        print(f"Current Email: {customer[2]}")

        new_name = input("Enter new name (or press Enter to keep current): ")
        new_email = input("Enter new email (or press Enter to keep current): ")

        updated_name = new_name if new_name.strip() else customer[1]
        updated_email = new_email if new_email.strip() else customer[2]

        # Update the customer information
        cursor.execute("""
            UPDATE Customer
            SET name = ?, email = ?
            WHERE customer_id = ?
        """, (updated_name, updated_email, customer_id))

        conn.commit()
        print("Account updated successfully.")

    except sqlite3.IntegrityError:
        print("Error: The new email address is already in use.")
    except Exception as e:
        print(f"Error updating account: {e}")
    finally:
        conn.close()

def add_credit_card():
    print("\n=== Add Credit Card ===")
    try:
        conn = sqlite3.connect("ecommerce.db")
        cursor = conn.cursor()

        customer_id = int(input("Enter your customer ID: "))

        # Verify customer exists
        cursor.execute("SELECT name FROM Customer WHERE customer_id = ?", (customer_id,))
        customer = cursor.fetchone()
        if customer is None:
            print("No customer found with that ID.")
            return

        print(f"Customer: {customer[0]}")
        card_number = input("Enter card number: ")
        expiration = input("Enter expiration date (MM/YY): ")

        # Insert the new credit card
        cursor.execute("""
            INSERT INTO CreditCard (customer_id, card_number, expiration)
            VALUES (?, ?, ?)
        """, (customer_id, card_number, expiration))

        conn.commit()
        print("Credit card added successfully.")

    except Exception as e:
        print(f"Error adding credit card: {e}")
    finally:
        conn.close()

def main():
    while True:
        print("\n==== E-Commerce Console ====")
        print("1. View Products")
        print("2. Make Purchase")
        print("3. Add Product (Staff)")
        print("4. View All Purchases (Staff)")
        print("5. Edit Existing Product (Staff)")
        print("6. Edit Customer Account")
        print("7. Add Credit Card (Customer)")
        print("8. Exit")
        choice = input("Select option: ")

        if choice == '1':
            view_products()
        elif choice == '2':
            make_purchase()
        elif choice == '3':
            add_product()
        elif choice == '4':
            view_purchases()
        elif choice == '5':
            edit_product()
        elif choice == '6':
            edit_customer_account()
        elif choice == '7':
            add_credit_card()
        elif choice == "8":
            print("Goodbye!")
            break
        else:
            print("Invalid option.")

if __name__ == "__main__":
    main()
