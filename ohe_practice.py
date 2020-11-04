#one-hot practice
import numpy as np
import pandas as pd
import string
lett=[let for let in string.ascii_lowercase]
arr=pd.DataFrame(['a','b','c','d','a'],columns=["key"])
#our goal is to turn arr into a one hot of the whoel alphabet
print(arr)

dummies=pd.get_dummies(arr,columns=['key'])
print(dummies)
'''
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
ct = ColumnTransformer(transformers=[('encoder', OneHotEncoder(categories=), [0])], remainder='passthrough')
arr = np.array(ct.fit_transform(arr))
print(arr)
'''