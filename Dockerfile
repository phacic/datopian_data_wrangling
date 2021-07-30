FROM python:3.7
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1
# set working directory
WORKDIR /app

# Copy requirements.txt to get cache to work here
COPY ./requirements.txt /app/
RUN pip install -r requirements.txt
COPY . /app/