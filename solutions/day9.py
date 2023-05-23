def start():
    return {0: {-1: 0, 1: 0}}


def play(marbles, last_marble, n_players):
    scores = {k: 0 for k in range(1, n_players + 1)}
    current = 0
    current_marble = 1
    divisor = 23
    moves_left = 8

    for turn in range(1, last_marble + 1):
        # Normal case: insert one right
        if turn % divisor == 0:
            player = turn % n_players
            player += n_players if player == 0 else 0
            # Go 7 left
            left = None
            for _ in range(moves_left):
                left = marbles[current][-1]
                current = left

            # left/right of removed marble
            removal = marbles[left][1]
            right = marbles[removal][1]
            marbles.pop(removal)
            marbles[left][1] = right
            marbles[right][-1] = left
            current = right

            scores[player] += removal + current_marble
        else:
            # Between 1 and 2 clockwise
            left = marbles[current][1]
            right = marbles[left][1]
            marbles[left][1] = current_marble
            marbles[current_marble] = {-1: left, 1: right}
            marbles[right][-1] = current_marble
            current = current_marble

        current_marble += 1

    return max(scores.values())


with open("inputs/day9.txt") as f:
    words = f.read().rstrip("\n").split(" ")
    n_players = int(words[0])
    last_marble = int(words[-2])

marbles = {0: {-1: 0, 1: 0}}
part1 = play(start(), last_marble, n_players)
print(part1)

factor = 100
part2 = play(start(), last_marble * factor, n_players)
print(part2)
