FROM ubuntu:24.04
RUN apt-get update && apt-get install -y git python3 python3-pip python3-venv && rm -rf /var/lib/apt/lists/*
# Base: pallets/click at tag 8.5.1 (fixed commit)
RUN git clone https://github.com/pallets/click.git /app \
 && cd /app && git checkout cf19179e8e2fd54c601378cec9e0d21bb12b6fb1
WORKDIR /app
RUN python3 -m venv /opt/venv && /opt/venv/bin/pip install -q -e . pytest
ENV PATH=/opt/venv/bin:$PATH
