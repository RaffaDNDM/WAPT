#######################
# @author: RaffaDNDM
# @date:   2022-09-17
#######################

import math
from termcolor import cprint
import matplotlib.pyplot as plt

ALPHABETS={
    'lower case' : 'abcdefghijklmnopqrstuvwxyz',
    'upper case' : 'ABCDEFGHIJKLMNOPQRSTUVWXYZ',
    'special IT': 'àáèéìíóòùú',
    'top-level characters': "'!@#$%^&*()",
    'numeric': "0123456789",
    'additional characters': r"""~`-_=+[]{}\|;:'",.<>?/"""
}

BAR_COLORS = {
    'weak': 'red',
    'medium': 'orange',
    'reasonable': 'yellow',
    'strong': 'green'
}

def entropy(password:str):
    global ALPHABETS
    # E = log_2(R^L) = L * log_2(R) = L * log(R) / log(2)
    # where:
    # R - Size of the pool of unique characters from which we build the password; and
    # L - Password length, i.e., the number of characters in the password.

    length = len(password)

    POOL_SETS = set()

    for c in password:
        for pool in ALPHABETS:
            if c in ALPHABETS[pool]:
                POOL_SETS.add(pool)
                break

    pool_size=0
    for pool in POOL_SETS:
        pool_size += len(ALPHABETS[pool])
    
    return length*math.log2(pool_size)

# importing library
import matplotlib.pyplot as plt
  
# function to add value labels
def addlabels(y,labels):
    for i in range(len(y)):
        plt.text(i, y[i], labels[i], ha = 'center', Bbox = dict(boxstyle='sawtooth', edgecolor='black', facecolor='white', alpha =1.))

def main():
    global BAR_COLORS

    PASSWORDS_LIST=[]
    ENTROPY_LIST=[]
    COLORS_LIST=[]
    LABELS_LIST=[]

    fig = plt.figure(figsize = (10, 5))

    # creating the bar plot
    plt.bar(PASSWORDS_LIST, ENTROPY_LIST, color ='maroon', width = 0.4)
    
    plt.xlabel("Courses offered")
    plt.ylabel("No. of students enrolled")
    plt.title("Students enrolled in different courses")

    plt.show(block=False)

    try:
        while True:
            cprint("Type the password to be tested (CTRL+C to exit):", 'blue')
            pwd = input()
            pwd_entropy = entropy(pwd)
            strength = 'strong'

            if pwd_entropy<25:
                strength = 'weak'
            elif pwd_entropy<50:
                strength='medium'
            elif pwd_entropy<75:
                strength='reasonable'

            PASSWORDS_LIST.append(pwd)
            ENTROPY_LIST.append(pwd_entropy)
            LABELS_LIST.append(strength)
            COLORS_LIST.append(BAR_COLORS[strength])

            plt.clf()
            plt.bar(PASSWORDS_LIST, ENTROPY_LIST, color =COLORS_LIST, width = 0.4)
            addlabels(ENTROPY_LIST, LABELS_LIST)
            plt.show(block=False)

    except KeyboardInterrupt:
        plt.show()
        exit(0)

if __name__=="__main__":
    main()