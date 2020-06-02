---
tilt: Structuring Multiple Repos
layout: docs
---

# Structuring Multiple Repos
When you run `tilt up` in a terminal, Tilt looks for a Tiltfile in that directory, parses it, and typically starts multiple services rooted in that directory. Usually that directory is one git source-controlled repo. But what if you you need to run multiple services, spread across multiple repos, during development? Tilt supports that too.

## Entrypoint Tiltfile
First create a Tiltfile for each repo that has resources of interest. Then, have an "entrypoint" repo with a Tiltfile that points to other Tiltfiles in other repos. Typically this would be in a parent directory. You then run Tilt in the entrypoint repo, with logic that starts resources in those other repos. In particular, use [`include()`](api.html#api.include) or [`load()`](api.html#api.load) to load those resources.

Each team or developer may have different needs in starting specific services, especially if your entrypoint Tiltfile is pointing to many downstream Tiltfiles. Consider using [Tiltfile Configs](tiltfile_config.html) to help customize accordingly.

If you have Tiltfile logic that can be abstracted out of your specific system, consider using [Extensions](extensions.html).

