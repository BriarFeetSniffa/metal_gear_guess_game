FROM python:3.11.5

RUN mkdir code
WORKDIR code

ADD requirements.txt /code/
RUN pip install -r requirements.txt

ADD . /code/
ADD .env.docker /code/.env

ENV APP_NAME = METAL_GEAR_GUESS_GAME

CMD gunicorn metal_gear_guess_game.wsgi:application -b 0.0.0.0:8000