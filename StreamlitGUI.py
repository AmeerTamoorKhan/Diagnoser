import pandas as pd
import re
import Testing as model
import streamlit as st

st.set_page_config(page_title='Diagnoser', page_icon="\U0001fa7a", layout='wide', initial_sidebar_state='auto')


def text_preprocessing(text):
    text = text.capitalize()
    text = text.replace(' ', '')
    text = text.replace('_', ' ')
    text = re.sub(r"\((.*?)\)", '', text)

    return text


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


def about():
    st.header('Working Demonstration:')
    st.video('images/diagnoser.mp4')
    st.header('How It Works:')
    st.markdown('''
    Diagnoser is a fun Machine Learning project to diagnose the disease based on the symptoms.\n
    The tested diseases along with the symptoms are on the right text file. The dataset consists of 41 diseases with 17
    symptoms max. The total dataset comprises 5000 samples. The accuracy is around 90% (Validation/Test data). Along
    with the diagnosis of the disease, some basic precautions are also provided. The model is made of LSTM and Dense 
    layers.\n
    <strong>#LSTM #neuralnetworks #machinelearning #DiagnoserDiagnoser </strong>
    ''', unsafe_allow_html=True)

symptoms = pd.read_csv('data/Symptom-severity.csv')
symptoms = symptoms.iloc[:, 0]
symptoms = symptoms.values


for i in range(len(symptoms)):
    symptoms[i] = text_preprocessing(symptoms[i])

symptoms = sorted(symptoms)
st.sidebar.header('Welcome To Diagnoser')
options = ['About', 'Diagnoser']
radio = st.sidebar.radio('Select', options)

st.sidebar.markdown('''<h3>Created By: Ameer Tamoor Khan</h3>
                    <h4>Github : <a href="https://github.com/AmeerTamoorKhan" target="_blank">Click Here </a></h4> 
                    <h4>Email: drop-in@atkhan.info</h4> ''', unsafe_allow_html=True)
#************************************** GUI *************************************
col1, col2, col3, col4, col5, col6 = st.beta_columns(6)
with col1:
    st.image('Images/Logo1.png', width=100)
with col2:
    st.title('Diagnoser')


if radio == options[1]:
    st.empty()
    selected_symptoms = st.multiselect('Select the Symptoms', symptoms)

    enter = st.button('Enter')


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
elif radio == options[0]:
    st.empty()
    about()







