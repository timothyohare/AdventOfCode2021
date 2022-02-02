
import sys
import getopt
import logging


class BingoCell:
    # want to know what the value is, and if it has been marked
    logger = ""

    def __init__(self, logger, val):
        self.logger = logger
        self.val = val
        self.marked = False

    def print(self):
        mark = 'f' if not self.marked else 't'
        self.logger.debug(f"{self.val},{mark} ")


class BingoRow:
    logger = ""

    def __init__(self, logger, row):
        self.logger = logger
        self.bingoCell = []
        # self.logger.debug(f"BingoRow: rowlen {len(row)}\n")
        for num in row:
            d = BingoCell(logger, num)
            # self.logger.debug(f"creating cell {num}, ")
            self.bingoCell.append(d)
        # self.logger.debug(f"after create: bingocell count {len(self.bingoCell)}")

    def print(self):
        # self.logger.debug(f"bingoCell count: {len(self.bingoCell)}\n")
        for cell in self.bingoCell:
            cell.print()
        self.logger.debug('\n')

    def setMarked(self, picked: int) -> bool:
        for cell in self.bingoCell:
            if cell.val == picked:
                cell.marked = True
                return True
        return False

    def isWinner(self, picked) -> bool:
        rowContainsPicked = False
        for cell in self.bingoCell:
            if not cell.marked:
                return False
            if picked == cell.val:
                rowContainsPicked = True
        return True if rowContainsPicked else False

    def sumUnmarked(self) -> int:
        sumUnmarked = 0
        for cell in self.bingoCell:
            if not cell.marked:
                sumUnmarked += cell.val
        return sumUnmarked


class BingoBoard:
    logger = ""

    def __init__(self, logger, id):
        self.logger = logger
        # self.logger.debug("Init Bingoboard\n")
        self.bingoRow = []
        self.boardId = id
        self.hasWon = False

    def update(self, row_num, row):
        # self.logger.debug(f"row_num: {row_num}, row: {row}, bingoRow len:{len(self.bingoRow)}\n")
        t = BingoRow(self.logger, row)
        # self.logger.debug(f"BingoRow - t: {t}")
        # self.bingoRow.append(BingoRow(self.logger, row))
        self.bingoRow.append(t)
        # self.logger.debug(f"After update: bingoRow cnt: {len(self.bingoRow)}")

    def print(self):
        for row in self.bingoRow:
            row.print()
        # self.logger.info('finshed board print\n')

    def setMarked(self, picked: int) -> bool:
        for row in self.bingoRow:
            if row.setMarked(picked):
                return True
        return False

    def isWinner(self, picked):
        row_cnt = 0
        for row in self.bingoRow:
            if row.isWinner(picked):
                self.logger.info(f"Row {row_cnt} is the winner\n")
                row.print()
                self.hasWon = True
                return True
            row_cnt += 1
        # check vertical rows
        for i in range(0, 5):
            if picked == 13:
                self.logger.info(f"Vertical row at {i} with picked 13, with " )
                for j in range(0, 5):
                    self.logger.info(f"{self.bingoRow[j].bingoCell[i].val},{self.bingoRow[j].bingoCell[i].marked}\n")
            pickedInRow = self.bingoRow[0].bingoCell[i].val == picked or \
                self.bingoRow[1].bingoCell[i].val == picked or \
                self.bingoRow[2].bingoCell[i].val == picked or \
                self.bingoRow[3].bingoCell[i].val == picked or \
                self.bingoRow[4].bingoCell[i].val == picked
            if pickedInRow:
                allMarked = self.bingoRow[0].bingoCell[i].marked and \
                    self.bingoRow[1].bingoCell[i].marked and \
                    self.bingoRow[2].bingoCell[i].marked and \
                    self.bingoRow[3].bingoCell[i].marked and \
                    self.bingoRow[4].bingoCell[i].marked
                if allMarked:
                    self.logger.info(f"Vertical row at {i} is the winner, with {self.bingoRow[0].bingoCell[i].val}, "\
                                     f"{self.bingoRow[1].bingoCell[i].val}, {self.bingoRow[2].bingoCell[i].val}," \
                                     f"{self.bingoRow[3].bingoCell[i].val}, {self.bingoRow[4].bingoCell[i].val}\n")
                    self.hasWon = True
                    return True
        return False

    def winningScore(self, picked: int) -> int:
        sumUnmarked = 0
        for row in self.bingoRow:
            sumUnmarked += row.sumUnmarked()
        total = sumUnmarked * picked
        self.logger.debug(f"Sum unmarked {sumUnmarked} * picked {picked} = {total}\n")
        return total


    # want to store BingoCells in 5x5 matrix
    # want to know if all numbers on a vertical or horizontal line
    #  have all been marked
    # want to know if a number is on a board, and
    #  if so, then to mark it as picked, and
    #  check if the horizontal or vertical row is all
    #  selected (separate function but has to be run after each number)
    # want to know if any vert col or hori row is all picked
    # want to know if one specifc set of numbers are all picked
    # sum of all unmarked numbers on the board
    # w ,h = 5, 5
    # bingoBoard = [[0 for x in range(w)] for y in range(h)]


class Bingo:

    def __init__(self, logger, filename):
        self.filename = filename
        self.logger = logger
        self.markedNumbers = []
        self.bingoBoards = []
        # self.logger.debug(f"1:marketNum len; {len(self.markedNumbers)}, {len(self.bingoBoards)} \n")
        self.readFile()

    def readFile(self):
        # self.logger.debug(f"marketNum len; {len(self.markedNumbers)}, {len(self.bingoBoards)} \n")
        with open(self.filename) as f:
            line = f.readline()

            # first line is list of marked numbers
            line_list = line.split(',')
            map_obj = map(int, line_list)
            self.markedNumbers = list(map_obj)
            self.logger.debug(self.markedNumbers)
            f.readline()  # blank

            # start reading the bingo boards
            line = f.readline()
            board = 0
            while (line != ""):
                # match 5 rows of 5 numbers
                m = BingoBoard(self.logger, board)
                self.bingoBoards.append(m)
                # self.logger.debug(f"bingoBoards len:{len(self.bingoBoards)}\n")
                for row in range(5):
                    line_list1 = line.split()
                    map_obj1 = map(int, line_list1)
                    bingoBoardRow = list(map_obj1)
                    # self.logger.debug(f"before_update: {row}, board:{board}, {bingoBoardRow}\n")
                    self.bingoBoards[board].update(row, bingoBoardRow)
                    line = f.readline()
                self.logger.debug(f"Printing board {board}\n")
                self.bingoBoards[board].print()
                board += 1
                line = f.readline()

    def checkPicked(self, picked) -> bool:
        foundWinner = False
        for board in self.bingoBoards:
            if not board.hasWon and board.setMarked(picked):
                if board.isWinner(picked):
                    self.logger.info(f"Board {board.boardId} winner winner chicken dinner.\n")
                    self.winningScore = board.winningScore(picked)
                    foundWinner = True
        return foundWinner

    def playGame(self):
        # iterate through the numbers
        # for each number interate through the boards
        # if the number is on the board, mark it as picked
        # check if that board has won
        # if board has won calculate final score
        #   (sum of unmarked numbers * number just called)
        for picked in self.markedNumbers:
            self.logger.info(f"Picked {picked}\n")
            if self.checkPicked(picked):
                pass

def main(argv):
    inputfile = ''
    outputfile = ''
    try:
        opts, args = getopt.getopt(argv, "hi:o:", ["ifile=", "ofile="])
    except getopt.GetoptError:
        print('test.py -i <inputfile> -o <outputfile>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('test.py -i <inputfile> -o <outputfile>')
            sys.exit()
        elif opt in ("-i", "--ifile"):
            inputfile = arg
        elif opt in ("-o", "--ofile"):
            outputfile = arg
    logger = logging.getLogger("Basic logger")
    logger.setLevel(logging.DEBUG)
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.DEBUG)
    stream_handler.terminator = ""
    logger.addHandler(stream_handler)
    logger.debug(f"Input file is {inputfile}")
    logger.debug(f"Output file is {outputfile}")

    bingo = Bingo(logger, inputfile)
    output = bingo.playGame()
    logger.info(f"Returned {output},{bingo.winningScore}\n")


if __name__ == "__main__":
    main(sys.argv[1:])
