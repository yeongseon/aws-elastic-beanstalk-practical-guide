# Logging and Monitoring for Spring Boot on Elastic Beanstalk

This tutorial explains how to combine Spring Boot logging, Elastic Beanstalk log collection, CloudWatch Logs streaming, and health visibility.
The goal is to keep request diagnostics centralized while preserving application-level structure through Logback.

## Prerequisites

- Running Java Elastic Beanstalk environment.
- Familiarity with `eb logs`, environment health, and Spring Boot basics.
- IAM permissions for CloudWatch Logs and CloudWatch metrics.

## What You'll Build

You will build:

- Console logging formatted for CloudWatch ingestion.
- Elastic Beanstalk log streaming to CloudWatch Logs.
- Health visibility through `/health` and environment monitoring.

```mermaid
flowchart LR
    A[Spring Boot Logback] --> B[stdout and stderr]
    B --> C[Elastic Beanstalk Log Files]
    C --> D[CloudWatch Logs]
    E[/health Endpoint] --> F[Enhanced Health]
    F --> G[Elastic Beanstalk Console]
```

## Steps

1. Start with Spring Boot console logging so Elastic Beanstalk can collect it.

```properties
logging.level.root=INFO
logging.pattern.console=%d{yyyy-MM-dd'T'HH:mm:ss.SSSXXX} %-5level [%thread] %logger{36} - %msg%n
management.endpoints.web.exposure.include=health,info
```

2. Add a basic `logback-spring.xml` for structured fields.

```xml
<configuration>
    <appender name="CONSOLE" class="ch.qos.logback.core.ConsoleAppender">
        <encoder>
            <pattern>{"timestamp":"%date{ISO8601}","level":"%level","logger":"%logger{36}","message":"%msg"}%n</pattern>
        </encoder>
    </appender>
    <root level="INFO">
        <appender-ref ref="CONSOLE" />
    </root>
</configuration>
```

3. Enable log streaming to CloudWatch Logs.

```yaml
option_settings:
    aws:elasticbeanstalk:cloudwatch:logs:
        StreamLogs: true
        DeleteOnTerminate: false
        RetentionInDays: 14
```

4. Keep the environment health check path on `/health`.

```yaml
option_settings:
    aws:elasticbeanstalk:environment:process:default:
        HealthCheckPath: /health
```

5. Review logs from the CLI.

```bash
eb logs --all
aws logs describe-log-groups --log-group-name-prefix "/aws/elasticbeanstalk" --region "$REGION"
```

6. Inspect health and events.

```bash
eb health
eb events
```

## Verification

Use these checks after enabling monitoring:

```bash
eb logs --all
aws logs tail "/aws/elasticbeanstalk/$ENV_NAME/var/log/web.stdout.log" --follow --region "$REGION"
curl --verbose "http://$CNAME/health"
```

Expected outcomes:

- Spring Boot logs appear in Elastic Beanstalk and CloudWatch Logs.
- The environment health check remains green.
- Structured console output is readable in CloudWatch Logs.
- Environment events help correlate deployments and incidents.

## See Also

- [Configuration](./03-configuration.md)
- [CI/CD](./06-ci-cd.md)
- [Operations Overview](../../operations/index.md)

## Sources

- [Viewing logs from Elastic Beanstalk environments](https://docs.aws.amazon.com/elasticbeanstalk/latest/dg/using-features.logging.html)
- [Streaming Elastic Beanstalk environment logs to CloudWatch Logs](https://docs.aws.amazon.com/elasticbeanstalk/latest/dg/AWSHowTo.cloudwatchlogs.html)
- [Enhanced health reporting](https://docs.aws.amazon.com/elasticbeanstalk/latest/dg/health-enhanced.html)
