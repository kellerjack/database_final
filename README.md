Hopefully this counts as some documentation.

The database uses sqlite3. The .sql file includes 5 schema (Customer, Staff, Purchase, PurchaseItem, and CreditCard). 
PurchaseItem is a associative table that lets users make multiple purchases in a single transaction.
This file also includes some insert statements
Finally, it includes a multi-table query

The .py file includes some CLI looking logic for user interaction. 
User authentication is out of scope, so it's assumed that users will use the software according to their role.
