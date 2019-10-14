FROM python:alpine

RUN apk --no-cache add build-base python-dev jpeg-dev zlib-dev && \
    pip install pillow tornado && \
    apk del build-base python-dev && \
    mkdir hash2image

COPY . /hash2image

RUN chmod +x /hash2image/start.sh

WORKDIR /hash2image

EXPOSE 8099

CMD ["/hash2image/start.sh"]
