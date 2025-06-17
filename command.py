from abc import ABC, abstractmethod

class InsufficientFundsError(Exception):
    """Raised when an account has insufficient balance for the operation."""


class MoneyValidator:
    """
    Provides static validation for monetary values.
    Ensures the amount is a positive number (int or float).
    """

    @staticmethod
    def validate_money(amount) -> float:
        """
        Validates that the given amount is a positive number.

        :param amount: The amount to validate.
        :raises TypeError: If amount is not a number.
        :raises ValueError: If amount is not positive.
        """
        if not isinstance(amount, (int, float)):
            raise TypeError(
                "Parameter 'amount' must be an instance of float"
            )
        if amount <= 0:
            raise ValueError("Parameter 'amount' must be positive number")


class BankAccount(MoneyValidator):
    """
    Represents a simple bank account with methods for deposit, withdrawal, and balance display.
    Inherits from MoneyValidator to validate monetary input.
    """

    _precision: int = 2  # Number of decimal places to round to

    def __init__(self):
        """
        Initializes the account with a zero starting balance.
        """
        self.__balance = 0

    def increase_balance(self, amount: float):
        """
        Increases the account balance by the given amount.

        :param amount: Amount to deposit.
        """
        self.validate_money(amount)
        amount = round(amount, self._precision)
        self.__balance += amount
        self.__balance = round(self.__balance, self._precision)
    
    def decrease_balance(self, amount: float):
        """
        Decreases the account balance by the given amount if sufficient funds are available.

        :param amount: Amount to withdraw.
        :raises InsufficientFundsError: If withdrawal amount exceeds balance.
        """
        self.validate_money(amount)
        amount = round(amount, self._precision)
        if self.__balance < amount:
            raise InsufficientFundsError("Insufficient funds for withdrawal")
        self.__balance -= amount
        self.__balance = round(self.__balance, self._precision)
    
    def show_balance(self):
        """
        Prints the current balance.
        """
        print(f"Current balance: {self.__balance:.2f}")


class Command(ABC):
    """
    Abstract base class for all commands.
    Holds a reference to the BankAccount object.
    """

    def __init__(self, account: BankAccount):
        """
        Initializes the command with a target bank account.

        :param account: The target BankAccount.
        :raises TypeError: If account is not a BankAccount instance.
        """
        if not isinstance(account, BankAccount):
            raise TypeError(
                "Parameter 'account' must be an instance of BankAccount"
            )
        self._account = account

    @abstractmethod
    def execute(self):
        """Executes the command."""


class IncreaseBalanceCommand(Command, MoneyValidator):
    """
    Command to deposit money into a bank account.
    """

    def __init__(self, account: BankAccount, amount: float):
        """
        Initializes the command with an amount to deposit.

        :param account: The target BankAccount.
        :param amount: Amount to deposit.
        """
        super().__init__(account)
        self.validate_money(amount)
        self._amount = amount

    def execute(self):
        """
        Executes the deposit operation.
        """
        self._account.increase_balance(self._amount)


class DecreaseBalanceCommand(Command, MoneyValidator):
    """
    Command to withdraw money from a bank account.
    """

    def __init__(self, account: BankAccount, amount: float):
        """
        Initializes the command with an amount to withdraw.

        :param account: The target BankAccount.
        :param amount: Amount to withdraw.
        """
        super().__init__(account)
        self.validate_money(amount)
        self._amount = amount

    def execute(self):
        """
        Executes the withdrawal operation.
        """
        self._account.decrease_balance(self._amount)


class ShowBalanceCommand(Command):
    """
    Command to display the current account balance.
    """

    def execute(self):
        """
        Executes the show balance operation.
        """
        self._account.show_balance()


class Button:
    """
    Represents an invoker that triggers a command via a button press.
    """

    def __init__(self, name: str, command: Command):
        """
        Initializes the button with a name and a command.

        :param name: Button label.
        :param command: Command to be executed.
        :raises TypeError, ValueError: On invalid parameters.
        """
        if not isinstance(name, str):
            raise TypeError("Parameter 'name' must be a string.")
        if not name.strip():
            raise ValueError("Parameter 'name' could not be empty")
        if not isinstance(command, Command):
            raise TypeError("Parameter 'command' must be an instance of Command")
        self.__name = name
        self.__command = command

    def do_operation(self):
        """
        Executes the associated command.
        """
        self.__command.execute()

    def __str__(self):
        """
        Returns the button's label as a string.
        """
        return self.__name


def main():
    """
    Entry point demonstrating the Command pattern with interactive input.

    The user can:
    - press 'd' to deposit money
    - press 'w' to withdraw money
    - press 's' to show the balance
    - press 'q' to quit
    """
    account = BankAccount()
    deposit_cmd = IncreaseBalanceCommand(account, 50)
    deposit_btn = Button("Deposit $50", deposit_cmd)
    withdraw_cmd = DecreaseBalanceCommand(account, 30)
    withdraw_btn = Button("Withdraw $30", withdraw_cmd)
    show_cmd = ShowBalanceCommand(account)
    show_btn = Button("Show Balance", show_cmd)
                   
    while True:
        print("\n--- MENU ---")
        print(f"d - {deposit_btn}")
        print(f"w - {withdraw_btn}")
        print(f"s - {show_btn}")
        print("q - Quit")

        command = input("Choose an action: ").strip().lower()
        match(command):
            case 'd':
                deposit_btn.do_operation()
                print("Transaction successful: $50 deposited.")
            case 'w':
                try:
                    withdraw_btn.do_operation()
                    print("Transaction successful: $30 withdrawn.")
                except InsufficientFundsError as e:
                    print(f"Error: {e}")
            case 's':
                show_btn.do_operation()
            case 'q':
                print("Exiting.")
                break
            case _:
                print("Invalid input. Please choose 'd', 'w', 's', or 'q'.")
        input("Press Enter to continue. ")


if __name__ == "__main__":
    main()
