# 使用官方 Python 作为基础镜像
FROM m.daocloud.io/docker.io/library/python:3.9-slim

# 设置工作目录
WORKDIR /app

# 复制 requirements 文件并安装依赖
COPY backend/requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt

# 复制 Django 项目文件
COPY backend/ /app/

# 设置环境变量
ENV PYTHONUNBUFFERED 1

# 暴露 uWSGI 默认端口
EXPOSE 8000

# 启动 uWSGI
CMD ["uwsgi", "--ini", "uwsgi.ini"]
