from sklearn.cross_validation import train_test_split
from sklearn.decomposition import PCA

# regression loop over models and inputs
# inputs
# models

# CREATE REGRESSION MODELS
reg_models = [gp_reg,
			  bayesian_lin_reg,

			 ]

# CREATE CLASSIFICATION MODELS
class_models = [gp_class,
				bayesian_log_reg,
		  		SVM
		 		]

# CREATE INPUTS LIST
inputs = []
for X in [X_skills, X_task, X_context]:
	pctiles = get_percentiles(X)
	for data in [X, pctiles]:
		inputs.append(data)
		inputs.append(data[data[auto_delta_pct > 0]])
		inputs.append(data[data[auto_delta_pct < 0]])
		inputs.append(data[emp_delta_pct > 0])
		inputs.append(data[emp_delta_pct < 0])

# CREATE TARGET MODELS
reg_targets = []
for y in [automation, computerisation]:
	y_1, y_0 = y[1], y[0]
	p_1, p_0 = get_percentiles(y_1), get_percentiles(y_0)
	delta = y_1 - y_0
	pctile_delta = p_1 - p_0
	reg_targets.append(delta)
	reg_targets.append(pctile_delta)
	reg_targets.append(delta/float(y_0))
	reg_targets.append(pctile_delta/float(p_0))

# CREATE CLASS TARGETS

class_targets = []
for target in reg_targets:
	# pct change
	# absolute delta
	for sd_threshold_value in [0.5, 0.75, 1.0, 1.25, 1.5, 1.75, 2.00, 2.25, 2.50, 2.75, 3.00]:
		low_threshold = target > (np.mean(target) - sd_threshold_value*np.std(target))
		class_targets.append(low_threshold)
	
	mean_threshold = target > np.mean(target)
	class_targets.append(mean_threshold)


#### aggregate models as list of tuples [(name, val), (name, val)]
# loop

def run_loop():
	## returns all models in comparison, as dict
	evals = {}
	for inp in inputs:
		X_name, X, y = inputs[0], inputs[1], inputs[2]
		X_train, X_test, y_train, y_test = train_test_split(X, y)
		for mod in models:
			model_name, model = models[0], models[1]
			model.fit(X_train, y_train)
			y_pred = model.predict(X_test)
			score = score_model(y_pred, y_test, inp, mod)
			dict_key = model_name + X_name
			evals[dict_key] = score
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
	model_name, model = models[0], models[1]
	if len(set(y_test)) == 2: # NEED BETTER CLASSIFICATION MODEL
		eval_type = "classification"
	else:
		eval_type = "regression"

	if eval_type == "classification":
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
		""".format(model_name,
				   X_name,
				   np.mean(y_test),
				   np.mean(y_pred),
				   np.mean(errors),
				   se)

		## plot pca
		
		## plot errors

		print eval_text
		return score


	# accuracy
	# precision
	# recall
	# match