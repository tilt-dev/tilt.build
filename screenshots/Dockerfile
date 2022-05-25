FROM tiltdev/tilt:latest

RUN apt-get update && apt-get install -y --no-install-recommends \
  curl less firefox-esr python3 python3-pip python-is-python3 unzip

ENV GECKODRIVER_VERSION 0.31.0

RUN curl -SL https://github.com/mozilla/geckodriver/releases/download/v$GECKODRIVER_VERSION/geckodriver-v$GECKODRIVER_VERSION-linux64.tar.gz | tar -C /usr/local/bin -zxf -

WORKDIR /app

COPY requirements.txt /app
RUN pip3 install -r requirements.txt

COPY . /app

CMD ["/app/main.sh"]
