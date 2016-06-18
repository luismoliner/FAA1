import pandas as pd
import numpy as np
import re

#data = pd.read_csv("Example1.csv")
#data = pd.read_csv("TESTFA1.csv", sep=',' and ';')
def Faa1(data):
    np.seterr(invalid='ignore')
    print("Original Data Frame\n", data)
    
    #==============================================================================
    # GOAL: Clean files trying to get numerical columns:
    # - Usually NaN are 0 as there is no value.
    # - Whitespaces which can appear when copying data are noisy as they convert 
    #   numbers into strings that are not operable.
    # - Outliers usually are errors which can modify average values. Then it is
    #   better to sustitute them for more reasonable values.
    #==============================================================================
    
    # Replace all NaN with 0
    data.fillna(0, inplace=True)
    
    # If all the values in the column are float and whitespaces (one or several),
    # replaces the latter with 0.
    # Removes whitespaces before or after the numbers.
    for column in data.columns:
        
        if data[column].dtypes in ["object"]:
            change = True
    # The column is going to change if all the values (without whitespaces)
    # match numbers. Numbers need to have int side, though it could be easily
    # changed to accept numbers like .35 as 0.35
            for i in range (0,len(data)):
                if (re.match(r"[-+]?\d+(\.\d+)?$", str(data[column][i]).strip()) is None):
                    if (not pd.isnull(data[column][i]) and data[column][i].strip() != ''):
                        change = False
            if change:
    # If the value is a set of whitespaces, they are replaced by 0, otherwise
    # whitespaces are deleted and finally the column type is changed to numeric
                data[column]= data[column].replace(r"^\s+$", '0', regex=True)
                data[column]= data[column].replace(r"\s+", '', regex=True)
                data[column] = pd.to_numeric(data[column], errors='coerce')
    
    # Replace outliers for the border values
    # For each column several values which define it, are created
    # Values out of the upper and lower limits are replaced for the limit values
    datadict = {}
    for column in data.columns:
        if (data[column].dtypes in ["int64", "float64"]):
            max = np.max(data[column])        
            p75 = data[column].quantile(0.75)
            p50 = data[column].quantile(0.5)
            p25 = data[column].quantile(0.25)
            min = np.min(data[column])        
            mean = data[column].mean()
            iqr = p75 - p25
            lower = p25-1.5*iqr
            upper = p75 + 1.5*iqr
            valueslist = [lower, min, p25, p50, mean, p75, max, upper]
            tagslist = ["LOWER", "MIN", "P25", "P50", "Mean", "P75", "MAX", "UPPER"]
            datadict.update({column : pd.Series([data[column].dtypes]+valueslist, index=["Type"]+tagslist)})
    # If it is binary don't detect outliers
            if (set(data[column]) == {0,1}):
                continue
    # Loops the values in a column looking for extreme values
    # When it finds extreme values sustitutes them, offering several choices
            for i in range (0,len(data)):
                if (data[column][i] > upper):
                    data.set_value(i, column, upper)
                if (data[column][i] < lower):
                    data.set_value(i, column, lower)
            
    print ("\nInfo about the columns to transform:\n", pd.DataFrame(datadict),"\n")
    
    print("Transformed Data Frame\n", data)
    
    data.to_csv("transformed.csv", index=False)


data = pd.read_csv("Example1.csv")
Faa1 (data)