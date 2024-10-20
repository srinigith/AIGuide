import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.model_selection import GridSearchCV

# Load dataset
df = pd.read_csv('data/loan_data.csv')
df = df.drop("Loan_ID",axis=1)
# Convert categorical variables to numerical variables
categorical_cols = ['Gender', 'Married', 'Dependents', 'Education', 'Self_Employed', 'Property_Area','Loan_Status']
le = LabelEncoder()
for col in categorical_cols:
    df[col] = le.fit_transform(df[col])

#Handle missing values
df.fillna(df.mean(), inplace=True)
    
# Scale numerical variables
from sklearn.preprocessing import StandardScaler
scaler = StandardScaler()
df[['ApplicantIncome', 'CoapplicantIncome', 'LoanAmount']] = scaler.fit_transform(df[['ApplicantIncome', 'CoapplicantIncome', 'LoanAmount']])

X = df.drop('Loan_Status', axis=1)
y = df['Loan_Status']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Random Forest Classifier
rfc = RandomForestClassifier()

# Hyperparameter tuning using GridSearchCV
param_grid = {
    'n_estimators': [100, 200, 300],
    'max_depth': [5, 10, 15],
    'min_samples_split': [2, 5, 10]
}

grid_search = GridSearchCV(estimator=rfc, param_grid=param_grid, cv=5)
grid_search.fit(X_train, y_train)

# Best parameters
print("Best Parameters: ", grid_search.best_params_)

# Train model with best parameters
rfc_best = grid_search.best_estimator_

# Predict on test set
y_pred = rfc_best.predict(X_test)
print("Accuracy: ", accuracy_score(y_test, y_pred))
print("Classification Report: \n", classification_report(y_test, y_pred))
print("Confusion Matrix: \n", confusion_matrix(y_test, y_pred))
# Evaluate model
def check_accuracy():
    print("Accuracy: ", accuracy_score(y_test, y_pred))
    print("Classification Report: \n", classification_report(y_test, y_pred))
    print("Confusion Matrix: \n", confusion_matrix(y_test, y_pred))
    accuracy = {
            accuracy: accuracy_score(y_test, y_pred),
            classification_report: classification_report(y_test, y_pred),
            confusion_matrix: confusion_matrix(y_test, y_pred)
        }
    return accuracy

def predict_loan_eligibility(data):
    # Preprocess data
    data = pd.DataFrame(data)
    
    categorical_cols = ['Gender', 'Married', 'Dependents', 'Education', 'Self_Employed', 'Property_Area']
    for col in categorical_cols:
        data[col] = le.fit_transform(data[col])
    
    #data[['Gender', 'Married', 'Dependents', 'Education', 'Self_Employed']] = le.transform(data[['Gender', 'Married', 'Dependents', 'Education', 'Self_Employed', 'Property_Area','Loan_Status']])
    data[['ApplicantIncome', 'CoapplicantIncome', 'LoanAmount']] = scaler.transform(data[['ApplicantIncome', 'CoapplicantIncome', 'LoanAmount']])
    
    # Predict loan eligibility
    prediction = rfc_best.predict(data)
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