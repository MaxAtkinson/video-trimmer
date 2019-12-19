FROM python:3-alpine
RUN python -m pip install --upgrade pip
COPY . /app
WORKDIR /app
RUN apk add --no-cache musl-dev linux-headers g++ build-base jpeg-dev zlib-dev
RUN apk add --no-cache --virtual build-deps build-base linux-headers
RUN pip install -r requirements.txt
RUN apk del build-deps
ENTRYPOINT ["python"]
CMD ["api.py"]