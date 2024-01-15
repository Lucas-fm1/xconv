# =============================================================
# ||  PROGRAM:  full_conv                                   ||
# ||  AUTHOR:   Lucas Farias Martins                        ||
# ||  EMAIL:    lucas.martins@embedded.ufcg.edu.br          ||
# ||  PORPOUSE: Gather all the methods needed to do         ||
# ||            the convoluiton algorithm                   ||
# ||--------------------------------------------------------||
# ||  VERSION: 0.1 (First compiling)                        ||
# ||--------------------------------------------------------||
# ||  UPDATE: 2022-07-06                                    ||
# =============================================================

import numpy as np

# -------------------------------------------------------------
# 					      Read & index
# -------------------------------------------------------------
def read_idx(image):
	# _____________________________________________
	# _________________ VARIABLES _________________ 
	file1 = open('index.txt', 'r')
	image = image.getT()
	volu  = np.array([])
	# _____________________________________________
	# _______________READ INDEX FILE_______________ 
	while True:
		line = file1.readline()
		if not line:
			break
		elmt = image[int(line)]
		volu = np.append(volu, elmt)
	file1.close()
	volu = np.matrix(volu)

	return volu
# -------------------------------------------------------------
# 					 	     Unit
# -------------------------------------------------------------
def unit(image,kern):
    # _____________________________________________
    # ________________ TRANSPOSE __________________ 
    image = image.getT()
    kern  = kern.getT()
    # _____________________________________________
    # ________________MULT AND ADD_________________ 
    summ = 0
    for m in range(kern.size):
        prod = image[m] * kern[m]
        summ = summ + prod

    return summ

#---------------------------------------------------
#    	 		   THE TESTATION		
#---------------------------------------------------


#--------------------------------- INPUT IMAGE
image = np.matrix([[1,1,1,0,0],
                   [0,1,1,1,0],
                   [0,0,1,1,1],
                   [0,0,1,1,0],
                   [0,1,1,0,0]])
#-------------------------------------- KERNEL
kern = np.matrix([[1,0,1],
                  [0,1,0],
                  [1,0,1]])

#-------------------------------------- OUTPUT
outp = np.array([])
stride = 1
rout_size = int((image.shape[0] - kern.shape[0] + 1)/stride)
cout_size = int((image.shape[1] - kern.shape[1] + 1)/stride)
outp_size = int(rout_size * cout_size)

# ks = kern.shape[0]
# ts = kern.shape[0] * kern.size

# ------------------------------------ FLATTEN
image = image.ravel()
kern = kern.ravel()

# ------------------------------- READY SET GO
volu = read_idx(image)
volu = np.reshape(volu, (kern.size,kern.size))
print("\nvolume (tensor, matrizes linearizadas) =\n",volu,"\n")

for m in range(outp_size):
	outm = unit(volu[m],kern)
	outp = np.append(outp, [outm])

outp = np.reshape(outp, (rout_size,cout_size))
print("\noutput =\n",outp,"\n")