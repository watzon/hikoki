FROM python:3

WORKDIR /usr/src/app

RUN apt update
RUN apt install -y netcat
RUN pip install pipenv

COPY Pipfile .
COPY Pipfile.lock .

RUN pipenv install

COPY . .

ADD https://github.com/ufoscout/docker-compose-wait/releases/download/2.2.1/wait /wait
RUN chmod +x /wait

CMD pipenv run python -m userbot
