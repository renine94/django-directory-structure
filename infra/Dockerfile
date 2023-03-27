FROM python:3.11

WORKDIR /app
RUN apt -y update

COPY ./requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY .  ./

RUN python manage.py test  --settings=riiid_django.settings_test

# TODO gunicorn process 추후 결정 (Server 스펙에 따라 결정)
CMD sh -c "python manage.py makemigrations --noinput && python manage.py migrate --noinput && python manage.py collectstatic --noinput && gunicorn riiid_django.wsgi --bind 0.0.0.0:8000"

EXPOSE 8000