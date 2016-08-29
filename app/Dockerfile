FROM python:3.5-alpine

ADD $PWD/app/requirements.txt /tmp/requirements.txt
RUN set -ex \
        && apk add --no-cache --virtual .build-deps  \
                musl-dev \
                gcc \
        && pip install  --no-cache-dir --upgrade --force-reinstall -r /tmp/requirements.txt \
        && apk del .build-deps \
        && rm /tmp/requirements.txt

WORKDIR /srv/app
CMD ["python", "-u", "-m", "server"]
