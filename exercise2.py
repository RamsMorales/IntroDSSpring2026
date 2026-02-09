import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

data = {
    "year": [2010,2011,2012,2010,2011,2012,2010,2011,2012],
    "team": ["FCBarcelona","FCBarcelona","FCBarcelona","RMadrid","RMadrid","RMadrid","Valencia","Valencia","Valencia"],
    "wins": [38,28,32,29,32,26,21,17,19],
    "draws": [6,7,4,5,4,7,8,10,8],
    "losses": [2,3,2,4,2,5,9,11,11] 
}
#print(len(data["team"])==len(data["losses"])) # used this to ensure that data loading was accurate
#print(data)

soccer_data = pd.DataFrame(data)
#print(soccer_data)

## The point of above was to review creating data frames from python dictionaries

edu_data = pd.read_csv("logs/educ_figdp_1_Data.csv",usecols=["TIME","GEO","Value"],na_values=":")
## Use columns param indicates column selections although one can sub-select from a full data frame by indexing.
## We also introduce some data cleaning by indicating that ':' from the data represent true 'NaN' values in the data.
#print(edu_data.info())# with the above modifications we see that Value column has 361 True values and 23 null vals

#print(edu_data.loc[90:94]) #vs
#print(edu_data[90:94])

# note the difference: in the .loc case the range uses the df index so includes all indicies in the range specified.
# in the latter case, however, we use python indexing; thus, the max bound is not included i.e. [90,94) vs [90,94] in the former
#print(edu_data[edu_data["Value"] > 6.5]) 
# the former point is further illustrated in this print out. python maps 0:k for the structure in question. so this is techinically printing a new object whose 0th index is labeled 93 but this 93 maps to the df index

#print(edu_data[edu_data["Value"].isnull()])

#print(edu_data.max(axis=0))# max value for all columns among each row

#print(f"Pandas max: {edu_data["Value"].max()}")
#print(f"Python max: {max(edu_data["Value"])}")
# Interesting to note.

### Numpy with pd
transformed_edu = edu_data["Value"].apply(np.sqrt)
print(transformed_edu.head())

#### anonymous functions
transformed_edu = edu_data["Value"].apply(lambda d: d**2)
print(transformed_edu.head())

### Appending columns
edu_data["ValueNorm"] = edu_data["Value"]/edu_data["Value"].max()
print(edu_data.head())

### Dropping columns
#edu_data.drop("ValueNorm",axis=1,inplace=True)
# here we drop the new added column. axis=1 makes sure the we drop the column not just the row. inplace makes sure a copy isn't made first. Default behavior is to make a copy

edu_data = pd.concat([edu_data,pd.DataFrame({"TIME":2000,"Value":5.00,"GEO":"a"},index=[max(edu_data.index)+1])]) # this adds another row/observation to our df
print(edu_data.tail()) # note if we reverse the dropping the ValueNorm column, then since our new data frame (observation) did not initialize this value,a NaN is placed there instead.

### Example 3

toy_example ={
    "A":[1,None,3,None],
    "B":[None,None,6,None],
    "C":[7,8,9,None]
}
toy_df = pd.DataFrame(toy_example)
print(toy_df)

toy_any = toy_df.dropna(how="any") 
print(toy_any)# any drops the rows containing any <==> at least one NaN value

toy_all = toy_df.dropna(how="all")
print(toy_all) # drops rows containing all  <==> \forall columns in a row, NaN is present in the column for that row

# default behavior is "any"

## we return to example 2
eduDrop = edu_data.dropna(how="any",subset=["Value"])
#expectign to yield only rows in edu_data that don't have NaN in the value column
print(eduDrop)
#Notice we kept the row with the ValueNorm == NaN

#eduFilled = edu_data.fillna(value={"Value":0})
eduFilled = edu_data.fillna(value={"Value":0,"ValueNorm":0}) #this version fills the specified columns
print(eduFilled.head())

### sorting
edu_data.sort_values(by="Value",ascending=False,inplace=True)
print(edu_data.head())

edu_data.sort_index(axis=0,ascending=True,inplace=True)
print(edu_data.head())

### grouping
group = edu_data[["GEO","Value"]].groupby("GEO").mean()
print(group)

### Pivot tables
'''
Summarizing data in a way that you specify

Case: you want to explain data to some audience. The data is not well formatted. This will allow you to fix the formatting accordingly <- this is how it was sold to us. Lets see if we can understand the abstraction here
'''
piv_edu = pd.pivot_table(edu_data,
                         values="Value",
                         index=["GEO"],
                         columns=["TIME"])
print(piv_edu.head()) # what did we get out of this?
'''
For each unique value in the index -> "GEO" column we created columns from the unique values in "TIME" column, and calculated the average "Value" for the ("GEO","TIME)
Effectively ("GEO","TIME") |->  mean("Value") for the pair is this a true function? I don't yet understand the mechanics to say yes or no, but the language used implies yes.
'''

## can filter the data first to build pivot table from filtered data

filtered_edu = edu_data[edu_data["TIME"] > 2005]

piv_edu = pd.pivot_table(filtered_edu,
                         values="Value",
                         index=["GEO"],
                         columns=["TIME"])

print(type(piv_edu)) #pivot table returns DataFrame object

print(piv_edu.loc[["Spain","Portugal"],[2006,2011]])
# example case of prior methods applicable to this object

piv_edu = piv_edu.rename(index={"Germany (until 1990 former territory of the FRG)":"Germany"})
# renaming seems like a frequent operation given that it was tested in the interview.
print(piv_edu)
