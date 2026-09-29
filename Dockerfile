# Distributable image: the skill corpus plus the validation/registry tooling.
# The default command runs the same full-corpus zero-warning gate as CI.
FROM python:3.12-slim AS builder

# Dependencies go into a virtualenv so the runtime stage can copy them; a plain
# `pip install` here would land in this stage's site-packages and be lost.
COPY tools/requirements.txt /tmp/requirements.txt
RUN python -m venv /opt/venv && \
    /opt/venv/bin/pip install --no-cache-dir -r /tmp/requirements.txt

FROM python:3.12-slim
RUN apt-get update && apt-get install -y --no-install-recommends ca-certificates tini && \
    rm -rf /var/lib/apt/lists/* && \
    adduser --disabled-password --gecos "" --uid 1000 skills

COPY --from=builder /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

WORKDIR /opt/graycode-skills
# manifest-schema.toml is the validator's schema source of truth; without it
# validation cannot run.
COPY pyproject.toml manifest-schema.toml VERSION ./
COPY tools/ tools/
COPY categories/ categories/

USER skills
ENTRYPOINT ["tini", "--"]
CMD ["python", "tools/validate_skill.py", "--all", "--warning-budget", "tools/validation_warning_budget.json"]
