import pandas as pd 
import numpy as np
import plotly.express as px

#--------------------------------------------------------------------------------------------------------------
#                                                       Loading Data
#--------------------------------------------------------------------------------------------------------------

data_set = pd.read_csv("logs/biscayne_bay_water_quality2.csv")

#--------------------------------------------------------------------------------------------------------------
#                                                        Basic EDA
#--------------------------------------------------------------------------------------------------------------

print(f"Featues: {data_set.columns}\n")
print(f"Top 5 rows:\n{data_set.head()}\n")
print(f"Sum of Null Values:\n{data_set.isna().sum()}\n")
print(f"Sum of Duplicate Values: {data_set.duplicated().sum()}\n")
print(f"Descriptive statistics:\n{data_set.describe()}\n")
print(f"Mean Temperature: {data_set["Temperature (c)"].mean():.2f}\n")
print(f"Median Temperature: {data_set["Temperature (c)"].median():.2f}\n")
print(f"Mode Temperature: {data_set["Temperature (c)"].mode()[0]:.2f}")
print(f"Variance Tmeprature {data_set["Temperature (c)"].std() ** 2:.2f}\n")
print(f"Standard Deviation Temperature: {data_set["Temperature (c)"].std():.2f}\n")

reduced_features = [
    "Total Water Column (m)",
    "Temperature (c)",
    "Salinity (ppt)",
    "pH",
    "ODO mg/L"
]

for feature in reduced_features:
    fig = px.box(data_set,
                 x = feature,
                 title= f"Box Plot of {feature}",
                 labels= {feature:feature}) ### Note: plotting the features vertically resulted in a a skewed data set appearing normal at this aspect ratio. 
    ## The fix was to do a horizontal plot by letting X be the plot of the feature.
    #fig.show() # potential outliers identifed across all features

#--------------------------------------------------------------------------------------------------------------
#                                           Detecting and Removing Outliers
#--------------------------------------------------------------------------------------------------------------

def detect_outliers(df: pd.DataFrame, column:String):

    """
    Detects the Outliers for a given pd.Series by computing IQR and defining bounds at 

    lower = Q1 - 1.5 * IQR
    upper = Q3 + 1.5 * IQR
    
    :param df: Data frame 
    :type df: pd.DataFrame
    :param column: Column of interest
    :type column: String

    yields:

    lower bound, upper bound, and set of outliers
    """
    Q1 = df[column].quantile(0.25)
    Q3 = df[column].quantile(0.75)
    
    IQR = Q3 - Q1

    lower = Q1 - 1.5 * IQR

    upper = Q3 + 1.5 * IQR


    cond_1 = df[column] < lower 
    cond_2 = df[column] > upper
    outliers = df[cond_1 | cond_2]

    return outliers,lower, upper

outliers_dictionary = {}
for feature in reduced_features:
    outliers, lower, upper = detect_outliers(data_set,feature)
    outliers_dictionary[feature] = {
        "Lower Bound": lower,
        "Upper Bound": upper,
        "Number of Outliers": len(outliers),
        "Percent Outliers": len(outliers)/ len(data_set) * 100,

    }

outliers_df = pd.DataFrame.from_dict(outliers_dictionary,orient="index")

print(outliers_df)

data_set_clean = data_set.copy()

for f in reduced_features:
    Q1 = data_set[feature].quantile(0.25)
    Q3 = data_set[feature].quantile(0.75)

    IQR = Q3 - Q1
    lower = Q1 - 1.5 * IQR
    upper = Q3 + 1.5 * IQR   

    condition_1 = data_set_clean[feature] >= lower
    condition_2 = data_set_clean[feature] <= upper
    data_set_clean = data_set_clean[condition_1 & condition_2]

for feature in reduced_features:
    fig = px.box(data_set_clean,
                 x = feature,
                 title= f"Box Plot of {feature}",
                 labels= {feature:feature})
    #fig.show()

#--------------------------------------------------------------------------------------------------------------
#                                               Covariance matrices
#--------------------------------------------------------------------------------------------------------------

## Temp and Salinity

cov_mat_TempSal = data_set_clean[["Tempurature (c)","Salinity (ppt)"]].cov()
cov_mat_TempSal.loc()


