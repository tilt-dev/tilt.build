# -*- mode: Python -*-

k8s_resource_assembly_version(2)

default_registry('gcr.io/windmill-public-containers')

read_file('Makefile') # rebuild if we change the Makefile

# Generate the API docs.
read_file('api/api.py')
local('make api')

k8s_yaml('serve.yaml')

docker_build('tilt-site', 'src', dockerfile='site.dockerfile',
             live_update = [
               sync('./src', '/src/'),
               run('bundle install', trigger=['src/Gemfile', 'src/Gemfile.lock'])
             ])

docker_build('docs-site', '.', dockerfile='docs.dockerfile',
             live_update = [
               # we don't care about this being on the container but we don't want it to trigger a full rebuild,
               # just toss it somewhere so it's accounted for by a LiveUpdate step
               # This is hacky. Right now a change to api.py kicks off TWO container updates, one
               # to sync api.py (which we don't care about), and one when the local('make api') call
               # above changes docs/_includes/api.html -- but it's still faster than a full rebuild ¯\_(ツ)_/¯
               sync('./api/api.py', '/tmp/api.py'),

               sync('./src', '/src/'),
               sync('./docs', '/docs/'),
               run('bundle install', trigger=['src/Gemfile', 'src/Gemfile.lock',
                                              'docs/Gemfile', 'docs/Gemfile.lock'])
             ])

k8s_resource('tilt-site', port_forwards=4000)
k8s_resource('docs-site', port_forwards=4001)
