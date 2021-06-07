FROM node:lts-alpine

ENV WORK_DIR "/application/src"
ENV USER user
ENV GROUP usergroup

RUN mkdir -p ${WORK_DIR}
WORKDIR ${WORK_DIR}

RUN addgroup --system ${GROUP} &&\
    adduser --system --home ${WORK_DIR}/../user --ingroup ${GROUP} ${USER} --shell /bin/bash &&\
    chown -R ${USER}:${GROUP} ${WORK_DIR}/..

COPY package*.json ./
RUN npm install

COPY . .

RUN npm run build

# USER ${USER}
