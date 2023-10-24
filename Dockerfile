FROM  python:3.11-alpine
# env
ENV VIRTUAL_ENV=/opt/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app
RUN apk add mc \
    && apk add --virtual build-deps gcc python3-dev musl-dev \
    && apk add --no-cache mariadb-dev

# configure user
RUN addgroup -g 2000 django \
    && adduser -u 2000 -G django -s /bin/sh -D django


RUN mkdir -p /app/logs/celery
RUN mkdir -p /app/run/celery
COPY requirements.txt /app
RUN pip3 install -r requirements.txt --no-cache-dir
COPY . /app

RUN chown -R django:django /app
ADD ./docker-entrypoint.sh /app
RUN chmod a+x /app/docker-entrypoint.sh
USER django


