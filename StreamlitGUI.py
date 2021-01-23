import pandas as pd
import re
import Testing as model
from PIL import Image, ImageTk
import streamlit as st
import numpy as np

st.set_page_config(page_title='Diagnoser', page_icon="\U0001fa7a", layout='wide', initial_sidebar_state='auto')


def text_preprocessing(text):
    text = text.capitalize()
    text = text.replace(' ', '')
    text = text.replace('_', ' ')
    text = re.sub(r"\((.*?)\)", '', text)

    return text


symptoms = pd.read_csv('data/Symptom-severity.csv')
symptoms = symptoms.iloc[:, 0]
symptoms = symptoms.values


for i in range(len(symptoms)):
    symptoms[i] = text_preprocessing(symptoms[i])

symptoms = sorted(symptoms)

#************************************** GUI *************************************
col1, col2, col3, col4, col5, col6 = st.beta_columns(6)
with col1:
    st.image('Images/Logo1.png', width=100)
with col2:
    st.title('Diagnoser')


selected_symptoms = st.sidebar.multiselect('Select the Symptoms', symptoms)

enter = st.sidebar.button('Enter')

st.sidebar.markdown('''<h3>Created By: Ameer Tamoor Khan</h3>
                    <h4>Github : <a href="https://github.com/AmeerTamoorKhan" target="_blank">Click Here </a></h4> 
                    <h4>Email: drop-in@atkhan.info</h4> ''', unsafe_allow_html=True)


def default():
    st.subheader('Disease Name & Description')
    st.text_area('Disease')
    st.text_area('Disease Description')
    st.subheader('Precautions')
    st.markdown('Precautions 1')
    st.write('Precautions 2')
    st.write('Precautions 3')
    st.write('Precautions 4')


def display(Disease, Precaution):
    st.subheader('Disease Name & Description')
    st.text_area('Disease', Disease[0])
    st.text_area('Disease Description', Disease[1])
    st.subheader('Precautions')
    st.write('1)', Precaution[0])
    st.write('2)', Precaution[1])
    st.write('3)', Precaution[2])
    st.write('4)', Precaution[3])


def analyzer(symptoms):
    Disease, Precaution = model.model(symptoms)
    return Disease, Precaution


if enter:
    Disease, Precaution = analyzer(selected_symptoms)
    display(Disease, Precaution)
else:
    default()


reset = st.button('Reset')

if reset:
    st.sidebar.empty()




