# What I've Been Working On
* Analyzing results from all different combinations of inputs, target variables, and models:
	* Inputs: all skill data, occupations who've increased/decreased in automation, log & percentile transforms of the data
	* Targets: automation in each year, automation change, automation % change, 
	* Models: Gaussian processes, SVR, LASSO & Ridge Regressions
* Reading more historical economics literature – **Carl,** I'll say that reading 1940-1980's theories on automation is very useful as a practice of bad forecasting
* Self-teaching: probability theory & causality (Jaynes' & Pearl's textbooks)
* I've also just started looking again at technology data to identify clusters of technologies that lead to automation.


# Discoveries / Problems

* Gaussian Processes, and other models for that matter, do ok at predicting every outcome other than change in automation. You can predict fairly well the automation for a given year, all different transforms (log, percentile being the key ones), and even using subsets of data (for occupations that changed significantly in automation, for example.)
	* On these measures, a typical mean-absolute-error for a prediction would be +- 20-30% of the actual value, which isn't great.
	* **But, again,** change in automation is hard to predict.
	* A big reason for this is automation is an all-encompassing measure: it captures human capital replacement and expansion. I continue the search for a better measure.
* **See attached** – An interactive plot you may enjoy exploring. A chart of occupations, color-mapped into 10 "types of professions". Occupations are clustered by skill level similarity. The size of the bubbles indicate the % change in automation between 2009 and 2015. (Mike, I used t-SNE to reduce dimensions)

# Next Steps

1. Before moving on from our automation measure (which is habitually annoying), I'd like to look at year-by-year evolutions.
2. Second, I want to augment the skill-level data with education & context requirements.
3. Because automation is an annoying target, I'd like to see if I can either a) find a better target variable or b) investigate clusters of technology that lead to automation.
4. Performing Autor & Dorn's (2014) analysis. I hope their data may be useful.

