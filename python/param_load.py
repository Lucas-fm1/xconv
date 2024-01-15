import numpy as np
import tensorflow as tf
from tensorflow import keras
import tensorflow_model_optimization as tfmot



class Param_loader:
	"""Class to load parameters of a quantized neural network"""

	def __init__(self, nn):

		self.nn = nn
		self.data = nn.weights
		self.weights = []
		self.biases = []
		self.scales = []
		self.z_points = []
		self.sizes = []
		self.q_weights = []
		self.q_biases = []

	def __quantize_array(self, arr, scale, zero_point):
		
		quantized_layer = np.round((arr/scale) + zero_point)

		return quantized_layer

	def model_summary(self):
		self.nn.summary()


	def __save_real_weights(self):

		for item in self.data:
			if 'kernel:0' in item.name:
				self.weights.append(item.numpy().transpose())

	def __save_real_biases(self):

		for item in self.data:
			if 'bias:0' in item.name:
				value = np.reshape(item.numpy(), (item.numpy().size, 1))
				self.biases.append(value)


	def __save_scale_and_zpoints(self):

		# Input layer
		input_f_min = self.data[0].numpy()
		input_f_max = self.data[1].numpy()
		input_q_min = -128
		input_q_max = 127

		input_scale = (input_f_max - input_f_min) / (input_q_max - input_q_min)
		input_z_point = int(np.round(input_q_min - (input_f_min / input_scale)))

		self.scales.append(input_scale)
		self.z_points.append(input_z_point)

		# Weights

		for i, item in zip(range(len(self.data)), self.data):
			if 'kernel_min:0' in item.name:
				w_f_min = self.data[i].numpy()
				w_f_max = self.data[i+1].numpy()
				w_q_min = -127
				w_q_max = 127
				w_scale = (w_f_max - w_f_min) / (w_q_max - w_q_min)
				self.scales.append(w_scale)

				post_f_min = self.data[i+2].numpy()
				post_f_max = self.data[i+3].numpy()
				post_q_min = -128
				post_q_max = 127
				post_scale = (post_f_max - post_f_min) / (post_q_max - post_q_min)
				post_z_point = int(np.round(post_q_min - (post_f_min / post_scale)))
				self.scales.append(post_scale)
				self.z_points.append(post_z_point)


	def __save_size(self):
		for w, b in zip(self.weights, self.biases):
			self.sizes.append(w.shape[0])
			self.sizes.append(w.shape[1])
			self.sizes.append(b.shape[0])
			self.sizes.append(b.shape[1])


	def __save_quantized_parameters(self):

		for i in range(0, len(self.scales)-1, 2):
			q_weights = self.__quantize_array(self.weights[int(i/2)], self.scales[i+1], 0)
			self.q_weights.append(q_weights.astype('int8'))
			
			bias_scale = self.scales[i]*self.scales[i+1]
			q_biases = self.__quantize_array(self.biases[int(i/2)], bias_scale, 0)
			self.q_biases.append(q_biases.astype('int32'))



	def generate_files(self):

		self.__save_real_weights()
		self.__save_real_biases()
		self.__save_scale_and_zpoints()
		self.__save_size()
		self.__save_quantized_parameters()


		# sizes
		f_sizes = open('sizes.txt', 'w')

		for item in self.sizes:
			f_sizes.write(str(item) + '\n')


		f_sizes.close()

		# Scales
		f_scales = open('scales.txt', 'w')

		for item in self.scales:
			f_scales.write(str(item) + '\n')

		f_scales.close()

		# Z_points
		f_z_points = open('zero_points.txt', 'w')

		for item in self.z_points:
			f_z_points.write(str(item) + '\n')

		f_z_points.close()

		# Weights
		for i in range(len(self.weights)):
			np.savetxt(f'weights_{i+1}.txt', self.q_weights[i], delimiter=',', fmt='%d')


		# biases
		for i in range(len(self.biases)):
			np.savetxt(f'bias_{i+1}.txt', self.q_biases[i], delimiter=',', fmt='%d')


