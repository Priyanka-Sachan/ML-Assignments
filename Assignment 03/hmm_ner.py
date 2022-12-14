# -*- coding: utf-8 -*-
"""hmm_ner.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1Beonhye6djDTdUW0hiiYp7NrchKFldOc

# Hidden Markov Model for Named Entity Recognition
"""

import numpy as np # linear algebra
import pandas as pd # data processing

from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

"""## Pre-processing"""

dataset=[]
with open('NER-Dataset-Train.txt') as f:
    lines = f.readlines()
    sentence = []
    for line in lines:
      if line == '\n':
        if sentence:
          dataset.append(sentence)
          sentence = []
      else:
        sentence.append(tuple(line.split()))

"""## Training model"""

# Calculate emission probabilities
def emission_probabilities(data_train):
  emp={}
  count_words={'O':0,'I':0,'B':0}
  for i in range(len(data_train)):
    for j in range(len(data_train[i])):
      if data_train[i][j][0] not in emp.keys():
        emp[data_train[i][j][0]]={'O':0,'I':0,'B':0}
      emp[data_train[i][j][0]][data_train[i][j][1]]+=1
      count_words[data_train[i][j][1]]+=1
  for i in emp.keys():
    emp[i]['B']/=count_words['B']
    emp[i]['I']/=count_words['I']
    emp[i]['O']/=count_words['O']
  return emp

# Calculate start probabilities
def start_probabilities(data_train):
  sp={'O':0,'I':0,'B':0}
  for i in range(len(data_train)):
    sp[data_train[i][0][1]]+=1
  sp['B']/=len(data_train)
  sp['I']/=len(data_train)
  sp['O']/=len(data_train)
  return sp

# Calculate transmission probabilities
def transmission_probabilities(data_train):
  tmp={'B':{'B':0,'I':0,'O':0},'I':{'B':0,'I':0,'O':0},'O':{'B':0,'I':0,'O':0}}
  tout_count={'B':0,'I':0,'O':0}
  for i in range(len(data_train)):
    for j in range(len(data_train[i])-1):
      tmp[data_train[i][j][1]][data_train[i][j+1][1]]+=1
      tout_count[data_train[i][j][1]]+=1
  for i in ['B','I','O']:
    tmp[i]['B']/=tout_count[i]
    tmp[i]['I']/=tout_count[i]
    tmp[i]['O']/=tout_count[i]
  return tmp

sentences=len(dataset)//5
for idx in range(5):
  
  print('ROUND -',idx+1,'/ 5')
  # Split dataset in 4:1 ratio
  data_train= dataset[: sentences*(idx)]+dataset[sentences*(idx+1):]
  print('Length of train data: ',len(data_train))
  data_test=dataset[sentences*idx: sentences*(idx+1)]
  print('Length of test data: ',len(data_test))

  # Calculate emission probabilities
  emp=emission_probabilities(data_train)
  print('\nEmisision Probabilities')
  print(pd.DataFrame.from_dict(emp))

  # Calculate start probabilities
  sp=start_probabilities(data_train)
  print('\nStart Probabilities')
  print(sp)

  # Calculate transmission probabilities
  tmp=transmission_probabilities(data_train)
  print('\nTransmission Probabilities')
  print(pd.DataFrame.from_dict(tmp))

  # Validate on test set
  labels=[]
  preds=[]
  for i in range(len(data_test)):
    label=[]
    pred=[]
    for j in range(len(data_test[i])):
      label.append(data_test[i][j][1])
      if data_test[i][j][0] not in emp.keys():
          pred.append('UNK')
          continue
      if j==0:
        p={'B':emp[data_test[i][j][0]]['B']*sp['B'],
           'I':emp[data_test[i][j][0]]['I']*sp['I'],
           'O':emp[data_test[i][j][0]]['O']*sp['O']}
      elif pred[j-1]=='UNK':
        p={'B':emp[data_test[i][j][0]]['B'],
           'I':emp[data_test[i][j][0]]['I'],
           'O':emp[data_test[i][j][0]]['O']}
      else:
        p={'B':emp[data_test[i][j][0]]['B']*tmp[pred[j-1]]['B'],
           'I':emp[data_test[i][j][0]]['I']*tmp[pred[j-1]]['I'],
           'O':emp[data_test[i][j][0]]['O']*tmp[pred[j-1]]['O']}
      pred.append(max(zip(p.values(), p.keys()))[1])
    labels+=label
    preds+=pred
  
  print('\nMeasures')
  accuracy=accuracy_score(labels, preds)
  print('Accuracy Score: ',accuracy)
  recall=recall_score(labels, preds,average='weighted')
  print('Recall Score: ',recall)
  precision=precision_score(labels, preds,average='weighted')
  print('Precison Score: ',precision)
  f1=f1_score(labels, preds,average='weighted')
  print('F1 Score: ',f1)

  print('----------------------------------------------------------------------')

"""## Testing model"""

data_test=[]
with open('NER-Dataset--TestSet.txt') as f:
    lines = f.readlines()
    sentence = []
    for line in lines:
      if line == '\n':
        if sentence:
          data_test.append(sentence)
          sentence = []
      else:
        sentence.append(line.split()[0])

data_test

# Validate on test set
preds=[]
for i in range(len(data_test)):
  pred=[]
  for j in range(len(data_test[i])):
    if data_test[i][j][0] not in emp.keys():
        pred.append('UNK')
        continue
    if j==0:
      p={'B':emp[data_test[i][j][0]]['B']*sp['B'],
          'I':emp[data_test[i][j][0]]['I']*sp['I'],
          'O':emp[data_test[i][j][0]]['O']*sp['O']}
    elif pred[j-1]=='UNK':
      p={'B':emp[data_test[i][j][0]]['B'],
          'I':emp[data_test[i][j][0]]['I'],
          'O':emp[data_test[i][j][0]]['O']}
    else:
      p={'B':emp[data_test[i][j][0]]['B']*tmp[pred[j-1]]['B'],
          'I':emp[data_test[i][j][0]]['I']*tmp[pred[j-1]]['I'],
          'O':emp[data_test[i][j][0]]['O']*tmp[pred[j-1]]['O']}
    pred.append(max(zip(p.values(), p.keys()))[1])
  preds.append(pred)
  print('\nTest-',i)
  print(data_test[i])
  print(pred)

preds