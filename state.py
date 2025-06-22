from enum import Enum
from abc import ABC, abstractmethod


class Status(Enum):
    """
    Represents the result of a code entry attempt.
    """
    CORRECTCODE = 1
    SUPERCODE = 2
    WRONGCODE = 3


class LockState(ABC):
    """
    Abstract base class for representing the state of a Lock.

    Each subclass should define behavior for how the lock responds
    when a code is entered in a given state.
    """

    def __init__(self):
        """
        Initializes the LockState with no associated Lock context.
        """
        self.__lock = None

    @property
    def lock(self):
        """
        Returns the lock context associated with this state.

        :return: The Lock object using this state.
        """
        return self.__lock

    @lock.setter
    def lock(self, lock: "Lock"):
        """
        Sets the context lock that owns this state.

        :param lock: A Lock object.
        :raises TypeError: If the object is not an instance of Lock.
        """
        if not isinstance(lock, Lock):
            raise TypeError("Parameter 'lock' must be an instance of Lock")
        self.__lock = lock

    @abstractmethod
    def on_code_entered(self, status: Status) -> None:
        """
        Handle behavior when a code is entered in this state.

        :param status: Status indicating result of code comparison.
        """


    def _check_context(self):
        """
        Validates that the lock context has been set for this state.

        :raises RuntimeError: If the lock is not set.
        """
        if not self.lock:
            raise RuntimeError("State isn't associated with any Lock context")


class Lock:
    """
    Context class representing a digital lock that can transition between different states.

    Uses the State pattern to delegate state-specific behavior.
    """

    _max_failed_attempts = 3

    def __init__(self, code: str, supercode: str, state: LockState):
        """
        Initializes the lock with a user code, a supercode, and an initial state.

        :param code: The regular code to unlock the lock.
        :param supercode: The emergency code to reset from error state.
        :param state: The initial state of the lock.
        :raises TypeError, ValueError: On invalid arguments.
        """
        if not isinstance(code, str):
            raise TypeError("Parameter 'code' must be a string")
        if not isinstance(supercode, str):
            raise TypeError("Parameter 'supercode' must be a string")
        if not self._validate_code(code):
            raise ValueError(f"Invalid code: {code}")
        if not self._validate_code(supercode):
            raise ValueError(f"Invalid supercode: {supercode}")
        if code == supercode:
            raise ValueError(
                "Parameters 'code' and 'supercode' must be differrent"
            )
        self.__code = code
        self.__supercode = supercode
        self.set_state(state)
        self.__failed_attempts = 0

    def set_state(self, state: LockState) -> None:
        """
        Sets a new state for the lock.

        :param state: A new LockState instance.
        :raises TypeError: If the argument is not a LockState.
        """
        if not isinstance(state, LockState):
            raise TypeError(
                "Parameter 'state' must be an instance of LockState"
            )
        self.__state = state
        self.__state.lock = self

    def enter_code(self, code: str) -> None:
        """
        Accepts a code input and processes it using the current state.

        :param code: The code entered by the user.
        :raises TypeError, ValueError: On invalid input.
        """
        if not isinstance(code, str):
            raise TypeError("Parameter 'code' must be a string")
        if not code.strip():
            raise ValueError("Parameter 'code' must not be empty")
        status = self._check_status(code)
        self.__state.on_code_entered(status)

    def _validate_code(self, code: str) -> bool:
        """
        Validates if the given code is a numeric string of appropriate length.

        :param code: Code to validate.
        :return: True if valid, False otherwise.
        """
        return code.isdigit() and 8 <= len(code) < 13

    def _check_status(self, code: str) -> Status:
        """
        Determines the status of the entered code.

        :param code: The input code.
        :return: Corresponding Status enum value.
        """
        if self.__code == code:
            return Status.CORRECTCODE
        if self.__supercode == code:
            return Status.SUPERCODE
        return Status.WRONGCODE

    def increase_failed_attempts(self):
        """
        Increments the number of failed attempts by one.
        """
        self.__failed_attempts += 1

    def reset_failed_attempts(self):
        """
        Resets the failed attempts counter to zero.
        """
        self.__failed_attempts = 0

    def is_limit_exceeded(self) -> bool:
        """
        Checks if the number of failed attempts
        has exceeded the allowed limit.

        :return: True if limit exceeded, else False.
        """
        return self.__failed_attempts >= self._max_failed_attempts


class LockedState(LockState):
    """
    Concrete state where the lock is locked.

    Accepts the correct code to unlock,
    or transitions to ErrorState on too many failures.
    """

    def on_code_entered(self, status: Status) -> None:
        """
        Processes the entered code while in the locked state.

        :param status: Status of the entered code.
        """
        self._check_context()
        if status == Status.CORRECTCODE:
            print("Lock is unlocked")
            self.lock.reset_failed_attempts()
            self.lock.set_state(UnlockedState())
        else:
            print("Incorrect code. Lock remains closed.")
            self.lock.increase_failed_attempts()
            if self.lock.is_limit_exceeded():
                print("Lock is in error state. Supercode required to reset.")
                self.lock.set_state(ErrorState())


class UnlockedState(LockState):
    """
    Concrete state where the lock is unlocked.

    Accepts the correct code again to lock the lock.
    """

    def on_code_entered(self, status: Status) -> None:
        """
        Processes the entered code while in the unlocked state.

        :param status: Status of the entered code.
        """
        self._check_context()
        if status == Status.CORRECTCODE:
            print("Lock is locked")
            self.lock.set_state(LockedState())
        else:
            print("Incorrect code. Lock remains unlocked.")


class ErrorState(LockState):
    """
    Concrete state for error handling.

    Only accepts the supercode to return to locked state.
    """

    def on_code_entered(self, status: Status) -> None:
        """
        Processes the entered code while in the error state.

        :param status: Status of the entered code.
        """
        self._check_context()
        if status == Status.SUPERCODE:
            print("Lock is locked. Use code to unlock.")
            self.lock.reset_failed_attempts()
            self.lock.set_state(LockedState())
        else:
            print("Incorrect supercode. Lock remains in error state.")


def main():
    """
    Entry point for demonstrating the lock behavior.

    Initializes the lock and prompts user for code input in a loop.
    """
    lock = Lock('12345678', "55555555", LockedState())
    print("Lock was locked")
    while True:
        action = input("Do you want to enter code (input 'y' if yes): ")
        if action.lower() == "y":
            code = input("Enter code: ")
            if not code.strip():
                print("Code must not be empty")
                continue
            if not code.isdigit():
                print("Code must contain only digits")
                continue
            lock.enter_code(code)
        else:
            print("Exiting")
            break


# Run main() only when script is executed directly
if __name__ == "__main__":
    main()
