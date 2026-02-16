import math
from scipy.stats import norm
import scipy.stats as stats
import plotly.express as px
import pandas as pd
import numpy as np

def seperator(example :int):
    print(f"----------------------------------------------------------------------------------------------------\n\t\t\t\t\t\tExample {example}\n----------------------------------------------------------------------------------------------------\n")


## Example 1 One sample z-test one sided
seperator(1)
mu = 29
s_mean = 28.3
n = 50
sigma = 4
alpha = 0.05

z_score = (s_mean - mu) / (sigma / math.sqrt(n)) # for the sampling distribution
#z_score = (s_mean - mu) / (sigma)
print(f"Z score: {z_score}")
pval = norm.cdf(z_score)
print(f"Probability of observing this average assuming the population mean is true: {pval}") 

if pval < alpha:
    print("There is sufficient evidence to question their claim")
else:
    print("There is not sufficient evidence to reject their claim")

## Example 2 One sample z-test two sided 
seperator(2)
mu = 30
s_mean = 28.3
n = 50
sigma = 4
alpha = 0.05

z_score = (s_mean - mu) / (sigma / math.sqrt(n)) # for the sampling distribution
#z_score = (s_mean - mu) / (sigma)
print(f"Z score: {z_score}")
pval = 2*norm.cdf(z_score)
print(f"Probability of observing this average assuming the population mean is true: {pval}") 

if pval < alpha:
    print("There is sufficient evidence to question their claim")
else:
    print("There is not sufficient evidence to reject their claim")

## Example 3 One sample z-test two sided 
seperator(3)
n = 40
muA = 8.4
s_A = 4.2

muB = 6.9
s_B = 3.8

## Given we have two independent groups, a two sample t test is appropriate but our pooled group size is large enough that we can approximate with a ztes of the same kind

# a test is also appropriate given we want to see if they are meaningfully (statistically different)


z_score = (muA - muB) / (math.sqrt(((s_A **2)/ n) + ((s_B **2)/n))) # for the sampling distribution
#z_score = (s_mean - mu) / (sigma)
print(f"Z score: {z_score}")
pval = 1-norm.cdf(z_score) ## right tailed. we are testing if group A is bigger than
print(f"Probability of observing this average assuming the population mean is true: {pval}") 

if pval < alpha:
    print("There is sufficient evidence to question their claim")
else:
    print("There is not sufficient evidence to reject their claim")

## Example 4
seperator(4)
mu = 175.3
sample = [177.3, 182.7, 169.6, 176.3, 180.3, 179.4, 178.5, 177.2, 181.8, 176.5]
n = len(sample)

pval = stats.ttest_1samp(sample,175.3,alternative = 'two-sided')[1]
print(f"Probability of observing this average assuming the population mean is true: {pval}") 

if pval < alpha:
    print("There is sufficient evidence to question their claim")
else:
    print("There is not sufficient evidence to reject their claim")

## Example 5
seperator(5)
tipData = px.data.tips()
#print(tipData.head())
#print(tipData.info())
#print(tipData.describe())

# We want to know if the smokers have different average tip ammounts from non-smokers
print(tipData.groupby("smoker")["tip"].mean())

smokers = tipData[tipData["smoker"] == "Yes"]["tip"]
non_smokers = tipData[tipData["smoker"] == "No"]["tip"]

pval = stats.ttest_ind(smokers,non_smokers,equal_var = False,alternative = "two-sided")[1]

print(f"Probability of observing this average difference is true: {pval}") 

if pval < alpha:
    print("There is sufficient evidence to question their claim")
else:
    print("There is not sufficient evidence to reject their claim")

## Example 6
seperator(6)
n = 15
## We know beforehand this is a paried situation but the problem statement indicates we have one group under an intervention style condition
before = np.random.normal(loc=150,scale=10,size=n)
after = before - np.random.normal(loc= 3, scale= 7, size = n)

diff = after-before
print(f"Mean difference = {diff.mean()} (after - before)")

pval = stats.ttest_rel(after,before)[1]

print(f"Probability of observing this average difference is true: {pval}") 

if pval < alpha:
    print("There is sufficient evidence to question their claim")
else:
    print("There is not sufficient evidence to reject their claim")