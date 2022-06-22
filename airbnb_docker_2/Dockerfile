FROM python:3.9-alpine
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
WORKDIR /web
COPY . .

RUN pip install --upgrade pip

RUN apk update \
    && apk add --virtual build-dependencies gcc python3-dev musl-dev \
    && apk add zlib-dev jpeg-dev libjpeg \
    && pip install Pillow==8.1 \
    && apk del build-dependencies

RUN pip install -r requirements.txt

# RUN pip install pipenv \
#     && pipenv install flake --dev \
#     && pipenv install black --dev --pre