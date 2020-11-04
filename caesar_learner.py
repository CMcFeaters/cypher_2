'''
Caesar_learner.py
This ML is a Neural Network intended to learn to crack the keys for Caesar (shift) cyphered mono-alphabetic text

The file expects this folder layout:
./source_data/	#where the source files are
//[whatever the file is]/ #container for all the subfolders created and teh output data
///blks/	#where all the blocks will be stored
///enc/		#where the encoded files are stored
///keys/	#where the keys are stored

which is what is setup by "cypher_2.py"

Attack strategy is based off of:
http://ceur-ws.org/Vol-2243/paper10.pdf
section 3.1

The NN for this will consist of:
1 input layer of 26 nodes
1 Hidden layer of 26 nodes
1 output layer of 26 nodes

input layer nodes will be the frequency distribution of the current encoded text input[0]=a_pct, input[0]=b_pct, etc
output layer will be a 

'''

# Artificial Neural Network

# Importing the libraries
import numpy as np
import pandas as pd
import tensorflow as tf
import string
tf.__version__

# Part 1 - Data Preprocessing

# Importing the dataset
target='war_and_peace'
dataset = pd.read_csv('./source_data/%s_eval.csv'%target)
X = dataset.iloc[:, 1:-1].values	#inputs are all but the last column
y = dataset.iloc[:, -1].values	#dependent variable is the last column
print("Original x/y shapes")
print(X.shape)
print(y.shape)

# One Hot Encoding the "Geography" column
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder

#this has to be a category list, we can't get this as auto
ct = ColumnTransformer(transformers=[('encoder', OneHotEncoder(), [0])], remainder='passthrough')
#y=temp.reshape(-1, 1)
y=y.reshape(-1,1)
#y = np.array(ct.fit_transform(y)).tolist()
#print(ct.fit_transform(y))
y = ct.fit_transform(y).toarray()	#we needto convert this from a csr_matrix to an NParray
print("Y-shape")
print(y.shape)
print(type(y))

# Splitting the dataset into the Training set and Test set
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2, random_state = 0)

print("************")
print("Split complete")
print("************")

# Feature Scaling
from sklearn.preprocessing import StandardScaler
sc = StandardScaler()
X_train = sc.fit_transform(X_train)
X_test = sc.transform(X_test)
print("x train/test shape")
print(X_train.shape)
print(X_test.shape)

print("************")
print("scaling complete")
print("************")

# Part 2 - Building the ANN
from tensorflow import keras
from tensorflow.keras import layers

inputs=keras.Input(shape=(26,))		#input layer is 1 node per frequency analysis
dense=layers.Dense(26,activation="relu")	#create th hidden layer

ann=dense(inputs)	#put the inputs to the hideen layer
outputs=layers.Dense(24)(ann)	#assign the outputs as part of the "ann" layer

model=keras.Model(inputs=inputs,outputs=outputs, name="test_model")	#make the model

model.summary()	#lets see what this bad boy looks like
print("Original x's")
print(X_train.shape)
print(X_test.shape)

#X_train = X_train.reshape(800, 26).astype("float32") / 255
#X_test = X_test.reshape(200, 26).astype("float32") / 255
print("RESHAPED x's")
print(X_train.shape)
print(X_test.shape)


model.compile(
    loss=keras.losses.CategoricalCrossentropy(from_logits=True),
    optimizer=keras.optimizers.RMSprop(),
    metrics=["accuracy"],
)	#compiel our model 

#current error
print(type(X_train))
print(type(y_train))
history = model.fit(X_train, y_train, batch_size=1, epochs=2, validation_split=0.2)

test_scores = model.evaluate(X_test, y_test, verbose=2)
print("Test loss:", test_scores[0])
print("Test accuracy:", test_scores[1])

