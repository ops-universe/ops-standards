# Engineering standards

- Select the smallest viable stack; commit lockfiles and support lightweight local development.
- Validate typed inputs and model outputs. Separate policy decisions from model suggestions.
- Use least privilege, bounded retries, timeouts, idempotency, redacted logs and explicit approval for sensitive actions.
- Test denied actions, failures and recovery, not just happy paths.
- Use deterministic mocks and golden datasets; record evaluation methods, limitations and actual results.
- Document architecture, ADRs, threat model, runbooks and rollback.
- FDE case studies: synthetic customer discovery, integration, acceptance criteria, deployment, monitoring and feedback. Never imply real customers or invented results.
