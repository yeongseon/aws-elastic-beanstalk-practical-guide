---
hide:
  - toc
---

# Customize Platform Hooks and NGINX Extensions

This tutorial uses Elastic Beanstalk Linux platform extension points for Python environments.
It covers `.platform/hooks/`, `.platform/confighooks/`, and `.platform/nginx/` customization paths.

## Prerequisites

- Python environment on Amazon Linux platform branch.
- Shell scripting basics and executable permissions management.
- Access to deployment logs for hook troubleshooting.

## What You'll Build

You will build:

- Lifecycle hook scripts for prebuild, predeploy, and postdeploy.
- Configuration update hooks in `.platform/confighooks/`.
- Optional NGINX snippet extension in `.platform/nginx/`.

## Steps

1. Create hook directories.

```bash
mkdir -p .platform/hooks/prebuild
mkdir -p .platform/hooks/predeploy
mkdir -p .platform/hooks/postdeploy
mkdir -p .platform/confighooks/predeploy
mkdir -p .platform/nginx/conf.d
```

2. Add prebuild hook script.

```bash
#!/usr/bin/env bash
set -o errexit
set -o nounset
set -o pipefail
python3 --version > /var/app/staging/prebuild-python-version.txt
```

3. Add predeploy hook script.

```bash
#!/usr/bin/env bash
set -o errexit
set -o nounset
set -o pipefail
echo "predeploy start" > /var/log/predeploy-guide.log
```

4. Add postdeploy hook script.

```bash
#!/usr/bin/env bash
set -o errexit
set -o nounset
set -o pipefail
echo "postdeploy complete" > /var/log/postdeploy-guide.log
```

5. Add NGINX custom snippet if needed.

```nginx
client_max_body_size 10m;
```

6. Apply executable permissions and deploy.

```bash
chmod +x .platform/hooks/prebuild/*.sh
chmod +x .platform/hooks/predeploy/*.sh
chmod +x .platform/hooks/postdeploy/*.sh
eb deploy --staged
```

```mermaid
flowchart TD
    A[Application Version Bundle] --> B[prebuild hook]
    B --> C[predeploy hook]
    C --> D[Application and Proxy Start]
    D --> E[postdeploy hook]
    F[Config Update Event] --> G[confighooks execution]
    H[.platform/nginx snippets] --> D
```

## Verification

Inspect logs and generated files:

```bash
eb logs --all
eb events "$ENV_NAME"
```

Expected outcomes:

- Hook scripts execute in documented lifecycle order.
- Deployment logs include hook script output.
- NGINX customization is reflected after deployment.

## See Also

- [Configuration](../03-configuration.md)
- [Python Runtime](../python-runtime.md)
- [Logging and Monitoring](../04-logging-monitoring.md)

## Sources

- [Extending Linux platforms on Elastic Beanstalk](https://docs.aws.amazon.com/elasticbeanstalk/latest/dg/platforms-linux-extend.html)
