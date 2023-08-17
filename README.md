# The Heaven
[![Manga CI](https://github.com/zzhewei/manga/actions/workflows/main.yml/badge.svg)](https://github.com/zzhewei/manga/actions/workflows/main.yml)
[![codecov](https://codecov.io/gh/zzhewei/manga/graph/badge.svg?token=WUGQT1JIXN)](https://codecov.io/gh/zzhewei/manga)

## Getting Started
**這是一個紀錄常看的漫畫網址及精彩的頁數，有簡單實現使用者管理及權限部分。下面是如何安裝和使用這個工具的步驟。**

### Prerequisites
* python3.9
* pip
* redis
* 啟動gmail的二階段認證

### Installing
**1.clone repository到local。**
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

**4. 修改config.py裡的MAIL_USERNAME、MAIL_PASSWORD及資料庫參數** 

**5. 在另一個console輸入(linux可不輸 -P eventlet)**
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
python -m pytest -x -v --cov=./ --cov-report=html --cov-config=.coveragerc
```

**可在 htmlcov/index.html 觀看覆蓋率報告**

**reference:https://myapollo.com.tw/zh-tw/pytest-coverage/**

### And coding style tests
**想分析測試專案程式碼，可另外使用pylint進行分析**

**首先**
```shell
pip install pylint
```

**之後針對要分析的py檔執行:**
```shell
python -m pylint main.py
```
**即可觀看測試結果**


# 常用指令
## 自動生成requirements.txt
```shell
pipreqs ./ --encoding=utf8 --force 
```

## 根據dockerfile產生container
```shell
docker image build -t 'imagename' .

docker run -d -p 80:8888 --name 'containername' 'imagename'
```

## 根據docker-compose.yml產生container
**1. 更改config.py的sql連線**

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

## i18語言包
**1. 生成 messages.pot**
```shell
pybabel extract -F babel.cfg -k lazy_gettext -o messages.pot .
```

**2. 輸入**
```shell
pybabel update -i messages.pot -d translations
```

*(如果沒有資料夾的初始化)*
```shell
pybabel init -i messages.pot -d translations -l lan
```

**3. 翻譯 messages.po**

**4. 輸入**
```shell
pybabel compile -d translations
```

## flask profiling
**set FLASK_ANALYZE = True**

**enter pstat_files and in cmd "snakeviz 'filename under the pstat_files'"**

**reference:https://myapollo.com.tw/zh-tw/profiling-flask/**


## Contributing

Please read [CONTRIBUTING.md](https://gist.github.com/PurpleBooth/b24679402957c63ec426) for details on our code of conduct, and the process for submitting pull requests to us.

## Versioning

We use [SemVer](http://semver.org/) for versioning. For the versions available, see the [tags on this repository](https://github.com/your/project/tags). 

## Authors

* **ZheWei** - *Initial work* - [ZheWei](https://github.com/zzhewei)
