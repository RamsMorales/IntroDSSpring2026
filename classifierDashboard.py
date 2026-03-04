import streamlit as st
import plotly.express as px
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
import numpy as np

# Title

st.title("KNN Classifier Interactive Parameter Tool")
st.header("Spring 2026")
st.subheader("Ramson Munoz Morales")
st.divider()

# Background constants

iris = load_iris()

X = iris.data
y = iris.target

# User modified params
test_size = st.slider("Select a test size in percentage of total data from 10% to 100% ",10,100) / 100


#test_size=0.2
random_state= st.number_input("Pick a seed number",min_value=1,step=1,value=42)

# Train test split
trainFeatures, testFeatures, trainClasses, testClasses = train_test_split(X,y,test_size=test_size,random_state=random_state) 

n_neighbors= st.slider(f"Select the number of neighbors test split percentage from 1 to {trainClasses.size}",1,trainClasses.size) 

# model fitting
model = KNeighborsClassifier(n_neighbors=n_neighbors)
model.fit(trainFeatures,trainClasses)

# Model prediction
predictions = model.predict(testFeatures)

# evaluation report
accuracy = (predictions == testClasses).mean() #interesting seems like a nice way to code it.
st.text(f"Test accuracy: {accuracy}") # turn this into streamlit display