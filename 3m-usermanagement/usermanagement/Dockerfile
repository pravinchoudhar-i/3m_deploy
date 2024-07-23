FROM python:3.10.5-slim-buster

ADD 3m-usermanagement/usermanagement/requirements.txt /3m-usermanagement/usermanagement/requirements.txt

RUN apt-get update \
    && apt-get install -y libpq-dev gcc \
    && python -m venv /env \
    && /env/bin/pip install --upgrade pip \
    && pip install -r /3m-usermanagement/usermanagement/requirements.txt

ADD . /3m-usermanagement/usermanagement
WORKDIR /3m-usermanagement/usermanagement

ENV VIRTUAL_ENV /env
ENV PATH /env/bin:$PATH

EXPOSE 8000

CMD ["gunicorn", "--bind", ":8000", "--workers", "3", "usermanagement.wsgi:application"]
