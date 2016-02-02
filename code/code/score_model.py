def score_model(y_pred, y_test, y_name, X_inputs, models, score_type):
    score = {}
    X_name, X = X_inputs[0], X_inputs[1]
    model_name, model = models[0], models[1]
    
    score['Model name'] = model_name
    score['Model'] = model
    score['X_name'] = X_name
    score['y_name'] = y_name
    score['y_pred'] = y_pred
    score['y_test'] = y_test
    
    try:
        likelihood = model.likelihood
    except:
        likelihood = 'N/A'

    if score_type == "classification":
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
        Model       |   {}      |
        X name      |   {}      |
        Accuracy    |   {}      |
        Precision   |   {}      |
        Recall      |   {}      |
        Specificity |   {}      |
        F1          |   {}      |
        Likelihood  |   {}      |
        """.format(y_name,
                   model_name,
                   X_name,
                   accuracy,
                   precision,
                   recalll,
                   specificity,
                   f1,
                   likelihood)
        score['Accuracy'] = accuracy
        score['Precision'] = precision
        score['Recall'] = recall
        score['Specificity'] = specificity
        score['F1'] = F1
        score['AUC_data'] = chart_storage
        score['chart'] = plot_chart # when called, call on plot_chart( score['AUC_data'])

        print eval_text
        return score

    elif score_type == 'regression':
        errors = y_test - y_pred
        se = float(np.std(errors)) / np.sqrt(len(errors))

        eval_text = """
        y name      |     {}
        Model name  |     {}
        X name      |     {}
        Mean Y      |     {}
        Mean Y_hat  |     {}
        Mean error  |     {}
        SE          |     {}
        Likelihood  |     {}
        """.format(y_name,
                   model_name,
                   X_name,
                   np.mean(y_test),
                   np.mean(y_pred),
                   np.mean(errors),
                   se,
                   likelihood
                   )
        score['likelihood'] = likelihood
        score['Standard Error'] = se
        score['mean y'] = np.mean(y_test)
        score['mean y_hat'] = np.mean(y_pred)
        score['mean_error'] = np.mean(errors)
        
        ## plot pca
        ## plot errors

        print eval_text
        return score
    else:
        return "Please input a valid score_type {'regression', 'classification'}"