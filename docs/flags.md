---
title: Flags for Tiltfile Config Management
layout: docs
---


This doc describes how to use flags to maintain configuration of a developer instance. This is especially useful for teams that have both enough services that there are multiple ways you might want to run it, and a designated owner of the developer experience (often a "DevEx" team or principal engineer). We'll use "you" to mean that DevEx engineer and "your user" to mean a developer at your org that uses Tilt.

## Goal
Users can start Tilt in a specific mode with a single Tilt command. For instance, `tilt up consumer` will start just the services for consumer users (vs other modes, like `tilt up enterprise`). If they later run `tilt up` it can stay in the selected mode, and they can change the mode while tilt is running with `tilt flags enterprise`.

This doc describes how to describe your setup to Tilt to enable these shorthands. We aim to make common cases trivial, while also supporting escape hatches that enable arbitrarily-complex cases.

In order, we'll cover:
*) Examples that cover common cases, showing both the Tiltfiles and accompanying usage.
*) Describe how this is implemented. These details, especially around persistence, will let you understand how to write tooling that interacts with this system.
*) Future work (we see how it fits in but don't plan to implement until there's concrete demand).

## Examples

### Run only some services
Your app has many services, call them A, B, C, and D. You want users to be able to run only some of them.

and you want your users to be able to run only a subset of them. E.g., `tilt up` will run all services, but running `tilt up a b d` will run only the resources a, b, and d, ignoring c. Each run of Tilt will start from scratch.
#### Command-Lines
* `tilt up`: run all services
* `tilt up a b d`: run A, B, and D but not C
* `tilt flags a b`: change running Tilt to run A and B but neither C nor D.
* `tilt up` (a second time): run all services

#### Tiltfile
```python
flags.define_string_list("to-run", args=True, sticky=False)
cfg = flags.parse()

flags.exclude_all_resources()
for r in cfg['to-run']:
  flags.include_resource(r)
```

### Run a defined set of services
Your app has many services, call them A, B, C, and D. You have defined modes you want users to be able to start (e.g. consumer vs. enterprise) and you don't want them to have to remember which service is necessary for which mode.

You want to be able to write a doc that tells users to run `tilt up consumer` the first time and know that's enough that they'll be set up. Running Tilt subsequent times without arguments should default to the mode they already have set.

#### Command-Lines
* `tilt up`: run all services
* `tilt up consumer`: run consumer services and record mode
* `tilt up` (a second time): run consumer services

#### Tiltfile
```python
flags.define_string_list("to-run", args=True)
cfg = flags.parse()

groups = {
  'consumer': ['a', 'b', 'c'],
  'enterprise': ['a', 'b', 'd'],
}












flags.exclude_all_resources()
for arg in cfg['args']:
  if arg in groups:
    for r in groups[arg]:
      flags.include_resource(r)
  else:
    flags.include_resource(r)
```

By making the flag sticky (the default), Tilt will record the flag between runs.


### Specify services to edit
You have many services that your users frequently need to run, but don't expect to edit. Your YAML includes images from your CI that are suitably recently (and match what's in production or staging).

#### Command-Lines
* `tilt up`: run all services, editing none
* `tilt up -- --to-edit b`: run all services, editing b
* `tilt up -- consumer --to-edit b --to-edit c`: run consumer services and setup b and c for editing.

#### Tiltfile
```python
flags.define_string_list("to-run", args=True)
flags.define_string_list("to-edit")
cfg = flags.parse()

# omitting the code from above Tiltfile that includes correct resources

# only configure the build for services we want to edit
if 'a' in cfg['to-edit']:
  docker_build('a', './a')
if 'b' in cfg['to-edit']:
  docker_build('b', './b')
if 'c' in cfg['to-edit']:
  docker_build('c', './c')
if 'd' in cfg['to-edit']:
  docker_build('d', './d')
```

## How Flags Work
Tilt stores flags in a file next to the Tiltfile called `tilt_flags.json`. When the Tiltfile executes `flags.parse()`, it loads that file as JSON. If it's the first execution after a Tilt up, the execution will merge the flags passed on the command-line with the values from the file (using the definition of flags as a guide) and write the new values to the file if necessary.

Any change to the flags file will cause Tilt to reexecute the Tiltfile. You can modify the flags file with an editor or write scripts that write values into it, and Tilt will update.

A call to `tilt flags` will connect to the running Tilt instance on the server port and cause Tilt to reexecute the Tiltfile, using the passed command-line args as if it's the first execution after a Tilt up.

## Future Directions
This section describes places we expect flags to go. Let us know if any of these would be particularly helpful to you and your team.

### More Kinds of Flags
You should be able to define more kinds of flags. For example, a list of ints or floats, or a singly-valued string. By moving error-checking to the built-in library, you can make your Tiltfile shorter and more correct.

### Better Flag Manipulation
Your users should be able to understand what reasonable values are. This could be from help output, tab-completion, or in the Web UI.

Your users should be able to modify flags in the Web UI, without having to know there's a file underneath.

### Escape Hatch for Flag Parsing
You should be able to use a custom syntax for your flags. The flags module could take a function that would parse a command-line into a JSON value.