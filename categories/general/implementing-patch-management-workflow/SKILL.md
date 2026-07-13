---
name: implementing-patch-management-workflow
description: Patch management is the systematic process of identifying, testing, deploying,
  and verifying software updates to remediate vulnerabilities across an organization's
  IT infrastructure. An effective patc
license: MIT
tags:
- vulnerability-management
- patch-management
- wsus
- sccm
- ansible
domain: cybersecurity
subdomain: vulnerability-management
version: 1.0
author: mahipal
---

- name: Ring 1 - IT Early Adopters
  hosts: ring1_hosts
  serial: "25%"
  max_fail_percentage: 10
  become: yes
  tasks:
    - import_tasks: apply_patches.yml
    - import_tasks: validate_services.yml
    - name: Wait for soak period
      pause:
        hours: 48
      run_once: true

- name: Ring 2 - Business Pilot
  hosts: ring2_hosts
  serial: "20%"
  max_fail_percentage: 5
  become: yes
  tasks:
    - import_tasks: apply_patches.yml
    - import_tasks: validate_services.yml

- name: Ring 3 - General Deployment
  hosts: ring3_hosts
  serial: "10%"
  max_fail_percentage: 3
  become: yes
  tasks:
    - import_tasks: apply_patches.yml
    - import_tasks: validate_services.yml
```

### Step 5: Verification and Reporting

Run a post-patch vulnerability scan to confirm patch installation:
```bash
# Trigger post-patch verification scan
curl -k -X POST "https://nessus:8834/scans/$VERIFY_SCAN_ID/launch" \
  -H "X-Cookie: token=$TOKEN"

# Compare pre-patch and post-patch results
# Expecting reduction in vulnerabilities matching deployed patches
```

## Patch Management SLAs
| Severity | SLA (Internet-Facing) | SLA (Internal) | SLA (Air-Gapped) |
|----------|----------------------|----------------|-------------------|
| Critical (CVSS 9+) | 48 hours | 7 days | 14 days |
| High (CVSS 7-8.9) | 7 days | 14 days | 30 days |
| Medium (CVSS 4-6.9) | 30 days | 30 days | 60 days |
| Low (CVSS 0.1-3.9) | 90 days | 90 days | 90 days |

## Best Practices
1. Maintain current asset inventory to ensure complete patch coverage
2. Test all patches in a non-production environment before deployment
3. Use phased rollouts with automatic rollback capabilities
4. Coordinate patch windows with change management process
5. Track patch compliance metrics and report to leadership
6. Automate where possible to reduce manual effort and human error
7. Maintain exception documentation for systems that cannot be patched
8. Include third-party application patching (not just OS patches)

## Common Pitfalls
- Patching only operating systems and ignoring third-party applications
- No rollback plan if patches cause service disruption
- Treating all patches with equal urgency (no risk-based prioritization)
- Manual patch processes that cannot scale
- No post-patch verification to confirm successful installation
- Ignoring firmware and BIOS updates

## Related Skills
- prioritizing-vulnerabilities-with-cvss-scoring
- implementing-vulnerability-remediation-sla
- implementing-continuous-vulnerability-monitoring
@ref(api-reference.md)
@ref(standards.md)
@ref(workflows.md)
