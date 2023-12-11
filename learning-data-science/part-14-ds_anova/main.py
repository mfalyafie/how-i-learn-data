"""
    m.fauzanalyafie@gmail.com
    28-Agustus-2022 17:11
"""

from email import parser
from inspect import ArgSpec
from application import Anova
import argparse #type: ignore

if __name__ == '__main__':

    parser  =  argparse.ArgumentParser() 
    parser.add_argument("--action", help="'oneway' / 'twoway'", type=str)

    args    = parser.parse_args()
    action  = args.action
    if not action:
        while True:
            action      = input("'oneway' or 'twoway'?\n")
            if not action:
                print("please enter an argument")
            else:
                break
    if action not in['oneway','twoway']:
        raise ValueError("Invalid action: should be 'oneway' or 'twoway'")

    
    if action =='oneway':
        ax    = Anova()
        ax.one_way()
    elif action == 'twoway':
        ax    = Anova()
        ax.two_way()