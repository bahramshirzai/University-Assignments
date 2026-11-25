
import sqlite3

# 1. Connect to database
conn = sqlite3.connect("bank.db")
cursor = conn.cursor()

# 2. Create accounts table
cursor.execute("""
CREATE TABLE IF NOT EXISTS accounts (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    balance REAL NOT NULL
)
""")

# 3. Insert two sample accounts
cursor.execute("DELETE FROM accounts")

accounts = [
    (1, "Ahmad", 5000),
    (2, "Bahram", 3000)
]

cursor.executemany("""
INSERT INTO accounts (id, name, balance)
VALUES (?, ?, ?)
""", accounts)

conn.commit()


# Function to display account balances
def display_balances():
    cursor.execute("SELECT * FROM accounts")

    for account in cursor.fetchall():
        print(account)


# 4. Transfer function
def transfer(sender_id, receiver_id, amount):

    try:
        # Start transaction
        conn.execute("BEGIN")

        # Get sender balance
        cursor.execute(
            "SELECT balance FROM accounts WHERE id = ?",
            (sender_id,)
        )

        sender = cursor.fetchone()

        # Get receiver account
        cursor.execute(
            "SELECT id FROM accounts WHERE id = ?",
            (receiver_id,)
        )

        receiver = cursor.fetchone()

        # Validate accounts and amount
        if sender is None or receiver is None:
            raise Exception("Account not found!")

        if amount <= 0:
            raise Exception("Invalid transfer amount!")

        if sender[0] < amount:
            raise Exception("Insufficient balance!")

        # Subtract money from sender
        cursor.execute("""
        UPDATE accounts
        SET balance = balance - ?
        WHERE id = ?
        """, (amount, sender_id))

        # Add money to receiver
        cursor.execute("""
        UPDATE accounts
        SET balance = balance + ?
        WHERE id = ?
        """, (amount, receiver_id))

        # 5. Commit transaction
        conn.commit()

        print("\nTransfer successful!")

    except Exception as e:

        # 6. Rollback if an error occurs
        conn.rollback()

        print("\nTransfer failed:", e)


# 7. Display balances before transfer
print("\n--- Balances Before Transfer ---")
display_balances()

# Perform transfer
transfer(1, 2, 1000)

# 8. Display balances after transfer
print("\n--- Balances After Transfer ---")
display_balances()

# Close database connection
conn.close()
