from email import parser
from inspect import ArgSpec
from application import Prediction
import argparse #type: ignore

if __name__ == '__main__':

    parser  =  argparse.ArgumentParser() 
    parser.add_argument("--action", help="'MLR' / 'Decision tree classification'", type=str)

    args    = parser.parse_args()
    action  = args.action
    if not action:
        while True:
            action      = input("'MLR' or 'Decision tree classification'?\n")
            if not action:
                print("please enter an argument")
            else:
                break
    if action not in['MLR','Decision tree classification']:
        raise ValueError("Invalid action: should be 'MLR' or 'Decision tree classification'")
    
    data = input('Insert the relative path of the csv file in the data folder:\n')

    data = ('./' + str(data))

    cutoff = input("Insert how many variables you don't want to put inside the model (from far left)\n")
    
    cutoff = int(cutoff)

    if action =='MLR':
        ax    = Prediction(data, cutoff)
        ax.multiple_linear()

    elif action == 'Decision tree classification':
        ax    = Prediction(data, cutoff)
        ax.decision_tree_classification()