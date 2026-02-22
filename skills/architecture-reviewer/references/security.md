# Security

**Dimension Weight: 18%**

Evaluates the system's security posture across all layers — authentication, authorization,
data protection, network security, and vulnerability management.

## Table of Contents

1. Sub-Criteria Checklist
2. OWASP Top 10 Architectural Checklist
3. Threat Modeling Guidance
4. Common Security Anti-Patterns
5. Evaluation Guidance by Mode

---

## 1. Sub-Criteria Checklist

### 1.1 Authentication

- What mechanism is used? (OAuth2/OIDC, SAML, mTLS, API keys, session-based, JWT.)
- Is MFA supported and enforced for privileged access?
- Is there a centralized identity provider, or is auth implemented per-service?
- For API authentication: are tokens short-lived? Is refresh token rotation in place?
- Is passwordless authentication supported? (WebAuthn, magic links.)
- **Service-to-service auth:** Is there mutual authentication between services? (mTLS,
  service accounts, JWT with service identity.)

### 1.2 Authorization

- Is authorization enforced at every layer? (API gateway AND service layer, not just one.)
- What model is used? RBAC (Role-Based), ABAC (Attribute-Based), ReBAC (Relationship-Based)?
- Is the principle of least privilege applied?
- Are authorization policies centralized (OPA, Cedar, Casbin) or scattered in code?
- Is there fine-grained resource-level authorization? (Not just "can access the API" but
  "can access THIS specific resource.")
- **Broken access control test:** Can a user access another user's resources by changing IDs
  in the request?

### 1.3 Encryption in Transit

- Is TLS enforced for all external communication? (HTTPS, no mixed content.)
- What TLS version? (1.2 minimum, 1.3 preferred. TLS 1.0/1.1 is a finding.)
- Is HTTP Strict Transport Security (HSTS) enabled?
- For service-to-service: is mTLS or TLS used for internal communication?
- Is certificate management automated? (Let's Encrypt, AWS ACM, cert-manager.)
- Are weak cipher suites disabled?

### 1.4 Encryption at Rest

- Is database encryption enabled? (Transparent Data Encryption, volume encryption.)
- Is object/file storage encryption enabled?
- Is encryption managed via KMS with proper key rotation?
- Are encryption keys stored separately from encrypted data?
- Is application-level encryption used for sensitive fields? (Beyond volume-level encryption.)
- Are backups encrypted?

### 1.5 Secret Management

- How are secrets stored? (Vault, AWS Secrets Manager, Azure Key Vault, GCP Secret Manager.)
- Are secrets NEVER in source code, environment files committed to git, or container images?
- Is there a secret rotation policy? Are rotations automated?
- Are secrets scoped to the services that need them? (Principle of least privilege for secrets.)
- Are secret access events audited?
- **Critical check:** Search for hardcoded secrets, API keys, passwords, tokens in code.

### 1.6 Input Validation

- Is all user input validated server-side? (Never trust client-side validation alone.)
- Are inputs validated for type, length, range, and format?
- Are parameterized queries / prepared statements used for ALL database interactions?
  (No string concatenation of SQL.)
- Is content-type enforcement in place? (Reject unexpected content types.)
- Are file uploads validated? (Type, size, content scanning.)
- Is output encoding applied to prevent XSS? (HTML encoding, JSON encoding.)

### 1.7 OWASP Top 10 Exposure

See Section 2 for detailed checklist.

### 1.8 Rate Limiting & DDoS Protection

- Is per-user and per-IP rate limiting implemented?
- Is rate limiting applied at the edge before requests reach backend services?
- Is there a WAF (Web Application Firewall) in place?
- Is DDoS mitigation configured? (CloudFlare, AWS Shield, Akamai.)
- Are rate limit responses informative? (429 with Retry-After header.)
- Is there protection against brute-force attacks? (Login throttling, account lockout.)

### 1.9 Network Security

- Is network segmentation in place? (Public subnet for LB, private subnet for services,
  isolated subnet for databases.)
- Are security groups / firewall rules following least-privilege? (Not 0.0.0.0/0 for ingress.)
- Is there a zero-trust network model? (Verify every request, not just perimeter.)
- Is egress traffic restricted and monitored?
- Are bastion hosts / VPNs used for administrative access?

### 1.10 CORS & CSP

- Is CORS configured with specific origins? (Not `*` for authenticated endpoints.)
- Is Content Security Policy (CSP) header set? (Prevents XSS, data injection.)
- Is X-Frame-Options set? (Prevents clickjacking.)
- Is X-Content-Type-Options set to nosniff?
- Are Referrer-Policy and Permissions-Policy headers configured?

### 1.11 Dependency Security

- Are dependencies scanned for known CVEs? (Dependabot, Snyk, Trivy, OWASP Dependency Check.)
- Is scanning automated in CI/CD?
- Is there a policy for addressing critical CVEs? (Time SLA for remediation.)
- Are lock files used and committed? (Prevents supply chain attacks via version drift.)
- Is there an SBOM (Software Bill of Materials) capability?

### 1.12 Supply Chain Security

- Are commits signed? (GPG-signed commits.)
- Are container base images from trusted registries? Pinned to specific digests?
- Are container images scanned for vulnerabilities?
- Is there image provenance tracking? (SLSA framework, Sigstore.)
- Are CI/CD pipelines protected from injection? (No untrusted code execution in pipelines.)

### 1.13 API Security

- Are JWT tokens validated correctly? (Signature, expiration, issuer, audience.)
- Is token rotation and revocation supported?
- Are API scopes / permissions enforced per endpoint?
- Are API keys treated as secrets? (Not exposed in URLs, logs, or client-side code.)
- Is there API abuse detection? (Anomalous usage patterns.)

### 1.14 Data Privacy

- Is PII identified and classified across all data stores?
- Is data anonymization or pseudonymization applied where possible?
- Is the right to erasure (GDPR Art. 17) architecturally supported?
  (Cascade deletion across all stores, backups, caches.)
- Is data masking used for non-production environments?
- Is there data access logging for sensitive data?

### 1.15 Logging Security

- Are secrets, tokens, and passwords excluded from logs?
- Is PII handled appropriately in logs? (Masked, hashed, or excluded.)
- Are logs stored securely? (Encrypted, access-controlled.)
- Is there log injection prevention? (User input not directly interpolated into log messages.)
- Are log retention policies defined and enforced?

---

## 2. OWASP Top 10 Architectural Checklist

For each OWASP Top 10 category, evaluate architectural defenses:

| #   | Vulnerability                 | Architectural Defense                                          | What to Check                                                     |
| --- | ----------------------------- | -------------------------------------------------------------- | ----------------------------------------------------------------- |
| A01 | Broken Access Control         | Centralized authz policy engine, resource-level checks         | Can users access others' data by manipulating IDs?                |
| A02 | Cryptographic Failures        | TLS everywhere, KMS for keys, no custom crypto                 | Is sensitive data encrypted in transit and at rest?               |
| A03 | Injection                     | Parameterized queries, input validation layer, ORM             | Any string concatenation in queries?                              |
| A04 | Insecure Design               | Threat modeling, abuse case analysis, security requirements    | Is security a design consideration, not an afterthought?          |
| A05 | Security Misconfiguration     | Hardened defaults, automated config scanning, no debug in prod | Default credentials? Unnecessary features enabled?                |
| A06 | Vulnerable Components         | Dependency scanning, SBOM, automated patching                  | Known CVEs in dependencies?                                       |
| A07 | Auth Failures                 | Centralized auth, MFA, session management                      | Weak passwords accepted? No brute-force protection?               |
| A08 | Data Integrity Failures       | Code signing, CI/CD integrity, update verification             | Can untrusted code enter the pipeline?                            |
| A09 | Logging & Monitoring Failures | Centralized logging, SIEM, alerting on security events         | Would a breach be detected? How quickly?                          |
| A10 | SSRF                          | Allowlist for outbound requests, network segmentation          | Can user input trigger server-side requests to internal services? |

---

## 3. Threat Modeling Guidance

When reviewing, implicitly apply the STRIDE model:

| Threat                     | Question                                       | Architectural Mitigation                         |
| -------------------------- | ---------------------------------------------- | ------------------------------------------------ |
| **S**poofing               | Can an attacker impersonate a user or service? | Strong authentication, mTLS                      |
| **T**ampering              | Can data be modified in transit or at rest?    | Integrity checks, signed payloads, TLS           |
| **R**epudiation            | Can an actor deny performing an action?        | Audit logging, signed events                     |
| **I**nformation Disclosure | Can sensitive data leak?                       | Encryption, access controls, data classification |
| **D**enial of Service      | Can the system be overwhelmed?                 | Rate limiting, auto-scaling, DDoS protection     |
| **E**levation of Privilege | Can a user gain unauthorized capabilities?     | Least privilege, authorization enforcement       |

For each component and data flow in the architecture, consider which STRIDE threats apply.

---

## 4. Common Security Anti-Patterns

| Anti-Pattern                 | Description                                                 | Severity |
| ---------------------------- | ----------------------------------------------------------- | -------- |
| Hardcoded Secrets            | API keys, passwords, tokens in source code                  | S1       |
| SQL String Concatenation     | Building queries by concatenating user input                | S1       |
| Trust-All CORS               | `Access-Control-Allow-Origin: *` on authenticated endpoints | S2       |
| JWT Without Validation       | Accepting JWTs without verifying signature/expiry           | S1       |
| No Rate Limiting             | Endpoints open to unlimited requests                        | S2       |
| Debug Mode in Production     | Verbose errors, stack traces, debug endpoints exposed       | S2       |
| Overly Broad IAM Roles       | `*:*` or `Admin` for application service accounts           | S2       |
| Sensitive Data in URLs       | PII, tokens, or secrets in query parameters                 | S2       |
| Shared Service Accounts      | Multiple services using the same credentials                | S3       |
| No Egress Controls           | Application can make outbound requests to any destination   | S3       |
| Client-Side Only Validation  | Server trusts client-validated input                        | S2       |
| Unencrypted Internal Traffic | Plain HTTP between services in the same VPC                 | S3       |

---

## 5. Evaluation Guidance by Mode

### Mode A (Codebase)

- Search for hardcoded secrets: `grep -r` for patterns like `password=`, `api_key=`,
  `secret=`, `token=`, base64-encoded strings, high-entropy strings
- Check .gitignore for .env exclusion
- Inspect auth middleware: What is validated? What is skipped?
- Check SQL/query construction for parameterization
- Inspect CORS configuration for overly permissive origins
- Check dependency manifests for known vulnerable versions
- Look for input validation middleware/decorators
- Inspect network configs (security groups, Kubernetes NetworkPolicies)
- Check for security headers in server configuration
- Review Dockerfile for base image provenance and running as non-root

### Mode B (Document)

- Check if authentication mechanism is specified with sufficient detail
- Look for authorization model description (not just "we'll add auth")
- Verify encryption strategy is stated for transit AND rest
- Check for secret management strategy
- Look for threat model or security analysis
- Check if network security architecture is defined
- Look for compliance-driven security requirements
- Identify "TBD" security items — these are high-severity findings

### Mode C (Hybrid)

- Compare stated security controls against actual implementation
- Check if documented auth model matches code implementation
- Verify stated encryption is actually configured
- Cross-reference threat model (if exists) against actual mitigations
- Check if documented network segmentation matches actual security groups/network policies
