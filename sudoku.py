from itertools import chain
from math import sqrt, ceil

permittedValues = set(range(1, 10))
emptySquare = 0
gridSize = len(permittedValues)


def calcBoxSize():
    squareRoot = sqrt(gridSize)
    cols = next(n for n in range(ceil(squareRoot), gridSize + 1)
                if gridSize % n == 0)
    return (gridSize // cols, cols)


def calcBoxes():
    boxRows, boxCols = calcBoxSize()
    boxTopCorners = ((row, col) for row in range(0, gridSize, boxRows)
                     for col in range(0, gridSize, boxCols))
    return [((topRow, leftCol), (topRow + boxRows, leftCol + boxCols))
            for topRow, leftCol in boxTopCorners]


boxes = calcBoxes()


def solve(grid):
    try:
        return(s for s in solveAt(grid, next(emptySquares(grid))))
    except StopIteration:
        return (g for g in (grid,))


def emptySquares(grid):
    return ((row, col)
            for row, values in enumerate(grid)
            for col, value in enumerate(values)
            if value == emptySquare)


def solveAt(grid, square):
    return (s for value in allowedValues(grid, square)
            for s in solve(setValueAt(grid, square, value)))


def setValueAt(grid, square, value):
    row, col = square
    newRow = replaceValueAt(grid[row], col, value)
    return replaceValueAt(grid, row, newRow)


def replaceValueAt(lst, index, value):
    return [value if i == index else v for i, v in enumerate(lst)]


def allowedValues(grid, square):
    row, col = square
    blockedValues = set(chain(
        rowValues(grid, row),
        colValues(grid, col),
        boxValues(grid, boxContaining(square))
    ))
    return (v for v in permittedValues.difference(blockedValues))


def rowValues(grid, row):
    return (n for n in grid[row] if n != emptySquare)


def colValues(grid, col):
    return (n for n in (row[col] for row in grid) if n != emptySquare)


def boxValues(grid, box):
    (topRow, leftCol), (bottomRow, rightCol) = box
    boxRows = (r[leftCol:rightCol] for r in grid[topRow:bottomRow])
    return (n for n in chain(*boxRows) if n != emptySquare)


def boxContaining(square):
    row, col = square
    def squareIn(box):
        (topRow, leftCol), (bottomRow, rightCol) = box
        return row in range(topRow, bottomRow) and col in range(leftCol, rightCol)
    return next(box for box in boxes if squareIn(box))


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
    print(next(solve(puzzle), "No solutions found"))
