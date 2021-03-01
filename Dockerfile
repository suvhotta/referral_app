FROM python:3.8-alpine

ENV PATH="/scripts:${PATH}"

COPY ./requirements.txt ./requirements.txt
RUN apk add --update --no-cache --virtual .tmp gcc libc-dev linux-headers
RUN apk update && apk add postgresql-dev gcc python3-dev musl-dev
RUN pip install -r /requirements.txt
RUN apk del .tmp

RUN mkdir /app
COPY ./ /app
WORKDIR /app
COPY ./scripts /scripts

RUN chmod +x /scripts/*

RUN mkdir -p /vol/web/media
RUN mkdir -p /vol/web/static

RUN adduser -D user &&\
    chown -R user:user /vol &&\
    chmod -R 755 /vol/web

CMD [ "entrypoint.sh" ]

