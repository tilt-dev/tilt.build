---
title: Tiltfile Config
layout: docs
---

A Tiltfile can define a Tiltfile config, which allow the users of a Tiltfile to
provide input / configuration to that Tiltfile. For example, one might write a
Tiltfile such that one runs `tilt up consumer` to run Tilt with the services
needed for development for consumers, or `tilt up enterprise` to run Tilt with
the services needed for development for enterprise.

This doc describes how to configure these and other shorthands in Tilt. We aim
to make common cases trivial, while also supporting escape hatches that enable
arbitrarily complex cases.

In order, we'll cover:
* Examples that cover common cases, showing both the Tiltfiles and accompanying
  usage.
* Describe how this is implemented. These details will help you understand how
  to write tooling that interacts with this system and describe its behavior
  to teammates.
* Future work (we see how it fits in but don't plan to implement until there's
  concrete demand).

### Run only some services (reimplement default Tilt behavior)
Your app has many services, call them A, B, C, and D, and you want your users to
be able to run only a subset of them. E.g., `tilt up` will run all services, but
running `tilt up a b d` will run only the resources a, b, and d, ignoring c.
This is the same as the default `tilt up` behavior, but is useful as an example
and starting point.

#### Command-Lines
* `tilt up`: run all services
* `tilt up a b d`: run A, B, and D but not C
* `tilt flags a b`: change running Tilt to run A and B but neither C nor D.
* `tilt up`: run all services

#### Tiltfile
```python
config.define_string_list("to-run", args=True)
cfg = config.parse()
config.set_enabled_resources(cfg.get('to-run', []))
```

### Run a defined set of services
Your app has many services, call them A, B, C, and D. Some of your developers
work on consumer features, which need one subset of those services, and some of
your developers work on enterprise features, which need a different subset. You
don't want your developers to have to remember and keep up with the latest on
which services are in which subset.
You want to be able to write a doc that tells users to run `tilt up consumer`
and know that's enough that they'll be set up.

#### Command-Lines
* `tilt up`: run all services
* `tilt up consumer`: run only services in the "consumer" list
#### Tiltfile
```python
config.define_string_list("to-run", args=True)
cfg = config.parse()
groups = {
  'consumer': ['a', 'b', 'c'],
  'enterprise': ['a', 'b', 'd'],
}
resources = []
for arg in cfg.get('to-run', []):
  if arg in groups:
    resources += groups[arg]
  else:
    # also support specifying individual services instead of groups, e.g. `tilt up a b d`
    resources.append(arg)
config.set_enabled_resources(resources)
```

### Specify services to edit
You have many services that your users frequently need to run, but don't expect
to edit. Your YAML includes good enough images. (Perhaps they're from a suitably
recent CI invocation, or refer to standard images.)
#### Command-Lines
* `tilt up`: run all services, editing none
* `tilt up -- --to-edit b`: run all services, editing b (the '--' indicates the
  end of `tilt up` options and the start of user-defined settings)
* `tilt up -- consumer --to-edit b --to-edit c`: run consumer services and set
  up b and c for editing.
#### Tiltfile
```python
config.define_string_list("to-run", args=True)
config.define_string_list("to-edit")
cfg = config.parse()
# omitting the code from above Tiltfile that includes correct resources
# Only configure the build for services we want to edit
# Thanks to Tilt's existing behavior, an image that is mentioned in YAML but has no build set
# will use the existing tag.
to_edit = cfg.get('to-edit', [])
if 'a' in to_edit:
  docker_build('a', './a')
if 'b' in to_edit:
  docker_build('b', './b')
if 'c' in to_edit:
  docker_build('c', './c')
if 'd' in to_edit:
  docker_build('d', './d')
```

## The Config File
In addition to config settings coming from command-line args, Tilt will read
them from a `tilt_config.json` in the same directory as the `Tiltfile`, if one
exists. It should contain a single JSON dict, where the keys are config setting
names and the values are their values (e.g., `{"to-edit": ["b", "c"]}`).
As with any other file read by the Tiltfile, if this config file is changed
while Tilt is running, Tilt will pick up that change and reexecute the Tiltfile.
If the same setting is specified in both the config file and the command-line
args, the value from the args takes precedence.

## Changing args at runtime
While Tilt is running, if the user decides they need a different set of
Tiltfile args (i.e., args handled by config.parse, not args to tilt itself like
`--hud`) than what they passed to `tilt up`, they can use `tilt args` to
replace them, e.g.:
#### Command-Lines
* `tilt up a b d`: start tilt with just services a, b, and d
* `tilt args a b d -- --to-edit b`: connect to the tilt that is running from the
                   previous line, and enable editing for service b
* `tilt args --clear`: clear the Tiltfile args (change the running Tilt so that
                   it's as if it were just run as a bare `tilt up` with no
                   Tiltfile args)

Note that settings from args always take precedence over settings from the
config file, even if the config file is changed after the args were set.

### Comparison to Default Behavior
If you don't call `config.parse`, Tilt's default behavior is to set resources to
any (non-empty) passed args. As a starting point, this is an equivalent Tiltfile
implementation:
```python
config.define_string_list("args", args=True)
cfg = config.parse()
config.set_enabled_resources(cfg.get('args', []))
```

## Future Directions
This section describes places we expect the config to go. Let us know if any of
these would be particularly helpful to you and your team.
### More Kinds of Settings
You should be able to define more kinds of settings. For example, a bool, an
an enum, or a singly-valued string. By moving error-checking to the built-in
library, you can make your Tiltfile shorter and more correct.
### Better Config Manipulation/Discovery
Your users should be able to understand what reasonable values are. This could
be from help output, tab-completion, or in the Web UI.
Tilt should provide a way to manipulate tilt_config.json.
Your users should be able to modify the config in the Web UI.
### Escape Hatch for Argument Parsing
You should be able to use a custom syntax for command-line arguments. The config
module could take a function that would parse a command-line into JSON.
### Interaction with load/include
Tiltfiles that are used via `load`/`include` should be able to define and use
config settigs.
