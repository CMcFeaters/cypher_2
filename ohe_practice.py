#one-hot practice
import numpy as np
import pandas as pd
import string
lett=[let for let in string.ascii_lowercase]
arr=['a','b','c','d']
#our goal is to turn arr into a one hot of the whoel alphabet


from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
ct = ColumnTransformer(transformers=[('encoder', OneHotEncoder(), [1])], remainder='passthrough')
arr = np.array(ct.fit_transform(arr))
print(arr)
