import os
import pandas as pd
import json
import click

from rich.console import Console
from tqdm import tqdm
from typing import List, Dict, Union

ANS_1  = 'answer_1'
ANS_2  = 'answer_2'
ANS_3  = 'answer_3'
PRED = 'prediction'

console=Console(record=True)

def final_result(directory: str):
    #import data
    console.print('Loading data')
    files = os.listdir(directory)
    result = []
    for filename in tqdm(files):
        file = directory+filename
        filename_breakdown = filename.split('_', 3)
        threshold = float(filename_breakdown[1])
        k = int(float(filename_breakdown[3][:-5]))
        with open(file, 'r', encoding='utf-8') as f:
            temp=json.load(f)
            f.close()
        accuracy, recall, precision, f1_score = calculate_metrics(temp)
        result.append({
            'threshold': threshold,
            'k': k,
            'accuracy': accuracy,
            'recall': recall,
            'precision': precision,
            'f1_score': f1_score
            })
    output_filename = directory+'f1_score_table.csv'
    result_df=pd.DataFrame(result)
    result_df.to_csv(output_filename, encoding='utf-8')
    console.print('Complete Calculations')

def calculate_metrics(outcome: List[Dict[str, Union[int, List[int]]]]):
    tp, fn, tn, fp = 0, 0, 0, 0
    for row in outcome:
        ans_1 = row[ANS_1] # int > -1 if there is true answer, -1 if there is no answer
        ans_2 = row[ANS_2] # int > -1 if there is true answer, -1 if there is no answer
        ans_3 = row[ANS_3] # int > -1 if there is true answer, -1 if there is no answer
        predicts = row[PRED] # List[int] if there topK prediction has sth > threshold, [] if no prediction
        if predicts: #there is prediction
            if ans_1 != -1 or ans_2 != -1 or ans_3 != -1: #there is at least one answer
                if ans_1 in predicts or ans_2 in predicts or ans_3 in predicts: 
                    tp = tp+1 #prediction hits either of the answer
                else:
                    fp = fp+1 #none of the answers were predicted
            else:
                fp = fp+1 # no ans, but there are predictions
        else:
            if ans_1 == -1 and ans_2 == -1 and ans_3 == -1: 
                tn = tn + 1 # no answer no predictions
            elif ans_1 != -1 or ans_2 != -1 or ans_3 != -1:
                fn = fn + 1 # there are one or more answers but no prediction
    assert len(outcome) == tp + fn + tn + fp
    
    accuracy  = (tp + tn) / (tp + fn + tn + fp)
    recall = tp / (tp + fn)
    precision = tp / (tp + fp)
    f1_score  = 2 * recall * precision / (recall + precision)

    accuracy, recall, precision, f1_score = map(lambda x: round(x, 4), [accuracy, recall, precision, f1_score])
    return accuracy, recall, precision, f1_score

@click.command()
@click.option('--filtered_predictions_directory', '-fpd', type=str, default='threshold_k/')

def main(filtered_predictions_directory: str):

    final_result(filtered_predictions_directory)
    
if __name__ == '__main__':
    main()
