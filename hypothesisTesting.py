import math
from scipy.stats import norm

## Example 1 One sample z-test one sided

print("----------------------------------------------------------------------------------------\n\t\t\t\tExample 1\n----------------------------------------------------------------------------------------\n")

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
print("----------------------------------------------------------------------------------------\n\t\t\t\tExample 2\n----------------------------------------------------------------------------------------\n")
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