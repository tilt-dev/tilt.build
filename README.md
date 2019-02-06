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

## License

Copyright 2019 Windmill Engineering

Licensed under [the Apache License, Version 2.0](LICENSE)
