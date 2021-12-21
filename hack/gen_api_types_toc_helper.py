# Generates the CLI TOC
#
# Reads the auto-generated Cobra CLI docs.
# Reads docs.yml.
# Prints the new docs.yml to stdout.
# Must be run from the root of this repository.

typeCmds = [
  '        - title: Overview\n',
  '          href: api.html#types\n',
]
with open('docs/_data/api/classes.yaml') as f:
  file = f.readlines()
  file.pop(0)
  for line in file:
    name = line[2:]
    href = "modules." if "." in name else "api."
    href += name
    typeCmds.append('        - title: %s' % name)
    typeCmds.append('          href: api.html#%s' % href)

def find_index(lines, f):
  for l in lines:
    if f(l):
      return lines.index(l)
  return -1

with open('src/_data/docs.yml') as f:
  lines = f.readlines()
  start_line = find_index(lines, lambda l: '# Start Tiltfile Types Reference' in l)
  end_line = find_index(lines, lambda l: '# End Tiltfile Types Reference' in l)
  if start_line == -1 or end_line == -1:
    exit(1)

  new_lines = lines[0:start_line+1] + typeCmds + lines[end_line:]
  print(''.join(new_lines).rstrip())