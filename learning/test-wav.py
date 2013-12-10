#call to test a wav
import pickle
import sys
from itertools import imap, groupby
from operator import itemgetter
from chord import *

import feature

if len(sys.argv) < 2:
    data = "test1.wav"
else:
    data = sys.argv[1]

#load a trained model
#print "Loading model.."
model = pickle.load(open("../learning/trained/1train", "r"));

#extract features
#print "Extracting features.."
testex = feature.get_chroma(data);
#print "Predicting.."

outputseries = model.predict(testex.T);
#print "Results:"
outputcomp = list(imap(itemgetter(0), groupby(outputseries)));
print map(decode, outputcomp)
