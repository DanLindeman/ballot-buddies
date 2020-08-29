FROM python:3.8

RUN  curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python
ENV PATH="/root/.poetry/bin:$PATH"

COPY . .
RUN poetry config virtualenvs.create false
RUN poetry install --no-dev
EXPOSE 5000
ENTRYPOINT ["make", "run"]