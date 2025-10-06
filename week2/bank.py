class InsufficientBalanceError(Exception):
    """
    Custom exception raised when a withdrawal amount exceeds the account balance.
    """
    pass


class BankAccount:
    """
    Represents a bank account with basic operations like deposit, withdrawal, and balance check.
    """

    def __init__(self, account_holder, balance=0):
        """
        Initialize a new bank account.

        Returns:
        None
        """
        self.account_holder = account_holder
        self.balance = balance

    def deposit(self, amount):
        """
        Deposit a positive amount into the bank account.

        Raises:
            ValueError: If the deposit amount is not positive.
        """
        if amount <= 0:
            raise ValueError("Deposit amount must be positive.")
        self.balance += amount
        print(f"₹{amount} deposited successfully.")

    def withdraw(self, amount):
        """
        Withdraw a positive amount from the bank account.

        Raises:
            ValueError: If the withdrawal amount is not positive.
            InsufficientBalanceError: If the withdrawal amount exceeds the balance.
        """
        if amount <= 0:
            raise ValueError("Withdrawal amount must be positive.")
        if amount > self.balance:
            raise InsufficientBalanceError("Insufficient balance for this withdrawal.")
        self.balance -= amount
        print(f"₹{amount} withdrawn successfully.")

    def check_balance(self):
        """
        Display and return the current account balance.

        Returns:
            float: The current balance of the bank account.
        """
        print(f"Current balance: ₹{self.balance}")
        return self.balance


try:
    name = input("Enter account holder name: ")
    initial_balance = float(input("Enter initial balance: "))
    account = BankAccount(name, initial_balance)

    while True:
        print("\nChoose an option:")
        print("1. Deposit Money")
        print("2. Withdraw Money")
        print("3. Check Balance")
        print("4. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            amount = float(input("Enter amount to deposit: "))
            try:
                account.deposit(amount)
            except ValueError as e:
                print("Error:", e)

        elif choice == "2":
            amount = float(input("Enter amount to withdraw: "))
            try:
                account.withdraw(amount)
            except (ValueError, InsufficientBalanceError) as e:
                print("Error:", e)

        elif choice == "3":
            account.check_balance()

        elif choice == "4":
            print("Thank you! Goodbye!")
            break

        else:
            print("Invalid choice. Please select again.")

except Exception as e:
    print("Error:", e)
