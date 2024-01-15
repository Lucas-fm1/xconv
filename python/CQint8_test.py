
import numpy as np 
import conv_features as cf

#===================================================
#			  		 PARAMETERS
#===================================================

x_inpt = 5;		x_kern = 3;
y_inpt = 5;		y_kern = 3; 		stride = 1;

#===================================================
#			  		RESET VALUES
#===================================================

addr_mem = 0;	addr_conv = 0
cnt_OC 	 = 0;	cnt_KC    = 0
cnt_IR   = 0;	cnt_BYTE  = 0
cnt_str  = 0 

image = np.array([ [0],  [1],  [2],  [3],  [4],
	               [5],  [6],  [7],  [8],  [9],
	              [10], [11], [12], [13], [14],
	              [15], [16], [17], [18], [19],
	              [20], [21], [22], [23], [24]])

kern = np.array([ [1], [0], [1],
	              [0], [1], [0],
	              [1], [0], [1]])

out = np.array([])
#===================================================
#    	 		 FUNTION DEFINITION
#===================================================

def cqint8_model(image, kern, out, x_inpt, y_inpt, x_kern, y_kern, stride):
	# _____________________________________________
	# _________________ VARIABLES _________________ 

	cnt_OC = 0;		addr_conv = cnt_OC   
	cnt_IR = 0;		cnt_KC = 0

	jan = np.zeros(x_kern*y_kern)

	x_size = int((x_inpt - x_kern + 1)/stride)
	y_size = int((y_inpt - y_kern + 1)/stride)
	kern_size = x_kern * y_kern
	inpt_size = x_inpt * y_inpt
	outp_size = int(x_size * y_size)
	# _____________________________________________
	# _________________ CONVOLVE __________________ 

	while (cnt_OC < x_size): # __________ LOOP DE CNT_OC _______ 

		while (cnt_IR < y_inpt): # ______ LOOP DE CNT_IR _______
			# _________________________________________________________
    		# ________________ JANELAS VÁLIDAS & UNIT__________________
			jan, out = valid_window(jan, kern, out, addr_conv, cnt_IR, cnt_KC, 
					                cnt_OC, x_kern, y_kern)
			# _________________________________________________________
    		# ________ ATUALIZAR CONTADORES DE LINHA/COLUNA ___________ 
			if (cnt_KC == x_kern - 1):
				addr_conv = addr_conv + x_inpt - x_kern + 1 
				cnt_KC = 0
				cnt_IR += 1
			else:
				addr_conv = addr_conv + 1
				cnt_KC += 1
		# __________________________________________________________
    	# ________ ATUALIZAR CONTADOR DE COLUNA DA SAIDA ___________ 
		cnt_OC   += 1
		cnt_IR    = 0
		addr_conv = cnt_OC
	# __________________________________________________________
    # ________ LOOP ENCERRADO, PEGA ULTIMO ELEMENTO ____________ 
	summ = unit(jan, kern)
	out = np.append(out, summ)
	out = np.reshape(out, (x_size,y_size)); out = np.matrix(out, dtype=int)
	out = out.getT()
	print("\noutput =\n", out,"\n")

def valid_window(jan, kern, out, addr_conv, cnt_IR, cnt_KC, cnt_OC, x_kern, y_kern):
	if(cnt_IR > y_kern-1 or cnt_IR == 0 and cnt_OC != 0):
		if(cnt_KC == 0) and (cnt_IR > x_kern-1 or cnt_IR == 0):
			win = np.reshape(jan, (3,3)); win = np.matrix(win, dtype=int)
			print("\njan =\n", win.getT(),"\n"); 
			summ = unit(jan, kern)
			out  = np.append(out, int(summ))
	jan = np.roll(jan, -1)
	jan[x_kern*y_kern - 1] = image[addr_conv]
	
	return jan, out

def unit(jan,kern): 
    summ = 0
    for m in range(kern.size):
        prod = jan[m] * kern[m]
        summ = summ + prod
    return summ

# ====================================================
#    			 	TEST WORKSPACE
# ====================================================

#print ("\n")
#print ("      CCCCC   OOOO   N    N  V       V     ") 
#print ("     CC	     O    O  NN   N   V     V      ")
#print ("     CC      O    O  N N  N    V   V       ")
#print ("     CC      O    O  N  N N     V V        ")
#print ("      CCCCC   OOOO   N   NN      V         ")
print ("    ===================================    ")
print ("          Image size:  (",x_inpt,",",y_inpt,")")
print ("          Kernel size: (",x_kern,",",y_kern,")")
print ("    ===================================  \n")

#np.set_printoptions(formatter={'int':hex})

print("\ninput image =\n", np.reshape(image, (x_inpt,y_inpt)), 
	  "\n\nkernel (filter) =\n", np.reshape(kern, (x_kern,y_kern)))

cqint8_model(image, kern, out, x_inpt, y_inpt, x_kern, y_kern, stride)
