FROM python:3.11

WORKDIR /app

RUN apt -y update

COPY ../requirements .

RUN pip install -r requirements/prod.txt

COPY ..  ./

RUN python manage.py test  --settings=core.settings.test

# TODO gunicorn process 추후 결정 (Server 스펙에 따라 결정)
CMD sh -c "python manage.py makemigrations --noinput && python manage.py migrate --noinput && python manage.py collectstatic --noinput && gunicorn core.wsgi --bind 0.0.0.0:8000"

EXPOSE 8000