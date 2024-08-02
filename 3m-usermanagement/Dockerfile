FROM python:3.10.5-slim-buster

ENV DEBIAN_FRONTEND=noninteractive

# Set working directory
WORKDIR /3m

# Copy and install dependencies
COPY 3m-usermanagement/usermanagement/requirements.txt /3m/requirements.txt
RUN apt-get update \
    && apt-get -y install libpq-dev gcc \
    && python -m venv /env \
    && /env/bin/pip install --upgrade pip \
    && /env/bin/pip install --no-cache-dir -r /3m/requirements.txt

# Copy application files
COPY 3m-usermanagement /3m

# Set environment variables
ENV VIRTUAL_ENV /env
ENV PATH /env/bin:$PATH

# Expose port
EXPOSE 8000

# Command to run the application
CMD ["gunicorn", "--bind", ":8000", "--workers", "3", "usermanagement.wsgi:application"]
