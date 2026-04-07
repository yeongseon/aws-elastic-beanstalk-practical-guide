# Repository Map

This page explains the repository structure and where to find each type of content.

## Directory Structure

```text
.
├── .github/
│   └── workflows/              # GitHub Pages deployment
├── apps/
│   ├── python-flask/           # Python reference application
│   │   ├── application.py      # Flask WSGI entry point
│   │   ├── requirements.txt    # Python dependencies
│   │   └── Procfile            # Gunicorn startup command
│   ├── nodejs/                 # Node.js reference application
│   │   ├── app.js              # Express entry point
│   │   ├── package.json        # Node.js dependencies
│   │   └── Procfile            # Node.js startup command
│   ├── java-springboot/        # Java reference application
│   │   ├── src/                # Spring Boot source
│   │   ├── pom.xml             # Maven dependencies
│   │   └── Procfile            # Java startup command
│   └── dotnet-aspnetcore/      # .NET reference application
│       ├── Program.cs          # ASP.NET Core entry point
│       ├── *.csproj            # .NET project file
│       └── Procfile            # .NET startup command
├── docs/
│   ├── start-here/             # Orientation and learning paths
│   ├── platform/               # Architecture and concepts
│   ├── best-practices/         # Production patterns
│   ├── language-guides/        # Per-language tutorials
│   │   ├── python/             # Python (Flask) guide + recipes
│   │   ├── nodejs/             # Node.js (Express) guide + recipes
│   │   ├── java/               # Java (Spring Boot) guide + recipes
│   │   └── dotnet/             # .NET (ASP.NET Core) guide + recipes
│   ├── operations/             # Day-2 operational guides
│   ├── troubleshooting/        # Diagnosis and resolution
│   │   ├── cloudwatch/         # CloudWatch Logs Insights queries
│   │   ├── first-10-minutes/   # Quick checklists
│   │   ├── lab-guides/         # Hands-on troubleshooting labs
│   │   ├── playbooks/          # Hypothesis-driven playbooks
│   │   └── methodology/        # Systematic approach
│   └── reference/              # Quick lookups
└── mkdocs.yml                  # MkDocs Material configuration
```

## Content by Section

| Section | Pages | Description |
|---|---|---|
| Start Here | 3 | Orientation, learning paths, repository map |
| Platform | 9 | Architecture, environment tiers, scaling, networking, security |
| Best Practices | 8 | Production baseline, deployment, scaling, reliability, anti-patterns |
| Language Guides | 79 | Python, Node.js, Java, and .NET tutorials with recipes |
| Operations | 10 | Scaling, environments, health, updates, cost |
| Troubleshooting | 55+ | Decision tree, playbooks, labs, CloudWatch queries, methodology |
| Reference | 7 | EB CLI, limits, environment properties, diagnostics |

```mermaid
graph TD
    Root[Repository] --> Apps[apps/]
    Root --> Docs[docs/]
    Root --> Config[mkdocs.yml]
    Apps --> PyApp[python-flask/]
    Apps --> NodeApp[nodejs/]
    Apps --> JavaApp[java-springboot/]
    Apps --> DotnetApp[dotnet-aspnetcore/]
    Docs --> SH[start-here/]
    Docs --> PL[platform/]
    Docs --> BP[best-practices/]
    Docs --> LG[language-guides/]
    Docs --> OP[operations/]
    Docs --> TS[troubleshooting/]
    Docs --> RF[reference/]
    LG --> Py[python/]
    LG --> Nj[nodejs/]
    LG --> Jv[java/]
    LG --> Dn[dotnet/]
    TS --> CW[cloudwatch/]
    TS --> F10[first-10-minutes/]
    TS --> LB[lab-guides/]
    TS --> PB[playbooks/]
    TS --> MT[methodology/]
```

## Reference Applications

The `apps/` directory contains minimal reference applications:

- **`apps/python-flask/`** — Flask application with Gunicorn. Demonstrates the `application.py` entry point convention, health check endpoint, and environment property reading.
- **`apps/nodejs/`** — Express application. Demonstrates the `PORT` environment variable convention, health check endpoint, and `package.json` engines field.
- **`apps/java-springboot/`** — Spring Boot application with Maven. Demonstrates the embedded Tomcat entry point, health actuator, and `Procfile` configuration.
- **`apps/dotnet-aspnetcore/`** — ASP.NET Core application with Kestrel. Demonstrates the `Program.cs` entry point, health check middleware, and `.csproj` configuration.

These applications are designed for local development and testing. They mirror the patterns expected by Elastic Beanstalk platforms.

## See Also

- [Overview](./overview.md)
- [Learning Paths](./learning-paths.md)

## Sources

- [AWS Elastic Beanstalk Developer Guide](https://docs.aws.amazon.com/elasticbeanstalk/latest/dg/Welcome.html)
