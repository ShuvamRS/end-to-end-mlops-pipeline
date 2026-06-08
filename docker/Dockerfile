FROM ubuntu:22.04

ENV RUNNER_VERSION=2.329.0
LABEL RunnerVersion=${RUNNER_VERSION}
LABEL org.opencontainers.image.source="https://github.com/ShuvamRS/end-to-end-mlops-pipeline"

# Install dependencies needed by GitHub Actions runner and common workflow steps
RUN apt-get update -y && \
    apt-get install -y \
    build-essential \
    lsb-release \
    python3 \
    python3-pip \
    curl \
    jq \
    vim \
    gpg \
    git \
    unzip \
    tar \
    gettext-base \
    ca-certificates && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Add a non-root user
RUN useradd -m runner

WORKDIR /home/actions-runner

# Install GitHub Actions runner
RUN curl -o actions-runner-linux-x64-${RUNNER_VERSION}.tar.gz -L \
    https://github.com/actions/runner/releases/download/v${RUNNER_VERSION}/actions-runner-linux-x64-${RUNNER_VERSION}.tar.gz

RUN tar xzf ./actions-runner-linux-x64-${RUNNER_VERSION}.tar.gz

# Install extra dependencies for the runner
RUN ./bin/installdependencies.sh

# Install AWS CLI v2
RUN curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "/tmp/awscliv2.zip" && \
    unzip -q /tmp/awscliv2.zip -d /tmp && \
    /tmp/aws/install && \
    rm -rf /tmp/aws /tmp/awscliv2.zip

# Install kubectl
RUN curl -L -o /usr/local/bin/kubectl "https://dl.k8s.io/release/v1.34.0/bin/linux/amd64/kubectl" && \
    chmod +x /usr/local/bin/kubectl

COPY startup.sh .

RUN chmod +x startup.sh && \
    chown -R runner:runner /home/actions-runner

USER runner

ENTRYPOINT ["./startup.sh"]
