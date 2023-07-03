from board import Board
import time

def prompt() -> bool:
    starter = input("\nWho stars first? {type C for computer, H for human}: ")
    print()
    if starter == "H":
        human_starts_first = True
        prompt = open("prompt_when_human.txt", "r").readlines()
        print("".join(prompt))
    else:
        human_starts_first = False
        prompt = open("prompt_when_computer.txt", "r").readlines()
        print("".join(prompt))
    return human_starts_first

if __name__ == "__main__":
    human_starts_first = prompt()

    board = Board("board.txt", human_starts_first=human_starts_first)
    board.visualize(round_count=0)

    round_count = 1
    while not board.filled():

        if round_count != 1 or human_starts_first:
            coordinates = input("| What is your move? ").split(',')
            x,y = int(coordinates[0]), int(coordinates[1])
            board.play_as_human(x,y)
            if board.filled():
                continue

        start_time = time.time()
        move = board.ai_respond()
        print(f"| Computer has decided to play {move['x']},{move['y']} in {format(time.time() - start_time, '.2f')}s")
        board.play_as_computer(x=move['x'], y=move['y'])

        board.visualize(round_count=round_count)
        round_count += 1
    board.announce_winner()
