FROM python:3.12-slim

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends build-essential default-libmysqlclient-dev pkg-config && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
# CMD ["/bin/sh", "-c", "python manage.py collectstatic --noinput && gunicorn --bind 0.0.0.0:8080 se_test.wsgi:application"]
CMD ["/bin/sh", "-c", "python manage.py migrate && python manage.py collectstatic --noinput && gunicorn --bind 0.0.0.0:8080 se_test.wsgi:application"]
