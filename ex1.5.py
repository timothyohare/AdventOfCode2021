import sys, getopt

def readFile(fileName: str):
  cnt_increments = 0
  triplets = []
  with open(fileName) as f:
    a = f.readline()
    b = f.readline()
    c = f.readline()
    try:
        triplets.append(int(a) + int(b) + int(c))
    except ValueError:
        print("Ignoring: ", a,b,c)
    a = b
    b = c

    for line in f:
        c = line
        try:
            triplets.append(int(a) + int(b) + int(c))
        except ValueError:
          print("Ignoring: ", a,b,c)
          continue
        a = b
        b = c
        if triplets[-1] > triplets[-2]:
          cnt_increments += 1
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
