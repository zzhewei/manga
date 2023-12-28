# The Heaven
[![Manga CI](https://github.com/zzhewei/manga/actions/workflows/main.yml/badge.svg)](https://github.com/zzhewei/manga/actions/workflows/main.yml)
[![codecov](https://codecov.io/gh/zzhewei/manga/graph/badge.svg?token=WUGQT1JIXN)](https://codecov.io/gh/zzhewei/manga)
[![Imports: isort](https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336)](https://pycqa.github.io/isort/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

## Getting Started
**這是一個紀錄常看的漫畫網址及精彩的頁數，有簡單實現使用者管理及權限部分。下面是如何安裝和使用這個工具的步驟。**

### Prerequisites
* python3.9
* pip
* redis
* 啟動gmail的二階段認證

### Installing
**1.clone repository 到 local。**
```shell
git clone https://github.com/zzhewei/manga.git
```

**2.安裝相關套件**
```shell
cd manga
pip install -r requirements.txt
```

**3.初始化資料庫**
```shell
python -m flask init
```

**4. 修改 config.py 裡的 MAIL_USERNAME、MAIL_PASSWORD 及資料庫參數** 

**5. 在另一個 console 輸入( linux 可不輸 -P eventlet )**
```shell
celery -A app.celery_app worker --loglevel info -P eventlet 
```

### Usage
**1.命令列輸入:**
```shell
python -m flask run --host=0.0.0.0
```

### 運行測試
```shell
python -m pytest .
```

**可在 htmlcov/index.html 觀看覆蓋率報告**

**reference : https://myapollo.com.tw/zh-tw/pytest-coverage/**

### And coding style tests
**想分析測試專案程式碼，可另外使用 pylint 進行分析**

**首先**
```shell
pip install pylint
```

**之後針對要分析的py檔執行:**
```shell
python -m pylint main.py
```
**即可觀看測試結果**


## 常用指令
### 自動生成 requirements.txt
```shell
pipreqs ./ --encoding=utf8 --force 
```

### 根據 dockerfile 產生 container
```shell
docker image build -t 'imagename' .

docker run -d -p 80:8888 --name 'containername' 'imagename'
```

### 根據 docker-compose.yml 產生 container
**1. 更改 config.py 的 sql 連線**

**2. 建立**
```shell
docker-compose up -d
```

**3. 進入容器內**
```shell
docker exec -it 'flaskname' /bin/bash
```

**4. 建立初始資料**
```shell
python -m flask init
```

### i18語言包
**1. 生成 messages.pot**
```shell
pybabel extract -F babel.cfg -k lazy_gettext -o messages.pot .
```

**2. 輸入**
```shell
pybabel update -i messages.pot -d translations
```

*( 如果沒有資料夾的初始化 )*
```shell
pybabel init -i messages.pot -d translations -l lan
```

**3. 翻譯 messages.po**

**4. 輸入**
```shell
pybabel compile -d translations
```

### 效能分析
**set FLASK_ANALYZE = True**

**進入 pstat_files 資料夾並輸入**
```shell
snakeviz 'filename'
```

**reference : https://myapollo.com.tw/zh-tw/profiling-flask/**


## Contributing

Please read [CONTRIBUTING.md](https://gist.github.com/PurpleBooth/b24679402957c63ec426) for details on our code of conduct, and the process for submitting pull requests to us.


## Authors

* **ZheWei** - *Initial work* - [ZheWei](https://github.com/zzhewei)
