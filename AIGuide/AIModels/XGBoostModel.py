import pandas as pd
import numpy as np
import xgboost as xgb
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.model_selection import GridSearchCV, RandomizedSearchCV

# Load dataset
df = pd.read_csv('data/loan_data.csv')
df = df.drop('Loan_ID', axis=1)
#numeric_cols = ['Dependents',]
#df = pd.to_numeric(df)


# Convert categorical variables to numerical variables
#categorical_cols = ['Gender', 'Married', 'Dependents', 'Education', 'Self_Employed','Credit_History','Property_Area']
categorical_cols = ['Gender', 'Married', 'Dependents', 'Education', 'Self_Employed', 'Property_Area','Loan_Amount_Term','Credit_History','Loan_Status']        
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

# XGBoost Classifier
xgb_clf = xgb.XGBClassifier(tree_method='hist', n_jobs=-1)
xgb_clf.fit(X_train, y_train)

# Predict on test set
y_pred = xgb_clf.predict(X_test)

# Evaluate model
"""
print("Accuracy: ", accuracy_score(y_test, y_pred))
print("Classification Report: \n", classification_report(y_test, y_pred))
print("Confusion Matrix: \n", confusion_matrix(y_test, y_pred))
"""

# Hyperparameter tuning using GridSearchCV
"""
param_grid = {
    'n_estimators': [50, 100, 200],
    'max_depth': [3, 5, 7],
    'learning_rate': [0.1, 0.5, 1],
    'gamma': [0, 0.25, 1],
    'subsample': [0.5, 0.75, 1],
    'colsample_bytree': [0.5, 0.75, 1],
    'reg_alpha': [0, 0.1, 0.5],
    'reg_lambda': [0, 0.1, 0.5]
}

#grid_search = GridSearchCV(estimator=xgb_clf, param_grid=param_grid, cv=5)
grid_search = RandomizedSearchCV(estimator=xgb_clf, param_distributions=param_grid, cv=5, n_iter=10)

try:
    grid_search.fit(X_train, y_train)
except Exception as e:
    print("The error is: ",e)
# Best parameters
print("Best Parameters: ", grid_search.best_params_)

# Train model with best parameters
#best_params = grid_search.best_params_
xgb_best = grid_search.best_estimator_

# Predict on test set
y_pred = xgb_best.predict(X_test)
"""
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
    dfRev = pd.read_csv('data/loan_data.csv')
    dfRev = dfRev.drop(['Loan_ID','Loan_Status'], axis=1)
    data = pd.DataFrame(data)
    dfRev = pd.concat([dfRev,data], ignore_index = True)
    dfRev[['Loan_Amount_Term','Credit_History']] = dfRev[['Loan_Amount_Term','Credit_History']].apply(pd.to_numeric)
    categorical_cols = ['Gender', 'Married', 'Dependents', 'Education', 'Self_Employed', 'Property_Area','Loan_Amount_Term','Credit_History']
    for col in categorical_cols:
        dfRev[col] = le.fit_transform(dfRev[col])
        
    dfRev[['ApplicantIncome', 'CoapplicantIncome', 'LoanAmount']] = scaler.fit_transform(dfRev[['ApplicantIncome', 'CoapplicantIncome', 'LoanAmount']])
    
    # Predict loan eligibility
    data = dfRev.tail(1)
    prediction = xgb_clf.predict(data)
    return prediction[0]

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