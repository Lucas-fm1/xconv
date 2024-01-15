import numpy as np

#---------------------------------------------------
#    	 		 FUNTION DEFINITION
#---------------------------------------------------

def conv_mult(image,kern,outp):
	# _____________________________________________
	# _________________ VARIABLES _________________ 
	file1 = open('index_3x3.txt', 'r')
	count = 0
	volu  = np.array([])
	# _____________________________________________
	# _______________READ INDEX FILE_______________ 
	while True:
		count += 1
		line = file1.readline()
		if not line:
			break
		elmt = image[int(line)]
		volu = np.append(volu, elmt)
	file1.close()
	# _____________________________________________
	# _________________ TRANSPOSE _________________ 
	volu = np.matrix(volu);
	volu = volu.getT()
	# _____________________________________________
	# ________________MULT AND ADD_________________ 
	x = 0
	while (x < volu.size):
		wind = np.matrix(volu[x:x+4])
		summ = 0
		for m in range(ks):
			prod = wind[m] * kern[m]
			summ = summ + prod

		outp = np.append(outp, summ)
		x += kern.size
		return outp

#---------------------------------------------------
#    	 		   THE TESTATION		
#---------------------------------------------------

outp = np.array([])

#------ INPUT IMAGE -------
image = np.matrix([[1,0,0],
                   [0,1,0],
                   [0,0,1]])

#--------- KERNEL ---------
kern = np.matrix([[2,2],
	              [2,2]])
ks = kern.size
print("\nkern size =",ks,"\n")

#-------------------------------------
#    	  TRANSPOSE MATRICES
#-------------------------------------

image = image.flatten()
kern  = kern.flatten()
image = image.getT();
kern  = kern.getT();

outp = conv_mult(image, kern, outp);

outp = outp.reshape(2,2)
print("\noutp = \n",outp,"\n")
