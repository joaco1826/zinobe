FROM python:3.7-alpine3.9
RUN apk update \
    && pip install --upgrade pip

RUN apk add make automake gcc g++ subversion python3-dev

COPY requirements.txt /app-run/requirements.txt
RUN pip install -r /app-run/requirements.txt

WORKDIR /app-run
COPY . /app-run

CMD ["python", "-m", "server"]