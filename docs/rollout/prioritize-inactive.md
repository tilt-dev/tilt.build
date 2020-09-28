---
title: Prioritize Inactive Users
layout: rollout
---

Here's a triage guideline that's surprising and counterintuitive: during rollout, prioritize inactive users, i.e. people who tried Tilt but stopped using it. This isn't often one's first instinct--shouldn't you focus on your most active users? This doc explains how prioritizing inactive users puts your attention on the most pressing issues and can drive adoption.

## Why Inactive Users Over Active Users

Consider three classes of users:
* Active Users who use Tilt regularly.
* Inactive Users who have tried Tilt but don't use it regularly.
* Potential Users who could try Tilt and become Active Users.

Prioritizing Inactive Users can be counterintuitive because there are clear motivations to work with the other classes:
* Active Users are already excited. They know what's good about Tilt and may share your vision. You want to reward them, and every issue they hit can feel like it's your responsibility.
* Potential Users seem like low-hanging fruit. If you just tell them about Tilt, they might try it and adopt tomorrow.

The actual low-hanging fruit is Inactive Users.
* Turning one Inactive User into an Active User is the same adoption increase as doubling the activity of an Active User.
* Potential Users are likely to run into the same issues that block your current Inactive Users. Solve your existing issues before looking for new ones.

The key insight here is that users aren't always great at communicating severity. You can spend lots of time fixing nits but ignoring showstoppers. Active Users aren't trying to confuse you; they're human too and might just be reporting the issue they run into most often or most recently and this skews the reports. For Inactive Users, the showstoppers are more likely to be top of mind.

## Exceptions

You shouldn't totally ignore Active users, even if you're prioritizing Inactive Users. Here are some cases where you should focus on other users:
* Fix regressions. For example if a change to a build script makes the inner loop in Tilt jump from half a second to 30 seconds, of course you should fix it.
* Active Users are about to leave. If an issue reported by an Active User is so frustrating they're about to stop using Tilt, then they're nearly an Inactive User and you should prioritize their issue.
* Disqualified Inactive Users. If a user is Inactive because they do data science and configuring Tilt data science workflows is out-of-scope, then move on to the next set of Potential Users.
* Small changes. If something will take you an hour to fix, you should fix it.
* Inactive User feedback is unclear. Don't just do whatever the Inactive User asks for; figure out what's actually getting in the way.


## Evaluation

**Use this if**
* Your backlog has more issues reported by many users than you can deal with.

**Skip this if**
* You are confident your Inactive Users don't have problems worth solving.

**You know it's successful when**
* You prioritize an issue reported by an Inactive User and after it's fixed you see that multiple Inactive Users become Active and praise that improvement.
