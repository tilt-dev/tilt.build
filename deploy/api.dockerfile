FROM python:3.7

RUN curl -sL https://deb.nodesource.com/setup_10.x | bash -
RUN apt update && apt install nodejs -y
RUN npm install -g hgrep

RUN pip3 install sphinx==1.8.3 sphinx_rtd_theme==0.4.2 sphinx-autodoc-typehints==1.6.0 recommonmark==0.5.0

RUN mkdir -p /src
WORKDIR /src

ADD api .
RUN make html

RUN cat /src/_build/html/index.html | hgrep "dl.function" > functions.html
RUN echo "functions:" > functions.yaml
RUN cat /src/_build/html/index.html | hgrep -a id "dl.function > dt" | sed -e 's/^api./- /' >> functions.yaml

RUN cat /src/_build/html/index.html | hgrep "dl.class" > classes.html
RUN echo "classes:" > classes.yaml
RUN cat /src/_build/html/index.html | hgrep -a id "dl.class > dt" | sed -e 's/^api./- /' >> classes.yaml

RUN cat /src/_build/html/os.html | hgrep "dl.data" > os_data.html
RUN echo "data:" > os_data.yaml
RUN cat /src/_build/html/os.html | hgrep -a id "dl.data > dt" | sed -e 's/^modules.os./- /' >> os_data.yaml

ENTRYPOINT echo "~done~"
