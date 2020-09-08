---
title: experimental_analytics_report
description: "A Tiltfile builtin for better understanding your team's analytics"
layout: docs
---
## Summary
Tilt 0.17.4 adds the `experimental_analytics_report` Tiltfile builtin. This allows teams working with Tilt to better measure and improve their Tilt usage.

The main goal of this is to allow developer experience engineers working with Tilt to de-anonymize their teams' analytics data, identify teammates who are running into problems with Tilt, and then understand and solve those teammates' problems.

As the name says, this is *experimental*. It is intended only for use in coordination with the Tilt team.

## Usage
`experimental_analytics_report` takes a single `Dict[string,string]` of tags to report per user. This function causes Tilt to report all data specified, plus the (anonymized) machine and repo hashes to the Tilt analytics server.

Example:
```
username = str(local('whoami')).rstrip('\n')
experimental_analytics_report({'user.name': username})
```

This will allow the Tilt team to work with you to build a dashboard showing Tilt usage metrics broken down by individual usernames.

"user.name" is, by convention, the key used for identifying users. Its value might come from "whoami" (as in the example above, which would just show the user's local username) or some fancier command, e.g., `ldapsearch`, depending on your company's infrastructure.

## Other uses
This is an experimental feature, and there are not self-service graphs for any arbitrary data you'd like to attach. If you have other data you'd like to send to Tilt and see analytics for, please talk to us about it!
