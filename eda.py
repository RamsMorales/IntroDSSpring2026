import pandas as pd

'''
The purpose of this code is to explore exploratory data analysis techniques in python using live water quality data that may or may not be clean
'''

#--------------------------------------------------------------------------------------------------------------
#                                    data set: biscayne bay water qual
#--------------------------------------------------------------------------------------------------------------
water_quality_log_0 = pd.read_csv("logs/biscayne_bay_water_quality.csv",header=0)
#print(water_quality_log_0) # proof that I can load a dataset

#print(water_quality_log_0.head()) #prints first k rows of the dataframe, default is 5
#print(water_quality_log_0.tail())#prints last k rows of the dataframe, default is 5
#print(water_quality_log_0.columns) #Note TWC := total water column
#print(water_quality_log_0.shape) # gives you a sense of the shape of the comlumns
#print(water_quality_log_0.dtypes) # This is quite useful 
#print(water_quality_log_0.isna().sum()) # checks if we have NaN in any ### This data set is clean of missing values ###

#print(f"Min: {water_quality_log_0["Temp C"].min()}") # you can do it by hand, but better way is df.describe()
#print(water_quality_log_0["Temp C"].max())
#print(water_quality_log_0["Temp C"].mean())
#print(water_quality_log_0["Temp C"].std())

# Five point summary
#print(water_quality_log_0.describe())

# boolean indexing
#print(f"Number of data points with greater than 24.5 temperature: {water_quality_log_0[water_quality_log_0["Temp C"] > 25.4].shape[0]}")

#sub-selecting colmns or column indexing
#print(water_quality_log_0[["Latitude","Longitude","pH"]])

#Are there potential outliers? 
#What percentage of the data is questionable?

#Domain rule: salinity should be above 30 -> salinity has outliers
#print(water_quality_log_0.columns)
#print(water_quality_log_0[water_quality_log_0[["TWC","Speed","Salinity","Temp C","pH","ODO"]] > 3*water_quality_log_0[["TWC","Speed","Salinity","Temp C","pH","ODO"]].std()])
#print(water_quality_log_0[water_quality_log_0[["TWC","Speed","Salinity","Temp C","pH","ODO"]] < 3*water_quality_log_0[["TWC","Speed","Salinity","Temp C","pH","ODO"]].std()])
#print(water_quality_log_0 < 2*water_quality_log_0.std())

## indicates that salinity and potentially speed has outliers

### here focusing on salinity we can see the percent of the data that has potential issues

print(water_quality_log_0[water_quality_log_0["Salinity"] < 30].shape[0]/ water_quality_log_0["Salinity"].shape[0] * 100)

water_quality_removed_salinity_outliers = water_quality_log_0[water_quality_log_0["Salinity"].between(30,45)] #These rules are given by domain
#print(water_quality_removed_salinity_outliers) #Note, removing data biases the data a bit more

#print(water_quality_removed_salinity_outliers.describe())

print(water_quality_removed_salinity_outliers.corr(numeric_only=True))


