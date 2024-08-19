FROM python:3

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update && apt-get install -y \
    binutils \
    libproj-dev \
    gdal-bin \
    libgdal-dev \
    python3-gdal \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

RUN pip install psycopg2-binary

WORKDIR /usr/src/app
COPY requirements.txt ./
ADD . /usr/src/app/
RUN pip install --upgrade pip && pip install -r requirements.txt
# RUN python manage.py migrate

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]