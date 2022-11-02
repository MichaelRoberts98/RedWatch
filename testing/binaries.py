import os
import sys
import shutil

# total arguments
arglen = len(sys.argv)
#print("Total arguments passed:", arglen)

# Arguments passed
#print("\nArguments passed:", end = " ")
#for i in range(1, arglen):
#	print(sys.argv[i], end = " ")

#mv function - could also use os.rename/replace
if sys.argv[1] == "mv":
	shutil.move(sys.argv[2], sys.argv[3])

if sys.argv[1] == "cp":
	shutil.copy(sys.argv[2], sys.argv[3])

# Addition of numbers
#Sum = 0
# Using argparse module
#for i in range(1, arglen):
#	Sum += int(sys.argv[i])

#print("\n\nResult:", Sum)


#os.replace('test.txt','test2.txt')

