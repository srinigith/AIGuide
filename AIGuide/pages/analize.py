from AIGuide import app
from flask import jsonify, render_template, request
import pandas as pd
import sweetviz as sv

@app.route('/analize')
def analize():
    df = pd.read_csv('data/loan_data.csv')
    #df = df.drop('Loan_ID', axis=1)
    report = sv.analyze(df)
    report.show_html('AIGuide/templates/report.html',False)
    return render_template(
        'analize.html',
        title='analize',
    )