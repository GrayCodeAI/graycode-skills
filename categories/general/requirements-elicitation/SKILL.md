---
name: requirements-elicitation
description: "Use to transform ambiguous business needs into structured, validated, prioritized requirements with stakeholder discovery, user stories, NFRs, acceptance criteria, and traceability matrices."
license: MIT
tags:
- requirements
- specifications
- user-stories
- acceptance-criteria
- analysis
---

# Skills

This skill serves as the AI agent's comprehensive framework for transforming ambiguous business needs, user problems, and stakeholder inputs into well-structured, validated, and prioritized requirements. The agent should treat each phase as a mandatory checkpoint, producing concrete artifacts before advancing. The output of this skill feeds directly into downstream activities such as architecture design, development planning, and quality assurance.

## When to use

Activate this skill when any of the following conditions are detected:

- A user describes a product idea, business problem, or feature concept and needs help turning it into structured requirements.
- A user asks for help writing user stories, use cases, acceptance criteria, or a requirements specification document.
- A user presents a set of requirements and asks for a review, gap analysis, or improvement.
- A user needs help distinguishing functional requirements from non-functional requirements.
- A user asks how to prioritize a backlog of features or requirements.
- A user wants help identifying stakeholders and understanding their needs.
- A user asks how to resolve conflicting requirements from different stakeholders.
- A user needs help defining acceptance criteria, definition of done, or testable conditions for a feature.
- A user presents a vague or ambiguous request and needs help decomposing it into specific, actionable requirements.
- A user asks about requirements traceability, impact analysis, or change management for evolving product needs.
- A user wants to validate whether a set of requirements is complete, consistent, feasible, and unambiguous.
- A conversation involves terms such as "user story," "use case," "business requirement," "functional requirement," "non-functional requirement," "acceptance criteria," "MoSCoW," "INVEST," "jobs to be done," "requirement specification," "PRD," "BRD," "scope," "edge case," or similar requirements language.
- The user wants requirements or a PRD translated directly into a working, production-grade backend (API/CRUD/service) — in these cases ALSO load `backend-craft` and run its intent-first, backend-type classification, and library-first implementation flow against the derived requirements.

Do NOT activate this skill for pure system design or infrastructure questions with no requirements dimension (use product-architecture-design instead), code-level debugging or implementation tasks, or project scheduling and resource allocation questions with no product scope dimension.

## Instructions

### Phase 1 — Context and Stakeholder Discovery

1. **Establish the problem context.** Before capturing any requirements, ground the analysis in the problem space. Determine and explicitly state:
   - **Problem statement:** What problem is being solved? For whom? Write it as a single, clear sentence: *"[Stakeholder group] currently struggles with [problem] which results in [negative outcome]."*
   - **Product vision or objective:** What does success look like at the highest level? Capture this as a goal statement: *"Enable [target user] to [capability] so that [business/user value]."*
   - **Scope boundary:** What is explicitly in scope and what is explicitly out of scope for this requirements effort? Define the boundary early to prevent scope creep. If the user has not stated scope, propose one and seek confirmation.
   - **Stage of product:** Is this a new product (greenfield), a new feature within an existing product, a redesign of existing functionality, or a migration? This determines the baseline assumptions.

2. **Identify and classify stakeholders.** Enumerate every person, group, or system that has an interest in or is affected by the product. For each stakeholder, capture:
   - **Name or role:** e.g., "End User — Free Tier," "Operations Team," "Payment Gateway (external system)," "Compliance Officer."
   - **Stake type:** Classify as one of: *Primary user* (directly interacts), *Secondary user* (indirectly affected), *Business sponsor* (funds or authorizes), *Regulatory/compliance* (imposes constraints), *Technical/operations* (builds or maintains), *External system* (integrates programmatically).
   - **Key goals and motivations:** What does this stakeholder want from the system? What does success look like for them?
   - **Key concerns and fears:** What could go wrong for them? What would make them resist the solution?
   - **Influence and authority level:** High / Medium / Low. Who has final decision-making power when conflicts arise?
   - **Communication channel:** How will requirements be validated with this stakeholder (direct interview, survey, proxy through product owner, documentation review)?

   If the user has not provided stakeholder information, ask clarifying questions. At minimum, identify the primary end user, the business sponsor, and the technical/operations team.

3. **Understand the current state (as-is).** Before defining what the system should do, understand what exists today:
   - **Current workflow or process:** How do stakeholders accomplish their goal today? Map the steps, even if manual, inefficient, or nonexistent. This surfaces pain points and implicit requirements.
   - **Existing systems and tools:** What systems are currently in use? What data already exists? What integrations are in place?
   - **Known pain points:** What specific frustrations, bottlenecks, errors, or inefficiencies exist in the current state? Rank them by severity and frequency.
   - **Previous attempts:** Has this problem been attempted before? What was tried and why did it fail or fall short?

   If no current state exists (greenfield), state that explicitly and note that all workflows are net-new.

### Phase 2 — Requirement Elicitation

4. **Elicit business requirements.** Capture the high-level business needs that justify the product or feature. These are outcome-oriented, not solution-oriented. For each business requirement:
   - **ID:** BR-001, BR-002, etc.
   - **Statement:** *"The business must be able to [outcome] in order to [strategic value]."*
   - **Success metric:** How will we measure whether this business requirement is met? Define a quantifiable KPI or OKR (e.g., "reduce customer onboarding time from 3 days to 30 minutes," "increase conversion rate by 15%").
   - **Sponsoring stakeholder:** Who owns this requirement?
   - **Priority:** Critical / High / Medium / Low (refine in Phase 4).

5. **Elicit functional requirements using structured techniques.** Extract what the system must *do*. Use multiple elicitation lenses to ensure completeness:

   **Lens A — User Stories (for user-facing capabilities):**
   For each capability, write a user story following the INVEST criteria (Independent, Negotiable, Valuable, Estimable, Small, Testable):
   - **Format:** *"As a [specific user role], I want to [action/capability], so that [benefit/value]."*
   - **ID:** FR-001, FR-002, etc.
   - **Linked business requirement:** Which BR does this support?

   **Lens B — Use Cases (for complex interactions):**
   For workflows involving multiple steps, actors, or decision points, write structured use cases:
   - **Use case name:** Verb-noun format (e.g., "Process Refund").
   - **Primary actor:** Who initiates the use case.
   - **Preconditions:** What must be true before the use case begins.
   - **Main success scenario (happy path):** Numbered step-by-step sequence.
   - **Alternative flows:** Variations that still lead to success.
   - **Exception flows:** Error conditions and how the system should respond.
   - **Postconditions:** What must be true after the use case completes.

   **Lens C — Jobs To Be Done (for uncovering latent needs):**
   Ask: *"When [situation], I want to [motivation], so I can [expected outcome]."* This surfaces needs the user may not have articulated as features.

   **Lens D — Input/Output Analysis:**
   For data-intensive systems, enumerate: What data enters the system? What transformations occur? What outputs are produced? Who consumes them?

6. **Elicit non-functional requirements (quality attributes).** For each of the following categories, extract explicit requirements or state default assumptions. Every non-functional requirement must be measurable:

   - **Performance:**
     - Response time targets (p50, p95, p99) for critical operations.
     - Throughput targets (transactions per second, concurrent users).
     - Batch processing windows if applicable.
   - **Scalability:**
     - Expected initial load and projected growth (6-month, 12-month, 3-year).
     - Peak-to-average load ratio.
   - **Availability and Reliability:**
     - Uptime target (e.g., 99.9%).
     - Planned maintenance windows.
     - Mean time to recovery (MTTR) target.
   - **Security:**
     - Authentication requirements (SSO, MFA, API keys).
     - Authorization granularity (role-based, attribute-based, resource-level).
     - Data classification (public, internal, confidential, restricted).
     - Encryption requirements (at rest, in transit).
     - Audit logging requirements.
   - **Compliance and Regulatory:**
     - Applicable regulations (GDPR, HIPAA, PCI-DSS, SOX, ADA/WCAG, etc.).
     - Data residency requirements.
     - Retention and deletion policies.
   - **Usability:**
     - Accessibility standards (WCAG 2.1 level AA, etc.).
     - Supported devices, browsers, platforms.
     - Localization and internationalization requirements.
   - **Maintainability:**
     - Expected release cadence.
     - Logging, monitoring, and debugging requirements.
     - Documentation standards.
   - **Compatibility and Integration:**
     - Systems that must integrate (APIs, databases, file formats).
     - Data migration requirements from legacy systems.
     - Backward compatibility constraints.
   - **Data Requirements:**
     - Data volume estimates (storage, record counts).
     - Data freshness requirements (real-time, near-real-time, batch).
     - Backup and recovery requirements (RPO, RTO).

   Assign each non-functional requirement an ID: NFR-001, NFR-002, etc.

7. **Elicit constraints and assumptions.** Separate hard constraints from soft preferences and assumptions:
   - **Constraints (non-negotiable):** Technology mandates, budget limits, timeline deadlines, team skill limitations, regulatory mandates. Format: *"The system must [constraint] because [reason]."*
   - **Preferences (negotiable):** Desired but flexible parameters. Format: *"The system should preferably [preference], but [alternative] is acceptable if [condition]."*
   - **Assumptions:** Conditions believed to be true but not verified. Format: *"We assume [assumption]. If false, impact on requirements: [impact]."*

   Assign IDs: CON-001, PREF-001, ASMP-001, etc.

8. **Discover edge cases and negative requirements.** Explicitly ask and document:
   - **Edge cases:** What happens at boundary conditions? (zero items, maximum items, empty input, special characters, concurrent modifications, timezone boundaries, leap years, etc.)
   - **Negative requirements:** What must the system explicitly *not* do? (e.g., "The system must not store credit card numbers in plain text," "The system must not allow users to access other users' data.")
   - **Abuse cases:** How could a malicious actor misuse the system? What safeguards are required?

   Add these as functional or non-functional requirements with appropriate IDs.

### Phase 3 — Requirements Analysis and Modeling

9. **Check for completeness.** Systematically verify that no major category of requirements has been overlooked. Walk through this checklist:
   - [ ] All stakeholder groups have at least one requirement attributed to them.
   - [ ] All critical user journeys identified in Step 1 are covered by functional requirements.
   - [ ] All CRUD operations for every core entity are addressed (Create, Read, Update, Delete — plus Search, Archive, Export if applicable).
   - [ ] Error handling and failure scenarios are defined for every functional requirement.
   - [ ] Administrative and operational requirements are captured (user management, configuration, monitoring, reporting).
   - [ ] Onboarding and offboarding flows are defined (first-time setup, account creation, account deletion/data export).
   - [ ] Notification and communication requirements are captured (email, SMS, push, in-app).
   - [ ] All non-functional requirement categories from Step 6 have been addressed.

   Flag any gaps as open questions and present them to the user.

10. **Check for consistency and conflicts.** Analyze the full set of requirements for contradictions:
    - **Intra-stakeholder conflicts:** Does a single stakeholder's requirements contradict each other?
    - **Inter-stakeholder conflicts:** Do different stakeholders want mutually exclusive outcomes? (e.g., "marketing wants maximum data collection" vs. "compliance wants data minimization").
    - **Functional vs. non-functional conflicts:** Does a functional requirement make a non-functional requirement impossible? (e.g., "real-time global sync" vs. "99.999% availability" — CAP theorem tension).
    - **Constraint conflicts:** Do constraints contradict each other or make requirements infeasible?

    For each conflict discovered, document:
    - **Conflict ID:** CONF-001, CONF-002, etc.
    - **Conflicting requirements:** Reference the IDs.
    - **Nature of conflict:** Explain the contradiction.
    - **Proposed resolution options:** Offer at least two resolution paths.
    - **Recommended resolution:** State which option you recommend and why.
    - **Resolution owner:** Which stakeholder must make the final call?

11. **Check for feasibility.** Evaluate whether each requirement is technically and practically achievable given the stated constraints:
    - **Technical feasibility:** Can this be built with available technology within the constraints?
    - **Resource feasibility:** Can this be delivered within the budget and team capacity?
    - **Timeline feasibility:** Can this be delivered within the stated deadline?
    - **Dependency feasibility:** Does this depend on something outside the team's control (third-party API, regulatory approval, hardware availability)?

    Flag infeasible requirements with a clear explanation and propose alternatives: scope reduction, phased delivery, or constraint relaxation.

12. **Check for ambiguity.** Review every requirement statement for vague language. Replace the following ambiguous terms with measurable, specific alternatives:
    - "Fast" → specific latency target (e.g., "< 200ms p95")
    - "Scalable" → specific load target (e.g., "support 10,000 concurrent users")
    - "User-friendly" → specific usability criteria (e.g., "complete core task in < 3 clicks")
    - "Secure" → specific security controls (e.g., "AES-256 encryption at rest")
    - "Reliable" → specific availability target (e.g., "99.95% monthly uptime")
    - "Easy to maintain" → specific maintainability criteria (e.g., "deploy in < 15 minutes with zero downtime")
    - "Support large volumes" → specific data volume (e.g., "100M records, 5TB storage")
    - "Real-time" → specific latency (e.g., "< 1 second end-to-end")
    - "Seamless" → specific UX criteria
    - "Intuitive" → specific learnability metric

    Every requirement must pass the **testability test:** Can a QA engineer write a pass/fail test case from this requirement alone? If not, it is too ambiguous.

13. **Model the requirements.** Create structured models to expose relationships, dependencies, and gaps:
    - **Entity-Relationship Model:** Identify the core domain entities (nouns) and their relationships. List entities, key attributes, and cardinalities. Present as a textual description or Mermaid ER diagram.
    - **State Transition Model:** For entities with lifecycle states (e.g., Order: Draft → Submitted → Processing → Fulfilled → Cancelled), define valid state transitions, triggers, and guards.
    - **Process Flow Model:** For complex multi-step workflows, describe the flow as a numbered sequence or suggest a Mermaid flowchart/sequence diagram.
    - **Context Map:** If multiple bounded contexts or sub-domains are emerging, map their relationships (shared kernel, customer-supplier, conformist, anti-corruption layer).

    Only produce models that add clarity. Skip models that would be trivial for simple requirements.

### Phase 4 — Prioritization and Scoping

14. **Prioritize requirements using a structured framework.** Apply at least one of the following methods (choose the most appropriate, or combine):

    **Method A — MoSCoW:**
    Classify every requirement as:
    - **Must have:** The product is non-viable without this. These define the Minimum Viable Product (MVP).
    - **Should have:** Important, expected by users, but the product can launch without it temporarily.
    - **Could have:** Desirable enhancement, included if time and resources permit.
    - **Won't have (this iteration):** Explicitly excluded from current scope but acknowledged for future.

    **Method B — Value vs. Effort Matrix:**
    Score each requirement on two axes:
    - **Business value:** (1–5) based on revenue impact, user satisfaction, strategic alignment, or risk mitigation.
    - **Implementation effort:** (1–5) based on complexity, time, dependencies, and risk.
    - Plot into quadrants: Quick Wins (high value, low effort) → do first. Big Bets (high value, high effort) → plan carefully. Fill-ins (low value, low effort) → include opportunistically. Money Pits (low value, high effort) → deprioritize or eliminate.

    **Method C — RICE Scoring:**
    For each requirement, calculate: **(Reach × Impact × Confidence) / Effort**
    - **Reach:** How many users/transactions will this affect in a given period?
    - **Impact:** How significantly will it affect each user? (3 = massive, 2 = high, 1 = medium, 0.5 = low, 0.25 = minimal)
    - **Confidence:** How confident are we in the estimates? (100% = high, 80% = medium, 50% = low)
    - **Effort:** Person-months or story points.

    Present the prioritized list as a ranked table with the scoring visible.

15. **Define the MVP (Minimum Viable Product) or iteration scope.** Based on the prioritization:
    - Draw a clear line between what is in the MVP and what is deferred.
    - Validate that the MVP is coherent: does it solve the core problem end-to-end for the primary user? Can the primary user journey (Step 1) be completed with only MVP requirements?
    - Identify any "Must have" requirements that are particularly risky or uncertain and flag them for early prototyping or spike work.
    - If applicable, define subsequent iterations (v1.1, v2.0) and tentatively assign "Should have" and "Could have" requirements to them.

16. **Build a dependency map.** Identify requirements that depend on other requirements:
    - **Format:** *"FR-012 depends on FR-003 (user authentication must exist before role-based access can be implemented)."*
    - Identify critical path chains: sequences of dependent requirements that determine the minimum delivery timeline.
    - Flag circular dependencies as design risks that need resolution.
    - Present as a textual dependency list or suggest a Mermaid graph.

### Phase 5 — Acceptance Criteria and Validation

17. **Write acceptance criteria for every functional requirement.** Each requirement must have testable acceptance criteria that define "done." Use the **Given-When-Then** format:
    ```
    Given [precondition / initial context]
    When [action / trigger performed by the actor]
    Then [expected observable outcome]
    ```
    Write at minimum:
    - **One happy path** scenario (the main success case).
    - **One alternative path** scenario (a valid but non-default flow).
    - **One error/edge case** scenario (invalid input, boundary condition, unauthorized access, system failure).

    Example:
    ```
    FR-005: User can reset their password via email
    
    AC-1 (Happy path):
    Given a registered user with a verified email address
    When they request a password reset and click the link within 30 minutes
    Then they are prompted to enter a new password and can log in with the new password

    AC-2 (Expired link):
    Given a registered user who requested a password reset
    When they click the reset link after 30 minutes have elapsed
    Then they see a message "This link has expired" and are prompted to request a new one

    AC-3 (Invalid email):
    Given a visitor who enters an email not associated with any account
    When they request a password reset
    Then the system displays the same confirmation message as a valid request (to prevent email enumeration)
    ```

18. **Define non-functional acceptance criteria.** For each non-functional requirement, define how it will be verified:
    - **Performance:** Load test scenario, target metric, tool to be used (e.g., "Using k6, simulate 5,000 concurrent users; p99 response time for /api/search must be < 500ms").
    - **Security:** Specific test or audit (e.g., "Pass OWASP Top 10 scan using ZAP with zero high-severity findings").
    - **Availability:** Chaos engineering scenario (e.g., "Terminate one application instance; system continues serving requests with < 1% error rate").
    - **Compliance:** Audit checklist item (e.g., "All PII fields encrypted at rest; verified by database inspection").
    - **Accessibility:** Specific standard and test (e.g., "All pages pass axe-core automated scan at WCAG 2.1 AA level").

19. **Validate requirements with stakeholders.** Before finalizing, present a structured validation checkpoint:
    - **Completeness check:** "Have we captured everything you need the system to do?"
    - **Correctness check:** "Does each requirement accurately reflect your intent?"
    - **Priority check:** "Do you agree with the MVP scope and priority rankings?"
    - **Conflict resolution check:** "Are the proposed conflict resolutions acceptable?"
    - **Feasibility check:** "Are you aware of the tradeoffs required for infeasible requirements?"

    Document any changes from validation as a revision with a changelog entry.

### Phase 6 — Traceability and Change Management

20. **Build a requirements traceability matrix (RTM).** Create a mapping that connects every requirement to:
    - **Upstream:** The business requirement, stakeholder goal, or regulatory mandate it serves.
    - **Downstream:** The architectural component, API, data entity, or test case that implements/verifies it.
    - **Format (table):**

    | Req ID | Requirement Summary | Source (Stakeholder/BR) | Architectural Component | Test Case ID | Priority | Status |
    |--------|-------------------|------------------------|------------------------|-------------|----------|--------|
    | FR-001 | User registration  | BR-001 / End User      | Auth Service           | TC-001–003  | Must     | Draft  |

    This matrix ensures no requirement is orphaned (implemented but unjustified) or forgotten (justified but unimplemented).

21. **Define the change management process for requirements.** Establish how requirements will evolve:
    - **Change request format:** What information must a change request contain? (Requestor, affected requirement IDs, proposed change, justification, impact assessment.)
    - **Impact analysis protocol:** When a requirement changes, trace through the RTM to identify all affected components, interfaces, test cases, and downstream requirements.
    - **Approval authority:** Who can approve requirement changes at each priority level? (e.g., "Must have" changes require product owner + tech lead; "Could have" changes require product owner only.)
    - **Version control:** All requirements documents must be versioned. Each version includes a changelog with: date, change description, affected requirement IDs, approved by.

### Phase 7 — Requirements Deliverable Assembly

22. **Compose the final requirements specification document.** Organize all outputs into a structured deliverable with these sections:
    1. **Executive Summary** — One-paragraph overview of the product/feature purpose, target users, and scope.
    2. **Problem Statement and Vision** — Problem context, product vision, and success metrics (from Step 1).
    3. **Stakeholder Register** — Stakeholder inventory with roles, goals, concerns, and influence (from Step 2).
    4. **Current State Analysis** — As-is workflow, existing systems, pain points (from Step 3).
    5. **Business Requirements** — Numbered list with success metrics (from Step 4).
    6. **Functional Requirements** — User stories and/or use cases with full detail (from Step 5).
    7. **Non-Functional Requirements** — Categorized, measurable quality attribute requirements (from Step 6).
    8. **Constraints, Preferences, and Assumptions** — Clearly separated and numbered (from Step 7).
    9. **Edge Cases and Negative Requirements** — Boundary conditions, abuse cases, exclusions (from Step 8).
    10. **Domain Models** — Entity-relationship diagrams, state machines, process flows (from Step 13).
    11. **Prioritized Requirements Backlog** — Ranked list with scoring rationale and MVP scope line (from Steps 14–15).
    12. **Dependency Map** — Requirement dependencies and critical path (from Step 16).
    13. **Acceptance Criteria** — Given-When-Then criteria for all functional and non-functional requirements (from Steps 17–18).
    14. **Requirements Traceability Matrix** — Full upstream and downstream mapping (from Step 20).
    15. **Conflict Log and Resolutions** — All identified conflicts and their resolutions (from Step 10).
    16. **Open Questions** — Unresolved items requiring stakeholder input, flagged with owner and deadline.
    17. **Glossary** — Definitions of all domain-specific terms used in the document to ensure shared understanding.
    18. **Changelog** — Version history of the requirements document.

23. **Adapt the depth and format to the user's need.** Not every request requires all preceding steps at full depth. Apply these guidelines:
    - **Quick requirement clarification** (user asks a focused question, e.g., "help me write acceptance criteria for this feature"): Jump directly to Step 17 and produce targeted acceptance criteria. Reference upstream context if provided.
    - **Single feature analysis** (user describes one feature or user story): Execute Steps 1, 5, 6, 8, 12, and 17 scoped to that feature. Produce a concise feature specification.
    - **Full product requirements** (user asks for a complete requirements analysis): Execute all steps sequentially, producing the full deliverable from Step 22.
    - **Requirements review** (user presents existing requirements for critique): Map existing requirements against the checklists in Steps 9–12, identify gaps and ambiguities, and provide a prioritized list of improvements.
    - **Backlog grooming assistance** (user has a list of items to refine): Focus on Steps 5, 12, 14, and 17 — refine story format, remove ambiguity, prioritize, and add acceptance criteria.

    Always state which depth level you are operating at and why.

24. **Maintain a collaborative, iterative approach.** Requirements evolve through conversation. After delivering the initial analysis:
    - Invite the user to challenge, correct, or extend any requirement.
    - When new information surfaces, re-enter the affected phase and trace the impact of changes through downstream steps (e.g., a new stakeholder discovered in Step 2 may introduce new functional requirements in Step 5, shift priorities in Step 14, and add rows to the RTM in Step 20).
    - Version every iteration of the requirements. Clearly state what changed and why.
    - Proactively identify areas of uncertainty and recommend specific questions the user should ask their stakeholders, users, or technical team to resolve them.
