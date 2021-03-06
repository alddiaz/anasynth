# Filtering library
# Developed by Aldo Diaz
# University of Campinas, 2020

import numpy as np
import scipy.signal as signal

# Upsampling
def upsampling(x, L):
	# Input:
	# x: Input signal
	# L: Upsampling factor
	#
	# Output:
	# y: Upsampled signal

	l = len(x)*L
	y = np.zeros(l)
	y[::L] = x

	return y

# Downsampling
def downsampling(x, M, FLAG=0):
	# Input:
	# x: Input signal
	# M: Downsampling factor
	# FLAG: Even or odd indexed samples of x
	#
	# Output:
	# y: Downsampled signal

	if np.mod(FLAG, 2):
		y = x[1::M] # Downsampling using odd indexes
	else: # default
		y = x[0::M] # Downsampling using even indexes

	return y

# Upsampling -> FIR Filtering -> Downsampling
def up_fir_dn(x, h, L, M):
	# Input:
	# x: Input signal
	# h: Filtering matrix. The columns contain the impulse response coefficients of each filter h_k[n]
	# L: Upsampling factor
	# M: Downsampling factor
	#
	# Output:
	# A: Filter signal array

	if L != 1: # Synthesis step
		y = upsampling(x, L) # Upsampling x in a factor L
		A = np.convolve(y, h) # Convolution
		A = A[:len(A)-(L-1)] # Prune ending zeros
	else: # Analysis step
		y = x
		temp = np.convolve(y, h[:, 0]) # First convolution
		NC = len(h[0]) # Number of h columns
		NF = len(temp) # Size of the convolution vector
		A = np.empty((NF, NC)) # Allocate matrix A
		A[:, 0] = temp # Store the first convolution
		for k in xrange(1, NC):
			A[:, k] = np.convolve(y, h[:, k])
	if M != 1:
		A = downsampling(A, M, 0) # Downsampling A in factor M (even indexes)

	return A

# # Upsampling -> FIR Filtering -> Downsampling
# def up_fir_dn(x, h, L=1, M=1):
# 	# Input:
# 	# x: Input signal
# 	# h: Filtering matrix. The columns contain the impulse response coefficients of each filter h_k[n]
# 	# L: Upsampling factor
# 	# M: Downsampling factor
# 	#
# 	# Output:
# 	# A: Filter signal array
#
# 	if h.ndim == 1: # 1-D filter signal
# 		A = signal.upfirdn(h, x, L, M)#[int(np.floor((len(h)-1)/2.)*L/M):]
# 		# shape = int(np.ceil(((len(x)-1)*L+len(h))/M)) # size of 'upfirdn' result
# 	else: # Array filter signal
# 		M = h.shape[1] # Number of filter channels
# 		A = np.empty((int(np.ceil(((len(x)-1.0)*L+len(h))/M)), M))
#
# 		for k in range(M):
# 			A[:, k] = signal.upfirdn(h[:, k], x, L, M)
#
# 	return A
