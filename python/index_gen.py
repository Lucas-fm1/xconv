
import numpy as np

#===================================================
#			  SET THE VALUES FOR TEST
#===================================================

print("\n") # to beginning a more friendly human-machine interface

# ------------------------ INPUT and KERNEL
x_inpt = 5;		x_kern = 3
y_inpt = 5;		y_kern = 3

print("  =============================  ")
print("      Image size:  (",x_inpt,",",y_inpt,")")
print("      Kernel size: (",x_kern,",",y_kern,")")
print("  =============================  \n")

stride = 1 # ------------- STRIDE	

#===================================================
#    	 		 FUNTION DEFINITION
#===================================================

def windowing(x_inpt, y_inpt, x_kern, y_kern, stride):
	# _____________________________________________
	# _________________ VARIABLES _________________ 

	cnt_OC = 0;		idx = cnt_OC   
	cnt_IR = 0;		cnt_KC = 0
	jan = np.array([])

	x_size = (x_inpt - x_kern + 1)/stride
	y_size = (y_inpt - y_kern + 1)/stride
	kern_size = x_kern * y_kern
	inpt_size = x_inpt * y_inpt
	outp_size = int(x_size * y_size)
	# _____________________________________________
	# _________________ CONVOLVE __________________ 

	with open('index.txt','a') as f:

		while (cnt_OC < x_size):

			while (cnt_IR < y_inpt):

				# ------------ IDENTIFICAR JANELAS VÁLIDAS ------------
				if (len(jan) == x_kern*y_kern):
					if(cnt_KC == 0) and (cnt_IR > x_kern-1 or cnt_IR == 0):
						jan = np.reshape(jan, (x_kern,y_kern))
						print("index window =\n", jan,"\n")
						jan = np.reshape(jan, (x_kern*y_kern,1))
					jan = np.roll(jan, -1)
					jan[x_kern*y_kern - 1] = idx
				else:
					jan = np.append(jan, [idx])

				# -------- ATUALIZAR CONTADORES DE LINHA/COLUNA --------
				f.write(str(idx)+'\t')
				if (cnt_KC == x_kern - 1):
					idx    = idx + x_inpt - x_kern + 1 
					cnt_KC = 0
					cnt_IR += 1
					f.write('\n')
				else:
					idx = idx + 1
					cnt_KC += 1
				#-----------------------------------#

			f.write('\n\n')
			cnt_OC += 1
			if(cnt_OC == x_inpt - x_kern + 1):
				cnt_KC = x_kern - 1
			else:
				cnt_KC = 0
				cnt_IR = 0
			idx = cnt_OC

	jan = np.reshape(jan, (x_kern,y_kern))
	print("last one =\n", jan,"\n")

"""# ------------ IDENTIFICAR JANELAS VÁLIDAS ------------
def valid_window(jan, cnt_KC, cnt_IR, x_kern, y_kern, idx):
	if (len(jan) == x_kern*y_kern):
		if(cnt_KC == 0) and (cnt_IR > x_kern-1 or cnt_IR == 0):
				jan = np.reshape(jan, (x_kern,y_kern))
				print("janela =\n", jan,"\n")
				jan = np.reshape(jan, (x_kern*y_kern,1))
			jan = np.roll(jan, -1)
			jan[x_kern*y_kern - 1] = idx
		else:
			jan = np.append(jan, [idx])
"""

# ===================================================
#				   Functions calls
# ===================================================

windowing(x_inpt, y_inpt, x_kern, y_kern, stride)