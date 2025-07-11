---
title: Tilt CLI Reference
layout: docs
sidebar: reference
hideEditButton: true
---
## tilt

Multi-service development with no stress

### Synopsis


Tilt helps you develop your microservices locally.
Run 'tilt up' to start working on your services in a complete dev environment
configured for your team.

Tilt watches your files for edits, automatically builds your container images,
and applies any changes to bring your environment
up-to-date in real-time. Think 'docker build && kubectl apply' or 'docker-compose up'.


### Options

```
  -d, --debug      Enable debug logging
  -h, --help       help for tilt
      --klog int   Enable Kubernetes API logging. Uses klog v-levels (0-4 are debug logs, 5-9 are tracing logs)
  -v, --verbose    Enable verbose logging
```

### SEE ALSO

* [tilt alpha](tilt_alpha.html)	 - unstable/advanced commands still in alpha
* [tilt analytics](tilt_analytics.html)	 - info and status about tilt-dev analytics
* [tilt api-resources](tilt_api-resources.html)	 - Print the supported API resources
* [tilt apply](tilt_apply.html)	 - Apply a configuration to a resource by filename or stdin
* [tilt args](tilt_args.html)	 - Changes the Tiltfile args in use by a running Tilt
* [tilt ci](tilt_ci.html)	 - Start Tilt in CI/batch mode with the given Tiltfile args
* [tilt completion](tilt_completion.html)	 - Generate the autocompletion script for the specified shell
* [tilt create](tilt_create.html)	 - Create a resource from a file or from stdin.
* [tilt delete](tilt_delete.html)	 - Delete resources by filenames, stdin, resources and names, or by resources and label selector
* [tilt demo](tilt_demo.html)	 - Creates a local, temporary Kubernetes cluster and runs a Tilt sample project
* [tilt describe](tilt_describe.html)	 - Show details of a specific resource or group of resources
* [tilt disable](tilt_disable.html)	 - Disables resources
* [tilt docker](tilt_docker.html)	 - Execute Docker commands as Tilt would execute them
* [tilt docker-prune](tilt_docker-prune.html)	 - Run docker prune as Tilt does
* [tilt doctor](tilt_doctor.html)	 - Print diagnostic information about the Tilt environment, for filing bug reports
* [tilt down](tilt_down.html)	 - Delete resources created by 'tilt up'
* [tilt dump](tilt_dump.html)	 - Dump internal Tilt state
* [tilt edit](tilt_edit.html)	 - Edit a resource on the server
* [tilt enable](tilt_enable.html)	 - Enables resources
* [tilt explain](tilt_explain.html)	 - Get documentation for a resource
* [tilt get](tilt_get.html)	 - Display one or many resources
* [tilt logs](tilt_logs.html)	 - Get logs from a running Tilt instance (optionally filtered for the specified resources)
* [tilt lsp](tilt_lsp.html)	 - Language server for Starlark
* [tilt patch](tilt_patch.html)	 - Update fields of a resource
* [tilt snapshot](tilt_snapshot.html)	 - 
* [tilt trigger](tilt_trigger.html)	 - Trigger an update for the specified resource
* [tilt up](tilt_up.html)	 - Start Tilt with the given Tiltfile args
* [tilt verify-install](tilt_verify-install.html)	 - Verifies Tilt Installation
* [tilt version](tilt_version.html)	 - Current Tilt version
* [tilt wait](tilt_wait.html)	 - Experimental: Wait for a specific condition on one or many resources

###### Auto generated by spf13/cobra on 13-Jun-2025
