FROM alpine:3.3

ENV PROJECT_DIR=/app



RUN apk add --update \
    python \
    python-dev \
    py-pip \
    build-base \
  && rm -rf /var/cache/apk/*

VOLUME $PWD/*:/test
# add requirements.txt to the image
ADD requirements.txt /app/requirements.txt

WORKDIR $PROJECT_DIR
COPY . $PROJECT_DIR

ONBUILD COPY . /app
ONBUILD RUN pip install -r /app/requirements.txt

# create unprivileged user
RUN addgroup -S app && adduser -S -g app app