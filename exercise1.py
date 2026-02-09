import pandas as pd
import plotly.express as px

"""
In-Class Activity: Exploratory Data Analysis (EDA) with Starbucks Drinks

Dataset: starbucks_drinkMenu_expanded.csv (available in Canvas)
Goal: Understand what the dataset contains, identify patterns, and create a meaningful visualization.
"""

print("*************** Part 1 ***************")

"""
1. Load the CSV file into a pandas DataFrame
2. Print:
- The full DataFrame (⚠️ observe what happens)
- The first 5 rows
- The last 5 rows

3. Display:
- Column names
- Dataset info (data types + missing values)
- Descriptive statistics

💡 Reflection questions:

A) Why is printing the entire DataFrame usually a bad idea?
    We encounter issues with data being occulted since the resolution cannot display the entire dataframe. The head and tail methods are helpful here.
B) Which columns are numeric? Which are categorical?
    Beverage_category,Beverage, and Veverage_prep are categorical, the rest are numeric
C) Do the statistics make sense for food and drinks?
    They seem to so far. Nothing stands out.
"""

## 1
menu_dat = pd.read_csv("logs/starbucks_drinkMenu_expanded.csv")

## 2
print(menu_dat)
print(menu_dat.head())
print(menu_dat.tail())
print("************************************************************************************")

##3
#print(menu_dat.columns)
menu_dat.info() # this is a very nice method. quicker than the other methods. 
print(menu_dat.describe())
print("*************** Part 2 ***************")
"""
1. Select and print only these columns:
- Beverage
- Caffeine (mg)
- Sodium (mg)

Display:
- One specific row (your choice)
- Two different rows (your choice)
- Those same rows, but only for two columns

💡 Reflection questions:
A) When would you select rows vs columns?
B) What kind of question would each selection help answer?
"""
## 1
columns_of_interest = ["Beverage","Caffeine (mg)","Sodium (mg)"]
print(menu_dat[columns_of_interest])

#menu_dat = menu_dat.set_index("Beverage")
#print(menu_dat[columns_of_interest])
print(menu_dat.loc[7,:])
print(menu_dat.loc[[13,220],:])
print(menu_dat.loc[[13,220],["Beverage","Calories"]])
print("*************** Part 3 ***************")

"""
1. Create a table showing where missing values exist
2. Count how many missing values each column has

💡 Reflection questions:

A) Which columns have missing values?
B) Would you drop, fill, or ignore them? Why?
"""
print(menu_dat[menu_dat["Caffeine (mg)"].isna() == True])
print(menu_dat.isna().sum())

# Suggested answer 
## I like this answer. Its nice to look at and clean 
missing_values = {
    "Feature": menu_dat.columns,
    "Missing Values": menu_dat.isna().sum(),
    "Percentage of Missing Values": menu_dat.isna().sum()/ len(menu_dat) * 100
}
print(pd.DataFrame(missing_values))


print("*************** Part 4 ***************")
"""
1. Filter the dataset to show beverages with:
- Calories below 100
- Improve the filter to show beverages with:
- Calories below 100 AND
- Caffeine below 50 mg

⚠️ Challenge:
Make sure your condition works correctly. If it doesn’t, debug it.

💡 Reflection questions:
A) What kind of customer might this filter represent?
B) Why do we need parentheses in compound conditions?
"""
lowCal = menu_dat["Calories"] < 100
lowCaf = menu_dat["Caffeine (mg)"] < 50

print(menu_dat[lowCal],menu_dat[lowCaf],menu_dat[lowCal & lowCaf])

print(menu_dat[lowCal & ~lowCaf])


print("*************** Part 5 ***************")
"""
1. Group the dataset by Beverage_category
2. Compute the average calories per category
3. Print the result

💡 Reflection questions:
A) Which category is the most calorie-dense on average?
B) Why is the mean a reasonable (or not) choice here?
"""
print(menu_dat.groupby("Beverage_category")["Calories"].mean())

print("*************** Part 6 ***************")

"""
1. Create a new DataFrame containing only numeric nutrition columns
2. Compute the correlation matrix
3. Plot a correlation heatmap using Plotly

💡 Reflection questions:

A) Which nutrients are strongly correlated?
B) Are there any surprising relationships?
C) Why does correlation not imply causation?
"""
numeric_only = menu_dat.select_dtypes(include="number")
print(numeric_only.head())
corr = numeric_only.corr()

fig = px.imshow(
    corr,
    text_auto = True,
    title="Correlation Matrix Heatmap"
)
#fig.show()

## Box plot for the calories 
fig2 = px.box(menu_dat,x="Caffeine (mg)")
#fig2.show()

beverage_view = menu_dat.groupby("Beverage_category")
print(beverage_view["Caffeine (mg)"].mean())

#__________________________________________________________________________________
#                        Case Study on Handling Missing Values
#__________________________________________________________________________________
missing_drinks = menu_dat[menu_dat["Caffeine (mg)"].isna() == True]
print(missing_drinks)

## Strategy 1 - Dropping the values
dropped_missing = menu_dat.dropna(subset=["Caffeine (mg)"])
print(f"Original dataset shape: {menu_dat.shape}. New data shape: {dropped_missing.shape}")
# Pros: preserves data integrity. Cons: 

## Strategy 2 - Filling with average of caffiene
# Pro: preserves the overall distribution Cons: Per Category comparison is altered since it is based on fake data
filled_dat = menu_dat.copy()
mean_caffiene = menu_dat["Caffeine (mg)"].mean()
filled_dat["Caffeine (mg)"].fillna(mean_caffiene,inplace=True)
print(f"Original dataset shape: {menu_dat.shape}. New data shape: {filled_dat.shape}")

## Strategy 3 - Analyze what the categories mean and see if that data makes sense (fill with 0s) LEAST FAVORABLE
fill_zero = menu_dat.copy()
fill_zero["Caffeine (mg)"].fillna(0,inplace=True)
print(f"Original dataset shape: {menu_dat.shape}. New data shape: {fill_zero.shape}")

# Strategy 4 - do a per category comparison and fill with mean for that category 
## these are especially useful for atributes with high variance per category
## Pro it is a closer estimate ## con: still fake data

category_df = menu_dat.copy()
category_df["Caffeine (mg)"] = category_df.groupby("Beverage_category")["Caffeine (mg)"].transform(lambda x: x.fillna(x.mean()))
print(menu_dat.describe())
print(category_df.describe())