# About
Application Security requirements generator, based on ASVS, OWASP Testing guide and some experience :)

![App homescreen](/images/requirements.png?raw=true "App homescreen")

## More about the problem
Many of you have seen a huge set of requirements from OWASP and met developers faces with many words to your side about such a big document.
If not - you may find it [here](https://owasp.org/www-pdf-archive/OWASP_Application_Security_Verification_Standard_4.0-en.pdf) and try to share it to devs without prepairing them :)

## What we did
- Split ASVS requirements by functionality
- Have added a function to mark some requirements as important (so your devs can start from them for example)
- Mapped requirements to tests
- Shared it for you in this repository and [on our subdomain](https://requirements.whitespots.io/en)

## Now you can
- Use our free tool online [here](https://requirements.whitespots.io/en)
- Use our free tool in your infrastructure (see instructions below)

And have a useful set of **important** and **relevant** requirements:

![pdf](/images/pdf_download.png?raw=true "pdf")

# Clone
```bash
git clone https://github.com/Whitespots-OU/security-requirements-generator.git srg && \
cd srg
```

# Deploy
## Server
```bash
export BASE_URL=http://hostname.com
docker-compose up -d --build
docker-compose run back migrate
docker-compose run back loaddata
docker-compose run back collectstatic
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
- set environments
```bash
export DEBUG=on
export ALLOWED_HOSTS=*
export BASE_URL=http://localhost:8000
export REDIS_DSN=redis://localhost:6379/0
export DB_USER=user
export DB_PASS=pass
export DB_HOST=localhost
export DB_NAME=srg
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

# FAQ
### How to add my own categories (app functions), requirements and tests?
1. Just visit <your_host>/admin and login to the django admin 
2. Go to categories/requrements/tests (depends on what do you want to add/edit)
3. After that execute `docker-compose run back dumpdata`
It will make a dump of all your current categories, requirements and tests config

### How to contribute categories, requrements, tests?
This is not going to cover ALL possible requirements, described in full OWASP ASVS.
Instead, this tool was designed to help small teams to follow the most important and relevant stuff.

1. Before adding something new, try to find the same requirement/test/category in existing data
2. Feel free to describe existing tests/requirements better
3. Describe your changes in merge request 
- Put your changes in a title: New category/New requirements/New tests 
- Describe in the text which problems have been solved and which have not 

# Contributors

## Development
@alex-deus - Did all this nice repositories with working code

## Idea drivers
- @sarosbacz - Noticed, that requirements are mixed with tests without categories
- @httpnotonly - Brought everyone together

## Special thanks for working with content
- @totoshky - Complexity reduction and refactoring according to recent security trends
- @edgesec
- @W0uldYk1ndlY

## Hackers
- @acrono - Gave us more requirements and tests
- @a_ashwarya - Gave us more requirements and tests

