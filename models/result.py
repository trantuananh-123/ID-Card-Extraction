class Result:
    def __init__(self, name, value):
        self.name = name
        self.value = value

    def serialize(self):
        return {
            "name": self.name,
            "value": self.value
        }
