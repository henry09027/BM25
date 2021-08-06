# BM25

## Prerequiste
* tensorflow pip installed
* ckiptagger pip installed
* ckiptagger model saved under current directory in a folder named "data/" 
  * Model data can be downloaded and extracted to the desired path by one of the included API.
```
# Downloads to ./data.zip (2GB) and extracts to ./data/
# data_utils.download_data_url("./") # iis-ckip
data_utils.download_data_gdown("./") # gdrive-ckip
```

## DataSet (List of dictionaries)

* Label Set \
External queries each with 0-3 internal pairs. \
Example:
```
{
    "外規內容": "第b6至b8段提供評估資產對企業是否有其他用途之指引。",
    "應匹配的內規1內容": NaN,
    "應匹配的內規2內容": NaN,
    "應匹配的內規3內容": NaN
},
{
    "外規內容": "檢舉案件之受理及調查過程,有利益衝突之人,應予迴避。",
    "應匹配的內規1內容": "指派檢舉受理人員或專責單位。",
    "應匹配的內規2內容": NaN,
    "應匹配的內規3內容": "檢舉案件受理、處理過程、處理結果及相關文件製作之紀錄與保存。"
},
{
    "外規內容": "分離帳戶保險商品費用:係凡符合國際財務報導準則第四號保險合約定義之分離帳戶保險商品之各項費用總和皆屬之。",
    "應匹配的內規1內容": "分離帳戶保險商品費用。",
    "應匹配的內規2內容": NaN,
    "應匹配的內規3內容": NaN
}
```
* Internal Set \
A list of internal corpus. \
Example:
```
{
    "法規名稱": "1050323融資循環_捷智_V1@20170410 (1)",
    "內文": "股東權益"
},
{
    "法規名稱": "1050323融資循環_捷智_V1@20170410 (1-1)",
    "內文": "目的："
}
```
## Model Workflow
![alt text](https://github.com/henry09027/BM25/workflow_pic.png)
