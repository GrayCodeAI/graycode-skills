FROM python:3.12-slim AS builder

WORKDIR /build
COPY pyproject.toml ./
COPY tools/ tools/
COPY categories/ categories/
RUN pip install --no-cache-dir pyyaml rich

FROM python:3.12-slim
RUN apt-get update && apt-get install -y --no-install-recommends ca-certificates tini && \
    rm -rf /var/lib/apt/lists/* && \
    adduser --disabled-password --gecos "" --uid 1000 skills

COPY --from=builder /build /opt/graycode-skills

USER skills
WORKDIR /opt/graycode-skills
ENTRYPOINT ["tini", "--"]
CMD ["python", "tools/validate_skill.py", "."]
