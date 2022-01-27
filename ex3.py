import sys, getopt, re
import logging

def readFile(logger, fileName: str):
  count_of_ones_zeros = {}
  with open(fileName) as f:
    for line in f:
      pos = 0
      #logger.debug(f"Line:{line}")
      for bit in line:
        logger.debug (f"Pos:{pos}, bit:{bit}")
        if bit == '1':
            if pos in count_of_ones_zeros:
                curr_1_count = count_of_ones_zeros[pos]
                count_of_ones_zeros[pos] = curr_1_count + 1
            else:
                logger.debug(f"init[{pos}] with 1")
                count_of_ones_zeros[pos] = 1
        elif bit == '0':
            logger.debug("bit 0")
            if pos in count_of_ones_zeros:
                curr_1_count = count_of_ones_zeros[pos]
                count_of_ones_zeros[pos]= curr_1_count - 1
            else:
                count_of_ones_zeros[pos] = -1
                logger.debug(f"init[{pos}]] with -1")
        pos = pos + 1   
  #print ('count_of_ones_zeros: ',count_of_ones_zeros)
  gamma = ""
  epsilon = ""
  for key,val in count_of_ones_zeros.items():
      if val > 0:
        gamma += '1'
        epsilon += '0'
      elif val < 0:
        gamma += '0'
        epsilon += '1'
      else:
        print("not +ve / -ve")
        gamma += '0'
        epsilon += '1'
  gamma_int = int(gamma, 2)
  epsilon_int = int(epsilon,2)
  logger.info(f"gamma:{gamma}, {gamma_int}, epsilon:{epsilon}, {epsilon_int}")
  logger.info(f"Power consumption: {gamma_int*epsilon_int}")

def main(argv):
   inputfile = ''
   outputfile = ''
   try:
      opts, args = getopt.getopt(argv,"hi:o:",["ifile=","ofile="])
   except getopt.GetoptError:
      print ('test.py -i <inputfile> -o <outputfile>')
      sys.exit(2)
   for opt, arg in opts:
      if opt == '-h':
         print ('test.py -i <inputfile> -o <outputfile>')
         sys.exit()
      elif opt in ("-i", "--ifile"):
         inputfile = arg
      elif opt in ("-o", "--ofile"):
         outputfile = arg
   logger = logging.getLogger("Basic logger")
   logger.setLevel(logging.INFO)
   stream_handler = logging.StreamHandler()
   stream_handler.setLevel(logging.INFO)
   logger.addHandler(stream_handler)
   logger.debug(f"Input file is {inputfile}")
   logger.debug(f"Output file is {outputfile}")
   readFile(logger, inputfile)

if __name__ == "__main__":
    main(sys.argv[1:])
