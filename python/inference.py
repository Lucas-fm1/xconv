#""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""#
#                                                                    #
#                         INFERENCE MODEL                            #
#   Class to calculate inference part of a machine learning model    #
#                                                                    #
#____________________________________________________________________#

import numpy as np

class Inference(object):

# ======================= INITIALIZE =========================

	def __init__(self, input_size, input_data, act_type, layer_type, n_of_layers):
		
		self.input_data  = np.reshape(input_data, (input_size, 1))
		self.act_type 	 = act_type
		self.layer_type  = layer_type
		self.n_of_layers = n_of_layers

		
		self.layer_multiplier = 0

	# ------------ Checks the max layer ------------
		f_sizes = open('files/sizes.txt', 'r')
		sizes 	= [0]*(n_of_layers*2)

		for line, i in zip(f_sizes, range(len(sizes))):
			sizes[i] = int(line)

		max_weights_r = max(sizes[::2])
		max_weights_c = max(sizes[1::2])

		self.weights = np.zeros((max_weights_r, max_weights_c))
		self.biases  = np.zeros((max_weights_r, 1))
		
# ======================== QUANTIZER ===========================

	def quantize_layer(self, layer, scale, zero_point):
		quantized_layer = np.round((layer/scale) + zero_point)
		return quantized_layer.astype('int8')

# ====================== M-EVALUATION ==========================

	def calculate_M(self, n, su, sw, so):

		M 			 = sw*su/so
		M_0 		 = np.round(M * 2**(n-1))
		M_normalized = M_0 / 2**(n-1)
		
		return M_normalized

# ===================== MULTIPLICATION =========================

	def multiplicate(self, inputs, weights, bias, su, sw, so, zu, zo):

		#M     = su*sw/so
		M      = self.calculate_M(32, su, sw, so)
		output = np.zeros(bias.shape)

		for j in range(output.shape[0]):
			parcel1 = 0
			parcel2 = 0
			for k in range(output.shape[1]):
				for i in range(weights.shape[1]):
					parcel1 += int(weights[j][i]) * int(inputs[i][k])
			        parcel2 += weights[j][i]
					output[j][k] = parcel1 - parcel2*zu + bias[j][k]
					output[j][k] = output[j][k] * M + zo

			output = np.round(output)

		return output.astype('int32')

# ======================== ACTIVATION ===========================

	def activation(self, act_type, inputs, su=0, zu=0):

		output = inputs.copy()

		if(act_type == 0): # RELU
			output[output < -128] = -128
		elif(act_type == 1): # Softmax
			real_inputs = su*(inputs - zu)
			e_x 		= np.exp(real_inputs - np.max(real_inputs))
			real_output = e_x / e_x.sum()
			output 		= self.quantize_layer(real_output, 1 / 255.0, -128)

		return output.astype('int8')

# ================== FINAL LAYER EVALUATION =====================

	def evaluate(self, final_layer):

		label = np.argmax(final_layer)
		return label

	# ====================================================
	# 				   INFERENCE TOMA-LE 
	# ====================================================

	def calculate_inference(self):

		# ------- Files to simulate memory access --------
		scales_f   = open('files/scales.txt', 'r')
		z_points_f = open('files/zero_points.txt', 'r')
		sizes_f    = open('files/sizes.txt', 'r')

		# ------------ Quantization of input -------------

		input_zero_point = int(z_points_f.readline())
		input_scale      = float(scales_f.readline())
		quantized_input  = self.quantize_layer(self.input_data, input_scale, input_zero_point)

		# ------> Extract from memory the first layer parameters and layers <------

		 # -----> Weights
		weights_1_f = open('files/weights_1.txt', 'r')

		 # -----> First 2 rows contains size of the weights at first layer
		weights_r_size = int(sizes_f.readline())
		weights_c_size = int(sizes_f.readline())

		 # -----> Scales of weights in first layer
		weights_scale = float(scales_f.readline())

		weights = np.zeros((weights_r_size, weights_c_size))

		for i in range(weights_r_size):
			line = np.array(weights_1_f.readline().split(','), dtype=np.int8)
			weights[i] = line

		weights_1_f.close()

		 # -----> Bias
		bias_1_f = open('files/bias_1.txt', 'r')

		 # -----> Next two rows of sizes
		bias_r_size = int(sizes_f.readline())
		bias_c_size = int(sizes_f.readline())

		bias = np.zeros((bias_r_size, bias_c_size))

		for i in range(bias_r_size):
			line = np.array(bias_1_f.readline().split(','), dtype=np.int32)
			bias[i] = line

		bias_1_f.close()

		 # -----> Scale and z_point of multiplication output

		output_scale = float(scales_f.readline())
		output_zero_point = int(z_points_f.readline())

		#  _____________________________________________________________
		# |																|
		# | 				 Initiates inference !!!     				|
		# |_____________________________________________________________|

		for i in range(self.n_of_layers):
			
			layer_mult_result = self.multiplicate(quantized_input, weights, bias, input_scale, weights_scale, output_scale, input_zero_point, output_zero_point)
			layer_act_result  = self.activation(self.act_type[i], layer_mult_result, output_scale, output_zero_point)


			if i < self.n_of_layers - 1:
				# --------- Updates all parameters ---------
				quantized_input  = layer_act_result.copy()
				input_scale 	 = output_scale
				input_zero_point = output_zero_point

				weights_r_size = int(sizes_f.readline())
				weights_c_size = int(sizes_f.readline())
				weights  	   = np.zeros((weights_r_size, weights_c_size))

				filename  = f'files/weights_{i+2}.txt'
				weights_f = open(filename, 'r')

				for j in range(weights_r_size):
					line = np.array(weights_f.readline().split(','), dtype=np.int8)
					weights[j] = line

				weights_f.close()

				filename = f'files/bias_{i+2}.txt'
				bias_f   = open(filename, 'r')

				# Next two rows of sizes
				bias_r_size = int(sizes_f.readline())
				bias_c_size = int(sizes_f.readline())
				bias        = np.zeros((bias_r_size, bias_c_size))

				for j in range(bias_r_size):
					line = np.array(bias_f.readline().split(','), dtype=np.int32)
					bias[j] = line

				bias_f.close()

		label = self.evaluate(layer_act_result)

		return label



			




