from circle import Circle
from symbols import Symbols

class Cell():
    def __init__(self, top_left_circle:Circle, top_right_circle:Circle, bottom_left_circle:Circle, bottom_right_circle:Circle):
        self.top_left_circle = top_left_circle
        self.top_right_circle = top_right_circle
        self.bottom_left_circle = bottom_left_circle
        self.bottom_right_circle = bottom_right_circle
        self._symbol = Symbols.EMPTY

    def __str__(self):
        match self._symbol:
            case Symbols.EMPTY:
                return " "
            case Symbols.SLASH:
                return "/"
            case Symbols.BACKSLASH:
                return "\\"

    @property
    def symbol(self):
        return self._symbol


    @symbol.setter
    def symbol(self, val:Symbols):
        self._symbol = val


    def play(self, symbol:Symbols) -> int:
        self._symbol = symbol
        return self._calc_point()

    def _calc_point(self) -> int:
        circle1 = None
        circle2 = None
        point = 0

        match self._symbol:
            case Symbols.SLASH:
                self.top_right_circle.intersection += 1
                self.bottom_left_circle.intersection += 1
                circle1 = self.top_right_circle
                circle2 = self.bottom_left_circle
            case Symbols.BACKSLASH:
                self.top_left_circle.intersection += 1
                self.bottom_right_circle.intersection += 1
                circle1 = self.top_left_circle
                circle2 = self.bottom_right_circle

        if circle1.intersection == circle1.point and circle1.points_claimed == False:
            point += circle1.point
            circle1.points_claimed = True
        if circle2.intersection == circle2.point and circle2.points_claimed == False:
            point += circle2.point
            circle2.points_claimed = True

        return point

