__author__ = 'wolfenfeld'

import os
import tkFileDialog
import tkMessageBox
from Tkinter import *
import ttk
from svm_handler import SVMHandler
from mail import sendemail
import threading


# thread that will handle the training of the model
class trainThread(threading.Thread):
    file_path = ""

    def run(self):
        # initialize the classifier attribute to the result of the training model
        svm_handler.classifier = svm_handler.trainTheModel(self.file_path)

        print ("The model has been trained successfully")


class testThread(threading.Thread):
    file_path = ""

    def run(self):
        # check if the classifier has been initialized
        if svm_handler.classifier != None:
            # initialize the error percentage rate from the test data using the classifier

            svm_handler.errorPercentage = svm_handler.testTheModel(self.file_path,
                                                                   svm_handler.classifier)

            print ("The model has been tested successfully!")
        else:
            print "The model hasn't been trained yet!"


class mailThread(threading.Thread):
    def run(self):
        # check if the error percentage rate has been initialized
        if svm_handler.errorPercentage != None:
            # send an email with the error percentage rate
            sendemail(("The error percentage is: {} ".format(svm_handler.errorPercentage)))
            print ("mail sent successfully")

        else:

            print "the error percentage hasn't been calculated yet"


# a function to check if the user entered a valid not empty file
def checkFileValidity(file_path):
    if (file_path == "" or os.stat(file_path).st_size == 0):
        return FALSE
    else:
        return TRUE


def run_gui():
    root = Tk()
    root.title("SVM GUI")
    # initialize the global handler so that testing and training will have common attributes

    global svm_handler
    svm_handler = SVMHandler()
    # declaration of the 3 threads
    trainWorker = trainThread()
    testWorker = testThread()
    mailWorker = mailThread()
    # Here you need to set the frame, grid, row and column configurations of the root.
    root.geometry('500x400')
    root.configure(bg='black')
    root.minsize(400, 300)
    mainframe = ttk.Frame(root)

    # the user selects the data file
    tkMessageBox.showinfo("select data file", "Select the data file to be used in the model")
    data_file_path = tkFileDialog.askopenfilename(filetypes=([('All files', '*.*'),
                                                              ('Text files', '*.data'),
                                                              ('CSV files', '*.csv')]))

    # the user selects the test file
    tkMessageBox.showinfo("select test file", "Select the test file")
    test_file_path = tkFileDialog.askopenfilename(filetypes=([('All files', '*.*'),
                                                               ('Text files', '*.data'),
                                                               ('CSV files', '*.csv')]))
    # Here you need to start the training of the svm. Remember, the other actions (testing/sending mail) must be
    # responsive to users actions (i.e. hitting their button)- How can this be achieved?
    def activate_train(worker, file_path):

        # check if the user entered empty string or empty file
        if checkFileValidity(file_path) == FALSE:
            tkMessageBox.showinfo("Title", "You entered an empty file path or an empty file")

        else:
            worker.file_path = file_path

            # check if the thread has been activated yet
            try:
                worker.start()

            # catch an exception in case the user clicked at the same thread(button) more than once
            except:
                tkMessageBox.showinfo("Title", "You used this thread before")

    # Here you need to start the testing with the svm. Remember, the other actions (training/sending mail) must be
    # responsive to users actions (i.e. hitting their button)- How can this be achieved?
    def activate_test(worker, file_path):

        # check if the user entered empty string or empty file
        if checkFileValidity(file_path) == FALSE:
            tkMessageBox.showinfo("Title", "You entered an empty file path or an empty file")
        else:

            worker.file_path = file_path
            # check if the classifier has been initialized
            if svm_handler.classifier != None:

                # check if the thread has been activated yet
                try:
                    worker.start()

                # catch an exception in case the user clicked at the same thread(button) more than once
                except:
                    tkMessageBox.showinfo("Title", "You used this thread before")
            else:

                tkMessageBox.showinfo("Title", "The model hasn't been initialized yet")

    # Here you need to send an email with the svm testing result. Remember, the other actions (training/testing)
    # must be responsive to users actions (i.e. hitting their button)- How can this be achieved?
    def send_mail(worker):

        # check if the error percentage rate has been initialized
        if svm_handler.errorPercentage != None:
            try:

                # check if the thread has been activated yet
                worker.start()

            # catch an exception in case the user clicked at the same thread(button) more than once
            except:
                tkMessageBox.showinfo("Title", "You used this thread before")

        else:

            tkMessageBox.showinfo("Title", "The Percentage error rate hasn't been calculated yet")

    # Here you need to implement three buttons, one for each action.
    # each button calls for the respective thread according to what the user clicked
    ttk.Button(root, text='train the model',
               command=lambda: activate_train(trainWorker, data_file_path)).pack(side=TOP, pady=10)
    ttk.Button(root, text='test the model',
               command=lambda: activate_test(testWorker, test_file_path)).pack(side=TOP, pady=10)
    ttk.Button(root, text='send mail', command=lambda: send_mail(mailWorker)).pack(side=TOP, pady=10)

    for child in mainframe.winfo_children():
        child.grid_configure(padx=5, pady=5)

    root.mainloop()


if __name__ == "__main__":
    run_gui()
