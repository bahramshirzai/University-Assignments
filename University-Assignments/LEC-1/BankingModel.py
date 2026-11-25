
from abc import ABC, abstractmethod


# 1. Abstract Account Base Class
class Account(ABC):

    def __init__(self, account_number, balance):
        self.account_number = account_number
        self._balance = balance

    # Encapsulation: Get balance safely
    @property
    def balance(self):
        return self._balance

    # Deposit money
    def deposit(self, amount):
        if amount > 0:
            self._balance += amount
            print(f"Deposited: ${amount}")
        else:
            print("Deposit amount must be positive!")

    # Withdraw money
    def withdraw(self, amount):
        if amount > 0 and amount <= self._balance:
            self._balance -= amount
            print(f"Withdrawn: ${amount}")
        else:
            print("Insufficient balance or invalid amount!")

    # Abstract method
    @abstractmethod
    def calculate_fee(self):
        pass

    def __str__(self):
        return f"Account Number: {self.account_number}, Balance: ${self.balance}"


# 2. Savings Account
class SavingsAccount(Account):

    def calculate_fee(self):
        return 0

    def __str__(self):
        return f"Savings Account | {super().__str__()}"


# 3. Current Account
class CurrentAccount(Account):

    def calculate_fee(self):
        return 10

    def __str__(self):
        return f"Current Account | {super().__str__()}"


# 4. Create Account Objects
account1 = SavingsAccount("SA101", 1000)
account2 = CurrentAccount("CA201", 2000)


# 5. Deposit and Withdraw
print("--- Savings Account Transactions ---")

account1.deposit(500)
account1.withdraw(200)

print("\n--- Current Account Transactions ---")

account2.deposit(300)
account2.withdraw(500)


# 6. Polymorphism
accounts = [account1, account2]

print("\n--- Account Information ---")

for account in accounts:
    print(account)
    print("Account Fee: $", account.calculate_fee())
    print("------------------------")


# 7. Display Final Balances
print("\n--- Final Balances ---")

for account in accounts:
    print(account.account_number, ":", account.balance)
