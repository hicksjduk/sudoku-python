from itertools import chain
from math import sqrt, ceil

permitted_values = set(range(1, 10))
empty_square = 0
grid_size = len(permitted_values)

if not grid_size:
    raise Exception("permitted_values is empty")
if empty_square in permitted_values:
    raise Exception("permitted_values includes the value of empty_square")


def calc_box_size():
    square_root = sqrt(grid_size)
    def divisor_of_grid_size(n):
        return grid_size % n == 0
    cols = next(filter(divisor_of_grid_size, range(
        ceil(square_root), grid_size)), grid_size)
    return (grid_size // cols, cols)


def calc_boxes():
    box_rows, box_cols = calc_box_size()
    box_top_left_corners = ((row, col) for row in range(0, grid_size, box_rows)
                         for col in range(0, grid_size, box_cols))
    return [((top_row, left_col), (top_row + box_rows, left_col + box_cols))
            for top_row, left_col in box_top_left_corners]


boxes = calc_boxes()


def solve(grid):
    try:
        yield from solve_at(grid, next(empty_squares(grid)))
    except StopIteration:
        yield grid


def empty_squares(grid):
    return ((row, col)
            for row, values in enumerate(grid)
            for col, value in enumerate(values)
            if value == empty_square)


def solve_at(grid, square):
    def solve_using(value):
        return solve(set_value_at(grid, square, value))
    return chain(*map(solve_using, allowed_values(grid, square)))


def set_value_at(grid, square, value):
    row, col = square
    new_row = replace_value_at(grid[row], col, value)
    return replace_value_at(grid, row, new_row)


def replace_value_at(lst, index, value):
    return [value if i == index else v for i, v in enumerate(lst)]


def allowed_values(grid, square):
    row, col = square
    blocked_values = set(chain(
        row_values(grid, row),
        col_values(grid, col),
        box_values(grid, box_containing(square))
    ))
    return permitted_values.difference(blocked_values)


def row_values(grid, row):
    return filter(not_empty, grid[row])


def col_values(grid, col):
    return filter(not_empty, (row[col] for row in grid))


def box_values(grid, box):
    (top_row, left_col), (bottom_row, right_col) = box
    box_rows = (row[left_col:right_col] for row in grid[top_row:bottom_row])
    return filter(not_empty, chain(*box_rows))


def not_empty(value):
    return value != empty_square


def box_containing(square):
    row, col = square
    def contains_square(box):
        (top_row, left_col), (bottom_row, right_col) = box
        return row in range(top_row, bottom_row) and col in range(left_col, right_col)
    return next(filter(contains_square, boxes))


puzzle = [
    [8, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 3, 6, 0, 0, 0, 0, 0],
    [0, 7, 0, 0, 9, 0, 2, 0, 0],
    [0, 5, 0, 0, 0, 7, 0, 0, 0],
    [0, 0, 0, 0, 4, 5, 7, 0, 0],
    [0, 0, 0, 1, 0, 0, 0, 3, 0],
    [0, 0, 1, 0, 0, 0, 0, 6, 8],
    [0, 0, 8, 5, 0, 0, 0, 1, 0],
    [0, 9, 0, 0, 0, 0, 4, 0, 0]
]


if __name__ == "__main__":
    def print_grid(grid):
        return "\n".join(" ".join(map(str, row)) for row in grid)
    print(next(map(print_grid, solve(puzzle)), "No solution found"))
