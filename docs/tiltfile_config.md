---
title: Tiltfile Config
layout: docs
---

Tools offer flags and args to support the wide range of users needs and preferences, and dev workflows are no different. Devs on your team will want options in how they use Tilt; some are long-standing personal preferences and others will change in the middle of working on a Pull Request. With Tilt's user configuration system, you can improve a Tiltfile that encodes one standard setup to power the breadth of workflows your team needs:
* Maintainers choose the options to expose that make sense for their project
* Users can easily set and change options, without having to learn a Tiltfile
* Tiltfile code uses the choices to power arbitrary customizations

This doc describes how you, the Dev Experience engineer who owns the Tiltfile, can offer this to your user, the App Developer who runs Tilt while they code. In order, we'll cover:
* Setting options as a user
* Examples of common configuration
* Config file that stores flags
* Future work

## Setting Options as a User
Because users have different needs around options, Tilt supports several ways of setting options:

* Jump into a mode quickly by adding flags and args on the command: `tilt up -- --key value`.
* Store long-lived preferences in a file named `tilt_config.json` so you don't have to remember to pass options on each invocation.
* Change options without having to restart/rebuild/redeploy: `tilt args -- --key value2` updates the running Tilt and reloads the config with the new value.
* Set options in existing scripts outside of Tilt. For example, a new-hire onboarding tool that provisions capacity and requests permissions can write that info to `tilt_config.json`.

## Examples

### Run only some services (reimplement default Tilt behavior)
Your app has many services, call them A, B, C, and D, and you want your users to
be able to run only a subset of them. E.g., `tilt up` will run all services, but
running `tilt up a b d` will run only the resources a, b, and d, ignoring c.
This is the same as the default `tilt up` behavior, but is useful as an example
and starting point.

#### Command-Lines
* `tilt up`: run all services
* `tilt up a b d`: run A, B, and D but not C
* `tilt args a b`: change running Tilt to run A and B but neither C nor D.
* `tilt down`: delete all services
* `tilt down a b d`: delete A, B, and D but leave C running

#### Tiltfile

(See the [config API reference](/api.html#modules.config.define_string_list)
for details on what exactly these calls are doing.)
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
* `tilt down -- consumer`: Delete consumer services but leave any other services alone.

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

## Flag types
Here are some sample usages of different types of flags that are supported:

### list of string
* Tiltfile syntax: `config.define_string_list("foo")`
* `tilt` invocation: `tilt up -- --foo bar --foo baz`

### single string
* Tiltfile syntax: `config.define_string("foo")`
* `tilt` invocation: `tilt up -- --foo bar`

### bool
* Tiltfile syntax: `config.define_bool("foo")`
* `tilt` invocation: `tilt up -- --foo` or `tilt up -- --foo=False`

## Future Directions
This section describes places we expect the config to go. Let us know if any of
these would be particularly helpful to you and your team.
### More Kinds of Settings
You should be able to define more kinds of settings (for example, an enum). By moving error-checking to the built-in
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
