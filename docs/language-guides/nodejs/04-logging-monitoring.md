---
hide:
  - toc
---

# Logging and Monitoring for Node.js Environments

## Prerequisites

- A running Elastic Beanstalk Node.js environment.
- IAM permissions for CloudWatch Logs and CloudWatch metrics.
- Application writing operational logs to standard output.
- Access to Elastic Beanstalk console and EB CLI.

## What You'll Build

You will validate Node.js application logs on instance paths, enable CloudWatch Logs streaming, inspect environment metrics, and understand where AWS X-Ray SDK instrumentation fits for trace collection.

```mermaid
flowchart LR
    A[Node.js app stdout and stderr] --> B[/var/log/web.stdout.log]
    B --> C[Elastic Beanstalk log retrieval]
    B --> D[CloudWatch Logs streaming]
    E[Environment metrics] --> F[CloudWatch alarms and dashboards]
    G[X-Ray SDK for Node.js] --> H[Trace data analysis]
```

## Steps

1. Ensure your application logs meaningful operational events.

    ```javascript
    app.get("/healthz", (req, res) => {
        console.log("health check request");
        res.status(200).send("ok");
    });
    ```

2. Retrieve logs from the environment.

    ```bash
    eb logs
    ```

3. Review primary web process output location on instances.

    ```text
    /var/log/web.stdout.log
    ```

4. Enable CloudWatch Logs streaming for persistent central log access.

    - Turn on log streaming in Elastic Beanstalk configuration.
    - Select retention policy according to your operational requirements.
    - Confirm log groups are created for the target environment.

5. Review environment metrics and health indicators.

    ```bash
    eb health --refresh
    ```

6. Add AWS X-Ray SDK instrumentation to application code where distributed tracing is required.

7. Configure log retention and lifecycle deliberately.

    - Keep short retention in development environments.
    - Use longer retention for production incident analysis windows.
    - Align retention with security and compliance policies.

8. Define basic CloudWatch alarms from key environment metrics.

    - Elevated latency over baseline.
    - Increased `5xx` error rates.
    - Persistent health degradation states.

## Verification

- `eb logs` returns recent logs from web instances.
- `web.stdout.log` contains application messages from requests.
- CloudWatch Logs groups include current environment log streams.
- CloudWatch metrics reflect request volume, latency, and health behavior.
- Optional X-Ray traces are visible when instrumentation is enabled.
- Alarm thresholds are documented and tied to on-call response expectations.

## See Also

- [Configuration Guide](./03-configuration.md)
- [CI/CD Guide](./06-ci-cd.md)
- [Operations Overview](../../operations/index.md)

## Sources

- [Streaming Elastic Beanstalk logs to CloudWatch Logs](https://docs.aws.amazon.com/elasticbeanstalk/latest/dg/AWSHowTo.cloudwatchlogs.html)
