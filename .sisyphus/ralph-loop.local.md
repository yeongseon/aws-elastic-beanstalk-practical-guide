---
active: true
iteration: 25
completion_promise: "DONE"
initial_completion_promise: "DONE"
started_at: "2026-04-07T10:35:00.069Z"
session_id: "ses_298d41871ffe6fB6hBB02oTZqO"
ultrawork: true
strategy: "continue"
message_count_at_start: 22
---
Upgrade the AWS Elastic Beanstalk Practical Guide to match the Azure App Service Practical Guide quality (100/100). Then create a new AWS Lambda Practical Guide as a separate repository with the same quality level.

## Phase 1: EB Guide Upgrade (Priority)

### Gap Analysis (from 3 explore agents):

**Troubleshooting gaps:**
- Missing: Evidence Map, Quick Diagnosis Cards, CloudWatch Insights Query Library (Azure's KQL equivalent)
- Missing: Lab Guides with reproducible infrastructure (Azure has 10 labs with Bicep/trigger/verify scripts)
- Playbooks need upgrade: Azure has 16 playbooks with real evidence, KQL queries, sample log patterns, CLI investigation commands, Normal vs Abnormal comparison tables
- EB currently has 10 playbooks without the same evidence depth
- Missing: KQL-equivalent section (CloudWatch Logs Insights queries categorized by HTTP, Console, Restarts, Correlation)

**Language Guides gaps:**
- EB has 2 languages (Python, Node.js) → needs 4 (add Java Spring Boot, .NET ASP.NET Core)
- Each language needs: 7 tutorials (01-local-run through 07-custom-domain-ssl) + runtime reference + recipes
- Azure Python has 10 recipes, Node.js has 12, Java has 10, .NET has 8
- EB Python has 6 recipes, Node.js has 6 → need AWS-equivalent recipes:
  - RDS integration (existing) → keep
  - ElastiCache Redis (existing) → keep  
  - S3 storage (existing) → keep
  - Add: Secrets Manager, IAM roles/instance profiles, DynamoDB, SQS worker, VPC endpoints, Docker multi-stage
- Need reference apps under apps/java-springboot/ and apps/dotnet-aspnetcore/

**Platform gaps:**
- Azure has deeper architecture docs (three-plane model, zero-trust security)
- EB needs deeper: security architecture, VPC/networking patterns
- Missing: deployment diagnostics reference (Azure has Kudu API docs)

**Operations gaps:**
- Azure has Deployment Slots → EB needs blue/green deployment patterns doc
- Missing: explicit immutable deployment runbook

**Reference gaps:**
- Missing: CloudWatch Logs Insights query reference (equivalent to Azure's KQL queries)
- Missing: EB platform diagnostics reference (equivalent to Azure's Kudu queries)

### Current EB file count: ~80 docs files
### Target: ~166+ docs files (matching Azure)

### Conventions from AGENTS.md:
- CLI: always long flags
- Variables: $APP_NAME, $ENV_NAME, $REGION, $ACCOUNT_ID, $VPC_ID, $SUBNET_ID
- PII removal in all CLI output
- 4-space indent for admonitions and nested lists
- Every page: Mermaid diagram + See Also + Sources (AWS official docs only)
- File naming: XX-topic-name.md for tutorials, topic-name.md for others

## Phase 2: AWS Lambda Guide (after EB is 100/100)
- Separate repository: aws-lambda-practical-guide
- Same structure as Azure/EB guides
- Same 4 languages
- Lambda-specific: event sources, layers, cold starts, SAM/CDK, API Gateway integration, Step Functions

## Quality target: Oracle scores 100/100 on every section before moving on.
## Approach: Ultrawork loop - implement section by section, verify with Oracle, fix until 100/100, repeat.
