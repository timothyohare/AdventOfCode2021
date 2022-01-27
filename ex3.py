import sys, getopt, re

def readFile(fileName: str):
  count_of_ones_zeros = {}
  with open(fileName) as f:
    for line in f:
      pos = 0
      print("Line:", line, end=" ")
      for bit in line:
        print (f"Pos:{pos}, bit:{bit}", end=" ")
        if bit == '1':
            print("bit 1", end=" ")
            if pos in count_of_ones_zeros:
                curr_1_count = count_of_ones_zeros[pos]
                print("curr1count:", curr_1_count)
                #count_of_ones_zeros[pos].update(curr_1_count + 1)
                count_of_ones_zeros[pos] = curr_1_count + 1
                #if 1 in count_of_ones_zeros[pos]:
                #    curr_1_count = count_of_ones_zeros[pos][1]
                #    count_of_ones_zeros[pos][1].update(curr_1_count + 1)
                #else:
                #    count_of_ones_zeros[pos][1] = 1
            else:
                #count_of_ones_zeros[pos] = {}
                print(f"init[{pos}] with 1")
                count_of_ones_zeros[pos] = 1
                #count_of_ones_zeros[pos][1] = 1
        elif bit == '0':
            print("bit 0", end=" ")
            if pos in count_of_ones_zeros:
                curr_1_count = count_of_ones_zeros[pos]
                print("curr0count:", curr_1_count)
                #count_of_ones_zeros[pos].update(curr_0_count - 1)
                count_of_ones_zeros[pos]= curr_1_count - 1
                #if 0 in count_of_ones_zeros[pos]:
                #    curr_0_count = count_of_ones_zeros[pos][0]
                #    count_of_ones_zeros[pos][0].update(curr_0_count + 1)
                #else:
                #    count_of_ones_zeros[pos][0] = 1
            else:
                count_of_ones_zeros[pos] = -1
                print(f"init[{pos}]] with -1")
                #count_of_ones_zeros[pos][0] = 1

        else:
            print ( "Ekk: ", bit)
        pos = pos + 1   
  print ('count_of_ones_zeros: ',count_of_ones_zeros)
  gamma = []
  epsilon = []
  for key,val in count_of_ones_zeros:
      if val > 0:
        gamma[key] = 1
        epsilon[key] = 0
      elif val < 0:
        gamma[key] = 0
        epsilon[key] = 1
      else:
        print("not +ve / -ve")
        gamma[key] = 0
        epsilon[key] = 0
  print(f"gamma:{gamma}, epsilon:{epsilon}")


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
