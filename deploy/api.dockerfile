FROM python:3.7

RUN apt update && curl -sL https://deb.nodesource.com/setup_14.x | bash - && apt install nodejs -y
RUN npm install -g hgrep

RUN pip3 install sphinx==4.2.0 sphinx_rtd_theme==1.0.0 sphinx-autodoc-typehints==1.12.0 recommonmark==0.7.1 beautifulsoup4

RUN mkdir -p /src
WORKDIR /src

ADD api .
ADD healthcheck.sh .

RUN git clone https://github.com/tilt-dev/tilt-extensions.git
RUN ./parse_extensions.py
RUN tar zcf api-py.tgz api.py extensions/ modules/

# Setting SPHINXOPTS= empty for now due to extension docstring issues
RUN make html SPHINXOPTS=

RUN ./remove_prefix.py /src/_build/html/index.html > index_without_prefixes.html
RUN ./remove_prefix.py /src/_build/html/extensions.html > extensions_without_prefixes.html

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

RUN cat extensions_without_prefixes.html | hgrep "section[id]" > extensions.html
RUN echo "extensions:" > extensions.yaml
RUN cat extensions_without_prefixes.html | hgrep -a id "section[id], dl.function > dt" | \
  egrep "^(module-)?extensions" | \
  sed -e 's/module-extensions\.\(.*\)/  \1:/' \
      -e 's/extensions\.[^.]*\./  - /' \
  >> extensions.yaml

ENTRYPOINT echo "~done~"
