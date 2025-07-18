---
title: Tilt CLI Reference
layout: docs
sidebar: reference
hideEditButton: true
---
## tilt apply

Apply a configuration to a resource by filename or stdin

```
tilt apply (-f FILENAME | -k DIRECTORY)
```

### Options

```
      --all                             Select all resources in the namespace of the specified resource types.
      --allow-missing-template-keys     If true, ignore any errors in templates when a field or map key is missing in the template. Only applies to golang and jsonpath output formats. (default true)
      --cascade string[="background"]   Must be "background", "orphan", or "foreground". Selects the deletion cascading strategy for the dependents (e.g. Pods created by a ReplicationController). Defaults to background. (default "background")
      --dry-run string[="unchanged"]    Must be "none", "server", or "client". If client strategy, only print the object that would be sent, without sending it. If server strategy, submit server-side request without persisting the resource. (default "none")
      --field-manager string            Name of the manager used to track field ownership. (default "kubectl-client-side-apply")
  -f, --filename strings                The files that contain the configurations to apply.
      --force                           If true, immediately remove resources from API and bypass graceful deletion. Note that immediate deletion of some resources may result in inconsistency or data loss and requires confirmation.
      --force-conflicts                 If true, server-side apply will force the changes against conflicts.
      --grace-period int                Period of time in seconds given to the resource to terminate gracefully. Ignored if negative. Set to 1 for immediate shutdown. Can only be set to 0 when --force is true (force deletion). (default -1)
  -h, --help                            help for apply
      --host string                     Host for the Tilt HTTP server. Only necessary if you started Tilt with --host. Overrides TILT_HOST env variable. (default "localhost")
  -k, --kustomize string                Process a kustomization directory. This flag can't be used together with -f or -R.
      --openapi-patch                   If true, use openapi to calculate diff when the openapi presents and the resource can be found in the openapi spec. Otherwise, fall back to use baked-in types. (default true)
  -o, --output string                   Output format. One of: (json, yaml, name, go-template, go-template-file, template, templatefile, jsonpath, jsonpath-as-json, jsonpath-file).
      --overwrite                       Automatically resolve conflicts between the modified and live configuration by using values from the modified configuration (default true)
      --port int                        Port for the Tilt HTTP server. Only necessary if you started Tilt with --port. Overrides TILT_PORT env variable. (default 10350)
      --prune                           Automatically delete resource objects, that do not appear in the configs and are created by either apply or create --save-config. Should be used with either -l or --all.
      --prune-allowlist stringArray     Overwrite the default allowlist with <group/version/kind> for --prune
  -R, --recursive                       Process the directory used in -f, --filename recursively. Useful when you want to manage related manifests organized within the same directory.
  -l, --selector string                 Selector (label query) to filter on, supports '=', '==', '!=', 'in', 'notin'.(e.g. -l key1=value1,key2=value2,key3 in (value3)). Matching objects must satisfy all of the specified label constraints.
      --server-side                     If true, apply runs in the server instead of the client.
      --show-managed-fields             If true, keep the managedFields when printing objects in JSON or YAML format.
      --subresource string              If specified, apply will operate on the subresource of the requested object.  Only allowed when using --server-side.
      --template string                 Template string or path to template file to use when -o=go-template, -o=go-template-file. The template format is golang templates [http://golang.org/pkg/text/template/#pkg-overview].
      --timeout duration                The length of time to wait before giving up on a delete, zero means determine a timeout from the size of the object
      --validate string[="strict"]      Must be one of: strict (or true), warn, ignore (or false). "true" or "strict" will use a schema to validate the input and fail the request if invalid. It will perform server side validation if ServerSideFieldValidation is enabled on the api-server, but will fall back to less reliable client-side validation if not. "warn" will warn about unknown or duplicate fields without blocking the request if server-side field validation is enabled on the API server, and behave as "ignore" otherwise. "false" or "ignore" will not perform any schema validation, silently dropping any unknown or duplicate fields. (default "strict")
      --wait                            If true, wait for resources to be gone before returning. This waits for finalizers.
```

### Options inherited from parent commands

```
  -d, --debug      Enable debug logging
      --klog int   Enable Kubernetes API logging. Uses klog v-levels (0-4 are debug logs, 5-9 are tracing logs)
  -v, --verbose    Enable verbose logging
```

### SEE ALSO

* [tilt](tilt.html)	 - Multi-service development with no stress

###### Auto generated by spf13/cobra on 13-Jun-2025
