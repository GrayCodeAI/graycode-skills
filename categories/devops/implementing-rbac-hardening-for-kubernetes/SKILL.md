---
name: implementing-rbac-hardening-for-kubernetes
description: Harden Kubernetes Role-Based Access Control by implementing least-privilege
  policies, auditing role bindings, eliminating cluster-admin sprawl, and integrating
  external identity providers.
license: MIT
tags:
- kubernetes
- rbac
- access-control
- least-privilege
- security-hardening
domain: cybersecurity
subdomain: container-security
version: 1.0
author: mahipal
---

apiVersion: apps/v1
kind: Deployment
metadata:
  name: payment-processor
  namespace: payments
spec:
  template:
    spec:
      serviceAccountName: payment-processor
      automountServiceAccountToken: true  # Only mount when explicitly needed
      containers:
        - name: processor
          image: payments/processor:v2.1@sha256:abc...
```

### 4. Restrict Dangerous Permissions

Block permissions that enable privilege escalation:

```yaml
# Dangerous verbs/resources to restrict:
# - secrets: get, list, watch (exposes all secrets in namespace)
# - pods/exec: create (enables command execution in pods)
# - pods: create with privileged securityContext
# - serviceaccounts/token: create (generates new tokens)
# - clusterroles/clusterrolebindings: create, update (self-escalation)
# - nodes/proxy: create (bypasses API server authorization)

# Safe read-only role example
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRole
metadata:
  name: security-viewer
rules:
  - apiGroups: [""]
    resources: ["pods", "services", "namespaces", "nodes"]
    verbs: ["get", "list", "watch"]
  - apiGroups: ["apps"]
    resources: ["deployments", "daemonsets", "statefulsets"]
    verbs: ["get", "list", "watch"]
  - apiGroups: ["networking.k8s.io"]
    resources: ["networkpolicies"]
    verbs: ["get", "list", "watch"]
```

### 5. OIDC Integration for User Authentication

```yaml
# API server flags for OIDC integration
apiVersion: v1
kind: Pod
metadata:
  name: kube-apiserver
spec:
  containers:
    - name: kube-apiserver
      command:
        - kube-apiserver
        - --oidc-issuer-url=https://idp.company.com
        - --oidc-client-id=kubernetes
        - --oidc-username-claim=email
        - --oidc-groups-claim=groups
        - --oidc-ca-file=/etc/kubernetes/pki/oidc-ca.crt
```

## RBAC Audit Process

### Step 1: Enumerate All Bindings

```bash
# All ClusterRoleBindings with subjects
kubectl get clusterrolebindings -o json | jq -r '
  .items[] | select(.subjects != null) |
  .subjects[] as $s |
  "\(.metadata.name) | \(.roleRef.name) | \($s.kind)/\($s.name)"
' | sort | column -t -s '|'

# All RoleBindings across namespaces
kubectl get rolebindings --all-namespaces -o json | jq -r '
  .items[] | select(.subjects != null) |
  .subjects[] as $s |
  "\(.metadata.namespace) | \(.metadata.name) | \(.roleRef.name) | \($s.kind)/\($s.name)"
' | sort | column -t -s '|'
```

### Step 2: Identify Overprivileged Service Accounts

```bash
# Find service accounts with cluster-admin or admin roles
kubectl get clusterrolebindings -o json | jq -r '
  .items[] |
  select(.roleRef.name == "cluster-admin" or .roleRef.name == "admin") |
  select(.subjects[]?.kind == "ServiceAccount") |
  "\(.subjects[] | select(.kind == "ServiceAccount") | "\(.namespace)/\(.name)")"
'
```

### Step 3: Check Default Service Account Usage

```bash
# Find pods using the default service account
kubectl get pods --all-namespaces -o json | jq -r '
  .items[] |
  select(.spec.serviceAccountName == "default" or .spec.serviceAccountName == null) |
  "\(.metadata.namespace)/\(.metadata.name)"
'
```

### Step 4: Verify Token Auto-Mount

```bash
# Find pods with auto-mounted service account tokens
kubectl get pods --all-namespaces -o json | jq -r '
  .items[] |
  select(.spec.automountServiceAccountToken != false) |
  "\(.metadata.namespace)/\(.metadata.name) sa=\(.spec.serviceAccountName // "default")"
'
```

## Tooling

### rbac-lookup

```bash
# Install rbac-lookup
kubectl krew install rbac-lookup

# View RBAC for a specific user
kubectl rbac-lookup developer@company.com

# View all RBAC bindings wide format
kubectl rbac-lookup --kind user -o wide
```

### rakkess (Review Access)

```bash
# Install rakkess
kubectl krew install access-matrix

# Show access matrix for current user
kubectl access-matrix

# Show access for a specific service account
kubectl access-matrix --sa payments:payment-processor
```

## References

- [Kubernetes RBAC Documentation](https://kubernetes.io/docs/reference/access-authn-authz/rbac/)
- [CIS Kubernetes Benchmark - RBAC Controls](https://www.cisecurity.org/benchmark/kubernetes)
- [Kubernetes Security Hardening Guide 2025](https://sealos.io/blog/a-practical-guide-to-kubernetes-security-hardening-your-cluster-in-2025/)
- [OWASP Kubernetes Security Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Kubernetes_Security_Cheat_Sheet.html)
@ref(api-reference.md)
@ref(standards.md)
@ref(workflows.md)
