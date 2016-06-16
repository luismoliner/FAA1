import pandas as pd
import numpy as np
import re
#from sklearn.cluster import KMeans
#import matplotlib.pyplot as plt
#from sklearn.decomposition import PCA
#import pylab as pl
#import pylab as p
#import matplotlib

df = pd.read_csv("dev.csv")
#df = pd.read_csv("TESTFA1.csv", sep=',' and ';')
np.seterr(invalid='ignore')
#pd.set_option('display.max_rows', len(df))
print("Original Data Frame\n", df)
### Have a quick look at the data
#df.head()
#print(df.columns)
#df.describe
#print(df.dtypes)

#for column in df.columns:
#    print (column, df[column][0], df[column][1], df[column].mean())

# Replace all NaN with 0
df.fillna(0, inplace=True)

# If all the values in the column are float and whitespaces (one or several), replaces the latter with 0
# Removes spaces before or after the numbers
# print(df)
for column in df.columns:
    if df[column].dtypes in ["object"]:
        change = True
        for i in range (0,len(df)):
#            print (column, i, df[column][i], type(df[column][i]))
#            if not df[column][i].replace('.','',1).isdigit(): Fails with NEG
#                continue
            if (re.match(r"[-+]?\d+(\.\d+)?$", str(df[column][i]).strip()) is None):
#                if (re.match(r"[-+]?\d+(\.\d+)?$", df[column][i].strip()) is None):
                if df[column][i].strip() != '':
                    change = False
#        print (column, change)
        if change:
            df[column]= df[column].replace(r"^\s+$", '0', regex=True)
#            print("HOLA\n", df)
            df[column]= df[column].replace(r"\s+", '', regex=True)
            df[column] = pd.to_numeric(df[column], errors='coerce')
#            if df[column][i]).strip() == '':
#                df[column][i] = df[column].replace(r"\s+", '', regex=True)
#            df[column]= df[column].replace(r"\s+", '0', regex=True)
#            df[column] = pd.to_numeric(df[column], errors='coerce')
#            if (re.match(r"\d\s+$", str(df[column][i])) is not None):
#                df[column]= df[column].replace(r"\s+", '', regex=True)
#            df[column]= df[column].replace(r"\s+", '0', regex=True)
#            df[column] = pd.to_numeric(df[column], errors='coerce')

#print (space(3))


#    print (df[column].dtypes == "object")
#    df[[column]] = df[[column]].astype(float)
#    df[column] = df[column].convert_objects(convert_numeric=True)
#    df[column] = pd.to_numeric(df[column], errors='coerce')
#print(df)
#df = df.convert_objects(convert_numeric=True)

#type(df["Id"][1]) in [np.float64, np.int64]
#type(df["var3"][1])
#df["var3"][2].isdigit()
#    pd.to_numeric(df[[column]], errors='ignore')
#    df[['two', 'three']] = df[['two', 'three']].astype(float)
#    df["var3"] = df["var3"].astype(float) #No funciona si hay un string
#df["var3"].columns
## Fuerza la conversión de la columna a número sustituyendo strings por NaN
#######################33
#    df["var3"] = pd.to_numeric(df["var3"], errors='coerce')
# df["var3"][2] != ' '

#    df[column]= df[column].replace(" ", 0)

# Replace outliers and out of range, for the border values
data = {}
for column in df.columns:
#    print (column, df[column].dtypes)
    if df[column].dtypes in ["int64", "float64"]:
#        print ("Vale")
        max = np.max(df[column])        
        p75 = df[column].quantile(0.75)
        p50 = df[column].quantile(0.5)
        p25 = df[column].quantile(0.25)
        min = np.min(df[column])        
        mean = df[column].mean()
        iqr = p75 - p25
        data.update({column : pd.Series([df[column].dtypes, min, p25, p50, mean, p75, max], index=["Type", "MIN", "P25", "P50", "Mean", "P75", "MAX"])})
#        print (column, df[column].dtypes, p25, p50, p75, mean)
        for i in range (0,len(df)):
            if (df[column][i] > (p75 + 1.5*iqr)):
                df.set_value(i, column, p75 + 1.5*iqr)
            if (df[column][i] < (p25 - 1.5*iqr)):
                df.set_value(i, column, p25 - 1.5*iqr)
print ("\nInfo about the columns to transform:\n", pd.DataFrame(data),"\n")

print("Transformed Data Frame\n", df)

df.to_csv("transformed.csv")

#for column in df.columns:
#    print (column, df[column].dtypes)
#    for i in range (0,len(df)):
#        if (df[column][i] == ""):
#            print ("HOLA")
#        else:
#            print (df[column][i])


#print(df['var1'][1])
#print (df["var1"][0])
#print (df['var1'].mean())
