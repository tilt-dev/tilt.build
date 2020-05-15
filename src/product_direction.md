---
layout: page
title: Product Direction
permalink: /product_direction
---

The continuously changing product direction of Tilt and Tilt Cloud is based on conversations with existing and potential users, and our current thinking of multi-service development. We are always considering new ideas and plans; this is an interesting subset.

Comment on linked issues or [create a new one](https://github.com/tilt-dev/tilt). [Contact us](/contact.html) using your preferred method, including emailing Victor Wu, Head of Product at <a href="mailto:victor@tilt.dev">victor@tilt.dev</a>. 

## Recent releases
- [Use `tilt ci` to test in CI](https://blog.tilt.dev/2020/04/16/how-to-not-break-server-startup.html)
- [Team owner promotes current Tilt version for team](https://docs.tilt.dev/teams.html)
- [Extensions](https://blog.tilt.dev/2020/04/01/more-customizable-tiltfiles-with-extensions.html)
- [Tilt configs](https://blog.tilt.dev/2020/02/21/add-your-own-options-to-your-tilt-config.html)
- [Improved integration with Kind](https://blog.tilt.dev/2020/02/11/delete-clusters-faster-with-kind.html)

## Tilt Cloud
[Tilt Cloud](https://docs.tilt.dev/sign_in_tilt_cloud.html) is the integrated companion experience to Tilt, empowering software developers to better collaborate in teams, and help developer experience (DX) owners manage consistent and elevated DX experiences across a software organization. Interesting features:

- [Private team cloud snapshots](https://github.com/tilt-dev/tilt/issues/3128)
- [View Tilt usage on team page](https://github.com/tilt-dev/tilt/issues/3130)

## Tilt 1.0
We will soon be able to show Tilt to the greater development community, and we want to signal that with a 1.0 release. In particular, Tilt 1.0 should:
- Work for your platform
- Work for your development language
- Work for your app size (from one to many services)

## Other interesting features

- We aim to support Tilt for all popular development platforms. Tilt is [currently available for macOS and Linux](https://docs.tilt.dev/install.html). Windows support is in alpha, but we plan to support it fully. See [Windows Support issue](https://github.com/tilt-dev/tilt/issues/1961).
- [Categorize non-workload Kubernetes objects](https://github.com/tilt-dev/tilt/issues/2989)
- [View logs of init containers as they are brought up](https://github.com/tilt-dev/tilt/issues/2292)
- Port forward improvements
  - [Add a way to specify a URL for a local_resource](https://github.com/tilt-dev/tilt/issues/2983)
  - [Organization Tools for Port Forwards](https://github.com/tilt-dev/tilt/issues/2548)
- [Tilt lifecycle hooks](https://github.com/tilt-dev/tilt/issues/1699)
- Fixing confusion about what [`tilt down`](https://docs.tilt.dev/cli/tilt_down.html) does
- As described in [Contribute an Extension](https://docs.tilt.dev/contribute_extension.html), contributors cannot actually verify that an extension actually works before submitting a PR. This should be improved, where [development of extensions allows you test that it actually works before submitting a PR](https://github.com/tilt-dev/tilt/issues/3188).


