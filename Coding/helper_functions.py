import json
import numpy as np
import sys
sys.path.append("conll16st")
import aligner as aligner
import partial_scorer as ps
import read_write_files as rw
import itertools
import numpy as np
import matplotlib.pyplot as plt
from sklearn import svm, datasets
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix

def change_sets_to_list(alignments):
    for gold,pred in alignments:
        if gold != None:
            gold["Arg1"]["TokenIndexSet"] = list(gold["Arg1"]["TokenIndexSet"])
            gold["Arg2"]["TokenIndexSet"] = list(gold["Arg2"]["TokenIndexSet"])
        if pred != None:
            pred["Arg1"]["TokenIndexSet"] = list(pred["Arg1"]["TokenIndexSet"])
            pred["Arg2"]["TokenIndexSet"] = list(pred["Arg2"]["TokenIndexSet"])
        
    return alignments


def align_parsers_to_gold(gold_rel,parsers):
    total_alignment = {gold["ID"]:{"gold":gold,"parsers":[]} for gold in gold_rel}
    parsers_not_mappable = []
    
    parser_names = [name for name,parser in parsers]
    
    for name,parser_relations in parsers:
        arg1_alignment, arg2_alignment, relation_alignment = aligner.align_relations(
            gold_rel, 
            parser_relations, 
            0.7)
         
        relation_alignment = change_sets_to_list(relation_alignment)
        for gold_align,pred_align in relation_alignment:
            if gold_align == None:
                parsers_not_mappable += [pred_align]
            else:
                total_alignment[gold_align["ID"]]["parsers"] += [pred_align]
                total_alignment[gold_align["ID"]]["parser_names"] = parser_names
     
    return total_alignment,parsers_not_mappable


def get_sense_lists(relations):
    gold_senses = []
    parser_senses = []
    parser_names = relations[0]["parser_names"]
    
    for rel in relations:
        gold_senses += [rel["gold"]["Sense"][0]]
        
        parser_pred = []
        for parser in rel["parsers"]:
            if parser == None:
                parser_pred += ["None"]
            else:
                parser_pred += [parser["Sense"][0]]
        
        parser_senses += tuple([parser_pred])
    parser_senses_zip = list(zip(*parser_senses))
    
    return gold_senses,parser_senses_zip,parser_names


def plot_confusion_matrix(cm,
                          normalize=False,
                          title='Confusion matrix',
                          cmap=plt.cm.Blues):
    """
    This function prints and plots the confusion matrix.
    Normalization can be applied by setting `normalize=True`.
    """
    classes = []
    alpha = cm.alphabet
    for i in xrange(alpha.size()):
        classes += [alpha.get_label(i)]


    if normalize:
        cm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]
        print("Normalized confusion matrix")
    else:
        print('Confusion matrix, without normalization')

    print(cm)

    plt.imshow(cm, interpolation='nearest', cmap=cmap)
    plt.title(title)
    plt.colorbar()
    tick_marks = np.arange(len(classes))
    plt.xticks(tick_marks, classes, rotation=45)
    plt.yticks(tick_marks, classes)

    fmt = '.2f' if normalize else 'd'
    thresh = cm.max() / 2.
    for i, j in itertools.product(range(cm.shape[0]), range(cm.shape[1])):
        plt.text(j, i, format(cm[i, j], fmt),
                 horizontalalignment="center",
                 color="white" if cm[i, j] > thresh else "black")

    plt.tight_layout()
    plt.ylabel('True label')
    plt.xlabel('Predicted label')