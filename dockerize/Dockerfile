FROM python

ARG PROJECT_DIR="/config"

COPY . ${PROJECT_DIR}

WORKDIR ${PROJECT_DIR}

RUN pip install --upgrade pip && pip install -r requirements.txt

CMD python manage.py runserver 0:8000 --settings=config.settings.local

EXPOSE 8000