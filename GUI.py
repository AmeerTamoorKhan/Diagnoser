from flask import Flask, render_template
from flask_wtf import FlaskForm
from wtforms import SelectField
import pandas as pd
import re

def text_preprocessing(text):
    text = text.lower()
    text = text.replace(' ', '')
    text = text.replace('_', ' ')
    text = re.sub(r"\((.*?)\)", '', text)

    return text


symptoms = pd.read_csv('data/Symptom-severity.csv')
symptoms = symptoms.iloc[:, 0]
symptoms = symptoms.values
print(symptoms)

for i in range(len(symptoms)):
    symptoms[i] = text_preprocessing(symptoms[i])

symptoms = sorted(symptoms)


app = Flask(__name__)


@app.route("/")
def hello():
    return render_template('gui.html', symptoms=symptoms)


if __name__ == "__main__":
    app.run(debug=True)

