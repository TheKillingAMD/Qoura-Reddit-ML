import numpy as np
from nltk.corpus import stopwords
import pandas as pd
from gensim.models import Word2Vec as w2v
from nltk.stem import PorterStemmer
from tensorflow import keras
from tensorflow.keras.models import Sequential
# from keras.models import Sequential
from keras.layers import LSTM
from keras.layers import BatchNormalization
from keras.layers import Dense

stop_words = set(stopwords.words('english'))
ps = PorterStemmer()

X = []
punc = '''!()-[]{};:'"\,<>./?@#$%^&*_~'''
punc += '1234567890'

model = w2v.load("skipgram_v2.model")
wv = model.wv

vocab = wv.key_to_index

vocab1 = pd.read_csv('vocabulary.csv')

vocab_to_int = {}

for i in range(len(vocab1)):
    vocab_to_int[vocab1['Word'][i]] = int(vocab1['Id'][i])

model = Sequential()
model.add(LSTM(256, input_shape = (244, 1)))
model.add(BatchNormalization())
model.add(Dense(1, activation = "sigmoid"))
model.compile(loss = "mse", optimizer = "sgd", metrics = ["accuracy"])

model.load_weights("./formality_model_v1.h5")

def transform_text(A):
    str = []
    
    A = A.lower()
    temp = ''

    for j in range(len(A)):
        if A[j] not in punc:
            temp += A[j]

    temp = temp.split(' ')

    for i in range(len(temp)):
        if temp[i] != '' and temp[i] not in stop_words:
            p = ps.stem(temp[i])
            if p in vocab:
                str.append(p)
    return str

def similarity(Q, A):
    result = 0
    for i in A:
        x1 = wv[i]
        r = 0
        for j in Q:
            x2 = wv[j]
            if r < np.dot(x1, x2)/(np.linalg.norm(x1)* np.linalg.norm(x2)):
                r = np.dot(x1, x2)/(np.linalg.norm(x1)* np.linalg.norm(x2))
        result += r
    if len(A) > 0:
        result = result / len(A)
    result = round(result, 4)
    return result

def get_result(Q, A):
    q = transform_text(Q)

    result = []
    alt_result = []
    
    for i in range(len(A)):
        a = transform_text(A[i])
        
        X_train = []

        temp = [0] * len(vocab_to_int)

        for j in a:
            if j in vocab_to_int:
                temp[vocab_to_int[j]] += 1
        X_train.append(temp)
        
        X_train = np.reshape(X_train, (1,len(vocab_to_int),1))
        
        x = model.predict(X_train)
        
        alt_result.append(x[0])
        
        result.append(similarity(q, a) + (x[0] / 2))
        
    return result

# Q = 'What is my name?'

# A = ['My name is Ayush','Byush','Mango']

# result = get_result(Q, A)

# for i in result:
#     print(i[0], end = ' ')

# print()