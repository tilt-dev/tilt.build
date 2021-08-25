---
title: Smart Rebuilds with Live Update
subtitle: Tilt Tutorial
layout: docs
---
Tilt's deep understanding of your resources means the right things get rebuilt at the right times.

> 🧠 **Monorepo? No Problem!**
> 
> Tilt lets you include or exclude files per-resource without enforcing a specific file hierarchy on you.
> 
> Refer to [Debugging File Changes: Rebuilds and Ignores][guide-file-changes] for guidance and examples.

However, even with Docker layer caching, rebuilding a container can be slow.
It also often needs to be pushed to a registry and the Deployment on the cluster updated to roll out new Pods using the updated image.

Live Update solves these challenges by performing an in-place update of the containers in your cluster.
It works with both frameworks that natively support hot reload (e.g. Webpack) as well as compiled languages.




[guide-file-changes]: /file_changes.html
