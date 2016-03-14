def _similarity(xi, xj, Xk):
	"""
	xi: array you are interested in
	xj: array you're comparing it against
	"""
	l2_norm = (xi - xj)**2
	normalizer = 2*(np.std(xi)**2)
	numerator = np.exp(-l2_norm / normalizer)
	denominator = 0:
	for variable in Xk.T:
		l2_v_norm = (xi - variable)**2
		denominator += np.exp(-l2_v_norm / normalizer)
	return numerator / denominator

def _similarity_probability(xi, xj, Xk):
	return similarity(xi, xj, Xk) + similarity(xj, xi, Xk)/2*(len(Xk) + 2)

def create_similarity_matrix(X):
	X = X.T
	new_matrix = np.zeros(X.shape[1] - 1, X.shape[1])
	for i, col_1 in X:
		for j, col_2 in X[:,i:]:
			other_columns = np.delete(X, i, axis = 0) ## DETERMINE IF THIS IS EXCLUSION SYNTAX
			new_matrix[i, j] = new_matrix[j, i] = _similarity_probability(col_1, col_2, other_columns)
	return new_matrix

def general_symmetric_kernel(X, function, **kwargs):
	new_matrix = np.zeros(X.shape[1] - 1, X.shape[1])
	for i, col_1 in X:
		for j, col_2 in X[:,i:]:
			other_columns = X[:,-i] ## DETERMINE IF THIS IS EXCLUSION SYNTAX
			new_matrix[i, j] = new_matrix[j, i] = function(col_1, col_2, **kwargs)
	return new_matrix

class TSNE(matrix, bandwith):
	self.X = matrix
	self.bandwith = bandwidth

	def _similarity(self, xi, xj, Xk):
		"""
		xi: array you are interested in
		xj: array you're comparing it against
		"""
		l2_norm = (xi - xj)**2
		normalizer = 2*(np.std(xi)**2)
		numerator = np.exp(-l2_norm / normalizer)
		denominator = 0:
		for variable in Xk.T:
			l2_v_norm = (xi - variable)**2
			denominator += np.exp(-l2_v_norm / normalizer)
		return numerator / denominator