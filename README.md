# 코드 실행
1. `docker-compose -f infra/docker-compose.yml up -d`
   - 실행전, 본인 로컬에서 8000, 5432, 6379, 80번 포트 사용중인걸 모두 종료해주세요.

# .env
```shell
# API KEY
OPENAI_API_KEY='...'

# DJANGO
SECRET_KEY='django-insecure-2tayt=1zq!ng9(@6hrhkzz+w@ogoxf_c9f7gj3tk_*$dck%!o%'

# DB
DB_NAME='postgres'
DB_USER='postgres'
DB_PASSWORD='postgres'
DB_HOST='db'
DB_PORT='5432'

# Cache
REDIS_HOST='redis://redis:6379/0'

```

# 환경
1. python 3.11.2
2. django 4.1.7 (port: 8000)
3. redis (port: 6379)
4. postgreSQL (port: 5432)
5. nginx (port: 80)
