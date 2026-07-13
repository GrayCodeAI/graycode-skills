---
name: implementing-kubernetes-network-policy-with-calico
description: Implement Kubernetes network segmentation using Calico NetworkPolicy
  and GlobalNetworkPolicy for zero-trust pod-to-pod communication.
license: MIT
tags:
- calico
- kubernetes
- network-policy
- network-segmentation
- zero-trust
domain: cybersecurity
subdomain: container-security
version: 1.0
author: mahipal
---

# platform-tier.yaml
apiVersion: projectcalico.org/v3
kind: Tier
metadata:
  name: platform
spec:
  order: 200
```

## Monitoring and Troubleshooting

```bash
# List all network policies
kubectl get networkpolicy --all-namespaces

# List Calico-specific policies
kubectl exec -n calico-system calicoctl -- calicoctl get networkpolicy --all-namespaces -o wide
kubectl exec -n calico-system calicoctl -- calicoctl get globalnetworkpolicy -o wide

# Check policy evaluation for a specific endpoint
kubectl exec -n calico-system calicoctl -- calicoctl get workloadendpoint -n production -o yaml

# View Calico logs
kubectl logs -n calico-system -l k8s-app=calico-node --tail=100

# Test connectivity
kubectl exec -n production frontend-pod -- wget -qO- --timeout=2 http://backend-svc:8080/health
```

## Best Practices

1. **Start with default deny** - Apply deny-all policies to every namespace, then allow specific traffic
2. **Use labels consistently** - Define a labeling standard for app, tier, environment
3. **Order policies** - Use Calico policy ordering (`order` field) to control evaluation precedence
4. **Allow DNS first** - Always create DNS egress rules before applying egress deny policies
5. **Use GlobalNetworkPolicy** for cluster-wide security baselines
6. **Test policies in staging** - Validate network connectivity after applying policies
7. **Monitor denied traffic** - Enable Calico flow logs for visibility into blocked connections
8. **Use tiers** - Organize policies into security, platform, and application tiers
@ref(api-reference.md)
@ref(standards.md)
@ref(workflows.md)
