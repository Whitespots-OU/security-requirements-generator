# Deploy
## Server
```bash
docker-compose up -d --build
docker-compose run back migrate
docker-compose run back collectstatic
docker-compose run back loaddata
docker-compose exec back ./manage.py create_super_user --username admin --password PASSWORD
open https://hostname.com/admin/  # to login and set your company name
```

## Local
### Back
- create virtualenv & install requirements
```bash
cd back
pyenv virtualenv 3.9.0 srg_back
pyenv activate srg_back
pip install poetry
poetry install
```
- call `pre-commit install` at command line
- create DB in pg market
- add envs from [.env.dev](back/.env.dev)
- apply DB migrations `./manage.py migrate`
- create super user `./manage.py create_super_user`
- run localserver `./manage.py runserver`
- open [admin panel](http://localhost:8000/admin/) and login as admin:admin
- call `make pre-commit` before making a commit

### Front
```bash
cd front
npm install
npm run serve
open http://localhost:8080
npm run build
```
