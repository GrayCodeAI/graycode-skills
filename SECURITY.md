# Security Policy — graycode-skills

## Reporting a Vulnerability

Please report security vulnerabilities to security@graycode.ai. We handle all reports in confidence.

## Security Update Process

1. Reports are acknowledged within 48 hours
2. We assess the vulnerability and determine the scope
3. We develop a fix and coordinate disclosure
4. A security advisory is published when the fix is released

## Supported Versions

| Version | Supported |
|---------|-----------|
| Current stable | Yes |
| Previous stable | Security patches only |
| Development | No |

## Security Considerations

- Dependencies are audited regularly using pip-audit for Python and govulncheck for Go
- All dependency updates follow the project's dependency management policy
- Backwards compatibility is maintained for security fixes where possible

## Security Tools

This project uses the following tools for security:
- pip-audit (Python dependency vulnerability scanning)
- govulncheck (Go dependency vulnerability scanning)
- ruff / gofumpt (static analysis and formatting)
- Trivy (container and filesystem vulnerability scanning)

## Responsible Disclosure

We follow responsible disclosure principles:
- Provide reasonable time for the project to address the vulnerability before public disclosure
- Do not exploit the vulnerability beyond what is necessary to demonstrate it
- Refrain from disclosing details that could enable widespread exploitation before a fix is available
