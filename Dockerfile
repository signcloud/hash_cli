FROM python:3.8
WORKDIR /usr/app/src
ADD requirements.txt .
RUN pip install -r requirements.txt
ADD sha.py .
ENTRYPOINT ["python", "sha.py"]