from AIGuide import app
from flask import jsonify, render_template, request
from AIGuide.AIModels.XGBoostModel import predict_loan_eligibility


@app.route('/loanapp')
def loanapp():
    return render_template(
        'loanapp.html',
        title='Loan Application'
    )   

@app.route('/loanapp/validate',methods=['POST'])
def loanapp_validate():
    result = ""
    if request.method == "POST":
        content = request.get_json()
        data = {
            'Gender': [content['Gender']],
            'Married': [content['Married']],
            'Dependents': [content['Dependents']],
            'Education': [content['Education']],
            'Self_Employed': [content['Self_Employed']],
            'ApplicantIncome': [content['ApplicantIncome']],
            'CoapplicantIncome': [content['CoapplicantIncome']],
            'LoanAmount': [content['LoanAmount']],
            'Loan_Amount_Term': [content['Loan_Amount_Term']],
            'Credit_History': [content['Credit_History']],
            'Property_Area': [content['Property_Area']],
        }
        result = predict_loan_eligibility(data)
        
    return jsonify({"airesp":str(result)})