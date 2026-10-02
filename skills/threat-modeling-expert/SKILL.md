---
name: threat-modeling-expert
description: "Expert in threat modeling methodologies, security architecture review, and risk assessment. Masters STRIDE, PASTA, attack trees, and security requirement extraction. Use PROACTIVELY for security architecture reviews, threat identification, or building secure-by-design systems."
risk: unknown
source: community
date_added: "2026-02-27"
---

# Threat Modeling Expert

Expert in threat modeling methodologies, security architecture review, and risk assessment. Masters STRIDE, PASTA, attack trees, and security requirement extraction. Use PROACTIVELY for security architecture reviews, threat identification, or building secure-by-design systems.

## Capabilities

- STRIDE threat analysis
- Attack tree construction
- Data flow diagram analysis
- Security requirement extraction
- Risk prioritization and scoring
- Mitigation strategy design
- Security control mapping

## Use this skill when

- Designing new systems or features
- Reviewing architecture for security gaps
- Preparing for security audits
- Identifying attack vectors
- Prioritizing security investments
- Creating security documentation
- Training teams on security thinking

## Do not use this skill when

- You lack scope or authorization for security review
- You need legal or compliance certification
- You only need automated scanning without human review

## Instructions

1. Define system scope and trust boundaries
2. Create data flow diagrams
3. Identify assets and entry points
4. Apply STRIDE to each component
5. Build attack trees for critical paths
6. Score and prioritize threats
7. Design mitigations
8. Document residual risks

### STRIDE — apply to every element that crosses a trust boundary

| Category | Violates | Example on a login endpoint |
|---|---|---|
| **S**poofing | Authentication | Attacker submits a forged JWT with `alg: none` |
| **T**ampering | Integrity | Request body modified in transit without signature check |
| **R**epudiation | Non-repudiation | No audit log of who changed a permission — user denies doing it |
| **I**nformation disclosure | Confidentiality | Verbose error message leaks whether a username exists |
| **D**enial of service | Availability | Unbounded login attempts exhaust a rate limiter's memory |
| **E**levation of privilege | Authorization | IDOR — user A edits user B's resource via a guessable ID in the URL |

Walk each data flow arrow on the diagram through all six categories — most real threat models
miss Repudiation and Information Disclosure because they don't map to an obvious "attack",
not because they're rare.

### Attack tree — example (root goal, then AND/OR decomposition)

```
Goal: Compromise admin account
├─ OR: Credential stuffing (reused password from a breach dump)
├─ OR: Phishing (fake login page harvests credentials)
└─ AND: Session hijacking
   ├─ Steal session token (XSS, or unencrypted transport)
   └─ Replay token before expiry
```

`OR` nodes are alternative paths to the goal (mitigate the cheapest one first). `AND` nodes
require every child to succeed (breaking any one child defeats that whole branch — often the
highest-leverage mitigation).

### Scoring: DREAD (simple, use when a full CVSS pass is overkill)

`Damage + Reproducibility + Exploitability + Affected users + Discoverability`, each scored 1-10,
averaged. A threat scoring 8+ average blocks release; 5-7 needs a tracked mitigation before GA;
below 5 can ship with the risk documented.

Pitfall: threat models that stop at "apply STRIDE" without walking every trust-boundary-crossing
arrow individually produce a false sense of coverage — teams tend to threat-model the happy-path
data flow and skip the admin/internal/batch-job flows that usually have weaker controls and are
where real breaches originate.

## Safety

- Avoid storing sensitive details in threat models without access controls.
- Keep threat models updated after architecture changes.

## Best Practices

- Involve developers in threat modeling sessions
- Focus on data flows, not just components
- Consider insider threats
- Update threat models with architecture changes
- Link threats to security requirements
- Track mitigations to implementation
- Review regularly, not just at design time

## Limitations
- Use this skill only when the task clearly matches the scope described above.
- Do not treat the output as a substitute for environment-specific validation, testing, or expert review.
- Stop and ask for clarification if required inputs, permissions, safety boundaries, or success criteria are missing.
