"""
    m.fauzanalyafie@gmail.com
    4-September-2022 02:56
"""

from email import parser
from inspect import ArgSpec
from application import Regression
import argparse #type: ignore

if __name__ == '__main__':

    parser  =  argparse.ArgumentParser() 
    parser.add_argument("--action", help="'Simple linear' / 'MLR'", type=str)

    args    = parser.parse_args()
    action  = args.action
    if not action:
        while True:
            action      = input("'Simple linear' or 'MLR'?\n")
            if not action:
                print("please enter an argument")
            else:
                break
    if action not in['Simple linear','MLR']:
        raise ValueError("Invalid action: should be 'Simple linear' or 'MLR'")
    
    data = input('Insert the relative path of the csv file in the data folder:\n')

    data = ('./' + str(data))

    if action =='Simple linear':
        ax    = Regression(data)
        ax.simple_linear()
    elif action == 'MLR':
        ax    = Regression(data)
        ax.multiple_linear()