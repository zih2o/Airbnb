FROM python:latest
ENV PYTHONUNBUFFERED 1
WORKDIR /Users/parkjisu/Documents/workspace/private_project/Airbnb/Airbnb_docker/docker_workspace
COPY . .
RUN apt-get update
RUN pip install -r requirements.txt
EXPOSE 8000
# CMD ["bash", "-c", "python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]
