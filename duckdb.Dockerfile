FROM ubuntu:22.04

ARG TARGETARCH

RUN apt-get update && apt-get install -y wget unzip && \
    if [ "$TARGETARCH" = "arm64" ]; then \
        wget https://github.com/duckdb/duckdb/releases/download/v1.1.3/duckdb_cli-linux-aarch64.zip; \
    else \
        wget https://github.com/duckdb/duckdb/releases/download/v1.1.3/duckdb_cli-linux-amd64.zip; \
    fi && \
    unzip duckdb_cli-linux-*.zip && \
    mv duckdb /usr/local/bin/ && \
    rm -f duckdb_cli-linux-*.zip && \
    apt-get clean

WORKDIR /data

ENTRYPOINT ["duckdb"]
