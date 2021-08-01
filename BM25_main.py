import os

def main():
    os.system('BM25_setting_environment.py')
    os.system('BM25_generate_scores.py')
    os.system('BM25_filter_and_index.py')
    os.system('BM25_calculate_matrics.py')
if __name__=='__main__':
    main()
