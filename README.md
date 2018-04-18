# Starting

App can be run locally or in the docker image. Local version support pytest based tests.

## Running locally

Install requirements:

`pip install -r requirements.txt`

Start application on port 0.0.0.0:8000

`python main.py`

Running tests requires `pip install pytest-aiohttp` (I used version 0.3.0) and done with

`pytest`

## Building and running docker image

**Building docker image can consume a lot of traffic and disk space. It's not optimal in terms of
size. Smaller python image should be used instead of whole Fedora.** First we need build the image
with

`docker build -t booking:latest .`

After build process finished, you can start application with

`docker run --rm -p 8000:8000 booking:latest`

Dockerized application will listen for the same 0.0.0.0:8000 address/port pair.

# Notes

App has no persistent storage. That means that restarting will start it from scratch. aiohttp app
used as a storage, it supports dictionary protocol.

No authentication or authorization implemented.
