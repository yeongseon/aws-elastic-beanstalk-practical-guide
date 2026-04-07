# Python Recipes on Elastic Beanstalk

This recipe collection extends the core Python tutorial track with integration and platform customization patterns documented by AWS.
Each recipe is designed for incremental adoption without assuming a production deployment.

## Prerequisites

- Completed core Python guide through deployment and configuration basics.
- Familiarity with environment properties and `.ebextensions` files.
- IAM permissions for related AWS services used in each recipe.

## What You'll Build

You will build optional capabilities around a Python Flask application:

- RDS connectivity with decoupled database lifecycle.
- Secrets retrieval with AWS Secrets Manager.
- Centralized configuration lookup with Parameter Store.
- Instance profile-based AWS API access without static credentials.
- DynamoDB-backed key-value data access.
- ElastiCache Redis-backed caching in VPC contexts.
- S3 object storage integration using instance profile permissions.
- VPC endpoint connectivity for private service access.
- Platform hook customizations and NGINX extension points.
- Worker environment patterns using SQS and scheduled tasks.
- Docker-based deployment alternative to native Python platform.
- Custom CloudWatch metrics for app-level telemetry.

## Steps

Choose recipes in this order if you want low-to-high operational complexity:

| Order | Recipe | Primary Service | Outcome |
|---|---|---|---|
| 1 | [rds-integration.md](./rds-integration.md) | Amazon RDS | Externalized relational data |
| 2 | [secrets-manager.md](./secrets-manager.md) | AWS Secrets Manager | Runtime secret retrieval |
| 3 | [parameter-store.md](./parameter-store.md) | AWS Systems Manager | Centralized configuration lookup |
| 4 | [iam-instance-profile.md](./iam-instance-profile.md) | IAM | Instance role-based AWS access |
| 5 | [dynamodb.md](./dynamodb.md) | Amazon DynamoDB | Managed key-value storage |
| 6 | [s3-storage.md](./s3-storage.md) | Amazon S3 | Durable object storage |
| 7 | [elasticache-redis.md](./elasticache-redis.md) | Amazon ElastiCache | Low-latency cache layer |
| 8 | [vpc-endpoints.md](./vpc-endpoints.md) | Amazon VPC | Private AWS service connectivity |
| 9 | [custom-platform-hooks.md](./custom-platform-hooks.md) | Platform hooks | Deployment lifecycle extensions |
| 10 | [sqs-worker.md](./sqs-worker.md) | Amazon SQS | Queue-driven worker tier |
| 11 | [worker-environments.md](./worker-environments.md) | Amazon SQS | Async and scheduled processing |
| 12 | [docker-multi-stage.md](./docker-multi-stage.md) | Docker | Smaller runtime images |
| 13 | [docker-deploy.md](./docker-deploy.md) | Docker on EB | Containerized deployment path |
| 14 | [cloudwatch-custom-metrics.md](./cloudwatch-custom-metrics.md) | Amazon CloudWatch | Application-specific telemetry |

```mermaid
flowchart TD
    A[Core Python Web Environment] --> B[RDS Integration]
    A --> C[Secrets Manager]
    A --> D[Parameter Store]
    A --> E[IAM Instance Profile]
    A --> F[DynamoDB]
    A --> G[S3 Storage]
    A --> H[ElastiCache Redis]
    A --> I[VPC Endpoints]
    A --> J[Custom Platform Hooks]
    A --> K[SQS Worker Patterns]
    A --> L[Docker Options]
    A --> M[CloudWatch Custom Metrics]
```

## Verification

Before starting any recipe, run baseline checks:

```bash
eb status "$ENV_NAME"
eb printenv
eb logs --all
```

Recipe completion checks should include:

- Service-specific connectivity validation.
- Environment events and health review.
- Configuration committed to source control.
- No unmasked account IDs or sensitive tokens in docs output.

Suggested verification order for each recipe:

1. Confirm environment state with `eb status` and `eb health`.
2. Confirm configuration values with `eb printenv`.
3. Confirm logs with `eb logs --all`.
4. Confirm AWS service API visibility with targeted `aws` CLI commands.

Operational note from Elastic Beanstalk docs context:

- Prefer decoupled managed services (RDS, ElastiCache, S3) for durability and replacement-safe operations.
- Keep application versions immutable and traceable when testing recipe changes.
- Use masked placeholders in shared command outputs (`<account-id>`, `<db-password>`).

## See Also

- [Python Guide Index](../index.md)
- [Python Runtime](../python-runtime.md)
- [Operations Section](../../../operations/index.md)

## Sources

- [Elastic Beanstalk Developer Guide](https://docs.aws.amazon.com/elasticbeanstalk/latest/dg/Welcome.html)
