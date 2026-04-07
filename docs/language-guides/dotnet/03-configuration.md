# Configure ASP.NET Core for Elastic Beanstalk

This tutorial explains configuration precedence for ASP.NET Core on Elastic Beanstalk.
It combines `appsettings.json`, Elastic Beanstalk environment properties, and `.ebextensions` option settings.

## Prerequisites

- Running .NET Elastic Beanstalk environment.
- Source control for `appsettings.json` and `.ebextensions/`.
- Familiarity with the ASP.NET Core configuration provider order.

## What You'll Build

You will configure:

- Safe application defaults in `appsettings.json`.
- Environment-specific values through Elastic Beanstalk environment properties.
- Platform settings in `.ebextensions`.
- A health check path aligned with `/health`.

## Steps

1. Keep non-secret defaults in `appsettings.json`.

```json
{
  "Application": {
    "Name": "GuideApi",
    "Region": "ap-northeast-2"
  },
  "Logging": {
    "LogLevel": {
      "Default": "Information",
      "Microsoft.AspNetCore": "Warning"
    }
  }
}
```

2. Set runtime overrides with Elastic Beanstalk environment properties.

```bash
eb setenv ENV_NAME="production" APP_VERSION="2026-04-07" LOG_LEVEL="Information" ASPNETCORE_ENVIRONMENT="Production"
```

3. Add `.ebextensions/01-dotnet.config`.

```yaml
option_settings:
    aws:elasticbeanstalk:application:environment:
        ASPNETCORE_ENVIRONMENT: Production
        DOTNET_PRINT_TELEMETRY_MESSAGE: false
    aws:elasticbeanstalk:environment:process:default:
        HealthCheckPath: /health
    aws:elasticbeanstalk:cloudwatch:logs:
        StreamLogs: true
        DeleteOnTerminate: false
        RetentionInDays: 14
```

4. Read configuration in ASP.NET Core using built-in providers.

```csharp
app.MapGet("/", (IConfiguration configuration) => Results.Ok(new
{
    application = configuration["Application:Name"],
    region = configuration["Application:Region"],
    environmentName = configuration["ENV_NAME"]
}));
```

5. Inspect effective configuration from Elastic Beanstalk.

```bash
eb printenv
aws elasticbeanstalk describe-configuration-settings --application-name "$APP_NAME" --environment-name "$ENV_NAME" --region "$REGION"
```

```mermaid
flowchart TD
    A[appsettings.json] --> D[ASP.NET Core Configuration]
    B[Elastic Beanstalk Environment Properties] --> D
    C[.ebextensions option_settings] --> B
    D --> E[Controllers and Minimal API]
    E --> F[/info and /demo/env]
```

## Verification

Run these checks after each configuration change:

```bash
eb printenv
eb deploy "$ENV_NAME" --staged
curl --silent "http://$CNAME/info"
```

Expected outcomes:

- Environment properties appear in `eb printenv`.
- `/health` remains the effective Elastic Beanstalk health path.
- ASP.NET Core sees updated values without hard-coded secrets.
- CloudWatch log streaming settings are visible in the environment configuration.

## See Also

- [First Deploy](./02-first-deploy.md)
- [Logging and Monitoring](./04-logging-monitoring.md)
- [Secrets Manager Recipe](./recipes/secrets-manager.md)

## Sources

- [Configuring environments with configuration files](https://docs.aws.amazon.com/elasticbeanstalk/latest/dg/ebextensions.html)
- [Environment properties and other software settings](https://docs.aws.amazon.com/elasticbeanstalk/latest/dg/environments-cfg-softwaresettings.html)
