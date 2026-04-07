# AWS Elastic Beanstalk Practical Guide

Comprehensive guide for running web applications on AWS Elastic Beanstalk — from first deployment to production troubleshooting.

## What's Inside

| Section | Description |
|---------|-------------|
| [Start Here](https://yeongseon.github.io/aws-elastic-beanstalk-practical-guide/) | Overview, learning paths, and repository map |
| [Platform](https://yeongseon.github.io/aws-elastic-beanstalk-practical-guide/platform/) | Architecture, environment tiers, networking, scaling |
| [Best Practices](https://yeongseon.github.io/aws-elastic-beanstalk-practical-guide/best-practices/) | Production baseline, security, networking, deployment, scaling, reliability |
| [Language Guides](https://yeongseon.github.io/aws-elastic-beanstalk-practical-guide/language-guides/) | Step-by-step tutorials for Python, Node.js, Java, and .NET |
| [Operations](https://yeongseon.github.io/aws-elastic-beanstalk-practical-guide/operations/) | Environment management, health monitoring, updates, cost optimization |
| [Troubleshooting](https://yeongseon.github.io/aws-elastic-beanstalk-practical-guide/troubleshooting/) | 10 playbooks, decision tree, methodology, log source map |
| [Reference](https://yeongseon.github.io/aws-elastic-beanstalk-practical-guide/reference/) | EB CLI cheatsheet, platform limits, environment properties |

## Language Guides

- **Python** (Flask + Gunicorn)
- **Node.js** (Express)
- **Java** (Spring Boot + Maven)
- **.NET** (ASP.NET Core + Kestrel)

Each guide covers: local development, first deploy, configuration, logging, infrastructure as code, CI/CD, and custom domains.

## Quick Start

```bash
# Clone the repository
git clone https://github.com/yeongseon/aws-elastic-beanstalk-practical-guide.git

# Install MkDocs dependencies
pip install mkdocs-material mkdocs-minify-plugin

# Start local documentation server
mkdocs serve
```

Visit `http://127.0.0.1:8000` to browse the documentation locally.

## Reference Applications

Minimal reference applications demonstrating Elastic Beanstalk patterns:

- `apps/python-flask/` — Flask + Gunicorn
- `apps/nodejs/` — Express
- `apps/java-springboot/` — Spring Boot + Maven
- `apps/dotnet-aspnetcore/` — ASP.NET Core

## Contributing

Contributions welcome. Please ensure:
- All CLI examples use long flags (`--environment-name`, not `-e`)
- All documents include Mermaid diagrams
- All content references AWS official documentation with source URLs
- No PII in CLI output examples

## Related Projects

| Repository | Description |
|---|---|
| [azure-app-service-practical-guide](https://github.com/yeongseon/azure-app-service-practical-guide) | Azure App Service practical guide |

## Disclaimer

This is an independent community project. Not affiliated with or endorsed by Amazon Web Services. AWS and Elastic Beanstalk are trademarks of Amazon.com, Inc.

## License

[MIT](LICENSE)
