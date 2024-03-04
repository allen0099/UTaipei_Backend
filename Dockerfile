FROM python:3.11-slim AS base
LABEL authors="allen0099"

WORKDIR /app
ENV PATH="/opt/venv/bin:$PATH"

FROM base AS library

RUN pip install uv
RUN uv venv /opt/venv && source /opt/venv/bin/activate

COPY requirements.txt .
RUN uv pip install --no-cache -r requirements.txt

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

RUN mkdir /app/logs && \
    chown -R app:app /app/logs

# Change to non-root user
USER ${user}

COPY . .
