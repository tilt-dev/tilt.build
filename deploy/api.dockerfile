FROM python:3.7

RUN curl -sSL https://github.com/ericchiang/pup/releases/download/v0.4.0/pup_v0.4.0_linux_amd64.zip -o pup.zip && unzip pup.zip && cp pup /usr/local/bin/pup

RUN pip3 install sphinx==4.2.0 sphinx_rtd_theme==1.0.0 sphinx-autodoc-typehints==1.12.0 recommonmark==0.7.1 beautifulsoup4

RUN mkdir -p /src
WORKDIR /src

ADD api .
RUN make html

RUN ./remove_prefix.py /src/_build/html/index.html > index_without_prefixes.html

# Correctly handle module variables (__var_name__)
RUN sed -i 's/file__/__file__/g' index_without_prefixes.html

RUN pup -f index_without_prefixes.html --pre "dl.function" > functions.html
RUN echo "functions:" > functions.yaml
RUN pup -f index_without_prefixes.html "dl.function > dt attr{id}" | \
  sed -e 's/^api./- /'  \
  >> functions.yaml

RUN pup -f index_without_prefixes.html --pre "dl.class" > classes.html
RUN echo "classes:" > classes.yaml
RUN pup -f index_without_prefixes.html "dl.class > dt attr{id}" | \
  sed -e 's/^api./- /'  \
  >> classes.yaml

RUN pup -f index_without_prefixes.html --pre "dl.data" > data.html
RUN echo "data:" > data.yaml
RUN pup -f index_without_prefixes.html "dl.data > dt attr{id}" | \
  sed -e 's/^api./- /'  \
  >> data.yaml

ENTRYPOINT echo "~done~"
