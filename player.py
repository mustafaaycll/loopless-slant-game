from symbols import Symbols

class Player():
    def __init__(self, name:str, symbol:Symbols):
        self.name:str = name
        self.symbol:Symbols = symbol
        self._points:int = 0

    @property
    def points(self):
        return self._points

    @points.setter
    def points(self, val:int):
        self._points = val