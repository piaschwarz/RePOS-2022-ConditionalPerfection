# Influence of Focus on CP

# Useful links:
# https://michael-franke.github.io/intro-data-analysis/logistic-regression.html
# https://www.rensvandeschoot.com/tutorials/generalised-linear-models-with-brms/

#install.packages("remotes")
#install.packages("V8")
#install.packages("rstan")
#install.packages("brms")

# package for convenience functions (e.g. plotting)
library(tidyverse)
# package for Bayesian regression modeling
library(brms)

# load the data into variable "politedata"
data_path = "~/Schreibtisch/ReproResearch/ConditionalPerfection_ReplicationStudy/RePOS-2022-ConditionalPerfection/statistical_analysis/pilotData_selected.csv"
data_all = read_csv(data_path)
df <- subset(data_all, select=c("item_type", "item_answer_type", "response"))
df

# Pre-process the data
# select only rows with the test items
df_selected <- df[df$item_type == "test", ] 
df_selected
# rename column as 'question_type' makes more sense than 'item_answer_type'
df_final <- rename(df_selected, question_type = item_answer_type)
df_final


# Inspect the data

# count total number of test items
df_final %>%  dplyr::count()

# Hypothesis: Amount of 'Nein','whenq' > Amount of 'Nein', 'whatifp'
# (the amount of 'Nein' responses is higher with question type 'when' than the amount of 'Nein' responses with 'whatifp')
# in other words we try to test whether the presence of Focus (= having a 'whenq'-question) makes CP rise (response = 'Nein')

# Fit a Bayesian Logistic Regression Model
fit_brms = brm(
  # regress 'correctness' against 'condition'
  formula = response ~ question_type, 
  # specify link and likelihood function
  family = bernoulli(link = "logit"),
  # which data to use
  data = df_final %>% 
    # 'reorder' answer categories (making 'Nein' the target to be explained)
    mutate(response = response == 'Nein'),
  # also collect samples from the prior (for point-valued testing)
  sample_prior = 'yes',
  # take more than the usual samples (for numerical stability of testing)
  iter = 20000
)

# In the Bayesian model, the 95% uncertainty interval (called credibility interval) states 
# that there is 95% chance that the true population value falls within this interval. 
# When the 95% credibility intervals do not contain zero, 
# we conclude that the respective model parameters are likely meaningful."
summary_model <- summary(fit_brms)$fixed[,c("l-95% CI", "Estimate", "u-95% CI")]


# Inverse Logit function: transforms a real number (usually the logarithm of the odds) to a value (usually probability p) 
# in the interval [0,1]. The invlogit function is: 1 / (1 + exp(-x)) or: exp(x) / (1 + exp(x)
# The mean estimate for the linear predictor ξwhatifp condition is: invlogit(Estimate of the Intercept)
# The mean estimate for the linear predictor ξwhenq condition is: invlogit(Estimate of Intercept + Estimate of question_typewhenq)
# The central predictors corresponding to these linear predictors are: 
# whatifp = invlogit(Estimate of Intercept)
# whenq = invlogit(Estimate of Intercept + Estimate of question_typewhenq)
invlogit <- function(x){
  exp(x) / (1 + exp(x))
}
invlogit(summary_model["Intercept", "Estimate"])
invlogit(summary_model["Intercept", "Estimate"] + summary_model["question_typewhenq", "Estimate"])

# They should roughly correspond to the proportion of "Nein" answers for whenq and whatifp question types
# (in case there is no whatifp with the response "Nein" in the data it won't show up in the table and proportion is 0)
df_final %>%
  group_by(question_type, response) %>%
  dplyr::count() %>% 
  group_by(question_type) %>% 
  mutate(proportion_nein = (n / sum(n))) %>%
  filter(response == "Nein")


# Test the hypothesis: 
# given the model and data, there is reason to believe that the number of 'Nein'-responses in whenq questions 
# is higher than in whatifp questions if there is a * in Star, as the posterior probability exceeds 95%.
brms::hypothesis(fit_brms, "question_typewhenq > 0")


# The following plot shows the densities of the parameter estimates.
# The dark blue line in each density represents the point estimate, while the light-blue area 
# indicates the 95% credibility intervals.
# If credibility intervals do not contain zero and their densities have a very narrow shape, then the predictors are meaningful. 
# If above 0 a predictor positively predicts the 'response', if below 0 a predictor negatively predicts the 'response'. 
# If above 0 then: in comparison to whatifp, the question type whenq is more likely to result in a 'Nein' response (i.e. letting CP arise).
# If below 0 then: whenq less likely to result in a 'Nein' response.")
stanplot(fit_brms, 
         type = "areas",
         prob = 0.95)


# plot the marginal effects (i.e. estimated probabilities of getting a 'Nein' response) of the variables in the model
# as probabilities are more interpretable than odds
plot(conditional_effects(fit_brms))





