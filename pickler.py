__author__ = 'jamiebrew'

import cPickle as pickle


# saves an object to a file
def save_object(obj, filename):
    with open(filename, 'wb') as output:
        pickle.dump(obj, output, pickle.HIGHEST_PROTOCOL)

def loadobject(path):
    with open(path, 'rb') as input:
        bodyD = pickle.load(input)
    return bodyD