import sys
import getopt
import logging


class BinaryManip:
    og_list = []
    filename = ""
    logger = ""
    oxygenratList = []

    def __init__(self, logger, filename):
        self.filename = filename
        self.logger = logger
        self.readFile()

    def readFile(self):
        # read list into list
        with open(self.filename) as f:
            for line in f:
                self.og_list.append(line[:-1])
                # self.logger.debug(f"Appending: {line}")
        # self.printList(self.og_list, "First")

    def calculateMCV(self, pos, list):
        # calculate most common binary value at pos
        mcv = 0
        for val in list:
            # logger.debug(f"val:{val}")
            bit = val[pos]
            # logger.debug (f"val[{pos}]: {bit}")
            if bit == '1':
                mcv += 1
            else:
                mcv -= 1
        self.logger.debug(f"mcv:{mcv}")
        return "1" if (mcv >= 0) else "0"

    def removeVals(self, matchVal, pos):
        # remove values from the list that don't match
        self.oxygenratList = [x for x in self.oxygenratList if x[pos] == matchVal]

    def printList(self, list, id):
        self.logger.debug(f"start: {id}")
        if list is not None:
            for val in list:
                self.logger.debug(f"{val}")
        self.logger.debug(f"end:   {id}")

    def FindSingVal(self, OxGenRating):
        pos = 0
        self.oxygenratList = self.og_list
        line_len = len(self.og_list[0])
        while pos < line_len and \
                self.oxygenratList is not None and \
                len(self.oxygenratList) > 1:
            mcv = self.calculateMCV(pos, self.oxygenratList)
            if not OxGenRating:
                mcv = "0" if (mcv == "1") else "1"
            self.logger.debug(f"pos:{pos}, mcv:{mcv}, OxGenRating:{OxGenRating}")
            self.printList(self.oxygenratList, "--Before--")
            self.removeVals(mcv, pos)
            self.printList(self.oxygenratList, "--After--")
            pos += 1
        self.logger.debug(f"pos:{pos},len(oxygenratList):{len(self.oxygenratList)}")
        return int(self.oxygenratList[0], 2)


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
    stream_handler.setLevel(logging.INFO)
    logger.addHandler(stream_handler)
    logger.debug(f"Input file is {inputfile}")
    logger.debug(f"Output file is {outputfile}")

    binmip = BinaryManip(logger, inputfile)
    OxyGen = binmip.FindSingVal(True)
    CO2 = binmip.FindSingVal(False)
    logger.info(f"OxyGen:{OxyGen}, CO2:{CO2}, Combined: {OxyGen*CO2}")


if __name__ == "__main__":
    main(sys.argv[1:])
