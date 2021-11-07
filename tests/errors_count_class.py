class error_count:
    def __init__(self):
        self.no_errors = 0
        self.type_errors = []

    def add_error(self, error_type: str):
        self.type_errors.append(error_type)
        self.no_errors += 1

    def check_errors(self) -> bool:
        if self.no_errors >= 1:
            print("\n")
            errors: str
            for errors in self.type_errors:
                print("Error: {}", errors)
            return False
        print("\nAll clear!  Asserting test true")
        return True

    def reset_errors(self):
        self.no_errors = 0
        self.type_errors.clear()