# AGENTS.md

Guidance for AI agents working in this repository.

## Project Overview

**AWS Elastic Beanstalk Practical Guide** — a unified documentation hub and reference applications for deploying and operating web apps on AWS Elastic Beanstalk.

- **Live site**: <https://yeongseon.github.io/aws-elastic-beanstalk-practical-guide/>
- **Repository**: <https://github.com/yeongseon/aws-elastic-beanstalk-practical-guide>

## Repository Structure

```text
.
├── .github/
│   └── workflows/              # GitHub Pages deployment
├── apps/
│   ├── python-flask/           # Python reference application
│   ├── nodejs/                 # Node.js reference application
│   ├── java-springboot/        # Java Spring Boot reference application
│   └── dotnet-aspnetcore/      # .NET ASP.NET Core reference application
├── docs/
│   ├── assets/                 # Images, icons
│   ├── best-practices/         # Production patterns and anti-patterns (8 pages)
│   ├── javascripts/            # Mermaid zoom JS
│   ├── language-guides/
│   │   ├── python/             # Python (Flask) — 7 tutorials + 14 recipes
│   │   ├── nodejs/             # Node.js (Express) — 7 tutorials + 14 recipes
│   │   ├── java/               # Java (Spring Boot) — 7 tutorials + 10 recipes
│   │   └── dotnet/             # .NET (ASP.NET Core) — 7 tutorials + 10 recipes
│   ├── operations/             # Day-2 operational execution (10 pages)
│   ├── platform/               # Architecture and design decisions (9 pages)
│   ├── reference/              # CLI cheatsheet, platform limits, diagnostics (7 pages)
│   ├── start-here/             # Overview, learning paths, repository map (3 pages)
│   ├── stylesheets/            # Custom CSS
│   └── troubleshooting/        # Troubleshooting hub (55+ pages)
│       ├── architecture-overview.md
│       ├── decision-tree.md
│       ├── mental-model.md
│       ├── evidence-map.md     # Evidence collection reference
│       ├── quick-diagnosis-cards.md  # Quick diagnosis by symptom
│       ├── cloudwatch/         # CloudWatch Logs Insights query library (14 pages)
│       │   ├── http/           # HTTP queries (5xx trends, latency, slowest)
│       │   ├── application/    # App queries (startup errors, exceptions)
│       │   ├── platform/       # Platform queries (deploy events, health)
│       │   └── correlation/    # Correlation queries (deploy-vs-errors)
│       ├── first-10-minutes/   # Checklists by symptom category (4 pages)
│       ├── lab-guides/         # Hands-on troubleshooting labs (11 pages)
│       ├── methodology/        # Troubleshooting method, log sources (2 pages)
│       └── playbooks/          # 16 playbooks by category
│           ├── deployment-availability/  # 6 playbooks
│           ├── performance/              # 5 playbooks
│           └── networking/               # 5 playbooks
└── mkdocs.yml                  # MkDocs Material configuration (7-tab nav)
```

## Content Categories

| Section | Purpose | Page Count |
|---|---|---|
| **Start Here** | Entry points, learning paths, repository map | 3 |
| **Platform** | Architecture, design decisions — WHAT and HOW it works | 9 |
| **Best Practices** | Production patterns — HOW to use the platform well | 8 |
| **Language Guides** | Per-language step-by-step tutorials and recipes | 79 |
| **Operations** | Day-2 execution — HOW to run in production | 10 |
| **Troubleshooting** | Diagnosis and resolution — hypothesis-driven | 55+ |
| **Reference** | Quick lookup — CLI, limits, environment properties | 7 |

## Documentation Conventions

### File Naming

- Tutorial: `XX-topic-name.md` (numbered for sequence)
- All others: `topic-name.md` (kebab-case)

### CLI Command Style

```bash
# ALWAYS use long flags for readability
aws elasticbeanstalk create-environment --application-name $APP_NAME --environment-name $ENV_NAME

# NEVER use short flags in documentation
aws elasticbeanstalk create-environment -a $APP_NAME  # Don't do this
```

### Variable Naming Convention

| Variable | Description | Example |
|----------|-------------|---------|
| `$APP_NAME` | Application name | `my-flask-app` |
| `$ENV_NAME` | Environment name | `my-flask-app-prod` |
| `$REGION` | AWS region | `ap-northeast-2` |
| `$ACCOUNT_ID` | AWS account ID placeholder | `<account-id>` |
| `$VPC_ID` | VPC identifier | `vpc-xxxxxxxx` |
| `$SUBNET_ID` | Subnet identifier | `subnet-xxxxxxxx` |

### PII Removal (Quality Gate)

**CRITICAL**: All CLI output examples MUST have PII removed.

Patterns to mask:

- AWS Account IDs: `<account-id>`
- ARNs: mask account portion
- Access Keys: NEVER include
- IP addresses: `x.x.x.x` or `10.0.x.x` for private
- Instance IDs: `i-xxxxxxxxxxxxxxxxx`

### Admonition Indentation Rule

For MkDocs admonitions, every line in the body must be indented by **4 spaces**.

### Mermaid Diagrams

All architectural diagrams use Mermaid. Every documentation page should include at least one diagram.

### Nested List Indentation

All nested list items MUST use **4-space indent** (Python-Markdown standard).

### Tail Section Naming

Every document ends with these tail sections (in this order):

| Section | Purpose | Content |
|---|---|---|
| `## See Also` | Internal cross-links within this repository | Links to other pages in this guide |
| `## Sources` | External authoritative references | Links to AWS official documentation (primary) |

- `## See Also` is required on every page.
- `## Sources` is required when external references are cited. Omit if none exist.
- Order is always `## See Also` → `## Sources` (never reversed).
- All content must be based on AWS official documentation with cited sources.

### Source Policy

- **Primary source**: AWS official documentation (docs.aws.amazon.com)
- **No third-party sources**: Blog posts, tutorials, Stack Overflow answers are NOT allowed
- Every factual claim should be traceable to an AWS documentation page

## Build & Preview

```bash
# Install MkDocs dependencies
pip install mkdocs-material mkdocs-minify-plugin

# Build documentation (strict mode catches broken links)
mkdocs build --strict

# Local preview
mkdocs serve
```

## Git Commit Style

```text
type: short description
```

Allowed types: `feat`, `fix`, `docs`, `chore`, `refactor`

## Tutorial Validation Tracking

Every tutorial document supports **validation frontmatter** that records when and how it was last tested against a real deployment.

### Frontmatter Schema

Add a `validation` block inside the YAML frontmatter (`---` fences) of any tutorial file:

```yaml
---
hide:
  - toc
validation:
  aws_cli:
    last_tested: 2026-04-09
    cli_version: "2.83.0"
    result: pass
  cloudformation:
    last_tested: null
    result: not_tested
---
```

### Agent Rules for Validation

1. **After deploying a tutorial end-to-end**, add or update the `validation` frontmatter with the current date, CLI version, and `result: pass`.
2. **If a tutorial step fails during validation**, set `result: fail` and note the issue.
3. **Never fabricate validation dates.**
4. **After updating frontmatter**, regenerate the dashboard:
    ```bash
    python3 scripts/generate_validation_status.py
    ```
5. **Include the regenerated dashboard** (`docs/reference/validation-status.md`) in the same commit.
6. **Do not manually edit** `docs/reference/validation-status.md` — it is auto-generated.
