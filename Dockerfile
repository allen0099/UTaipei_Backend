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

# Pull python dependences
COPY --from=library /opt/venv /opt/venv

COPY docker-entrypoint.sh /
ENTRYPOINT ["/docker-entrypoint.sh"]

FROM production

COPY . .
