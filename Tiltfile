# -*- mode: Python -*-

k8s_resource_assembly_version(2)

default_registry('gcr.io/windmill-public-containers')
set_team('tilt-dev')
enable_feature('update_history')

# Generate the API docs.
local_resource('make-api', 'make api', ['deploy/api.dockerfile', 'Makefile', 'api'])

k8s_yaml('deploy/serve.yaml')

docker_build('tilt-site', '.', dockerfile='deploy/site.dockerfile',
             ignore=['./api', './docs', './blog'],
             live_update=[
               sync('./src', '/src/'),
               run('bundle install', trigger=['src/Gemfile', 'src/Gemfile.lock'])
             ])

docker_build('docs-site', '.', dockerfile='deploy/docs.dockerfile',
             ignore=['./api', './blog'],
             live_update=[
               sync('./src', '/src/'),
               sync('./docs', '/docs/'),
               run('bundle install', trigger=['src/Gemfile', 'src/Gemfile.lock',
                                              'docs/Gemfile', 'docs/Gemfile.lock'])
             ])


docker_build('blog-site', '.', dockerfile='deploy/blog.dockerfile',
             ignore=['./api', './docs'],
             live_update=[
               sync('./src', '/src/'),
               sync('./blog', '/blog/'),
               run('bundle install', trigger=['src/Gemfile', 'src/Gemfile.lock',
                                              'blog/Gemfile', 'blog/Gemfile.lock'])
             ])

k8s_resource('tilt-site', port_forwards=4000, resource_deps=['make-api'])
k8s_resource('docs-site', port_forwards=4001, resource_deps=['make-api'])
k8s_resource('blog-site', port_forwards=4002, resource_deps=['make-api'])
