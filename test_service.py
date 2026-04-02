class TestService:

    def __init__(self, base_operation: dict = {}):

        if not base_operation:
            self.operations = {"+": self.add}
        else:
            self.operations = base_operation

    def extract_operation(self, operation: str, *args):

        if operation not in self.operations:
            raise Exception("Not an available operations")
        else:
            return self.operations[operation](*args)

    @staticmethod
    def add(*args):

        return sum(args)


test_service = TestService()
