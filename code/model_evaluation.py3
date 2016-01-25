from sklearn.cross_validation import train_test_split
from sklearn.decomposition import PCA

## UNSOLVED
# Using time series data – multiple years

## NOTES ABOUT GP MODELS
# optimize hyperparameters
# perform random restarts
# allow for multiple kernels
# optimize kernels
# optimize variances

## TO DO
# percentile regression model evaluation

# CREATE REGRESSION MODELS
from GPy.models import GPRegression
from sklearn.linear_model import BayesianRidge
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.svm import SVR

from GPy.models import GPClassification
from sklearn.linear_model import RidgeClassifier
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.svm import SVC
from sklearn.naive_bayes import BernoulliNB

reg_models = [GPRegression,
			  BayesianRidge(),
			  GradientBoostingRegressor(),
			  SVR()
			 ]

# CREATE CLASSIFICATION MODELS
class_models = [GPClassification,
				RidgeClassifier(),
				GradientBoostingClassifier(),
				SVC(),
				BernoulliNB()
		 		]

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

X_skills = pd.read_csv("X_skills.csv")
X_task = pd.read_csv("X_task.csv")
X_context = pd.read_csv("X_context.csv")

inputs = []
for X in [X_skills, X_task, X_context]:
	pctiles = get_percentiles(X)
	for data in [X, pctiles]:
		inputs.append(data)
		inputs.append(data[data[auto_delta_pct > 0]])
		inputs.append(data[data[auto_delta_pct < 0]])
		inputs.append(data[emp_delta_pct > 0])
		inputs.append(data[emp_delta_pct < 0])

automation = pd.read_csv("y_automation.csv")
computerisation = pd.read_csv("y_computerisation.csv")

# CREATE TARGET MODELS
reg_targets = []
for y in [automation, computerisation]:
	y_1, y_0 = y.iloc[:,1], y.iloc[:,0]
	p_1, p_0 = get_array_percentiles(y_1), get_array_percentiles(y_0)
	delta = y_1 - y_0
	pctile_delta = p_1 - p_0
	reg_targets.append(('before', y.iloc[:,0]))
	reg_targets.append(('after', y.iloc[:,1]))
	reg_targets.append(('delta', delta))
	reg_targets.append(('pctile_delta', pctile_delta))
	reg_targets.append(('pct_delta', delta/float(y_0))
	reg_targets.append(('pct_pctile_delta', pctile_delta/float(p_0)))

# CREATE CLASS TARGETS
class_targets = []
for name, target in reg_targets:
	# pct change
	# absolute delta
	for sd_threshold_value in [0.5, 0.75, 1.0, 1.25, 1.5, 1.75, 2.00, 2.25, 2.50, 2.75, 3.00]:
		low_threshold = target > (np.mean(target) - sd_threshold_value*np.std(target))
		new_name = str(sd_threshold_value)+"_gt_" + name
		class_targets.append((name,low_threshold))
	
	mean_threshold = target > np.mean(target)
	new_name = 'mean_gt_' + name
	class_targets.append((name, mean_threshold))


#### aggregate models as list of tuples [(name, val), (name, val)]
# loop

def run_loop(X_inputs, y_inputs, models):
	## returns all models in comparison, as dict
	evals = defaultdict(defaultdict({}))
	for X_inp in X_inputs:
		X_name, X = X_inputs[0], X_inputs[1]
		for y_inp in y_inputs:
			# format data
			y_name, y = y_inputs[0], y_inputs[1]
			X_train, X_test, y_train, y_test = train_test_split(X, y)
			data = [X_train, X_test, y_train, y_test]
			new_data = []
			# check that all data is np.ndarry
			for d in data:
				if not isinstance(data, np.ndarray):
					new_data.append(np.array(data))
				else:
					new_data.append(data)
			X_train, X_test, y_train, y_test = new_data

			#loop over models
			for mod in models:
				model_name, model, model_type = models[0], models[1], models[2]
				try:
					model.fit(X_train, y_train)
				except AttributeError:
					model = model(X_train, y_train)
				y_pred = model.predict(X_test)
				score = score_model(y_pred, y_test, X_inp, mod)
				evals[y_name][model_name][X_name] = score
	return evals

def do_ARD(model, feature_names):
	# uses ARD to find relevant features
	length_scales = model.length_scales # np.ndarray
	features = range(1, len(model.features) + 1)
	importances = 1./length_scales
	cutoff = 0.25 * min(importances) # note: arbitrary
	important_features = features * (importances >= cutoff)
	if_indices = np.trim_zeros(important_features)
	return zip(feature_names[if_indices], importances[if_indices])




#--------------------------------------------------#
#--------------------------------------------------#
#--------------------------------------------------#
#--------------------------------------------------#




def score_model(y_pred, y_test, model_inputs, model):
	score = {}
	X_name, X = model_inputs[0], model_inputs[1]
	model_name, model, model_type = models[0], models[1], models[2]

	if model_type == "classification":
		accuracy = -1
		precision = None
		recall = None
		specificity = None
		f1 = None
		ideal_cutoff = None

		chart_storage = np.array([None, None, None])
		for cutoff in np.arange(0, 1.001, 0.001):
			y_pred = y_pred > cutoff
			num_TP = float(np.sum((y_pred == 1) & (y_test == 1)))
			num_FP = float(np.sum((y_pred == 1) & (y_test == 0)))
			num_TN = float(np.sum((y_pred == 0) & (y_test == 0)))
			num_FN = float(np.sum((y_pred == 0) & (y_test == 1)))

			s_accuracy = np.mean(y_pred == y_test)
			s_precision = num_TP / (num_TP + num_FP)
			s_recall = num_TP / (num_TP + num_FN)
			s_specificity = num_TN / (num_TN + num_FP)
			s_f1 = (precision * recall) / (precision + recall)

			chart_storage.append([cutoff, s_recall, s_specificity])

			if s_accuracy > accuracy:
				ideal_cutoff = cutoff
				precision = s_precision
				recall = s_recall
				specificity = s_specificity 
				f1 = s_f1
				ideal_cutoff = s_ideal_cutoff

		def plot_chart(chart_storage):
			cutoffs = chart_storage[:,0]
			sensitivity = chart_storage[:,1]
			specificity = chart_storage[:,2]
			sns.plt.plot(sensitivity, specificity)
			sns.plt.close()

		eval_text = """
		Model 		| 	{}		|
		X name		|	{}		|
		Accuracy	|	{}		|
		Precision  	|	{}		|
		Recall 		|	{}		|
		Specificity |	{}		|
		F1			|	{}		|
		""".format(model_name,
				   X_name,
				   accuracy,
				   precision,
				   recalll,
				   specificity,
				   f1)
		score['Model name'] = model_name
		score['Model'] = model
		score['X_name'] = X_name
		score['Accuracy'] = accuracy
		score['Precision'] = precision
		score['Recall'] = recall
		score['Specificity'] = specificity
		score['F1'] = F1
		score['AUC_data'] = chart_storage
		score['chart'] = plot_chart # when called, call on plot_chart( score['AUC_data'])

		print eval_text
		return score

	else:
		errors = y_test - y_pred
		se = float(np.std(errors)) / np.sqrt(len(errors))

		eval_text = """
		Model 		| 	{}		|
		X name		|	{}		|
		Mean Y		|	{}		|
		Mean Y_hat	|	{}		|
		Mean error	|	{}		|
		SE			| 	{}		|
		Likelihood	|	{}		|
		""".format(model_name,
				   X_name,
				   np.mean(y_test),
				   np.mean(y_pred),
				   np.mean(errors),
				   se,
				   likelihood
				   )

		## plot pca
		
		## plot errors

		print eval_text
		return score