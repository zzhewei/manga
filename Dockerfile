# FROM：基底映像檔
FROM python:3.6.8-stretch

# WORKDI：建立 working directory
WORKDIR /sample

# ADD：將檔案加到 images 內
ADD . /sample

# 只有build 時使用，會執行此命令
RUN pip install -r requirements.txt

# run container 時要執行的命令
#CMD python app.py