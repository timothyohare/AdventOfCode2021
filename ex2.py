import sys, getopt, re

def readFile(fileName: str):
  hori_pos = 0
  depth = 0
  patterns = [r'forward (\d+)', r'up (\d+)', r'down (\d+)']
  with open(fileName) as f:
    for line in f:
        match = re.match(r'forward (\d+)', line)
        if match:
            hori_pos += int(match.group(1))
            continue
        match = re.match(r'up (\d+)', line)
        if match:
            depth -= int(match.group(1))
            continue
        match = re.match(r'down (\d+)', line)
        if match:
            depth += int(match.group(1))
            continue
  print ('hori: ', hori_pos, ', depth: ', depth, 'total:', hori_pos*depth)


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
