---
name: mobile-ads-integration-validation
description: "Validate a project's mobile ads SDK integration for iOS, Android, or Unity, covering ad unit IDs, ad formats, SKAdNetwork IDs, mediation compatibility, and ad preloading. Use for a pre-launch audit."
license: Apache-2.0
tags:
- mobile
- ads
- validation
---

# Validate Google Mobile Ads SDK Integration

Validate a project's Google Mobile Ads (GMA) SDK integration either as a
complete audit or for specific requested checks.

-   **Full Audit**: If the user requests a general validation or full audit,
    evaluate all checklist items.
-   **Specific Checks**: If the user asks to validate only a specific area
    (e.g., ad preloading), evaluate only the relevant check(s) without running
    the entire checklist.

## Scoring Rules

For each check, apply one of the following statuses:

-   **Pass**: None of the Warning, Fail, or N/A criteria are met.
-   **Warning**, **Fail**, or **N/A**: The conditions described under each
    respective status are met.

## Validation Checklist

Read the reference guide for each check to be performed:

-   No test application ID is in the project, format correct:
    `references/application-id.md`
-   No test ad units are in the project, format correct:
    `references/ad-units.md`
-   Implemented all Google SKAdNetwork IDs:
    `references/google-skadnetwork-ids.md`
-   Mediation adapter compatibility:
    `references/mediation-adapter-compatibility.md`
-   Ad preloading validation checks: `references/ad-preloading.md`

## Final Output

Generate a Markdown report following the format below. **ONLY** include the
findings for items that were actually checked.

| Check | Status | Findings | Next Steps |
| :--- | :---: | :--- | :--- |
| No test application ID is in the project, format correct | {{status_1}} | {{findings_1}} | {{next_steps_1}} |
| No test ad units are in the project, format correct | {{status_2}} | {{findings_2}} | {{next_steps_2}} |
| Implemented all Google SKAdNetwork IDs | {{status_3}} | {{findings_3}} | {{next_steps_3}} |
| Mediation adapter compatibility | {{status_4}} | {{findings_4}} | {{next_steps_4}} |
| Ad preloading validation checks | {{status_5}} | {{findings_5}} | {{next_steps_5}} |
