FROM python:3.10.5-slim-buster

ENV DEBIAN_FRONTEND=noninteractive
ADD 3m-usermanagement/usermanagement/requirements.txt /3m-usermanagement/usermanagement/requirements.txt

RUN apt-get update \
    && apt-get -y install libpq-dev gcc \
    && python -m venv /env \
    && /env/bin/pip install --upgrade pip \
    && /env/bin/pip install --no-cache-dir -r /3m-usermanagement/usermanagement/requirements.txt

ADD . /3m-usermanagement
WORKDIR /3m-usermanagement


# Copy the .env file
COPY /.env /.env

ENV VIRTUAL_ENV /env
ENV PATH /env/bin:$PATH

EXPOSE 8000

CMD ["gunicorn", "--bind", ":8000", "--workers", "3", "usermanagement.wsgi:application"]
