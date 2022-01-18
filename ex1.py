import sys, getopt

def readFile(fileName: str):
  previous = 0
  cnt_increments = 0
  with open(fileName) as f:
    line = f.readline()
    previous = int(line)
    #print(previous)
    for line in f:
        #print(line)
        #exit(0)
        try:
          val = int(line)
        except ValueError:
          print("Ignoring: ", line)
          continue 
        if val > previous:
          cnt_increments += 1
        previous = val
  print(cnt_increments)

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
   print ('Input file is "', inputfile)
   print ('Output file is "', outputfile)
   readFile(inputfile)

if __name__ == "__main__":
    main(sys.argv[1:])
