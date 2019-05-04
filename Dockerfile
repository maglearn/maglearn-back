FROM python:3.7.3-stretch

EXPOSE 5000

# Update system
RUN apt-get update && apt-get install -y \
    build-essential \
    python-dev

# Install pipenv
RUN pip3 install pipenv

RUN mkdir /app
WORKDIR /app

# Install dependencies
COPY Pipfile Pipfile
# COPY Pipfile.lock Pipfile.lock
RUN set -ex && pipenv install

# Install app
COPY . /app
VOLUME /app/instance

ENTRYPOINT ["pipenv", "run", "flask"]
CMD ["--help"]
