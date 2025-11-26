# Student exercise

## Exercises

1. [Walking skeleton](./exercises/exercise1.md)
2. [Running the tests](./exercises/exercise2.md)
3. [Finish implementation of entries](./exercises/exercise3.md)
4. [Mini hackathon](./exercises/exercise4.md)


## Overview

A [Flask](https://flask.palletsprojects.com) application integrating the [GOV.UK Design System](https://design-system.service.gov.uk/) with a realistic, containerised stack.

> **GOV.UK Frontend Flask App Template is a [community tool](https://design-system.service.gov.uk/community/resources-and-tools/) of the [GOV.UK Design System](https://design-system.service.gov.uk/). The Design System team is not responsible for it and cannot support you with using it. Contact the [maintainers](#contributors) directly if you need [help](#support) or you want to request a feature.**

## Highlights

- **GOV.UK components built in** – Accessible [Jinja templates](https://github.com/LandRegistry/govuk-frontend-jinja) and [WTForms helpers](https://github.com/LandRegistry/govuk-frontend-wtf) for compliant UI and forms.
- **Secure Flask foundation** – HTTPS, CSRF, CSP, rate limits, [SQLAlchemy](https://www.sqlalchemy.org/) and migrations ready to go.
- **Containerised by default** – [Nginx](https://nginx.org/en/) , [PostgreSQL](https://www.postgresql.org/), [Redis](https://redis.io/) and [Node](https://nodejs.org/en) pipeline managed via [Docker Compose](https://docs.docker.com/compose/).
- **Fast, lean builds** – Multi-stage Dockerfiles, wheel caching, non-root runtime, and CI via [GitHub Actions](https://github.com/features/actions).
- **Compliance-ready pages** – 404/500 errors, cookie banner, accessibility statement included.
- **Developer-first setup** – Example blueprints, templates, macros, and GOV.UK-style flash messages for instant feedback.

## Security

Secure by default with hardened containers, strong HTTP headers and built-in rate limiting.

- Applies strict CSP, HSTS, and other security headers.
- CSRF protection via Flask-WTF, with safe error handling.
- Rate limiting backed by Redis using Flask-Limiter.
- Non-root containers with read-only filesystem for runtime services.
- Secrets and credentials injected via environment variables (no in-repo secrets).
- Dependency scanning and Python version pinning via CI workflows.

## Performance

Optimised for speed and reliability through caching, minimal layers and lean builds.

- Multi-stage Docker builds minimise image size and attack surface.
- Static assets compiled once and cached efficiently.
- Connection pooling for SQLAlchemy database access.
- Redis caching support for transient or computed data.
- Nginx configured for compression and cache control.
- CI validates image build times and wheel caching efficiency.

## Developer Experience

Built to feel frictionless for rapid iteration, testing and deployment.

- Works identically across local and production environments.
- Uses docker compose watch for hot reloads of Python and static assets.
- Includes blueprints, forms, templates and example routes to extend quickly.
- Built-in error pages, logging and debug toolbar (development mode).
- Extensive comments and .env.example for easy onboarding.
- CI workflows for linting, tests, builds and security scans.

## Requirements

- Docker (Engine & Compose)


## Environment

| Service    | Role                              | Container | Port exposed     |
| ---------- | --------------------------------- | --------- | ---------------- |
| Nginx      | Reverse proxy + HTTPS termination | `web`     | 443 (HTTPS) / 80 |
| Flask      | Web framework                     | `app`     | 5000             |
| PostgreSQL | Relational database               | `db`      | 5432             |
| Redis      | Caching + rate limiting backend   | `cache`   | 6379             |

## Architecture

### Container stack

This project uses Docker Compose to provision containers:

```mermaid
flowchart TB
    compose(compose.yml)
    nginx(nginx:stable-alpine)
    node(node:kyrpton-alpine)
    postgres(postgres:18-alpine)
    python(python:3.14-slim)
    redis(redis:7-alpine)

    compose -- Creates --> App & Cache & Web & Database
    App -- Depends on --> Cache & Database
    Web -- Depends on --> App

    subgraph Web
        direction TB
        node -- COPY /dist /static --> nginx
    end

    subgraph App
        python
    end

    subgraph Database
        postgres
    end

    subgraph Cache
        redis
    end
```

### Request flow

```mermaid
flowchart TB
    browser([Browser])
    db@{ shape: cyl, label: "PostgreSQL" }
    flask(Gunicorn/Flask)
    nginx(NGINX)
    redis(Redis)
    static@{ shape: lin-cyl, label: "Static files" }

    browser -- https:443 --> nginx -- http:5000 --> flask -- postgres:5432 --> db
    flask -- redis:6379 --> redis

    subgraph Web
        nginx -- Read --> static
    end

    subgraph App
        flask
    end

    subgraph Database
        db
    end

    subgraph Cache
        redis
    end
```

## Maintainers

- [Matt Shaw](https://github.com/matthew-shaw) - Principal Software Developer at HM Land Registry

## Support

This software is provided _"as-is"_ without warranty. Support is provided on a _"best endeavours"_ basis by the maintainers and open source community.

For questions or suggestions, reach out to the maintainers listed [above](#maintainers) and the community of people using this project in the [#govuk-design-system](https://ukgovernmentdigital.slack.com/archives/C6DMEH5R6) Slack channel.

Otherwise, please see the [contribution guidelines](CONTRIBUTING.md) for how to raise a bug report or feature request.

