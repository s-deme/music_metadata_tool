FROM python:3.11-slim

ENV PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_NO_CACHE_DIR=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    VENV_PATH=/opt/venv

WORKDIR /workspace

RUN set -eux; \
    apt-get update; \
    apt-get install -y --no-install-recommends bash git ca-certificates nodejs npm; \
    rm -rf /var/lib/apt/lists/*

# 仮想環境を用意して dev 依存ごとインストール（pandas も含める）。
RUN python -m venv "$VENV_PATH" && \
    . "$VENV_PATH/bin/activate" && \
    pip install --upgrade pip

# musubi は npm パッケージとしてインストールする
RUN npm install -g musubi-sdd

ENV PATH="$VENV_PATH/bin:${PATH}"

# 依存インストール。開発用なので dev + pandas をインストール。
COPY pyproject.toml README* ./
COPY src ./src
RUN . "$VENV_PATH/bin/activate" && pip install -e .[dev,pandas]

# 開発コンテナ: ホストのソースをマウントして使う前提。

CMD ["bash"]
