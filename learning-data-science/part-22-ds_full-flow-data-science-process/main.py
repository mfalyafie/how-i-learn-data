from application import( 
        ModelTrainer, TestData
)

import argparse #type:ignore



if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("--action", help="'train' / 'test'", type=str)
    args = parser.parse_args()
    action = args.action
    if not action:
        while True:
            action = input("'train' or 'test'?\n")
            if not action:
                print('Please enter an argument')
            else:
                break
    if action not in ['train', 'test']:
        raise ValueError("Invalid action: should be 'train' or 'test'")

    
    if action == 'train':
        print("Training XGBoost Classifier.............")
        trainer = ModelTrainer()
        trainer.train()
        print("Training completed")
    elif action == 'test':
        print("test sentiment.............")
        test = TestData(20,"student","single","secondary","no",502,"no","no","cellular",261,1,-1,0,"unknown")
        #test = TestData(30,"unemployed","married","primary","no",1787,"no","no","cellular",19,1,-1,0,"unknown")
        test.test_data()