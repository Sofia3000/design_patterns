class IDGenerator:
    """
    Singleton class for generating sequential unique IDs.

    This class ensures only one instance exists during runtime.
    Each call to :meth:`get_next_id` returns the next integer ID.
    """

    # IDGenerator instance reference
    __instance = None
    # Flag to ensure one-time initialization
    __initialized = False

    def __new__(cls):
        """
        Creates or returns the single instance of IDGenerator.

        :return: The singleton instance of IDGenerator.
        :rtype: IDGenerator
        """
        # Create instance if it doesn't exist yet
        if not cls.__instance:
            cls.__instance = super(IDGenerator, cls).__new__(cls)
        return cls.__instance
    
    def __init__(self):
        """
        Initializes the ID counter only once during the first instantiation.
        """
        if not self.__initialized:
            # Set start value for id
            self.__id = 0
            self.__initialized = True

    def get_next_id(self):
        """
        Returns the next unique ID in the sequence.

        :return: The next available ID.
        :rtype: int
        """
        self.__id += 1
        return self.__id
    
    def reset(self):
        """
        Resets the ID counter to zero.
        """
        self.__id = 0


def main():
    """
    Demonstrates the singleton behavior and functionality of IDGenerator.
    """
    # Create two generators
    gen1 = IDGenerator()
    gen2 = IDGenerator()

    # Compare gen1 and gen2
    print("gen1 is gen2:", gen1 is gen2)

    # Generate id 4 times
    print("gen1 ID 1:", gen1.get_next_id())
    print("gen2 ID 2:", gen2.get_next_id())
    print("gen1 ID 3:", gen1.get_next_id())
    print("gen2 ID 4:", gen2.get_next_id())

    # Reset id
    gen1.reset()

    # Generate one id
    print("After reset:")
    print("gen2 ID 1 again:", gen2.get_next_id())

# Run main() only when script is executed directly
if __name__ == "__main__":
    main()