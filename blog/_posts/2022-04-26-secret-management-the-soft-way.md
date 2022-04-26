---
slug: "secret-management"
date: 2022-04-26
author: lian
layout: blog
title: Secret Management - The Soft Way
description: Three ways to manage secrets for Kubernetes
image: "/assets/images/secret-management/pexels-gotta-be-worth-it-1160845.jpg"
image_caption: "Many differently colored padlocks. Photo by Gotta Be Worth It from <a href='https://www.pexels.com/photo/assorted-color-metal-keys-1160845/'>Pexels</a>"
tags:
- secrets
- development
- kubernetes
- devtools
- open source
---
Secrets. Security best-practices mandate that they stay away from the code—or else! And for a long time that's exactly what we did. Sensitive data like database credentials would be injected into an application's environment from elsewhere in a process separate from how the software itself was delivered.

But since the emergence of [GitOps] as the hot new flavour of CI/CD, we have decided that we want to ship everything together, and I mean everything: the applications, their configs and environment - all in one conveniently accessible lump.  
The idea of GitOps is straightforward: Let’s presuppose you have a system like Kubernetes that manages an environment, whom you can feed a desired state and let it take care of the minute details of provisioning and configuring to bring your current into the desired state. We can then store all the state definitions we have requested in Git, so we can retrace our steps at a later time. Since Git already comes with convenient features like a persistent history and access control, devs and ops teams can collaborate on the same repository to make sure the applications and environments themselves are correctly configured before deployment even starts.

So what does that mean for Secrets?  
Well, let’s be clear first: [Kubernetes secrets][k8s-secrets] are not secret. They are at best obfuscated, but everyone who has access to a namespace or cluster, can read and decode all the secrets it contains.
The solution seems simple: Just don’t give devs access to the cluster. They can manipulate the state of the cluster by adding things to the GitOps repository. But that doesn't really solve the problem. If everything that lives on the cluster also lives in the repository, everyone who has access to it, also has access to the secrets, as they would also be stored in said repo.  
One way could be to even further remove the devs, by not even giving them direct access, instead have an automated pipeline pick up their relevant manifests from another place and move them into the GitOps repo.  
Once I helped set up this architecture for a client, but I found this approach quite unwieldy. It also scaled poorly.  
This solution only focused on keeping ops components secure, but neglected developer experience causing lots of unnecessary friction between dev and ops teams.

Instead, I’ll discuss three approaches which aim to make dealing with secrets less painful as developers.  
_Note: I am only dealing with delivering secrets to the cluster; the cluster itself still needs to be secured._

In the end, we want to end up with the same Kubernetes Secret.
```yaml
apiVersion: v1
kind: Secret
metadata:
  name: k8s-secret
type: Opaque
data:
  FOO: QkFS
  BAR: eWFtbA==
```

With the help of some excellent open source projects, it's possible to build some powerful tooling, so devs can focus on providing business value.

## Sealed Secrets
[Bitnami Sealed Secrets][sealedsecrets] allow you to properly encrypt secrets and store them with the rest of the deployment manifests.
The Sealed Secrets controller is an operator that lives on your Kubernetes cluster.  
The kubeseal CLI is its client-side companion. With kubeseal, any person who has access to the operator’s public key can encrypt a k8s secret and get a k8s custom resource of type `SealedSecret`.

```bash
$ kubeseal --cert=pub-cert.pem --format=yaml < k8s-secret.yaml > sealed-secret.yaml
```

```yaml
apiVersion: bitnami.com/v1alpha1
kind: SealedSecret
metadata:
  name: sealed-secret
spec:
  encryptedData:
    FOO: AgBxANXRVg5...
    BAR: AgDRslQw8...
  template:
    metadata:
      name: k8s-secret
    type: Opaque
```
This `SealedSecret` can only be decrypted by the controller, so it can be safely distributed with all the other k8s resources.  
What’s great about this approach is that it has a comparatively small overhead. Secrets don’t need to be managed in a separate tool or platform, they just live where everything else lives. On the downside, there’s no separate tool or platform to manage secrets, so they need to be managed “by hand”.  
For small, early stage organizations this seems to be a good way to start introducing good practices around secret management.

## Google Secret Manager & External Secrets Operator
If you’re using one of the popular cloud vendors, you probably already have access to a secret management product. Maybe you are already managing access credentials in there.  
The [External Secrets Operator][eso] can connect to a multitude of common secret providers like [Google Secret Manager][gcpsm], [AWS Secrets Manager][awscm] or [Azure Key Vault][azurekv], and provide that data as k8s Secrets.  
To access a secret in Google Cloud, we first need to provide the right credentials. There are a few operational steps:
- Create a Service Account in GCP
- Download the Service Account private key
- Attach the private key to a secret
- Pass the name of the secret into a `SecretStore`, a custom resource provided by the External Secret Operator installation

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: gcpsm-secret
  labels:
    type: gcpsm
type: Opaque
stringData:
  secret-access-credentials: |-
    {
      "type": "service_account",
      "project_id": "secret-management-talk",
      "private_key_id": "",
      "private_key": "-----BEGIN PRIVATE KEY-----\n\n-----END PRIVATE KEY-----\n",
      "client_email": "external-secrets@secret-management.iam.gserviceaccount.com",
      "client_id": "",
      "auth_uri": "https://accounts.google.com/o/oauth2/auth",
      "token_uri": "https://oauth2.googleapis.com/token",
      "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
      "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/external-secrets%40secret-management.iam.gserviceaccount.com"
    }
```
```yaml
apiVersion: external-secrets.io/v1alpha1
kind: ClusterSecretStore
metadata:
  name: gcp-backend
spec:
  provider:
      gcpsm:                                  # gcpsm provider
        auth:
          secretRef:
            secretAccessKeySecretRef:
              name: gcpsm-secret              # secret name containing SA key
              key: secret-access-credentials  # key name containing SA key
              namespace: eso
        projectID: secret-management-talk     # name of Google Cloud project
```
_Note: Since this secret includes the GCP SA private key, this should not be stored it in Git. Instead this should be done once during [day 1 operations][day-1]._

Now we can tell the operator which data to retrieve and how to provide it to the k8s cluster by defining the target secret via a custom Kubernetes resource of type `ExternalSecret`.
```yaml
apiVersion: external-secrets.io/v1alpha1
kind: ExternalSecret
metadata:
  name: gcp-external-secret
  namespace: gcp-eso-app
spec:
  refreshInterval: 1h           # rate SecretManager pulls GCPSM
  secretStoreRef:
    kind: ClusterSecretStore
    name: gcp-backend           # name of the SecretStore (or kind specified)
  target:
    name: k8s-secret            # name of the k8s Secret to be created
  data:
  - secretKey: FOO              # name of the GCPSM secret key
    remoteRef:
      key: FOO
  - secretKey: BAR              # name of the GCPSM secret key
    remoteRef:
      key: BAR
```


## HashiCorp Vault & External Secrets Operator
When your team is small, it's OK to throw all your secrets in one bucket. As your team grows, you'll likely want tighter control over the tool(s) managing creation and access of your secrets.

[Hashicorp Vault][vault] can help!  
And the External Secrets Operator in the last section can connect to Vault too. For this example I've installed a Vault instance directly on the Kubernetes cluster, but generally speaking it could live anywhere.  
All you have to do is allow Kubernetes to access your Vault by creating a role for it. You can make this role as granular as you like, for example, only allowing access to specific secrets or paths.

In the `SecretStore` we then point to the Kubernetes authentication secret stored in Vault.
```bash
$ vault policy write eso-policy -<<EOF     
path "kv/data/vault-secret"                                                  
{  capabilities = ["read"]                
}                         
EOF

$ vault write auth/kubernetes/role/eso-role \
    bound_service_account_names=external-secrets \
    bound_service_account_namespaces=es \
    policies=eso-policy \
    ttl=24h
```
```yaml
apiVersion: external-secrets.io/v1alpha1
kind: ClusterSecretStore
metadata:
  name: vault-backend
spec:
  provider:
    vault:
      server: "http://vault.vault:8200"
      path: "kv"
      version: "v2"
      auth:
        kubernetes:
          mountPath: "kubernetes"
          role: "eso-role"
```
(There's a bit more to it than shown here. For a full guide check out [this tutorial][eso-vault].)

The `ExternalSecret` resource will look almost exactly the same as in the example above.
```yaml
apiVersion: external-secrets.io/v1alpha1
kind: ExternalSecret
metadata:
  name: vault-external-secret
spec:
  secretStoreRef:
    name: vault-backend
    kind: ClusterSecretStore
  target:
    name: k8s-secret
  data:
  - secretKey: FOO
    remoteRef:
      key: vault-secret
      property: FOO
  - secretKey: SOURCE
    remoteRef:
      key: vault-secret
      property: SOURCE
```
Of course the big plus in this scenario is the full control over the entire lifecycle of a secret, however it comes with its own challenges. Managing a tool like Vault does not only require pure operational effort, but also intentionally creating proper security procedures to fully leverage its usefulness.

---

To summarize: There are a multitude of ways to get secrets inside Kubernetes, but keep in mind that you need to manage and secure them outside the cluster, as well as securing the cluster itself. Safeguarding your secrets relies on every single employee. Inconvenient or convoluted processes will compromise security efforts, as people will look for the path of the least resistance and grow less alert over time.  
When choosing the best security practice for your organization, start by understanding how your team works right now and try to find the tools and architecture that fits best to existing structures rather than reinventing the wheel.


You can find a prototype of the solutions explained in this [repository][secret-mgmt-repo].  
And if you'd like to see a live demo, come visit my talk at [Cloud Native Rejekts][rejekts] in Valencia!


[GitOps]: https://www.gitops.tech/
[sealedsecrets]: https://github.com/bitnami-labs/sealed-secrets
[eso]: https://external-secrets.io/
[gcpsm]: https://cloud.google.com/secret-manager
[awscm]: https://aws.amazon.com/secrets-manager/
[azurekv]: https://azure.microsoft.com/en-us/services/key-vault/
[vault]: https://www.hashicorp.com/products/vault
[eso-vault]: https://blog.container-solutions.com/tutorialexternal-secrets-with-hashicorp-vault
[secret-mgmt-repo]: https://github.com/lianmakesthings/secrets-management-talk
[day-1]: https://codilime.com/blog/day-0-day-1-day-2-the-software-lifecycle-in-the-cloud-age/
[k8s-secrets]: https://kubernetes.io/docs/concepts/configuration/secret/
[rejekts]: https://cfp.cloud-native.rejekts.io/cloud-native-rejekts-eu-valencia-2022/talk/QLZHSD/