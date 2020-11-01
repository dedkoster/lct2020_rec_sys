FROM python:3.8.6

ENV app lct_rec
WORKDIR /$app

RUN mkdir -p /$app/models && chmod -R 777 /$app/models

COPY main.py /$app/main.py

COPY requirements.txt /$app/requirements.txt
RUN pip install -r requirements.txt

COPY src /$app/src

CMD python main.py
