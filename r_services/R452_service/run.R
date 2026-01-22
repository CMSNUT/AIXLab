#!/usr/bin/env Rscript

# 运行R分析服务
library(plumber)

# 加载API定义
pr <- plumber::plumb("app.R")

# 启动服务
cat("========================================\n")
cat("AIXLab R分析服务启动\n")
cat("服务端口: 8002\n")
cat("健康检查: http://localhost:8002/api/r452_service/health\n")
cat("========================================\n")

pr$run(host = "localhost", port = 8002)
