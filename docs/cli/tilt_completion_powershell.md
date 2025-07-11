---
title: Tilt CLI Reference
layout: docs
sidebar: reference
hideEditButton: true
---
## tilt completion powershell

Generate the autocompletion script for powershell

### Synopsis

Generate the autocompletion script for powershell.

To load completions in your current shell session:

	tilt completion powershell | Out-String | Invoke-Expression

To load completions for every new session, add the output of the above command
to your powershell profile.


```
tilt completion powershell [flags]
```

### Options

```
  -h, --help              help for powershell
      --no-descriptions   disable completion descriptions
```

### Options inherited from parent commands

```
  -d, --debug      Enable debug logging
      --klog int   Enable Kubernetes API logging. Uses klog v-levels (0-4 are debug logs, 5-9 are tracing logs)
  -v, --verbose    Enable verbose logging
```

### SEE ALSO

* [tilt completion](tilt_completion.html)	 - Generate the autocompletion script for the specified shell

###### Auto generated by spf13/cobra on 13-Jun-2025
