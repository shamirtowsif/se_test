# se_test

Minimal Django + MySQL + Redis setup using Docker Compose.

## Run

```bash
docker compose up --build
```

## In a separate terminal run

```bash
docker compose exec web python manage.py makemigrations main
docker compose exec web python manage.py migrate
docker compose exec web python manage.py createsuperuser
```

## Unit tests

Run tests in Docker:

```bash
docker compose exec web python manage.py test --settings=se_test.test_settings
```
