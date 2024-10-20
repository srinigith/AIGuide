import pandas as pd
import numpy as np
from sklearn import metrics
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler

# Load dataset
df = pd.read_csv('data/loan_data.csv')
df = df.drop('Loan_ID', axis=1)
#numeric_cols = ['Dependents',]
#df = pd.to_numeric(df)


# Convert categorical variables to numerical variables
#categorical_cols = ['Gender', 'Married', 'Dependents', 'Education', 'Self_Employed','Credit_History','Property_Area']
categorical_cols = ['Gender', 'Married', 'Dependents', 'Education', 'Self_Employed', 'Property_Area','Loan_Status']        
le = LabelEncoder()
for col in categorical_cols:
    df[col] = le.fit_transform(df[col])

# Handle missing values
try:
    df.fillna(df.mean(), inplace=True)
except Exception as e:
    print("The error is: ",e)

# Scale numerical variables
from sklearn.preprocessing import StandardScaler
scaler = StandardScaler()
df[['ApplicantIncome', 'CoapplicantIncome', 'LoanAmount']] = scaler.fit_transform(df[['ApplicantIncome', 'CoapplicantIncome', 'LoanAmount']])

X = df.drop('Loan_Status', axis=1)
y = df['Loan_Status']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

#model
model = Sequential()
model.add(Dense(64,activation='relu',input_shape=(8,)))
model.add(Dropout(0.2))
model.add(Dense(32,activation='relu'))
model.add(Dropout(0.2))
model.add(Dense(1,activation='sigmoid'))
model.compile(loss='binary_crossentropy',optimizer='adam',metrics=['accuracy'])
#grid_search = GridSearchCV(estimator=xgb_clf, param_grid=param_grid, cv=5)
try:
    model.fit(X_train, y_train,epochs=10, batch_size=128, validation_data=(X_test, y_test))
except Exception as e:
    print("The error is: ",e)

# Evaluate model
loss, accuracy = model.evaluate(X_test, y_test)
print(f"Accuracy: {accuracy:.2f}")

# Predict on test set
y_pred = model.predict(X_test)
y_pred_class = (y_pred >= 0.5).astype('int32')

# Classification report and confusion matrix
from sklearn.metrics import classification_report, confusion_matrix
print("Classification Report: \n", classification_report(y_test, y_pred_class))
print("Confusion Matrix: \n", confusion_matrix(y_test, y_pred_class))

def predict_loan_eligibility(data):
    # Preprocess data
    data = pd.DataFrame(data)
    categorical_cols = ['Gender', 'Married', 'Dependents', 'Education', 'Self_Employed','Loan_Amount_Term', '', 'Property_Area']
    for col in categorical_cols:
        data[col] = le.fit_transform(data[col])
    data[['ApplicantIncome', 'CoapplicantIncome', 'LoanAmount']] = scaler.transform(data[['ApplicantIncome', 'CoapplicantIncome', 'LoanAmount']])
    
    # Predict loan eligibility
    prediction = model.predict(data)
    return prediction

# Sample loan data
"""
data = {
    'Gender': ['Male'],
    'Married': ['Yes'],
    'Dependents': [2],
    'Education': ['Graduate'],
    'Self_Employed': ['No'],
    'ApplicantIncome': [5000],
    'CoapplicantIncome': [3000],
    'LoanAmount': [200000],
    'Credit_History': [1]
}

prediction = predict_loan_eligibility(data)
print("Loan Eligibility: ", prediction)
"""