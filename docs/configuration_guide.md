# Configuration Guide

Configuration of `argocd-core` is done through the varying `values-*.yaml` files. Those which have an environment in their name are only used for that specific environment. Those with are used with all.

## ArgoCD

ArgoCD-specific config is found in `values-argocd.yaml`. This config should be the same for all environments. You can view the schema and possible values to use [from the upstream chart documentation].

## ArgoCD App of Apps

Config for the app-of-apps is found in `values-aoa-<environment>.yaml`, for example `values-aoa-ltrudev.yaml`. The schema for this values file is:

```yaml
environment: string # Environment this file belongs to
aoa_version: string # The version of the app-of-apps chart to use
argocd_chart_revision: string # Version of the upstream chart
argocd_app_of_apps:

  global: 
    # Configuration of the deploy cluster
    namespace: argocd
    defaultCluster: https://kubernetes.default.svc
    clusterName: deploy-auto-bel2
    syncPolicy:
      automated:
        prune: false
        selfHeal: false

  privateGitRepositories:
    # List of private git repos
    - name: string # Name of a private repository
      url: string # URL of the private repository (either ssh or https)

  publicHelmRepositories:
    # List of public chart repos
    - name: string # Name of the repository
      url: string # Url of the repository

  privateCredentialsTemplates:
    - name: string
      url: string

  privateHelmRepositories:
    # List of private repos for helm
    - name: string
      url: string

  clusters:
    # List of clusters, with associated labels
    - name: string
      url: string
      labels: map # Key-Value map of labels

  projects:
    # List of ArgoCD projects
    - name: string
      urls:
        # List of repositories and registries
        - name: string
          url: string
          path: string # optional
      permissions:
        rw:
          description: string
          groups: list # List of AD groups to be granted RW permission to the project
        ro:
          description: string
          groups: list # List of AD groups to be granted RO permission to the project
      destinations:
        # List of clusters and namespaces this project can deploy to
        - name: string # Cluster name
          namespace: string # Namespace (accepts wildcard "*")
          server: string # URL of the cluster API
      applications:
        # List of applications to deploy using this project
        - name: string # Application name
          url: string # Application repo URL
          path: string # Path within the repo to the chart
          targetRevision: string # Branch or tag from the repository to use
          namespace: string # Kubernetes namespace to deploy in
          directory:
            recurseDirectory: bool     
```