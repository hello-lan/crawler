# crawler



### 安装

```bash
pip3 install -r requirements.txt
```



### 启动

```bash
cd crawler/wineworld/wineworld/spiders
scrapy crawl wine
```



### 特别说明

1. 酒款年份爬虫 vintage 启动需要带路径参数（年份id的csv文件,其中第一列为酒款id，第二列为对应年份id），例如：

```
scrapy crawl vintage -a fpath=data/vintage_example.csv
```

