# Generates the CLI TOC
#
# Reads the auto-generated Cobra CLI docs.
# Reads docs.yml.
# Prints the new docs.yml to stdout.
# Must be run from the root of this repository.

functionCmds = [
  '        - title: Overview\n',
  '          href: api.html#functions\n',
]
with open('docs/_data/api/functions.yaml') as f:
  file = f.readlines()
  file.pop(0)
  for line in file:
    name = line[2:]
    href = "api."
    href += name
    functionCmds.append('        - title: %s' % name)
    functionCmds.append('          href: api.html#%s' % href)

def find_index(lines, f):
  for l in lines:
    if f(l):
      return lines.index(l)
  return -1

with open('src/_data/docs.yml') as f:
  lines = f.readlines()
  start_line = find_index(lines, lambda l: '# Start Tiltfile Functions Reference' in l)
  end_line = find_index(lines, lambda l: '# End Tiltfile Functions Reference' in l)
  if start_line == -1 or end_line == -1:
    exit(1)

  new_lines = lines[0:start_line+1] + functionCmds + lines[end_line:]
  print(''.join(new_lines).rstrip())

