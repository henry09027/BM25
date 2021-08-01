import click
import json
import numpy as np
import copy

from rich.console import Console
from tqdm import tqdm

console=Console(record=True)

def get_results(output_directory, internal_dictionary, prediction, max_threshold, mini_threshold, max_k, mini_k):
    console.print('Start Filtering and Indexing')
    threshold_range = np.linspace(mini_threshold, max_threshold, 20)
    k_range = [1, 5, 10, 20] #here I am custumizing the k_range so didn't use mini_k and max_k
    for threshold in tqdm(threshold_range):
        for k in k_range:
            temp_prediction = copy.deepcopy(prediction)
            filtered_predictions = filter_predictions(prediction=temp_prediction, k=k, threshold=threshold)
            result = index_predictions(internal_dictionary=internal_dictionary, prediction=filtered_predictions)
            filename = f"threshold_{threshold}_k_{k}.json"
            with open(output_directory+filename, 'w', encoding='utf-8') as f:
                json.dump(result, f, ensure_ascii=False,indent=4)
    console.print('Filtering and Indexing Completed')

def filter_predictions(prediction, k, threshold):
    for dic in prediction:
       # filter threshold
        for key_ in dic['prediction'].copy():
            if float(dic['prediction'][key_])<float(threshold):
                del dic['prediction'][key_]
        #filter top k -> list of keys(internal)
        dic['prediction'] = sorted(dic['prediction'], key=dic['prediction'].get,reverse=True)[:int(k)]
    return prediction

def index_predictions(internal_dictionary, prediction):
        
    #map internal to index
    for dic in prediction:
        temp = []
        for internal_ in dic['prediction']:
            temp.append(internal_dictionary[str(internal_)])
        dic['prediction']=temp
        if dic['answer_1'] == dic['answer_1']:
            dic['answer_1'] = internal_dictionary[str(dic['answer_1'])]
        else: dic['answer_1'] -1
        if dic['answer_2'] == dic['answer_2']:
            dic['answer_2'] = internal_dictionary[str(dic['answer_2'])]
        else: dic['answer_2'] = -1
        if dic['answer_3'] == dic['answer_3']:
            dic['answer_3'] = internal_dictionary[str(dic['answer_3'])]
        else: dic['answer_3'] = -1
    return prediction

@click.command()
@click.option('--internal', '-i', type=str, default='../train_data/data0716/internal_dictionary.json')
@click.option('--merged_predictions', '-mp', type=str, default='model_generations/result.json')
@click.option('--output_directory', '-o', type=str, default='threshold_k/')
@click.option('--max_threshold', '-max_t', type=float, default=9.5)
@click.option('--mini_threshold', '-mini_t', type=float, default=0)
@click.option('--max_k', '-max_k', type=int, default=20)
@click.option('--mini_k', '-mini_k', type=int, default=5)

def main(internal: str, merged_predictions: str, output_directory: str, max_threshold: float, mini_threshold: float, max_k: int, mini_k: int):
    
    #load internal
    with open(internal,'r',encoding='utf-8') as i:
        internal_dictionary = json.load(i)
        i.close()    
    with open(merged_predictions,'r',encoding='utf-8') as l:
        prediction = json.load(l)
        l.close()
    get_results(
        output_directory=output_directory, 
        internal_dictionary=internal_dictionary,
        prediction=prediction,
        max_threshold=max_threshold,
        mini_threshold=mini_threshold,
        max_k=max_k,
        mini_k=mini_k
        )
    
if __name__ == '__main__':
    main()
