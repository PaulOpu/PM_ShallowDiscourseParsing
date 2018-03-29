import json
import numpy as np
import sys
sys.path.append("conll16st")
import aligner as aligner
import partial_scorer as ps
import read_write_files as rw

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