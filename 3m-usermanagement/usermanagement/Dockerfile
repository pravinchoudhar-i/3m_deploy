FROM python:3.10.5-slim-buster

# Corrected the path to requirements.txt
ADD 3m-usermanagement/usermanagement/requirements.txt /3m/requirements.txt

RUN apt-get update \
    && apt-get -y install libpq-dev gcc \
    && python -m venv /env \
    && /env/bin/pip install --upgrade pip \
    && /env/bin/pip install --no-cache-dir -r /3m/requirements.txt

# Corrected the path to add the project files
ADD 3m-usermanagement /3m-production
WORKDIR /3m-production

ENV VIRTUAL_ENV /env
ENV PATH /env/bin:$PATH

EXPOSE 8000

CMD ["gunicorn", "--bind", ":8000", "--workers", "3", "usermanagement.wsgi:application"]
