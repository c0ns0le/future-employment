# November 27 Update

*For more info, consult the "EDA" and "Skills Regressions" iPython Notebooks.*

## Last time, we said that I would, going forward:
* Identify the appropriate problem:
  * Classification of IT use?
  * Regression of technology use?
  * What metric for technology use?
* Identify relationships
* Begin model design

## What I have been working on:
* Lots of EDA, which has borne interesting insights
* Regressing the major target variables on skills
  * delta_automation_2009_to_2015
  * log(\# of adopted technologies)
  * log(\# of adopted IT technologies)
* With multiple models
  * Random Forests
  * Gaussian Process Regression
  * LASSO regression

## Critical insights
* The broad (or poorly) defined "Technology" and "computerisation" components remain one of the critical sticking points
  * "Automation" seems to be the most logical outcome
* Adoption results are as expected
  * Most adopted technologies are hand technologies
  * New jobs adopted new technologies
  * Adoption gives limited info about the *intensity of adoption*
* Same with automation by occupation
  * Appears two stand-out groups:
    * Augmenting groups (biologists)
    * Replacing groups (clergy)
* There is a good argument this is a **regression problem**
  * However, with **unclear target variables**
* The models I've used:
  * Explain low to high variance
  * With **high RMSE**

## Questions I have
* Model Building
  * Doing good feature selection
    * Many, many techniques! (Which are best for Gaussian processes)
    * What is the effect on RMSE?
  * Model that maps R[n_o, n_s] to y_n – how to think about this?
  * is delta(2009, 2015) the right framework?
* Model Evaluation
  * How do you generate feature importances?
    * Especially in Gaussian processes – is this logically possible
* Gaussian processes
  * Optimizing the hyperparameters
* Should we aim to isolate specific technologies (or groups) instead?

## Further questions
* I would like to build out a structured ML learning plan. I've been making good progress but find some conceptual areas lacking (especially Bayesian learning)
