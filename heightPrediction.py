import pandas as pd
import numpy as np
from sklearn import linear_model, preprocessing
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.datasets import make_regression
import pymysql

#Setup connection
host="host" 
port= 3306
dbname="dbname"
user="username"
password="password"

conn = pymysql.connect(host, user=user, passwd=password, port=3306, db=dbname)

#Get inputs and create dictionary
dadHeight = float(input("How tall is your father (in inches)? "))
momHeight = float(input("How tall is your mother (in inches)? "))
gender = str(input("Are you M or F? "))
height = float(0)

inputDict = {"Father":[dadHeight], "Mother":[momHeight], "Gender":[gender], "Height":[height]}
inputdf = pd.DataFrame.from_dict(inputDict)

#Create another dataframe from research data and append inputs
df = pd.read_sql_query("select Father, Mother, Gender, Height from heightData", con=conn)

#Drop null values
df.dropna(how='any', inplace=True)
inputdf.dropna(how='any', inplace=True)

#Encode Gender columns
le = preprocessing.LabelEncoder()
df.Gender = le.fit_transform(df.Gender)
inputdf.Gender = le.fit_transform(inputdf.Gender)

#Predict height
def prediction():

    #Train and test
    X_train = df.drop(columns = ["Height"], axis = 1)
    y_train = df["Height"]
    X_test = inputdf.drop(columns = [ "Height"], axis=1)
    y_test = inputdf["Height"]

    #Regression
    clf = linear_model.LinearRegression()
    clf.fit(X_train, y_train)

    #Prediction
    predict = clf.predict(X_test)
    print("Expected height (inches): ", predict[-1])

prediction()
