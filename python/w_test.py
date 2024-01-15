import numpy as np

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

num_tests = 40

for x_k in range(num_tests+1):
	if(x_k > 0):
		w  = x_k/4;
		w4 = 0
		while w4 < x_k:
			w4 += 4

		if((x_k+1)%4 == True):
			print(bcolors.OKGREEN,"x_k = ","{0:02d}".format(x_k),
						   "(","{0:06b}".format(x_k),")",
						   "\t w =", w,
						   "\t 4w =",w4, bcolors.ENDC)
		else:
			print(" x_k = ","{0:02d}".format(x_k),
						   "(","{0:06b}".format(x_k),")",
						   "\t w =", w,
						   "\t w4 =",w4)
