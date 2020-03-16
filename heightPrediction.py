import pandas as pd
import numpy as np
from sklearn import linear_model, preprocessing
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.datasets import make_regression
import pymysql

# setup connection
host="host.rds.amazonaws.com" 
port=3306
dbname="sql-database"
user="username"
password="password"

conn = pymysql.connect(host, user=user, passwd=password, port=port, db=dbname)

#Get inputs
dadHeight = float(input("How tall is your father (in inches)? "))
momHeight = float(input("How tall is your mother (in inches)? "))
gender = str(input("Are you M or F? "))
height = float(0)

inputDict = {"Father":dadHeight, "Mother": momHeight, "Gender":gender, "Height":height}

#Create dataframe from research data
df = pd.read_sql_table("heightData", con=conn, columns=["Father", "Mother", "Gender", "Height"])
df.shuffle
df.dropna(how='any', inplace=True)

# Add inputs to dataframe and encode
df.append(inputDict)
le = preprocessing.LabelEncoder()
df.Gender = le.fit_transform(df.Gender)

def prediction():

    train, test = train_test_split(df, test_size=0.2)
    X_train = train.drop(columns = ["Height"], axis = 1)
    y_train = train["Height"]

    X_test = test.drop(columns = [ "Height"], axis=1)
    # y_test = test["Height"]

    clf = linear_model.LinearRegression()
    clf.fit(X_train, y_train)

    #Predict height
    predict = clf.predict(X_test)
    print("Expected height (inches): ", predict.tail(1))

prediction()
