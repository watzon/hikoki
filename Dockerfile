FROM python:3

WORKDIR /usr/src/app

RUN pip install pipenv

COPY Pipfile .
COPY Pipfile.lock .

RUN pipenv install

COPY . .

CMD ["pipenv", "run", "python", "-m", "userbot"]
