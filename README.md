# argocd-core

Bootstrap chart for ArgoCD, ported from the later internal evolution
(multi-source Applications, per-environment values, self-managing config).

Deploys three Applications into the `argocd-config` project:

| Application        | What it manages                                            |
|--------------------|------------------------------------------------------------|
| argocd-config      | this repo itself (self-management of the bootstrap)        |
| argocd             | ArgoCD via the public argo-helm chart + env values         |
| argocd-app-of-apps | polarpoint-io/argocd-app-of-apps chart: projects, clusters, repos, parent applications |

## Bootstrap (once per cluster)

```
helm template . -f non-prod-core-values.yaml | kubectl apply -n argocd -f -
```

Order on a fresh cluster: install ArgoCD minimally (installer/Ansible),
apply this chart, then ArgoCD adopts itself via the `argocd` Application.
The `argocd-config` AppProject is created by the app-of-apps chart; the
first sync of argocd-app-of-apps may need a manual retry before the
project exists.

## Per-environment files

- `<env>-core-values.yaml` — environment name + chart revisions
- `<env>-aoa-values.yaml`  — projects, clusters, repositories, parent apps
- `<env>-argocd-values.yaml` — argo-cd chart values (ingress, RBAC, OIDC)

## RKE1 → RKE2 migration

Workloads are disposable (no PV migration): build the RKE2 cluster
(kube-mstr-01/02 first), bootstrap with this chart, let parents converge
from `argocd-controller-applications` / `argocd-tooling-applications`,
verify, cut DNS over, retire the RKE1 node(s).
