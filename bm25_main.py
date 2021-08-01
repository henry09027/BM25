import json
import click

from tqdm import tqdm
from ckiptagger import WS
from BM25_model import BM25_Model

@click.command()
@click.option('--internal', '-i', type=str, default='../data0716/internal.json')
@click.option('--label', '-l', type=str, default='../data0716/label-test.json')
@click.option('--output_dir', '-o', type=str, default='model_generations/')
@click.option('--data_path', '-dp', type=str, default='../data')

def main(internal: str, label: str, output_dir: str, data_path: str):
    
    #loading data
    ws = WS(data_path)
    with open(internal, 'r', encoding='utf-8') as f:
        internal = json.load(f)
        f.close()
    
    with open(label, 'r', encoding='utf-8') as f:
        label_test = json.load(f)
        f.close()
        
    #tokenize all internal corpus and send to BM25 model
    tokenized_internal = ws(internal)
    bm25_model = BM25_Model(tokenized_internal)
    result =[]
    
    #tokenize external query and get a list of similarity scores for all internal corpus
    #here I combine the list of scores and list of internal to create a dictionary
    for dic in tqdm(label_train):
        
        tokenized_query = ws([str(dic['外規內容'])])[0]
        document_score = bm25_model.get_documents_score(tokenized_query)
        internal_scores = dict(zip(internal, document_score))
        top_internals = sorted(internal_scores, key=internal_scores.get, reverse=True)[:100]
        top_internals_dict = {}
        for i in top_internals:
            top_internals_dict.update({i:internal_scores[i]})
        result.append({'label':dic['外規內容'], 'prediction': top_internals_dict, 'answer_1':dic["應匹配的內規1內容"], \
                      'answer_2':dic["應匹配的內規2內容"], 'answer_3':dic["應匹配的內規3內容"]})
     
    #saving result
    output_path = output_dir+'result.json'
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(result,f,ensure_ascii=False,indent=4)
        
if __name__ == '__main__':
    main()
