# Use Amazon ElastiCache for Redis with ASP.NET Core

This recipe adds Redis-backed caching to an ASP.NET Core application on Elastic Beanstalk.
It uses `StackExchange.Redis` and the environment property pattern for endpoint discovery.

## Prerequisites

- Running .NET Elastic Beanstalk environment in a VPC.
- Existing ElastiCache for Redis cluster or replication group.
- Network access from application instances to the Redis endpoint.

## What You'll Build

You will build:

- Environment properties for the Redis endpoint.
- ASP.NET Core registration for Redis connectivity.
- A lightweight cache test endpoint.

## Steps

1. Set the Redis endpoint in environment properties.

```bash
eb setenv REDIS_ENDPOINT="guide-cache.xxxxxx.0001.apn2.cache.amazonaws.com:6379"
```

2. Add the client package.

```bash
dotnet add GuideApi.csproj package StackExchange.Redis
```

3. Register a singleton multiplexer.

```csharp
builder.Services.AddSingleton<IConnectionMultiplexer>(_ =>
    ConnectionMultiplexer.Connect(builder.Configuration["REDIS_ENDPOINT"]!));
```

4. Add a test endpoint.

```csharp
app.MapGet("/cache-check", async (IConnectionMultiplexer redis) =>
{
    var database = redis.GetDatabase();
    await database.StringSetAsync("guide:health", "ok");
    var value = await database.StringGetAsync("guide:health");
    return Results.Ok(new { redis = value.ToString() });
});
```

5. Deploy and test.

```bash
eb deploy "$ENV_NAME" --staged
curl --silent "http://$CNAME/cache-check"
```

```mermaid
flowchart LR
    A[Elastic Beanstalk App] --> B[Security Group Rule]
    B --> C[Redis Endpoint]
    D[REDIS_ENDPOINT Property] --> A
```

## Verification

Run these checks after deployment:

```bash
eb printenv
eb logs --all
curl --silent "http://$CNAME/cache-check"
```

Expected outcomes:

- The application resolves the Redis endpoint.
- Cache read and write operations succeed.
- Logs show no connection timeout or network errors.

## See Also

- [Configuration](../03-configuration.md)
- [IAM Instance Profile Recipe](./iam-instance-profile.md)
- [Secrets Manager Recipe](./secrets-manager.md)

## Sources

- [Using Elastic Beanstalk with Amazon ElastiCache](https://docs.aws.amazon.com/elasticbeanstalk/latest/dg/AWSHowTo.ElastiCache.html)
