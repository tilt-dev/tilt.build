FROM python:3.7

RUN curl -sL https://deb.nodesource.com/setup_14.x | bash -
RUN apt update && apt install nodejs -y
RUN npm install -g hgrep

RUN pip3 install sphinx==1.8.3 sphinx_rtd_theme==0.4.2 sphinx-autodoc-typehints==1.6.0 recommonmark==0.5.0 beautifulsoup4

RUN mkdir -p /src
WORKDIR /src

ADD api .
RUN make html

RUN ./remove_prefix.py /src/_build/html/index.html > index_without_prefixes.html

# Correctly handle module variables (__var_name__)
RUN sed -i 's/file__/__file__/g' index_without_prefixes.html

RUN cat index_without_prefixes.html | hgrep "dl.function" > functions.html
RUN echo "functions:" > functions.yaml
RUN cat index_without_prefixes.html | hgrep -a id "dl.function > dt" | \
  sed -e 's/^modules./- /' | sed -e 's/^api./- /'  \
  >> functions.yaml

RUN cat index_without_prefixes.html | hgrep "dl.class" > classes.html
RUN echo "classes:" > classes.yaml
RUN cat index_without_prefixes.html | hgrep -a id "dl.class > dt" | \
  sed -e 's/^modules./- /' | sed -e 's/^api./- /'  \
  >> classes.yaml

RUN cat index_without_prefixes.html | hgrep "dl.data" > data.html
RUN echo "data:" > data.yaml
RUN cat index_without_prefixes.html | hgrep -a id "dl.data > dt" | \
  sed -e 's/^modules./- /' | sed -e 's/^api./- /'  \
  >> data.yaml

ENTRYPOINT echo "~done~"
