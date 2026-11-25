FROM ubuntu:24.04
RUN apt-get update && apt-get install -y python3 python3-pip python3-venv && rm -rf /var/lib/apt/lists/*
RUN python3 -m venv /opt/verifier && /opt/verifier/bin/pip install -q pytest
ENV PATH=/opt/verifier/bin:$PATH
WORKDIR /app
COPY . /tests/
