from application import DecisionTree

if __name__ == '__main__':

    # Create an input for csv file paramater and variable cutoff
    data = input('Insert the relative path of the csv file in the data folder:\n')
    data = ('./' + str(data))
    cutoff = input("Insert how many variables you don't want to put inside the model (from far left)\n")
    cutoff = int(cutoff)

    ax = DecisionTree(data, cutoff)
    ax.classification()