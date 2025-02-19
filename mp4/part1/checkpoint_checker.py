import argparse

import numpy as np

def compare_checkpoints(number=1):
    """
    Compare the checkpoint generated by the agent.py with a checkpoint from the TAs.
    """

    ta_checkpoint_name = "checkpoint" + str(number) + ".npy"

    my_checkpoint = np.load('checkpoint.npy')
    ta_checkpoint = np.load(ta_checkpoint_name)

    differences = my_checkpoint == ta_checkpoint
    are_same = np.all(differences)

    print ("The checkpoints contain the same values: " + str(are_same))

    if not are_same:

        # find the locations where the arrays differ
        indx_diff = np.where(differences == False)
        print ("\nDifferences occur at the following locations in Q-table: ")
        location = []
        for i in range (np.shape(indx_diff)[1]):
            for j in range (np.shape(indx_diff)[0]):
                location.append(indx_diff[j][i])
            
            print ("\nAt : " + str(location) + " , the values are: ")
            print ("Mine: " + str(my_checkpoint[tuple(location)]))
            print ("TA's: " + str(ta_checkpoint[tuple(location)]))
            location = []

if __name__ == "__main__":
    """
    Usage:  python checkpoint#
            
            checkpoint# should range from 1-3
            if checkpoint# not specified, will run with checkpoint1.npy
    """

    parser = argparse.ArgumentParser()
    parser.add_argument('--checkpoint_num', type= int, default= 1, 
            help= 'choosing which checkpoint to compare with - default 1')
    arg = parser.parse_args()
    compare_checkpoints(arg.checkpoint_num)