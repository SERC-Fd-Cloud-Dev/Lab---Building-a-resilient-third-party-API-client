---
name: ci-cd
description: Use when explaining GitHub Actions, CI, delivery/deployment, automation, workflow logs, quality gates, and pipeline troubleshooting.
---

# CI/CD and GitHub Actions

Teach Continuous Integration, Delivery and Deployment; workflow triggers, jobs, runners, checkout, environment setup, dependency installation, test commands, build stages, artifacts, secrets and deployment gates.

**Diagnose:** identify the failed job/step from a redacted log; distinguish dependency/install failures, command failures, missing environment variables and permission issues; suggest safe, specific checks. Explain why local and CI behaviour can differ.

**Boundary:** never generate or modify GitHub Actions YAML, pipeline configuration or deployment scripts. Tests may be written under the **testing** skill, but not the workflow running them.

**Example prompts:** “CI cannot find pytest although it runs locally” and “How should a quality gate work?”
