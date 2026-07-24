class MappingStore:
    """
    Stores mapping between original PII and fake values.
    """

    def __init__(self):
        self.mapping = {}

    def get(self, original):
        """
        Return fake value if already exists.
        """
        return self.mapping.get(original)

    def add(self, original, fake):
        """
        Store new mapping.
        """
        self.mapping[original] = fake

    def exists(self, original):
        """
        Check whether mapping already exists.
        """
        return original in self.mapping

    def print_mapping(self):
        """
        Display all mappings.
        """
        print("\nStored Mapping")
        print("-" * 60)

        for original, fake in self.mapping.items():
            print(f"{original}  -->  {fake}")

    def get_mapping(self):
        """
        Return complete mapping dictionary.
        """
        return self.mapping