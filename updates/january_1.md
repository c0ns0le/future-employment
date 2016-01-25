# What I've Been Working On

* Mapping Skills / Tasks / Contexts --> Automation
* Engineering Automation Variables:
	* Automation score
	* Automation change
	* Percentiles
	* As classification variables.
* Manipulating inputs
	* As percentiles, to get rid of subjectivity.
	* As a 6-step time series
* I've been experimenting with employment projection data, too. Very fun to play around with, but little mapping to automation. (Though I've only done forward-looking.)

# Discoveries / Problems

* I've still found no clear association between X and y. I'm currently looping over models, inputs, targets to try a "shotgun" approach to see what works
* Check-in: seem to be on track with the original proposal and I expect that I'll find results soon.

# Questions and Next Steps

* Ideally, we could take data from a historical example of industry automation (like car manufacturing). I'm looking for data now; if I find any, I'll play around with it.
* Suppose X mapped to y quite well. For non-parametric models, what can you infer about the model once it's been optimized? I.e. does the specifications of an optimized GP tell you anything economically valuable?
* Carl has suggested I look into Autor et al (2014). This would map Occupation --> Skill_level --> Automation. I would engineer Skill_level from the input_X. Conceptually, is there any new information here?

# Related Topics
* It's time to work out a new learning plan and I'm open to suggestions. The AIMS courses are highly systems-focused. Right now, I'm thinking:
	* Andrew Ng's ML Course + Oxford's ML lecture
	* Jaynes: Probability Theory
