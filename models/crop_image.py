class CropImage:
    def __init__(self, id, name, x1, x2, y1, y2, confidence):
        self.id = id
        self.name = name
        self.x1 = x1
        self.x2 = x2
        self.y1 = y1
        self.y2 = y2
        self.confidence = confidence

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "x1": self.x1,
            "x2": self.x2,
            "y1": self.y1,
            "y2": self.y2,
            "confidence": self.confidence
        }
