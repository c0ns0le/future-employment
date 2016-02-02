def generate_inputs(X_name, X_input, output_columns, subset_columns, y_before_name, y_after_name, job_codes = None):
    """
    X_name: name of X_input
    X_input: raw input with O*NET-SOC Code
    output_columns: interest variable df, like automation, with O*NET-SOC Code
    subset_columns: output columns you want to subset X on. Str or List
    y_before: name of column containing before target
    y_after: name of column containing after target
    job_codes: necessary only if 
    """
    X = X_input.copy()
    # first, format inputs
    if job_codes and "O*NET-SOC Code" not in X_input.columns:
        X = pd.concat((X_input, job_codes), axis = 1)

    X = X.merge(output_columns, on = 'O*NET-SOC Code', how = 'inner')


    # generate X subsets
    print "CREATING X's"
    if isinstance(subset_columns, str):
        subset_columns = [subset_columns]

    subset_inputs = []
    subset_inputs.append(['full', X])
    for subset in subset_columns:
        Xss = X[subset]
        s = subset
        subset_inputs.append(['pos_change_' + s, X[Xss > 0]])
        subset_inputs.append(['neg_change_' + s, X[Xss < 0]])
        subset_inputs.append(['gt_mean_' + s, X[Xss > Xss.mean()]])
        subset_inputs.append(['lt_mean_' + s, X[Xss < Xss.mean()]])

    # generate transforms
    print "TRANFORMING X's"
    transformed_inputs = []
    cols = list(output_columns.columns)
    for subset_input in subset_inputs:
        transformed_inputs.append(subset_input)
        name, df = subset_input[0], subset_input[1]
        retain = df[cols]
        of_interest = df.drop(cols, axis = 1)

        # percentile
        pct_df = get_percentiles(of_interest)
        pct_df = pd.concat((pct_df, retain), axis = 1)
        pct_name = 'pile_' + name
        transformed_inputs.append([pct_name, pct_df])

        # log change
        if isinstance(of_interest, np.ndarray):
            minimum = np.min(of_interest)
        else:
            minimum = of_interest.values.min()
        if minimum > 0:
            log_df = np.log(of_interest)
            log_df = pd.concat((log_df, retain), axis = 1)
            log_name = 'log_' + name
            transformed_inputs.append([log_name, log_df])

    final_inputs = []
    
    # generate y inputs
    print "CREATING y's"
    for X in transformed_inputs:
        new_y_inputs = []
        X_name = X[0]
        y_before, y_after = X[1][y_before_name], X[1][y_after_name]
        delta = y_after - y_before
        pct_delta = (y_after.astype(float) - y_before.astype(float)) / y_before
        pile_pct_delta = get_array_percentiles(pct_delta)
        pctile_before = get_array_percentiles(y_before)
        pctile_after = get_array_percentiles(y_after)

        new_y_inputs.append(['before', y_before])
        new_y_inputs.append(['after', y_after])
        new_y_inputs.append(['pct_delta', pct_delta])
        new_y_inputs.append(['pile_pct_delta', pile_pct_delta])
        new_y_inputs.append(['pctile_before', pctile_before])
        new_y_inputs.append(['pctile_after', pctile_after])

        final_y_inputs = []
        for name, y_input in new_y_inputs:
            final_y_inputs.append([name, y_input])
            if min(y_input) > 0.0:
                final_y_inputs.append(['log_' + name, np.log(y_input)])

        X_final = X[1].drop(cols, axis = 1)
        for y_name, y_input_final in final_y_inputs:
            final_inputs.append([X_name, X_final, y_name, y_input_final])

    return final_inputs


def create_class_inputs(input_list):
    """
    Input list has to be structured as a list of lists, s.t. the inner list is constructed:

                [X_name, X, y_name, y]

    """
    class_list = []
    for i in input_list:
        X_name, X, y_name, y = i[0], i[1], i[2], i[3]

        # gt/lt than mean
        class_list.append([X_name, X, "gt_mean_" + y_name, y > np.mean(y)])
        class_list.append([X_name, X, "lt_mean_" + y_name, y < np.mean(y)])

        # gt/lt than 0
        if min(y) < 0 and max(y) > 0:
            class_list.append([X_name, X, "gt_0_" + y_name, y > 0])
            class_list.append([X_name, X, "lt_0_" + y_name, y < 0])

        # gt/lt Z std deviations from mean
        devs = np.array([0.5, 1, 1.5, 2, 2.5, 3])
        devs = np.hstack((devs, -devs))
        std = np.std(y)
        mean = np.mean(y)
        for sd in devs:
            new_y = y > (mean + sd*std)
            name = str(std) + "_gt_" + y_name
            class_list.append([X_name, X, name, new_y])

    return class_list