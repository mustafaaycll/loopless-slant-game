import copy


class SlantAI():
    def __init__(self, board, move:dict[str,int]):
        self.board_snapshot = copy.deepcopy(board)
        self.board_snapshot.play_as_computer(x=move['x'], y=move['y'])
        self.score = self._alphabeta(board=self.board_snapshot, depth=self.board_snapshot.empty_cells(), alpha=float('-inf'), beta=float('inf'), maximizing_player=False)


    def _h(self, board) -> int:
        return board.computer.points


    def _alphabeta(self, board, depth:int, alpha:float, beta:float, maximizing_player:bool):
        if depth == 0 or board.filled():
            return self._h(board)

        if maximizing_player:
            max_eval = float('-inf')
            for move in board.possible_moves():
                board.play_as_computer(x=move['x'], y=move['y'])
                evaluation = self._alphabeta(board=board, depth=depth-1, alpha=alpha, beta=beta, maximizing_player=False)
                board.undo()
                max_eval = max(max_eval, evaluation)
                alpha = max(alpha, evaluation)
                if beta <= alpha:
                    break
            return max_eval
        else:
            min_eval = float('inf')
            for move in board.possible_moves():
                board.play_as_human(x=move['x'], y=move['y'])
                evaluation = self._alphabeta(board=board, depth=depth-1, alpha=alpha, beta=beta, maximizing_player=True)
                board.undo()
                min_eval = min(min_eval, evaluation)
                beta = min(beta, evaluation)
                if beta <= alpha:
                    break
            return min_eval