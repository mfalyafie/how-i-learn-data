from application import KNN

if __name__ == '__main__':

    # Create an input for csv file paramater and variable cutoff
    data = input('Insert the relative path of the csv file in the data folder:\n')
    data = ('./' + str(data))
    test = input('Insert the relative path of the csv file of test set in the data folder:\n')
    test = ('./' + str(test))
    # Call the class and function with a complete paramater
    ax = KNN(data, test)
    ax.classification()