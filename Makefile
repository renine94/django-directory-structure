##################################################################
# Run
##################################################################
run:
	@python manage.py runserver

run_prod:
	@python manage.py makemigrations --noinput \
		&& python manage.py migrate --noinput \
		&& python manage.py collectstatic --noinput \
		&& gunicorn core.wsgi --bind 0.0.0.0:8000

##################################################################
# Test (https://docs.djangoproject.com/en/3.2/topics/testing/overview/)
##################################################################
test:
	@python manage.py test  --settings=core.settings.test --parallel

##################################################################
# Migrate
##################################################################
makemigrations:
	@python manage.py makemigrations

migrate:
	@python manage.py migrate

migrate-self: makemigrations
	@python manage.py migrate

##################################################################
# Celery (Local)
##################################################################
run_worker:
	@celery -A core worker -l info --concurrency=2

run_beat:
	@celery -A core beat -l info

##################################################################
# Shell
##################################################################
notebook:
	@python manage.py shell_plus --note