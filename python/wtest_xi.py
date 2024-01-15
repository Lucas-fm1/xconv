import numpy as np

class bcolors:
    HEADER  = '\033[95m'
    OKBLUE  = '\033[94m'
    OKCYAN  = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL    = '\033[91m'
    ENDC    = '\033[0m'
    BOLD    = '\033[1m'
    UNDERLINE = '\033[4m'

num_tests = 40

for x_i in range(num_tests+1):
	if(x_i > 0):
		w  = x_i/4;
		w4 = 0
		while w4 < x_i:
			w4 += 4
			if w4 + 4 > x_i:
				break

		if((x_i+1)%4 == True):
			print(bcolors.OKGREEN,"x_i = ","{0:02d}".format(x_i),
						   "(","{0:06b}".format(x_i),")",
						   "\t w =", w,
						   "\t w4 =",w4, bcolors.ENDC)
		else:
			print(" x_i = ","{0:02d}".format(x_i),
						   "(","{0:06b}".format(x_i),")",
						   "\t w =", w,
						   "\t w4 =",w4)
