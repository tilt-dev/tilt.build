# tilt.build

Build for the Tilt landing page

https://tilt.build/ and https://docs.tilt.build/

## Developing

1) Install [Tilt](https://github.com/windmilleng/tilt)

2) Run `tilt up`

The landing page will be running at http://localhost:4000/.

The docs page will be running at http://localhost:4001/.

Edits to the markdown will auto-update the HTML.
The landing page lives under src and the docs page lives under docs.
The docs directory has symlinks to share stuff with the landing page.

When you're finished, merge to master and Netlify will auto-deploy the site.

### API docs

The API docs are a little bit more complicated.

We write the API docs as docstrings in a Python file (api/api.py),
generate an HTML fragment with Sphinx (`make api`), and then
serve that HTML fragment with Jekyll.

You generally shouldn't need to run `make api` by hand. The Tiltfile
will do it automatically whenever api/api.py changes.

## License

Copyright 2019 Windmill Engineering

Licensed under [the Apache License, Version 2.0](LICENSE)
