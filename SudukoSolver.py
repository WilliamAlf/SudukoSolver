puzzle_easy = [0, 0, 3, 0, 0, 0, 2, 0, 0,  # easy
               0, 6, 0, 9, 8, 0, 0, 4, 3,
               4, 9, 0, 0, 3, 1, 0, 0, 6,
               9, 0, 7, 0, 0, 0, 8, 6, 0,
               0, 4, 0, 0, 9, 8, 0, 0, 0,
               0, 0, 5, 4, 0, 7, 1, 0, 9,
               6, 0, 0, 0, 0, 3, 9, 0, 5,
               5, 0, 8, 1, 0, 0, 0, 7, 2,
               2, 0, 9, 0, 5, 6, 0, 3, 8]

puzzle_medium = [0, 8, 0, 6, 0, 0, 0, 1, 0,  # medium
                 0, 0, 0, 0, 0, 8, 2, 5, 6,
                 0, 0, 1, 0, 0, 0, 0, 0, 0,
                 0, 0, 0, 9, 0, 4, 6, 0, 3,
                 0, 0, 9, 0, 7, 0, 5, 0, 0,
                 4, 0, 7, 5, 0, 2, 0, 0, 0,
                 0, 0, 0, 0, 0, 0, 8, 0, 0,
                 7, 1, 3, 4, 0, 0, 0, 0, 0,
                 0, 5, 0, 0, 0, 9, 0, 3, 0]

puzzle_hard = [0, 0, 5, 0, 0, 0, 0, 6, 2,  # super hard
               0, 6, 3, 0, 0, 9, 0, 0, 0,
               0, 0, 0, 0, 0, 0, 0, 0, 4,
               0, 0, 0, 0, 0, 6, 7, 0, 3,
               0, 0, 6, 7, 0, 5, 0, 0, 0,
               1, 0, 0, 8, 0, 0, 0, 0, 0,
               8, 0, 1, 2, 0, 0, 6, 0, 0,
               0, 0, 0, 0, 0, 0, 5, 3, 0,
               0, 4, 0, 0, 0, 0, 8, 0, 0]


def get_row(matrix, square_index) -> []:
    row = square_index - square_index % 9
    return matrix[row: row + 9]


def get_column(matrix, square_index) -> []:
    column_index = square_index % 9
    column = []

    for _ in range(9):
        column += [matrix[column_index]]
        column_index += 9

    return column


def get_box(matrix, square_index) -> []:
    upper_left_index = square_index - (square_index % 27) + (square_index % 9 - square_index % 3)
    box = []

    for _ in range(3):
        box += [
            matrix[upper_left_index],
            matrix[upper_left_index + 1],
            matrix[upper_left_index + 2]
        ]
        upper_left_index += 9

    return box


def find_possible_values(matrix, square_index) -> {}:
    return set(range(1, 9+1)) - set(
        get_row(matrix, square_index) +
        get_column(matrix, square_index) +
        get_box(matrix, square_index)
    )


def create_solver_matrix(puzzle) -> []:
    solver_matrix = []

    for square in range(81):
        square_value = puzzle[square]
        square_solution = square_value if square_value in set(range(1, 9 + 1)) else 0
        square_solved = False if square_solution == 0 else True
        square_possible_values = find_possible_values(puzzle, square)

        # Optimisation: Fill value here if possible values == 1

        solver_matrix.append({
            "solved": square_solved,
            "solution": square_solution,
            "possible_values": {} if square_solved else square_possible_values
        })

    return solver_matrix


def remove_possible_value(solver_matrix, square_index, value):
    affected_box = get_box(solver_matrix, square_index)
    affected_row = get_row(solver_matrix, square_index)
    affected_column = get_column(solver_matrix, square_index)
    affeced_squares = {affected_box + affected_row + affected_column} # Contains Duplicates

    for solver_square in affeced_squares:
        solver_square["possible_values"] -= {value}

    return solver_matrix


def fill_value(solver_matrix, square_index, value) -> []:
    solver_square = solver_matrix[square_index]
    solver_square["solved"] = True
    solver_square["solution"] = value
    solver_square["possible_values"] = {}

    solver_matrix = remove_possible_value(solver_matrix, square_index, value)

    return solver_matrix


def print_solution(solution):
    print("- - - - - - - - -")
    for i in range(len(solution)):
        if i % 9 == 0:
            print("|")
        print(solution[i]["solution"] + " ")
        if (i + 1) % 9 == 0:
            print("|")
        if i in {26, 53}:
            print("- - - - - - - - -")
    print("- - - - - - - - -")

"""
0  1  2  3  4  5  6  7  8
9  10 11 12 13 14 15 16 17
18 19 20 21 22 23 24 25 26
27 28 29 30 31 32 33 34 35
36 37 38 39 40 41 42 43 44
45 46 47 48 49 50 51 52 53
54 55 56 57 58 59 60 61 62
63 64 65 66 67 68 69 70 71
72 73 74 75 76 77 78 79 80
"""


def solve_puzzle(puzzle) -> []:
    solver_matrix = create_solver_matrix(puzzle)
    unsolved_squares = {
        square_index for square_index in range(len(solver_matrix)) if not solver_matrix[square_index]["solved"]
    }


    def filling_iteration(unsolved_squares, solver_matrix):
        remaining_unsolved_squares = unsolved_squares.copy()
        for square_index in remaining_unsolved_squares:
            solver_square = solver_matrix[square_index]

            if len(solver_square["possible_values"]) == 1:
                solution_value = list(solver_square["possible_values"])[0]
                solver_matrix = fill_value(solver_matrix, square_index, solution_value)
                remaining_unsolved_squares -= {square_index}

        return solver_matrix, remaining_unsolved_squares

    while len(unsolved_squares) > 0:
        solver_matrix, unsolved_squares = filling_iteration(unsolved_squares, solver_matrix)

    return solver_matrix


if __name__ == "__main__":
    puzzle = puzzle_hard
    solution = solve_puzzle(puzzle)
    print_solution(solution)

"""
TODO : 
    1. Complete working version
    2. Optimise program
    3. Make program able to detect if puzzle is unsolvable
    4. Start working on computer vision part
"""