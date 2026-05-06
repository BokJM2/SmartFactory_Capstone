FROM python:3.11.8-slim-bookworm

# gunicorn 进程数量 http服务端口号
ENV WORKER_NUM=1 \
    PORT=80

COPY . /api

WORKDIR /api

# 更新apt为国内源
RUN sed -i 's/deb.debian.org/mirrors.ustc.edu.cn/g' /etc/apt/sources.list.d/debian.sources && \
    sed -i 's/security.debian.org/mirrors.ustc.edu.cn\/debian-security/g' /etc/apt/sources.list.d/debian.sources && \
    # 安装python 依赖
    pip install -r requirements.txt
    # apt update && apt install -y --no-install-recommends xxx # apt 安装 xxx

CMD sh bin/boot.sh
