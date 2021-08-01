import zipfile

from ckiptagger import data_utils

def main():
    data_utils.download_data_gdown("./")
    zf=zipfile.ZipFile('data.zip','r')
    zf.extractall()

if __name__ == '__main__':
    main()
