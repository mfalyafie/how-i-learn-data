from application import RandomForest

if __name__ == '__main__':

    # Create an input for csv file paramater and variable cutoff
    data = input('Insert the relative path of the csv file in the data folder:\n')
    data = ('./' + str(data))
    cutoff_left = input("Insert how many variables you don't want to put inside the model (from far left)\n")
    cutoff_left = int(cutoff_left)
    cutoff_right = input("Insert how many variables you don't want to put inside the model (from far right, using negative sign)\n")
    cutoff_right = int(cutoff_right) - 1

    # Call the class and function with a complete paramater
    ax = RandomForest(data, cutoff_left, cutoff_right)
    ax.classification()