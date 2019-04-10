# -*- mode: Python -*-

default_registry('gcr.io/windmill-public-containers')

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
               sync('./src', '/src/'),
               sync('./docs', '/docs/'),
               run('bundle install', trigger=['src/Gemfile', 'src/Gemfile.lock',
                                              'docs/Gemfile', 'docs/Gemfile.lock'])
             ])

k8s_resource('tilt-site', port_forwards=4000)
k8s_resource('docs-site', port_forwards=4001)
