# %% [code]
# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python Docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load

import numpy as np  # linear algebra
import pandas as pd  # data processing, CSV file I/O (e.g. pd.read_csv)
import tensorflow as tf
from sklearn.preprocessing import OneHotEncoder
from sklearn.model_selection import train_test_split
# %% [code]
import re

# Input data files are available in the read-only "../input/" directory
# For example, running this (by clicking run or pressing Shift+Enter) will list all files under the input directory
# You can write up to 5GB to the current directory (/kaggle/working/) that gets preserved as output when you create a version using "Save & Run All"
# You can also write temporary files to /kaggle/temp/, but they won't be saved outside of the current session

# %% [code]
df = pd.read_csv('/kaggle/input/diagnoserdata/dataset.csv')

# %% [code]
features = df.loc[:, df.columns != 'Disease']
labels = df[['Disease']]
features = features.astype(str)
labels = labels.astype(str)


# %% [code]
def sentence_preprocessing(text):
    text = text.apply(lambda x: x.lower())
    text = text.str.replace(' ', '')
    text = text.str.replace('_', '')
    text = text.str.replace("\((.*?)\)", '', regex=True)

    return text


# %% [code]
def processed_features_labels(features, labels):
    for i in range(len(features)):
        features.iloc[i, :] = sentence_preprocessing(features.iloc[i, :])

    labels_processed = labels.Disease.values.reshape(-1, 1)
    encoder = OneHotEncoder(sparse=False)
    labels_processed = encoder.fit_transform(labels_processed)

    return features, labels_processed, encoder


# %% [code]
X_procesed, Y, encoder = processed_features_labels(features, labels)
print(X_procesed.iloc[181, :], Y.shape)


# %% [code]
def tokenization(features_processed):
    x = np.zeros(shape=features_processed.shape)
    f_tokenizer = tf.keras.preprocessing.text.Tokenizer()
    for i in range(len(features_processed)):
        f_tokenizer.fit_on_texts(features_processed.iloc[i])

    for i in range(len(features_processed)):
        x[i] = np.array(f_tokenizer.texts_to_sequences(features_processed.iloc[i, :])).reshape(1, 17)

    return x, f_tokenizer


# %% [code]
X, f_tokenizer = tokenization(X_procesed)

# %% [code]
train_X, test_X, train_Y, test_Y = train_test_split(X, Y, test_size=0.1, shuffle=True)

# %% [code]
epochs = 10
batch_size = 64
input_vocab = len(f_tokenizer.word_index) + 1
output_length = Y.shape[1]

# %% [code]
model = tf.keras.Sequential([
    tf.keras.layers.Embedding(input_vocab, 256, input_length=X_procesed.shape[1]),
    tf.keras.layers.Dropout(0.2),
    tf.keras.layers.LSTM(256, return_sequences=True),
    tf.keras.layers.Dropout(0.2),
    tf.keras.layers.LSTM(256, activation='tanh'),
    tf.keras.layers.Dense(output_length, activation='softmax')
])
model.compile(
    optimizer='adam',
    loss='CategoricalCrossentropy',
    metrics='accuracy'
)
model.summary()

# %% [code]
model.fit(np.array(train_X), np.array(train_Y), validation_split=0.1, batch_size=batch_size, epochs=epochs, verbose=2)

# %% [code]
model.evaluate(test_X, test_Y)


# saving the model, tokenizer, and the encoder
import pickle

with open('encoder.pickle', 'wb') as f:
    pickle.dump(encoder, f)

with open('f_tokenizer.pickle', 'wb') as f:
    pickle.dump(f_tokenizer, f)

model.save('model.h5', 'wb')
