# -*- mode: Python -*-

default_registry('gcr.io/windmill-public-containers')
set_team('0584d8f6-05a2-49f5-923b-657afef098fe')
username = str(local('whoami')).rstrip('\n')
experimental_analytics_report({'user.name': username})
experimental_metrics_settings(enabled=True)

# Generate the API docs.
local_resource('make-api', 'make api', ['deploy/api.dockerfile', 'Makefile', 'api'])
local_resource('make-stars', 'make stars', ['Makefile', 'stars'])

k8s_yaml('deploy/serve.yaml')

# files in common directories but specific to the API docs (all non-docs resources should ignore these)
api_ignores = ['./src/_data/api/', './src/_includes/api/']

docker_build('tilt-site-base', '.', dockerfile='deploy/base.dockerfile',
             only=['./src/Gemfile', './src/Gemfile.lock'])

docker_build('tilt-site', '.', dockerfile='deploy/site.dockerfile',
             ignore=['./api', './docs', './blog'] + api_ignores,
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
             ignore=['./api', './docs'] + api_ignores,
             live_update=[
               sync('./src', '/src/'),
               sync('./blog', '/blog/'),
               run('bundle install', trigger=['src/Gemfile', 'src/Gemfile.lock',
                                              'blog/Gemfile', 'blog/Gemfile.lock'])
             ])

k8s_resource('tilt-site', port_forwards=[port_forward(4000, name='tilt-site')])
k8s_resource('docs-site', port_forwards=[port_forward(4001, name='docs-site')], resource_deps=['make-api'])
k8s_resource('blog-site', port_forwards=[port_forward(4002, name='blog-site')])
