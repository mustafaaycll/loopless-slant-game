class Circle():
    def __init__(self, point:int):
        self.point:int = point
        self._intersection:int = 0
        self._points_claimed:bool = False

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return f"[Point: {self.point}, Current Intersections: {self._intersection}, Points Claimed: {self._points_claimed}]"

    @property
    def intersection(self):
        return self._intersection

    @intersection.setter
    def intersection(self, val:int):
        self._intersection = val

    @property
    def points_claimed(self):
        return self._points_claimed

    @points_claimed.setter
    def points_claimed(self, val:bool):
        self._points_claimed = val