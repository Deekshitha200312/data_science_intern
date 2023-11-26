# -*- coding: utf-8 -*-
"""SMS Classifier

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/10cd_71tMleejMzl_bu7Jrs3vwi-2lktO
"""

import numpy as np
import pandas as pd
import os
working_dir = os.getcwd()
print(working_dir)
path = working_dir + '/spam.csv'
df = pd.read_csv(path)

# Uploading the dataset


from google.colab import files

uploaded = files.upload()

df.sample(5)

df.shape

""" **Data** **Cleaning**"""

df.info()

df.sample(5)

# Library used to import LabelEncoder
from sklearn.preprocessing import LabelEncoder
encoder = LabelEncoder()

# To replace ham to 0 and spam to 1
df['Category'] = encoder.fit_transform(df['Category'])

df.head()

# To check the missing values in the Dataset
df.isnull().sum()

# Check for duplicate values
df.duplicated().sum()

# We need to remove the duplicates
df = df.drop_duplicates(keep = 'first')

# Check for duplicate values
df.duplicated().sum()

df.shape

"""EDA"""

df.head()

df['Category'].value_counts()

import matplotlib.pyplot as plt
plt.pie(df['Category'].value_counts(), labels = ['ham', 'spam'],autopct = "%0.2f")
plt.show()

# Data is Imbalanced
import nltk

!pip install nltk

nltk.download('punkt')

# Each SMS the length [no. of characters used]
df['num_characters'] = df['Message'].apply(len)

df.head()

# Fetch the number of words
df['num_words'] = df['Message'].apply(lambda x:len(nltk.word_tokenize(x)))

df.head()

# Another column need to be inserted in spreadsheet
df['num_sentences'] = df['Message'].apply(lambda x:len(nltk.sent_tokenize(x)))

df.head()

df[['num_characters', 'num_words','num_sentences']].describe()

# Describing the code for ham(0) messages
df[df['Category'] == 0][['num_characters','num_words','num_sentences']].describe()

# Describing the code for spam(1) messages
df[df['Category'] == 1][['num_characters','num_words','num_sentences']].describe()

df.head()

df.drop(columns = ['num_sentences'],inplace = True)

df.head()

import seaborn as sns

plt.figure(figsize=(12,6))
sns.histplot(df[df['Category'] == 0]['num_characters'])
sns.histplot(df[df['Category'] == 1]['num_characters'],color = 'pink')

plt.figure(figsize=(12,6))
sns.histplot(df[df['Category'] == 0]['num_words'])
sns.histplot(df[df['Category'] == 1]['num_words'],color = 'pink')

# To find the relationship b/w num of words and no of sentences.
sns.pairplot(df,hue = 'Category')

numeric_df = df.select_dtypes(include = 'number')
correlation_matrix = numeric_df.corr()

sns.heatmap(numeric_df.corr(),annot = True)

"""Data Pre-Processing"""

# Creating the new function which contains all these operations performed at once
def transform_text(Message):
  Message = Message.lower()
  Message = nltk.word_tokenize(Message)

  y = []
  for i in Message:
    if i.isalnum():
      y.append(i)
  Message = y[:]
  y.clear()

  for i in Message:
    y.append(ps.stem(i))


  return " ".join(y)

import nltk
nltk.download('stopwords')

from nltk.corpus import stopwords
stopwords.words('english')

import string
string.punctuation

df['Message'][0]

# Stemming
from nltk.stem.porter import PorterStemmer
ps = PorterStemmer()
ps.stem('dancing')

df['transformed_text'] = df['Message'].apply(transform_text)

df.head()

!pip install wordcloud

# Word cloud (Imp words are highlighted)
from wordcloud import WordCloud
wc = WordCloud(width = 500, height = 500, min_font_size = 10, background_color='grey')

spam_wc = wc.generate(df[df['Category'] == 1]['transformed_text'].str.cat(sep = " "))

plt.figure(figsize = (15,6))
plt.imshow(spam_wc)

ham_wc = wc.generate(df[df['Category'] == 0]['transformed_text'].str.cat(sep = " "))

plt.figure(figsize = (15,6))
plt.imshow(spam_wc)

df.head()

"""**Model** **Building**"""

from sklearn.feature_extraction.text import CountVectorizer,TfidfVectorizer
cv = CountVectorizer()
tfidf = TfidfVectorizer(max_features = 3000)

X = tfidf.fit_transform(df['transformed_text']).toarray()

X

X.shape

y = df['Category'].values

y

from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(X,y, test_size=0.2, random_state=2)

from sklearn.naive_bayes import GaussianNB, MultinomialNB, BernoulliNB
from sklearn.metrics import accuracy_score, confusion_matrix, precision_score

gnb = GaussianNB()
mnb = MultinomialNB()
bnb = BernoulliNB()

gnb.fit(X_train, y_train)
y_pred1 = gnb.predict(X_test)
print(accuracy_score(y_test, y_pred1))
print(confusion_matrix(y_test, y_pred1))
print(precision_score(y_test, y_pred1))

mnb.fit(X_train, y_train)
y_pred2 = gnb.predict(X_test)
print(accuracy_score(y_test, y_pred2))
print(confusion_matrix(y_test, y_pred2))
print(precision_score(y_test, y_pred2))

bnb.fit(X_train, y_train)
y_pred3 = gnb.predict(X_test)
print(accuracy_score(y_test, y_pred3))
print(confusion_matrix(y_test, y_pred3))
print(precision_score(y_test, y_pred3))

#tfidf --> MNB
!pip install xgboost

from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.naive_bayes import MultinomialNB
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import AdaBoostClassifier
from sklearn.ensemble import BaggingClassifier
from sklearn.ensemble import ExtraTreesClassifier
from sklearn.ensemble import GradientBoostingClassifier
from xgboost import XGBClassifier

svc = SVC(kernel='sigmoid', gamma = 1.0)
knc = KNeighborsClassifier()
mnb = MultinomialNB()
dtc = DecisionTreeClassifier(max_depth = 5)
lrc = LogisticRegression(solver = 'liblinear', penalty = 'l1')
rfc = RandomForestClassifier(n_estimators=50, random_state=2)
abc = AdaBoostClassifier(n_estimators=50,random_state=2)
bc = BaggingClassifier(n_estimators=50, random_state=2)
etc = ExtraTreesClassifier(n_estimators=50, random_state=2)
gbdt = GradientBoostingClassifier(n_estimators=50, random_state=2)
xgb = XGBClassifier(n_estimators=50, random_state=2)

clfs = {
    'SVC' : svc,
    'KN' : knc,
    'NB': mnb,
    'DT' : dtc,
    'LR' : lrc,
    'RF' : rfc,
    'AdaBoost' : abc,
    'BgC' : bc,
    'ETC' : etc,
    'GBDT' : gbdt,
    'xgb' : xgb
       }

def train_classifier(clf,X_train,y_train,X_test,y_test):
  clf.fit(X_train,y_train)
  y_pred = clf.predict(X_test)
  accuracy = accuracy_score(y_test,y_pred)
  precision = precision_score(y_test,y_pred)

  return accuracy,precision

train_classifier(svc,X_train,y_train,X_test,y_test)

accuracy_scores = []
precision_scores = []

for name,clf in clfs.items():

  current_accuracy,current_precision = train_classifier(clf, X_train,y_train,X_test,y_test)

  print("For",name)
  print("Accuracy - ",current_accuracy)
  print("Precision - ",current_precision)

  accuracy_scores.append(current_accuracy)
  precision_scores.append(current_precision)

performance_df = pd.DataFrame({'Algorithm':clfs.keys(),'Accuracy':accuracy_scores,'Precision':precision_scores}).sort_values('Precision',ascending=False)

performance_df

performance_df1 = pd.melt(performance_df, id_vars = "Algorithm")
performance_df1

sns.catplot(x = 'Algorithm',y = 'value', hue = 'variable',data = performance_df1,kind = 'bar',height=5)
plt.ylim(0.5,1.0)
plt.xticks(rotation='vertical')
plt.show()

"""**Improving the Model**"""

temp_df = pd.DataFrame({'Algorithm':clfs.keys(),'Accuracy_max_ft_3000':accuracy_scores,'Precision_max_ft_3000':precision_scores})
temp_df = pd.DataFrame({'Algorithm':clfs.keys(),'Accuracy_scaling':accuracy_scores,'Precision_scaling':precision_scores})

new_df = performance_df.merge(temp_df,on = 'Algorithm')
new_df_scaled = new_df.merge(temp_df,on = 'Algorithm')
temp_df = pd.DataFrame({'Algorithm':clfs.keys(),'Accuracy_num_chars':accuracy_scores,'Precision_num_chars':precision_scores})
new_df_scaled.merge(temp_df,on = 'Algorithm')

# Voting Classifier
svc = SVC(kernel='sigmoid', gamma=1.0,probability=True)
mnb = MultinomialNB()
etc = ExtraTreesClassifier(n_estimators=50, random_state=2)

from sklearn.ensemble import VotingClassifier

voting = VotingClassifier(estimators=[('svm', svc),('nb', mnb),('et',etc)],voting='soft')

voting.fit(X_train,y_train)

VotingClassifier(estimators=[('svm', SVC(gamma=1.0, kernel='sigmoid',probability=True)),('nb',MultinomialNB()),('et', ExtraTreesClassifier(n_estimators=50,random_state=2))], voting='soft')

y_pred = voting.predict(X_test)
print("Accuracy",accuracy_score(y_test,y_pred))
print("Precision",precision_score(y_test,y_pred))

#Applying stacking
estimators = [('svm', svc), ('nb',mnb),('et',etc)]
final_estimator = RandomForestClassifier()

from sklearn.ensemble import StackingClassifier

clf = StackingClassifier(estimators=estimators, final_estimator=final_estimator)

clf.fit(X_train,y_train)
y_pred = clf.predict(X_test)
print("Accuracy",accuracy_score(y_test,y_pred))
print("Precision",precision_score(y_test,y_pred))

import pickle
pickle.dump(tfidf,open('vectorizer.pkl','wb'))
pickle.dump(mnb,open('model.pkl','wb'))