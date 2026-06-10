# Deploying ArgoCD core

There are two separate ways to deploy ArgoCD core. Each method deploys the exact same chart with the exact same values from the exact same location. This means functionally there is no difference:

- Via the RKE Installer - for when you're standing up a cluster for the first time)
- Via Helm commands - for when you're upgrading a cluster from the old way we used to manage ArgoCD, and already has ArgoCD installed



## RKE Installer (Ansible)

Please refer to the [RKE Installer Documentation](https://git.internal.ru.com/RUNA/ansible-rke-installer/blob/main/docs/README.md)

ArgoCD will be installed as part of the standard RKE install procedure, using the `full-install.yaml` playbook. No further user action is required.

## Helm

### Prerequisites

- ArgoCD is already deployed on the cluster
- This repository is cloned locally

### Procedure

1. Log in to [bel2 argocd](https://deploy.bel2.corp-apps.com)
2. Navigate to the [argocd-configuration](https://deploy.bel2.corp-apps.com/applications/argocd-configuration)
3. On the `argocd-configuration` object which is at the head of the tree on the application page
   1. Click on the three dots to open the context menu
   2. Select delete
   3. Select **Non-cascading** so that the deletion _only_ deletes the application object, and not other objects which it has deployed
   4. Make sure you selected **Non-cascading**
   5. Type in `argocd-configuration` and click ok
4. Clone this repository and `cd` into it
5. Run `helm install argocd-core . -f values-aoa-bel2.yaml`
6. Verify `argocd-core` has deployed, and created the `argocd-config` application.

# Associated risks

There is minimal risk deploying this chart. This is for the following reasons
- ArgoCD itself is a stateless application which holds no information about deployments. This means it can be removed and redeployed without affecting any other workloads.
- The argocd-app-of-apps application doesn't deploy or modify any workloads. Rather, it deploys "parent" applications (eg, `deploy-argocd-applications`) and applicationsets. These parent applications are what deploy and manage actual workloads, and are configured in other repositories.

Similarly, the potential impact caused by ArgoCD becoming unavailable for any reason is limited. If ArgoCD does become unavailable, all applications and charts will still remain deployed - only the ability to manage their configuration and deployment will be impacted. In other words, if ArgoCD becomes unavailable for a certain amount of time, there will be no impact unless there are scheduled changes to deployed applications, or new deployments scheduled to happen.
