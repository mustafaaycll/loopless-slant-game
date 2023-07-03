from circle import Circle
from cell import Cell
from symbols import Symbols
from player import Player
from slantai import SlantAI

import copy

class Board():

    def __init__(self, board_path:str, human_starts_first:bool):
        self.human_starts_first = human_starts_first
        circles:list[list[Circle]] = self._read_board(path=board_path)
        self._path = board_path
        self.dimensions:list[int] = [len(circles) - 1, len(circles[0]) - 1]
        self.cells:list[list[Cell]] = self._generate_cells(circles=circles)
        self._previous_state:dict = None
        if human_starts_first:
            self.computer = Player(name="Computer", symbol=Symbols.BACKSLASH)
            self.human = Player(name="You", symbol=Symbols.SLASH)
        else:
            self.computer = Player(name="Computer", symbol=Symbols.SLASH)
            self.human = Player(name="You", symbol=Symbols.BACKSLASH)


    def __deepcopy__(self, memo):
        new_board = Board(board_path=self._path, human_starts_first=self.human_starts_first)
        new_board.cells = copy.deepcopy(self.cells, memo)
        new_board.dimensions = copy.deepcopy(self.dimensions, memo)
        return new_board

    def _read_board(self, path:str):
        lines = [line.strip() for line in open(path, "r").readlines()]
        returned_circles = []
        for line in lines:
            tmp = []
            for point in line:
                tmp.append(Circle(int(point)))
            returned_circles.append(tmp)
        return returned_circles


    def _generate_cells(self, circles:list):
        row_count = self.dimensions[0]
        col_count = self.dimensions[1]
        cells = []
        for x in range(row_count):
            tmp = []
            for y in range(col_count):
                cell = Cell(
                    top_left_circle = circles[x][y],
                    top_right_circle = circles[x][y+1],
                    bottom_left_circle = circles[x+1][y],
                    bottom_right_circle = circles[x+1][y+1],
                )
                tmp.append(cell)
            cells.append(tmp)
        return cells

    def filled(self) -> bool:
        row_count = self.dimensions[0]
        col_count = self.dimensions[1]
        for x in range(row_count):
            for y in range (col_count):
                if self.cells[x][y].symbol == Symbols.EMPTY:
                    return False
        return True

    def empty_cells(self) -> int:
        row_count = self.dimensions[0]
        col_count = self.dimensions[1]
        count = 0
        for x in range(row_count):
            for y in range (col_count):
                if self.cells[x][y].symbol == Symbols.EMPTY:
                    count += 1
        return count

    def _save(self):
        self._previous_state = {
            'cells': copy.deepcopy(self.cells),
            'computer': copy.deepcopy(self.computer),
            'human': copy.deepcopy(self.human),
        }

    def _recover(self):
        self.cells = copy.deepcopy(self._previous_state['cells'])
        self.human = copy.deepcopy(self._previous_state['human'])
        self.computer = copy.deepcopy(self._previous_state['computer'])

    def play_as_human(self, x:int, y:int):
        self._save()
        points = self.cells[x][y].play(symbol=self.human.symbol)
        self.human.points += points
        self.computer.points -= points

    def play_as_computer(self, x:int, y:int):
        self._save()
        points = self.cells[x][y].play(symbol=self.computer.symbol)
        self.computer.points += points
        self.human.points -= points

    def undo(self):
        self._recover()

    def ai_respond(self) -> dict:
        moves = self.possible_moves()
        scores = []
        for move in moves:
            ai:SlantAI = SlantAI(board=self, move=move)
            scores.append(ai.score)
        print(scores)
        selected_move = moves[scores.index(max(scores))]
        return selected_move


    def visualize(self, round_count:int):
        row_count = self.dimensions[0]
        col_count = self.dimensions[1]
        print("+---------------------------------------------------------------------------+")
        for x in range(row_count):
            if x == 0:
                first_line  = f"| ROUND {round_count}\t\t\t"
                second_line = f"| COM: {self.computer.points}\t\t\t"
                third_line  = f"| YOU: {self.human.points}\t\t\t"
            else:
                first_line  = "| \t\t\t\t"
                second_line = "| \t\t\t\t"
                third_line  = "| \t\t\t\t"

            for y in range(col_count):
                c:Cell = self.cells[x][y]

                if y == 0: # first column prints left pane
                    first_line += f"{c.top_left_circle.point} - {c.top_right_circle.point} "
                    second_line += f"| {c} |"
                    third_line += f"{c.bottom_left_circle.point} - {c.bottom_right_circle.point} "
                else:
                    first_line += f"- {c.top_right_circle.point} "
                    second_line += f" {c} |"
                    third_line += f"- {c.bottom_right_circle.point} "

            if x == 0: # first row prints 3 lines
                print(first_line)
            print(second_line)
            print(third_line)
        print("+---------------------------------------------------------------------------+")

    def print_additional(self):
        row_count = self.dimensions[0]
        col_count = self.dimensions[1]

        for x in range(row_count):
            l = ""
            for y in range(col_count):
                c:Cell = self.cells[x][y]
                l += f"{x}-{y} -> TL: {c.top_left_circle}, TR: {c.top_right_circle}, BL: {c.bottom_left_circle}, BR: {c.bottom_right_circle}\n"
            print(l)

    def possible_moves(self):
        row_count = self.dimensions[0]
        col_count = self.dimensions[1]
        possible_moves = []
        for x in range(row_count):
            for y in range(col_count):
                if self.cells[x][y].symbol == Symbols.EMPTY:
                    m = {'x': x,'y': y}
                    possible_moves.append(m)
        return possible_moves

    def announce_winner(self):
        subject = ""
        if self.computer.points == self.human.points:
            subject = "No one"
        elif self.computer.points > self.human.points:
            subject = self.computer.name
        else:
            subject = self.human.name
        print("+---------------------------------------------------------------------------+")
        print(f"| Game ended. {subject} won with {max(self.computer.points, self.human.points)} points")
        print("+---------------------------------------------------------------------------+")
