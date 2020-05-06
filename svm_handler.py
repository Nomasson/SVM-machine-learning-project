from sklearn import svm, metrics
from parse_data import parse_data, parse_test_data
from calc_error_pct import *
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix
from sklearn import preprocessing


class SVMHandler:
    """ In this class you will implement the classifier and it's methods. """

    def __init__(self):

        # establishing 3 parameters to be used and shared with the svm functions
        self.classifier = None
        self.errorPercentage = None
        self.means_and_frequents = None

    # training the model with the data set
    def trainTheModel(self, filePath):

        # receive the X matrix and y vector after parsing, as well as the means and frequents to be used in testTheModel
        X, y, self.means_and_frequents = parse_data(filePath)

        # scaling the matrix to be used in the SVM model
        X = preprocessing.scale(X)

        # split the data to train 70%, and test 30%
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=24, shuffle=True)

        # classify the data using best suited parameters, fitting the training data
        classifier = svm.SVC(kernel='rbf', gamma=0.0001, C=1000, verbose=10).fit(X_train, y_train)

        # predict the data using the model
        trainPredictions = classifier.predict(X_test)

        # print the confusion matrix, accuracy and recall
        print(confusion_matrix(y_test, trainPredictions))
        print("Accuracy:", metrics.accuracy_score(y_test, trainPredictions))
        print("Recall:", metrics.recall_score(y_test, trainPredictions))

        return classifier

    # testing the model with the .test set
    def testTheModel(self, filePath, classifier):

        # receive the X matrix and y vector after parsing, using the means and frequents already found in training
        X_test, y_test = parse_test_data(filePath, self.means_and_frequents)

        # scaling the matrix to be used in the SVM predictions
        X_test = preprocessing.scale(X_test)

        # predict the outcome of the testing data
        testPredictions = classifier.predict(X_test)

        # print the confusion matrix, accuracy and recall, as well as the error percentage rate
        print(confusion_matrix(y_test, testPredictions))
        print("Accuracy:", metrics.accuracy_score(y_test, testPredictions))
        print("Recall:", metrics.recall_score(y_test, testPredictions))
        print(calculate_error_percentage(y_test, testPredictions))
        return (calculate_error_percentage(y_test, testPredictions))
