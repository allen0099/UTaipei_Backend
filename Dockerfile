FROM python:3.11-slim AS base
LABEL authors="allen0099"

WORKDIR /app
ENV PATH="/opt/venv/bin:$PATH"

FROM base AS library

RUN python -m venv /opt/venv

# Upgrade pip and install dependences
RUN pip install --no-cache-dir --upgrade pip setuptools wheel

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

FROM base AS production

# Install curl
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
      curl && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* /var/cache/apt/archives/*

# Pull python dependences
COPY --from=library /opt/venv /opt/venv

COPY docker-entrypoint.sh /
ENTRYPOINT ["/docker-entrypoint.sh"]

FROM production

# Change to non-root user
ARG user=app
ARG group=app
ARG uid=1000
ARG gid=1000
RUN groupadd -g ${gid} ${group}
RUN useradd -u ${uid} -g ${group} -s /bin/sh -m ${user}

COPY . .
