def run_loop(loop_type = 'regression', reg_inputs = None, class_inputs = None, reg_models = None, class_models = None):
    ## returns all models in comparison, as dict
    scores = defaultdict(list)
    
    if loop_type == "regression":
        inputs = reg_inputs
        models = reg_models
    else:
        inputs = class_inputs
        models = class_models

    for inp in inputs:
        X_name, X, y_name, y = inp

        # clean data in Numpy format
        if not isinstance(X, np.ndarray):
            X = np.array(X)
        if not isinstance(y, np.ndarray):
            y = np.array(y)
        if y.ndim == 1:
            y = y[:,np.newaxis]

        X_train, X_test, y_train, y_test = train_test_split(X, y)

        for model in models:
            model_name, mod = model
            try:
                if y_train.ndim > 1:
                    new_y_train = y_train.flatten()
                mod.fit(X_train, new_y_train)
                y_pred = mod.predict(X_test)
            except AttributeError:
                mod = mod(X_train, y_train)
                mod.optimize()
                mod.optimize_restarts(10)
                y_pred, y_pred_var = mod.predict(X_test)
                
            score = score_model(y_pred, y_test, y_name, (X_name, X), model, score_type = loop_type) # CREATE TYPES
            scores[model_name].append(score)
    return scores