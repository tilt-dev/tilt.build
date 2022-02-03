#!/usr/bin/env python3.9
#
# NB: Need Python 3.9 for ast.unparse()

import ast
import os
import sys

def dump(node):
    print(ast.dump(node, indent=4))

def parse_function(fdef, outfile):
    docstring = ast.get_docstring(fdef)
    if not fdef.name.startswith("_") and docstring:
        docstring_node = fdef.body[0]
        docstring_node.value=ast.Constant(docstring.lstrip())
        fdef.body = [docstring_node, ast.Pass()]
        outfile.write(ast.unparse(fdef))
        outfile.write("\n\n")
        return True
    return False

def parse_default(node, outfile):
    outfile.write(ast.unparse(node))
    outfile.write("\n\n")
    return False

node_handlers = {
    ast.FunctionDef: parse_function
}

def parse(filename, output):
    wrote_content = False
    with open(filename) as file:
        tree = ast.parse(file.read(), filename)
    with open(output, 'w') as outfile:
        outfile.write("from api import *\n\n")
        outfile.write("import os\n\n")
        for node in ast.iter_child_nodes(tree):
            fn = node_handlers.get(type(node), parse_default)
            wrote_content = fn(node, outfile) or wrote_content
    if not wrote_content:
        os.remove(output)
    return wrote_content

def main():
    extensions = {}
    os.makedirs('extensions', exist_ok=True)
    for f in sys.argv[1:]:
        if os.path.basename(f) == "Tiltfile":
            extensions[os.path.basename(os.path.dirname(f))] = f

    if len(extensions) == 0:
        for f in os.listdir('./tilt-extensions'):
            ext_tiltfile = os.path.join('./tilt-extensions', f, 'Tiltfile')
            if os.path.exists(ext_tiltfile):
                extensions[f] = ext_tiltfile

    with open('extensions.rst', 'w') as ext_rst:
        keys = sorted(extensions.keys())
        for f in keys:
            output = 'extensions/'+f+'.py'
            ext_tiltfile = extensions[f]
            if parse(ext_tiltfile, output):
                subsection = f + "\n" + "-" * len(f)
                ext_rst.write("""
%s

.. automodule:: extensions.%s
   :members:

""" % (subsection,f))
                print('Parsed '+ext_tiltfile+' => '+output)

main()
