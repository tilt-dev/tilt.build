---
slug: "secret-management"
date: 2022-04-26
author: lian
layout: blog
title: Secret Management: The Soft Way
image: 
tags:
- secrets
- development
- kubernetes
- devtools
- open source
---
Secrets. Security best-practices mandate that they stay away from the code—or else! And that’s what we did for a long time.

But since the emergence of GitOps as the preferred flavor of CI/CD, we have decided that we want to ship everything together, and I mean everything: the applications, their configs and environment - all in one conveniently accessible lump.
The idea of GitOps is straightforward: Let’s presuppose you have a system like Kubernetes that manages an environment, whom you can feed a desired state and let it take care of the minute details of provisioning and configuring to bring your current into the desired state. To see which is the currently desired state, retrace the last state and consolidating multiple distributed application changes into one consistent state, we can use an old friend: Git. It already comes with convenient features like persistent history and access control. Devs and Ops teams can collaborate on the same repository to make sure the applications and environments themselves are correctly configured before deployment even starts.

So what does that mean for Secrets?
Well, let’s be clear first: Kubernetes secrets are not secret. They are at best obfuscated, but everyone who has access to a namespace or cluster, can read and decode all the secrets they contain.
The solution seems simple: Just don’t give devs access to the cluster. They can manipulate the state of the cluster by adding things to the GitOps repository. But now comes the crux: If everything that lives on the cluster also lives in the repository, everyone who has access to it also has access to the secrets.
One way could be to even further remove the devs, by not even giving them direct access, instead have an automated pipeline pickup their relevant manifests from another repo and move them into the GitOps repo.
I was once on a team that built this for a client, and I found this approach quite unwieldy, and it scaled poorly, This solution only focused on keeping ops components secure, but neglected developer experience causing lots of unnecessary friction between dev and ops teams. 

Instead, I’ll discuss three approaches which aim to make dealing with Secrets less painful with the help of some excellent Open Source tools, so devs can focus on providing business value.

## Sealed Secrets
Bitnami Sealed Secrets allow you to properly encrypt secrets and store them with the rest of the deployment manifests.
The central piece is the Sealed Secrets controller, which lives on the target Kubernetes cluster as an operator. With the companion kubeseal tool, any person who has access to the operator’s public key can encrypt a k8s secret and get a k8s custom resource of type Sealed Secret.
```
example
```
This sealed secret can only be decrypted by the controller, so it can be safely distributed with all the other k8s resources.
What’s great about this approach is that it has a comparatively small overhead. Secrets don’t need to be managed in a separate tool or platform, they just live where everything else lives.
On the downside, there’s no separate tool or platform to manage secrets, so they need to be managed “by hand”.
For small, early stage organizations this seems to be a good way to start introducing good practices around secret management.


## Google Secret Manager & External Secrets Operator
If you’re using one of the popular cloud vendors, you probably already have access to a secret management product. Maybe you are already managing access credentials in there. 
The External Secrets Operator can connect to a multitude of common secret providers like Google Secret Manager, AWS Secrets Manager or Azure Key Vault, and provide that data as k8s Secrets.
To access a secret, we first need to provide the right credentials as a secret store, in this case we have created a Service Account in GCP and have downloaded a key which we attached to this Secret Store.
```
Example
```
Now we can tell the operator which data to retrieve and how to provide it to the k8s cluster by defining the target secret in an External Secret resource.
```
Example
```

## HashiCorp Vault & External Secrets Operator
The External Secrets Operator does not only connect to secret management products provided by the big cloud vendors. If you have bigger security concerns than the mere storing of secrets, you might be using something like Hashicorp Vault to control not only your secrets, but also they way they are created and managed.
If you’re using ESO already, all you have to do is allow kubernetes to access your vault by creating a role for it. You can make this role as granular as you like, for example, only allowing access to specific secrets or paths.
In the secret store we then point to the kubernetes authentication secret stored in Vault.
```
Example
```
The External Resource will look exactly the same as in the example above.

Of course the big plus in this scenario is the full control over the entire lifecycle of a secret, however it comes with its own challenges. Managing a tool like vault does not only require pure operational effort, but also intentionally creating proper security procedures to fully leverage its usefulness.

—

To summarize: There are a multitude of ways to get secrets inside Kubernetes, but keep in mind that you need to manage and secure them outside the cluster. Safeguarding your secrets relies on every single employee. Inconvenient or convoluted processes will compromise security efforts, as people will look for the path of the least resistance and grow less alert over time.
When choosing the best security practice for your organization, start by understanding how your team works right now and try to find the tools and architecture that fits best to existing structures rather than reinventing the wheel.


