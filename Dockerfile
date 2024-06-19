# 使用官方Python 3.10镜像作为基础镜像
FROM python:3.10

# 安装Node.js
RUN curl -fsSL https://deb.nodesource.com/setup_18.x | bash - && \
    apt-get install -y nodejs

# 安装pnpm
RUN npm install -g pnpm

# 设置工作目录
WORKDIR /app

# 将项目文件复制到容器中
COPY ./ /app

# 安装Python依赖
RUN pip install --no-cache-dir -r requirements.txt

# 安装前端依赖
WORKDIR /app/webui
RUN pnpm install
WORKDIR /app

# 暴露端口
EXPOSE 8000 3000

# 设置默认环境变量
ENV PYTHONUNBUFFERED 1

# 设置默认运行命令为启动一个bash shell
CMD ["/bin/bash"
