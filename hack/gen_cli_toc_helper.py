# Generates the CLI TOC
#
# Reads the auto-generated Cobra CLI docs.
# Reads docs.yml.
# Prints the new docs.yml to stdout.
# Must be run from the root of this repository.

import re

commands = []
with open('docs/cli/tilt.md') as f:
  for line in f.readlines():
    # Example:
    # * [tilt alpha](tilt_alpha.html)	 - unstable/advanced commands still in alpha
    m = re.search(r'\[tilt ([a-zA-Z0-9-_]+)\][(](.+?)[)]\s*-\s*(.*)', line.strip())
    if m:
      commands.append((m.group(1), m.group(2), m.group(3)))

command_lines = [
  '      - title: tilt\n',
  '        href: cli/tilt.html\n',
  '        info: Manages your microservices in development\n',
]
for command in commands:
  command_lines.append('      - title: tilt %s\n' % command[0])
  command_lines.append('        href: cli/%s\n' % command[1])
  command_lines.append('        info: %s\n' % repr(command[2]))

with open('src/_data/docs.yml') as f:
  lines = f.readlines()
  start_line = lines.index('# Start Tilt CLI Reference\n')
  end_line = lines.index('# End Tilt CLI Reference\n')
  if start_line == -1 or end_line == -1:
    exit(1)

  new_lines = lines[0:start_line+1] + command_lines + lines[end_line:]
  print(''.join(new_lines).rstrip())
