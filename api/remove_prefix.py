#!/usr/bin/env python

# sphinx prefixes names with their module name, e.g. `api.docker_build` or `modules.os.environ`
# we don't want the "api" or "modules" to appear in our docs, since those are
# artifacts of how we're writing the docs, and not relevant to the Tiltfile or user
# there doesn't appear to be a simple way to fix this via sphinx / autodoc, so this script strips those out after the fact.

import sys
from bs4 import BeautifulSoup

def print_without_module_prefixes(filename):
  with open(filename) as f:
    soup = BeautifulSoup(f, features='html.parser')

  for t in soup.find_all('code', class_='descclassname'):
    s = t.string
    s = s.replace('api.', '').replace('modules.', '')
    t.string.replace_with(s)

  print(soup.prettify())

for f in sys.argv[1:]:
  print_without_module_prefixes(f)
