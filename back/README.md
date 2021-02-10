# Deploy
## Server side
This bash script will run services on 80 & 443 and create `./data/` folder with Postgres data.
1. Define envs from .end.docker
2. Execute:
```bash
docker-compose up -d --build
docker-compose run back migrate
docker-compose run back collectstatic
docker-compose exec back ./manage.py create_super_user --username admin --password sup-pass-123
open https://hostname.com/admin/  # to login and set your company name
```

## Local
- create virtualenv & install requirements
```bash
pyenv virtualenv 3.9.0 muze_back
pyenv activate muze_back
pip install poetry
poetry install
```
- call `pre-commit install` at command line
- create DB in pg market
- add envs from [.env.dev](.env.dev)
- apply DB migrations `./manage.py migrate`
- create super user `./manage.py create_super_user`
- run localserver `./manage.py runserver`
- open [admin panel](http://localhost:8000/admin/) and login as admin:admin
- call `make pre-commit` before making a commit