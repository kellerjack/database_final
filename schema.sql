DROP TABLE IF EXISTS Purchase;
DROP TABLE IF EXISTS Staff;
DROP TABLE IF EXISTS CreditCard;
DROP TABLE IF EXISTS Product;
DROP TABLE IF EXISTS Customer;
DROP TABLE IF EXISTS PurchaseItem;

CREATE TABLE Customer (
    customer_id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL
);

CREATE TABLE Staff (
    staff_id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    role TEXT
);

CREATE TABLE CreditCard (
    card_id INTEGER PRIMARY KEY,
    customer_id INTEGER NOT NULL,
    card_number TEXT NOT NULL,
    expiration TEXT NOT NULL,
    FOREIGN KEY (customer_id) REFERENCES Customer(customer_id)
);

CREATE TABLE IF NOT EXISTS Purchase (
    Purchase_ID INTEGER PRIMARY KEY AUTOINCREMENT,
    Customer_ID INTEGER NOT NULL,
    Card_ID INTEGER,
    Timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (Customer_ID) REFERENCES Customer(Customer_ID),
    FOREIGN KEY (Card_ID) REFERENCES CreditCard(Card_ID)
);

CREATE TABLE PurchaseItem (
    Purchase_ID INTEGER,
    product_id INTEGER,
    Quantity INTEGER,
    Price REAL,
    FOREIGN KEY (Purchase_ID) REFERENCES Purchase(Purchase_ID),
    FOREIGN KEY (product_id) REFERENCES Product(product_id)
);

CREATE TABLE Product (
    product_id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    price REAL NOT NULL,
    stock INTEGER NOT NULL
);

INSERT INTO Customer (customer_id, name, email) VALUES
(1, 'Alice Johnson', 'alice@example.com'),
(2, 'Bob Smith', 'bob@example.com');

INSERT INTO Staff (staff_id, name, role) VALUES
(1, 'Emily Carter', 'Inventory Manager'),
(2, 'Daniel Lee', 'Sales Manager');

INSERT INTO CreditCard (card_id, customer_id, card_number, expiration) VALUES
(1, 1, '4111111111111111', '12/26'),
(2, 1, '5500000000000004', '01/27'),
(3, 2, '340000000000009', '03/26');

INSERT INTO Product (product_id, name, price, stock) VALUES
(1, 'Wireless Mouse', 25.99, 100),
(2, 'Mechanical Keyboard', 79.99, 50),
(3, 'USB-C Hub', 34.99, 75),
(4, 'Laptop Stand', 39.99, 40);

INSERT INTO Purchase (purchase_id, customer_id, card_id, Timestamp) VALUES
(1, 1, 1, '2025-08-01 10:00:00'),
(2, 2, 3, '2025-08-02 15:30:00');

INSERT INTO PurchaseItem (purchase_id, product_id, quantity, price) VALUES
(1, 1, 2, 51.98),  -- Alice buys 2 Wireless Mice
(1, 2, 1, 79.99),  -- Alice buys 1 Mechanical Keyboard
(2, 3, 1, 34.99),  -- Bob buys 1 USB-C Hub
(2, 4, 2, 79.98);  -- Bob buys 2 Laptop Stands

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



