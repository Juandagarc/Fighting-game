class DiagonalPlatform:
    def __init__(self, x1, y1, x2, y2):
        """
        Initialize a diagonal platform defined by two points.
        """
        self.x1, self.y1 = x1, y1
        self.x2, self.y2 = x2, y2
        self.slope = (y2 - y1) / (x2 - x1)  # Calculate the slope
        self.y_intercept = y1 - self.slope * x1  # Calculate the y-intercept

    def get_y_at_x(self, x):
        """
        Get the y-coordinate on the platform for a given x-coordinate.
        """
        if not self.contains_x(x):
            return None  # Return None if x is out of bounds
        return self.slope * x + self.y_intercept

    def contains_x(self, x):
        """
        Check if the x-coordinate is within the bounds of the platform.
        """
        return self.x1 <= x <= self.x2
