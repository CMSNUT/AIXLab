#!/usr/bin/env Rscript

# 运行R分析服务
library(plumber)

# ==================== 核心: 添加跨域过滤器 ====================
# 定义跨域过滤器(所有请求都会经过这个过滤器)
cors_filter <- function(req, res) {
  # 允许所有域名跨域访问(* 表示任意来源, 也可指定具体域名如"http://localhost:8000")
  res$setHeader("Access-Control-Allow-Origin", "*")
  # 允许的请求方法(GET/POST/PUT/DELETE等)
  res$setHeader("Access-Control-Allow-Methods", "GET, POST, PUT, DELETE, OPTIONS")
  # 允许的请求头
  res$setHeader("Access-Control-Allow-Headers", "Content-Type, Authorization")
  # 预检请求(OPTIONS)的缓存时间(秒)
  res$setHeader("Access-Control-Max-Age", "86400")
  
  # 处理预检请求(OPTIONS), 直接返回200
  if (req$REQUEST_METHOD == "OPTIONS") {
    res$status <- 200
    return(list())
  }
  
  # 继续处理原请求
  plumber::forward()
}

# 加载API定义
pr <- plumber::plumb("app.R")

# 注册跨域过滤器
pr$registerHook("preroute", cors_filter)

# 启动服务
cat("========================================\n")
cat("AIXLab R分析服务启动\n")
cat("服务端口: 8002\n")
cat("健康检查: http://localhost:8002/api/r452/health\n")
cat("========================================\n")

pr$run(host = "127.0.0.1", port = 8002)
