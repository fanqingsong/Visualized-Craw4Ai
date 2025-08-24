FROM swr.cn-north-4.myhuaweicloud.com/ddn-k8s/docker.io/node:18-alpine

# 设置工作目录
WORKDIR /app

# 设置 npm 使用淘宝镜像源
RUN npm config set registry https://registry.npmmirror.com

# 复制package文件
COPY package*.json ./

# 安装依赖
RUN npm ci

# 复制应用代码
COPY . .

# 暴露端口
EXPOSE 3000

# 启动命令 - 使用Vite开发服务器
CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0"]
