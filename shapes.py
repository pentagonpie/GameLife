from framework import cell
import random


def gliderGun():
    cells = []
    cells.append(cell(17, 2))
    cells.append(cell(17, 1))
    cells.append(cell(16, 2))
    cells.append(cell(16, 1))

    cells.append(cell(-17, 1))
    cells.append(cell(-17, 0))
    cells.append(cell(-18, 1))
    cells.append(cell(-18, 0))

    cells.append(cell(6, 3))
    cells.append(cell(6, 4))
    cells.append(cell(6, -1))
    cells.append(cell(6, -2))
    cells.append(cell(4, 3))
    cells.append(cell(4, -1))

    cells.append(cell(3, 2))
    cells.append(cell(3, 1))
    cells.append(cell(3, 0))
    cells.append(cell(2, 2))
    cells.append(cell(2, 1))
    cells.append(cell(2, 0))

    cells.append(cell(-1, -1))
    cells.append(cell(-2, 0))
    cells.append(cell(-2, -1))
    cells.append(cell(-2, -2))
    cells.append(cell(-3, 1))
    cells.append(cell(-3, -3))
    cells.append(cell(-4, -1))
    cells.append(cell(-5, 2))
    cells.append(cell(-5, -4))
    cells.append(cell(-6, 2))
    cells.append(cell(-6, -4))
    cells.append(cell(-7, 1))
    cells.append(cell(-7, -3))
    cells.append(cell(-8, 0))
    cells.append(cell(-8, -1))
    cells.append(cell(-8, -2))
    return cells


def getRandomCells():
    limit = 27
    cells = []
    for x in range(400):
        x = random.choice(range(-limit, limit))
        y = random.choice(range(-limit, limit))
        cells.append(cell(x, y))
        # print("created random cell {},{}".format(x,y))

    return cells