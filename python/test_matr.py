import numpy as np

#------ INPUT IMAGE -------
image = np.matrix([[1,1,1,0,0],
                   [0,1,1,1,0],
                   [0,0,1,1,1],
                   [0,0,1,1,0],
                   [0,1,1,0,0]])
#--------- KERNEL ---------
kernel = np.matrix([[1,0,1],
                    [0,1,0],
                    [1,0,1]])

print("\n image X axis: ", image.shape[0])
print(" image Y axis: ", image.shape[1])
print(" image size: ", image.size)

print("\n kernel X axis: ", kernel.shape[0])
print(" kernel Y axis: ", kernel.shape[1])
print(" kernel size: ", kernel.size)
print("\n ===================================== ")

image = image.ravel()
print("\n flatten image X axis: ", image.shape[0])
print(" flatten image Y axis: ", image.shape[1])
print(" flatten image size: ", image.size)
print(" image = \n", image)

kernel = kernel.ravel()
print("\n flatten kernel X axis: ", kernel.shape[0])
print(" flatten kernel Y axis: ", kernel.shape[1])
print(" flatten kernel size: ", kernel.size)
print(" kernel = \n", kernel)
print("\n ===================================== ")

image = image.getT()
print("\n flatten image X axis: ", image.shape[0])
print(" flatten image Y axis: ", image.shape[1])
print(" flatten image size: ", image.size)

kernel = kernel.getT()
print("\n flatten kernel X axis: ", kernel.shape[0])
print(" flatten kernel Y axis: ", kernel.shape[1])
print(" flatten kernel size: ", kernel.size)
print("\n")