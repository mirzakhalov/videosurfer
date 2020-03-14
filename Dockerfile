# Dockerfile
FROM python:3.7-stretch
ENV PYTHON_VERSION 2.7.15
RUN apt-get update -y
RUN apt-get install -y python-pip python-dev build-essential
COPY src/ /app
COPY ./ /app
WORKDIR /app
RUN python3 -m pip install Flask gunicorn
RUN python3 -m pip install -r requirements.txt
RUN python2 -m pip install -r requirements2.txt
#ENTRYPOINT ["python3"]
#CMD ["app.py"]
# 4
ENV PORT 8080

# 5
CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 app:app