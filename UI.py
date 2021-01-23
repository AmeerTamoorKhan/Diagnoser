from tkinter import *
import pandas as pd
import re
import Testing as model
from PIL import Image, ImageTk


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
#*************************** All the UI functions ******************************
i = 0
added_symptoms = []


def sympt_added(symptom, symptoms_list):
    global i, added_symptoms
    if symptom.get() == 'Select':
        pass
    else:
        symptoms_list.insert(i, " "+symptom.get())
        added_symptoms.append(symptom.get())
        i += 1


def analyzer(disease, precaution, disease_var):
    global i, added_symptoms
    Disease, Precaution = model.model(added_symptoms)
    disease_var.set(" Disease: "+Disease[0])
    disease.insert(INSERT, Disease[1])

    for i in Precaution:
        if i != 'Nan':
            precaution.insert(INSERT, i)
            precaution.insert(INSERT, ', ')


def reset(symptoms_list, label_disease, disease, precaution):
    global i, added_symptoms
    symptoms_list.delete(0, 'end')
    i = 0
    added_symptoms = []

    label_disease.set(" ")
    disease.delete(1.0, END)
    precaution.delete(1.0, END)
#*************************** Implementation of GUI *****************************
#*******************************************************************************
HEIGHT = 800
WIDTH = 800
master = Tk()
master.title('Diagnoser')

# Main Canvas
canvas = Canvas(master, width=WIDTH, height=HEIGHT, bg='white')
canvas.pack()


image = Image.open("Images/logo.png")
image = image.resize((round(image.size[0]*0.5), round(image.size[1]*0.5)))
photo = ImageTk.PhotoImage(image)


label = Label(image=photo)
label.image = photo # keep a reference!
label.place(relx=0.3, rely=0.01)
#*******************************************************************************

# Upper Container
upper_cont = Frame(canvas, bg="#78787a")
upper_cont.place(relx=0.1, rely=0.15, relwidth=0.8, relheight=0.3)

# Dropdown Menu
symptom = StringVar(upper_cont)
symptom.set('Select')
symptom_dropdown = OptionMenu(upper_cont, symptom, *symptoms)
symptom_dropdown.config(font='Helvetica 18 bold')
symptom_dropdown.place(relx=0.07, rely=0.1, relwidth=0.5, relheight=0.1)
#*******************************************************************************

# List of Symptoms
symptoms_list = Listbox(upper_cont, font='Helvetica 18 bold')

symptoms_list.place(relx=0.6, rely=0.1, relwidth=0.35, relheight=0.6)
#*******************************************************************************

# Dropdown Button

dropdown_button = Button(upper_cont, text="Add Symptom", font='Helvetica 15 bold',
                         command=lambda: sympt_added(symptom, symptoms_list))
dropdown_button.place(relx=0.07, rely=0.3, relwidth=0.2, relheight=0.1)
#*******************************************************************************

# Analyze Button

button_Analyze = Button(upper_cont, text="Analyze", font='Helvetica 15 bold', bd=3, relief='raised',
                        command=lambda: analyzer(disease, precaution, disease_var))
button_Analyze.place(relx=0.6, rely=0.75, relwidth=0.15, relheight=0.1)

#*******************************************************************************

# Reset Button

button_Reset = Button(upper_cont, text="Reset", font='Helvetica 15 bold', bd=3, relief='raised',
                        command=lambda: reset(symptoms_list, disease_var, disease, precaution))
button_Reset.place(relx=0.8, rely=0.75, relwidth=0.15, relheight=0.1)

#*******************************************************************************

# Lower Container
lower_cont = Frame(canvas, bg="#78787a")
lower_cont.place(relx=0.1, rely=0.5, relwidth=0.8, relheight=0.4)


#*******************************************************************************

# Label for disease name
disease_var = StringVar()
label_disease = Label(lower_cont, textvariable=disease_var, anchor="w", bd=2, relief='groove', font='Helvetica 18 bold')
label_disease.place(relx=0.05, rely=0.1, relwidth=0.9)

#*******************************************************************************

# Disease description
disease = Text(lower_cont, font="Helvetica 13", bd=2, relief='groove')
disease.place(relx=0.05, rely=0.20, relwidth=0.9, relheight=0.3)

#*******************************************************************************

# Label for Precaution
precaution_var = StringVar()
precaution_var.set(" Precautions:")
label_precaution = Label(lower_cont, textvariable=precaution_var, anchor="w", bd=2, relief='groove', font='Helvetica 18 bold')
label_precaution.place(relx=0.05, rely=0.55)

#*******************************************************************************

# Precaution description
precaution = Text(lower_cont, font="Helvetica 13", bd=2, relief='groove')

precaution.place(relx=0.05, rely=0.65, relwidth=0.9, relheight=0.3)

mainloop()


