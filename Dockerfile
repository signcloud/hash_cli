WORKDIR /usr/app/src

COPY ./requirements.txt /usr/app/src/requirements.txt

RUN pip install -r requirements.txt

COPY sha.py ./

ENTRYPOINT ["python3", "./sha.py"]