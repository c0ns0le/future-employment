# CREATE INPUTS LIST
def get_array_percentiles(array):
		def percentile(x, array):
			return 100*np.mean(array <= x)

		return np.array(map(lambda x: percentile(x, array), array))

def get_percentiles(df):
	if isinstance(df, pd.DataFrame):
		new_df = df.copy()
		return new_df.apply(lambda x: get_array_percentiles(x), axis = 0)
	elif isinstance(df, np.ndarray):
		return np.apply_along_axis(get_percentiles, 0, a)
	else:
		print "TYPE ERROR; PLEASE INPUT pd.DataFrame OR np.ndarray"
		raise