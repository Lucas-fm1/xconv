import numpy as np

#---------------------------------------------------
#               FUNTIONS DEFINITIONS
#---------------------------------------------------

def unit(image,kern):
    # _____________________________________________
    # _________________ FLATTEN ___________________ 
    image = image.flatten(); image = image.getT()
    kern  = kern.flatten();  kern  = kern.getT()
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

outp = np.array([])

#------ INPUT IMAGE -------
image = np.matrix([[0,1,1],
                   [0,0,1],
                   [0,0,1]])

#--------- KERNEL ---------
kern = np.matrix([[1,0,1],
                  [0,1,0],
                  [1,0,1]])

print("\nkern size =",kern.size,"\n")

outp = unit(image,kern)
print("\nout =\n",outp,"\n")