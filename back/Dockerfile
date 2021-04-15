FROM python:3.9.0-slim-buster

ENV PYTHONDONTWRITEBYTECODE 1
ENV WORK_DIR "/application/src"
ENV USER user
ENV GROUP usergroup

RUN apt update &&\
    apt install wkhtmltopdf -y

RUN mkdir -p ${WORK_DIR}
WORKDIR ${WORK_DIR}

RUN addgroup --system ${GROUP} &&\
    adduser --system --home ${WORK_DIR}/../user --ingroup ${GROUP} ${USER} --shell /bin/bash &&\
    chown -R ${USER}:${GROUP} ${WORK_DIR}/..

RUN pip install poetry &&\
    poetry config virtualenvs.create false
ADD poetry.lock .
ADD pyproject.toml .
RUN poetry install --no-dev

ADD . ${WORK_DIR}

RUN chmod -R og+w ${WORK_DIR}/media ${WORK_DIR}/static ${WORK_DIR}/project/fixtures/
# USER ${USER}

ENTRYPOINT ["/application/src/docker-entrypoint.sh"]
CMD ["run-web"]
