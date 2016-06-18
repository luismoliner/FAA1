import pandas as pd
import numpy as np
import re

df = pd.read_csv("Example2.csv")
#df = pd.read_csv("TESTFA1.csv", sep=',' and ';')
np.seterr(invalid='ignore')
print("Original Data Frame\n", df)

#==============================================================================
# GOAL: Clean files trying to get numerical columns:
# - Usually NaN are 0 as there is no value.
# - Whitespaces which can appear when copying data are noisy as they convert 
#   numbers into strings that are not operable.
# - Outliers usually are errors which can modify average values. Then it is
#   better to sustitute them for more reasonable values.
#==============================================================================

# Replace all NaN with 0
df.fillna(0, inplace=True)

# If all the values in the column are float and whitespaces (one or several),
# replaces the latter with 0.
# Removes whitespaces before or after the numbers.
for column in df.columns:
    if df[column].dtypes in ["object"]:
        change = True
# The column is going to change if all the values (without whitespaces)
# match numbers. Numbers need to have int side, though it could be easily
# changed to accept numbers like .35 as 0.35
        for i in range (0,len(df)):
            if (re.match(r"[-+]?\d+(\.\d+)?$", str(df[column][i]).strip()) is None):
                change = False
        if change:
# If the value is a set of whitespaces, they are replaced by 0, otherwise
# whitespaces are deleted and finally the column type is changed to numeric
            df[column]= df[column].replace(r"^\s+$", '0', regex=True)
            df[column]= df[column].replace(r"\s+", '', regex=True)
            df[column] = pd.to_numeric(df[column], errors='coerce')

# Replace outliers for the border values
# For each column several values which define it, are created
# Values out of the upper and lower limits are replaced for the limit values
data = {}
for column in df.columns:
    if df[column].dtypes in ["int64", "float64"]:
        max = np.max(df[column])        
        p75 = df[column].quantile(0.75)
        p50 = df[column].quantile(0.5)
        p25 = df[column].quantile(0.25)
        min = np.min(df[column])        
        mean = df[column].mean()
        iqr = p75 - p25
        lower = p25-1.5*iqr
        upper = p75 + 1.5*iqr
        valueslist = [lower, min, p25, p50, mean, p75, max, upper]
        tagslist = ["LOWER", "MIN", "P25", "P50", "Mean", "P75", "MAX", "UPPER"]
        data.update({column : pd.Series([df[column].dtypes]+valueslist, index=["Type"]+tagslist)})
        for i in range (0,len(df)):
            if (df[column][i] > upper):
                df.set_value(i, column, upper)
            if (df[column][i] < lower):
                df.set_value(i, column, lower)
        
print ("\nInfo about the columns to transform:\n", pd.DataFrame(data),"\n")

print("Transformed Data Frame\n", df)

df.to_csv("transformed.csv", index=False)
