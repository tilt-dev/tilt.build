---
title: Flags for Tiltfile Config Management
layout: docs
---


Tools offer flags and args to support the wide range of users needs and preferences, and dev workflows are no different. Devs on your team will want options in how they use Tilt; some are long-standing personal preferences and others will change in the middle of working on a Pull Request. With Tilt's user configuration system, you can improve a Tiltfile that encodes one standard setup to power the breadth of workflows your team needs:
* Maintainers choose the options to expose that make sense for their project
* Users can easily set and change options, without having to learn a Tiltfile
* Tiltfile extensions expose the choices so they can power arbitrary customizations

This doc describes how you, the Dev Experience engineer who owns the Tiltfile, can offer this to your user, the App Developer who runs Tilt while they code. In order, we'll cover:
*) Setting options as a user
*) Defining and using options in the Tiltfile
*) Describe how this is implemented.
*) Examples of common configuration
*) Future work (we see how it fits in but don't plan to implement until there's concrete demand).

## Setting Options as a User
Because users have different needs around options, Tilt supports several ways of setting options:

* Jump into a mode quickly by adding flags and args on the command: `tilt up -- --key value`.
* Store long-lived preferences in a file named `tilt-config.json` so you don't have to remember to pass options on each invocation.
* Change options without having to restart/rebuild/redeploy: `tilt args -- --key value2` updates the running Tilt and reloads the config with the new value.
* Set options in existing scripts outside of Tilt. For example, a new-hire onboarding tool that provisions capacity and requests permissions can write that info to `tilt-config.json`.


## Defining and Using Options in the Tiltfile
Here's where we describe config.define_string_list(), config.parse(), and config.set_resources.

## Examples

### Run only some services
Your app has many services, call them A, B, C, and D. You want users to be able to run only some of them.

and you want your users to be able to run only a subset of them. E.g., `tilt up` will run all services, but running `tilt up a b d` will run only the resources a, b, and d, ignoring c. Each run of Tilt will start from scratch.
#### Command-Lines
* `tilt up`: run all services
* `tilt up a b d`: run A, B, and D but not C
* `tilt args a b`: change running Tilt to run A and B but neither C nor D.
* `tilt up` (a second time): run all services

#### Tiltfile
```python
config.define_string_list("to-run", args=True)
cfg = config.parse()

config.set_resources(cfg['to-run'])
```

### Run a defined set of services
Your app has many services, call them A, B, C, and D. You have defined modes you want users to be able to start (e.g. consumer vs. enterprise) and you don't want them to have to remember which service is necessary for which mode.

You want to be able to write a doc that tells users to run `tilt up consumer` the first time and know that's enough that they'll be set up. Running Tilt subsequent times without arguments should default to the mode they already have set.

#### Command-Lines
* `tilt up`: run all services
* `tilt up consumer`: run consumer services

#### Tiltfile
```python
config.define_string_list("to-run", args=True)
cfg = config.parse()

groups = {
  'consumer': ['a', 'b', 'c'],
  'enterprise': ['a', 'b', 'd'],
}

if cfg['args']:
  resources = []
  for arg in cfg['args']:
    if arg in groups:
      resources += groups[arg]
    else:
      resources.append(r)
  flags.set_resources(resources)
```


### Specify services to edit
You have many services that your users frequently need to run, but don't expect to edit. Your YAML includes good enough images. (Perhaps they're from a suitably recent CI invocation, or refer to standard images.)

#### Command-Lines
* `tilt up`: run all services, editing none
* `tilt up -- --to-edit b`: run all services, editing b
* `tilt up -- consumer --to-edit b --to-edit c`: run consumer services and setup b and c for editing.

#### Tiltfile
```python
config.define_string_list("to-run", args=True)
config.define_string_list("to-edit")
cfg = config.parse()

# omitting the code from above Tiltfile that includes correct resources

# Only configure the build for services we want to edit
# Thanks to Tilt's existing behavior, an image that is mentioned in YAML but has no build set
# will use the existing tag.
if 'a' in cfg['to-edit']:
  docker_build('a', './a')
if 'b' in cfg['to-edit']:
  docker_build('b', './b')
if 'c' in cfg['to-edit']:
  docker_build('c', './c')
if 'd' in cfg['to-edit']:
  docker_build('d', './d')
```

## How Options Work
Tilt stores options in a file next to the Tiltfile called `tilt-config.json`. When the Tiltfile executes `config.parse()`, it loads that file as JSON and merges the current args.

Any change to the flags file will cause Tilt to reexecute the Tiltfile. You can modify the flags file with an editor or write scripts that write values into it, and Tilt will update.

A call to `tilt args` will connect to the running Tilt instance on the server port and cause Tilt to reexecute the Tiltfile.

### Comparison to Default Behavior
If you don't call `config.parse`, Tilt's default behavior is to set resources to any (non-empty) passed args. The equivalent of a Tiltfile:
```python
config.define_string_list("args", args=True)
cfg = config.parse()
if cfg['args']:
  config.set_resources(cfg['args'])
```

## Future Directions
This section describes places we expect flags to go. Let us know if any of these would be particularly helpful to you and your team.

### More Kinds of Flags
You should be able to define more kinds of flags. For example, a list of ints or floats, or a singly-valued string. By moving error-checking to the built-in library, you can make your Tiltfile shorter and more correct.

### Better Flag Manipulation/Discovery
Your users should be able to understand what reasonable values are. This could be from help output, tab-completion, or in the Web UI.

Your users should be able to modify flags in the Web UI, without having to know there's a file underneath.

### Escape Hatch for Flag Parsing
You should be able to use a custom syntax for your flags. The flags module could take a function that would parse a command-line into a JSON value.
