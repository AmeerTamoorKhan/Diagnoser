#********************************************************************************************
#********************************************************************************************
#************************ Here we will test the Model ***************************************
#********************************************************************************************
#********************************************************************************************
import numpy as np  # linear algebra
import pandas as pd  # data processing, CSV file I/O (e.g. pd.read_csv)
import tensorflow as tf
import pickle
import re
from sklearn.preprocessing import OneHotEncoder
from sklearn.model_selection import train_test_split


def model(added_symptoms):
    # %% [code]
    with open('utils/encoder.pickle', 'rb') as f:
        enc = pickle.load(f)

    with open('utils/f_tokenizer.pickle', 'rb') as f:
        tok = pickle.load(f)

    m = tf.keras.models.load_model('utils/model.h5')


    disease_description = pd.read_csv('data/symptom_Description.csv')
    precaution = pd.read_csv('data/symptom_precaution.csv')


    def text_preprocessing(text):
        text = text.lower()
        text = text.replace(' ', '')
        text = text.replace('_', '')
        text = re.sub(r"\((.*?)\)", '', text)

        return text

    #sympts = added_symptoms
    symptoms = added_symptoms

    symptoms_total = []
    for i in range(17):
        symptoms_total.append('nan')

    for i in range(len(symptoms)):
        symptoms[i] = text_preprocessing(symptoms[i])
        symptoms_total[i] = symptoms[i]

    symptoms_total = np.array(tok.texts_to_sequences(symptoms_total)).reshape(1, 17)

    prediction = np.argmax(m.predict(symptoms_total))

    oneHotRepresentation = np.zeros(shape=(1, 41))
    for i in range(41):
        if i == int(prediction):
            oneHotRepresentation[0, i] = 1

    prediction = enc.inverse_transform(oneHotRepresentation.reshape(1, 41))

    Disease = disease_description.loc[disease_description['Disease'] == prediction[0][0]]
    Disease = [Disease['Disease'].values[0], Disease['Description'].values[0]]
    Precaution = precaution.loc[precaution['Disease'] == prediction[0][0]]
    Precaution = [str(Precaution['Precaution_1'].values[0]).capitalize(), str(Precaution['Precaution_2'].values[0]).capitalize(),\
                 str(Precaution['Precaution_3'].values[0]).capitalize(), str(Precaution['Precaution_4'].values[0]).capitalize()]

    return Disease, Precaution

    # print('Symptoms: ', sympts)
    # print("Actual:", 'Fungal infection')
    # print('Predicted: ', prediction[0][0])
    #
    # # Description of the disease
    # descript = disease_description.loc[disease_description['Disease'] == prediction[0][0]]
    # print('Desription: ', descript['Description'].values[0])
    #
    # # Precaution for the disease
    # precaut = precaution.loc[precaution['Disease'] == prediction[0][0]]
    # print('Precautions: ', precaut['Precaution_1'].values[0], ',',  precaut['Precaution_2'].values[0], ',',
    #       precaut['Precaution_3'].values[0], ',', precaut['Precaution_4'].values[0])


if __name__ == "__main__":
    pass

