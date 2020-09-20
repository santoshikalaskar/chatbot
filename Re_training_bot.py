import sklearn
from sklearn import preprocessing, svm
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
import re, os, pickle
from os.path import isfile, join
import nltk
import numpy as np
import pandas as pd


class Retrain_Bot:

    def __init__(self):
        pass

    def load_csv(self):
        path = "CC+FP_Data1.csv"
        data = pd.read_csv(path)
        data.drop_duplicates(['Question'], inplace=True)
        data.drop_duplicates(inplace=True)
        print("data shape: ",data.shape)
        return data

    def pre_processing_input(self, data):
        """
        This function will clean the received original data.
        :param data: Original data
        :return: cleaned data
        """
        regex = '[^a-z,A-Z]'
        tokenizer = nltk.tokenize.TweetTokenizer()
        lemma_function = nltk.stem.wordnet.WordNetLemmatizer()
        document = []
        for text in data.Question:
            collection = []
            tokens = tokenizer.tokenize(text)
            for token in tokens:
                # Apply regular expression to remove unwanted data.
                collection.append(lemma_function.lemmatize(re.sub(regex, " ", token.lower())))
            document.append(" ".join(collection))
        return document

    def pre_processing_label(self, data):
        """
        This function will convert categorical data(i.e., intent) into label encoded form.
        :param data: Original data
        :return: intent in numerical form
        """
        le = preprocessing.LabelEncoder()
        le.fit(data.Intent)
        label = le.transform(data.Intent)
        return label, le

    def countVectorFeaturizer(self, cleaned_data, label):
        """
        :param label: output values
        :param X_train: train data features
        :param X_test: test data features
        :param cleaned_data: cleaned data features
        :return: text data in the form of numbers
        """

        X_train, X_test, y_train, y_test = train_test_split(np.array(cleaned_data),
                                                            np.array(label),
                                                            test_size=0.1,
                                                            train_size=0.9,
                                                            random_state=42)

        count_vect = CountVectorizer(ngram_range=(1, 1))
        count_vect.fit(cleaned_data)
        X_train_cv = count_vect.transform(X_train)
        X_test_cv = count_vect.transform(X_test)
        return X_train_cv, y_train, X_test_cv, y_test, count_vect

    def train_model(self, X_train_cv, y_train, X_test_cv, y_test):
        svm = sklearn.svm.LinearSVC(C=0.1)
        svm.fit(X_train_cv, y_train)
        pred = svm.predict(X_test_cv)
        f1 = sklearn.metrics.f1_score(pred, y_test, average='weighted')
        accuracy = int(round(svm.score(X_test_cv, y_test) * 100))
        return svm, f1, accuracy

    def save_model(self, le, count_vect, classifier):
        obj = {'le': le, 'count_vect': count_vect, 'model': classifier}
        pickle.dump(obj, open('model/' + "model" + ".pickle", 'wb'))
        print("Model saved")

    def load_model(self):
        mypath = 'model/'
        model_file = [f for f in os.listdir(mypath) if (isfile(join(mypath, f)) and ("model" in f))][0]
        return model_file

    def Answer_Prediction(self, data, model_file):
        model = pickle.load(open("model/" + model_file, 'rb'))
        le = model['le']
        count_vect = model['count_vect']
        classifier = model['model']
        cleaned_data = self.pre_processing_input(data)
        X_train_cv = count_vect.transform(cleaned_data)
        pred = classifier.predict(X_train_cv)
        intent = le.inverse_transform(pred)
        return intent[0]

if __name__ == '__main__':
    retrain = Retrain_Bot()

    data = retrain.load_csv()

    label, le = retrain.pre_processing_label(data)
    cleaned_data = retrain.pre_processing_input(data)
    X_train_cv, y_train, X_test_cv, y_test, count_vect = retrain.countVectorFeaturizer(cleaned_data, label)
    print("train-test shape: ",X_train_cv.shape, y_train.shape, X_test_cv.shape, y_test.shape)

    classifier, f1, accuracy = retrain.train_model(X_train_cv, y_train, X_test_cv, y_test)
    f1_value = int(round(f1 * 100))
    print("F1 & acc : ",f1_value, accuracy)

    retrain.save_model(le, count_vect, classifier)

    model_file = retrain.load_model()

    test_path = "ReTrain_BOT.csv"
    test_data = pd.read_csv(test_path)
    questions_list = test_data['Question']

    intent_list = []
    for question in questions_list:
        df = pd.DataFrame([{'Question': question}])
        intent = retrain.Answer_Prediction(df, model_file)
        intent_list.append(intent)

    test_data['Retain_Predicted_intent'] = intent_list
    test_data.to_csv('Retain_Predicted_intent.csv')
    print(test_data.head(10))