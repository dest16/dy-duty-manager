# 使用 Node.js 官方镜像作为基础镜像
FROM m.daocloud.io/docker.io/library/node:16

# 设置工作目录
WORKDIR /app

# 复制 package.json 和 package-lock.json
COPY frontend/package*.json /app/

# 安装依赖
RUN npm install

# 复制所有项目文件
COPY frontend/ /app/

# 构建 Vue 项目
RUN npm run build

# 使用 nginx 作为前端部署的服务器
FROM nginx:alpine

# 删除默认的 nginx 配置
RUN rm /etc/nginx/conf.d/default.conf

# 复制前端构建的文件到 nginx 的默认位置
COPY --from=0 /app/dist /usr/share/nginx/html

# 暴露 nginx 默认端口
EXPOSE 8080

# 启动 nginx
CMD ["nginx", "-g", "daemon off;"]
