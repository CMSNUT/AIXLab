#!/usr/bin/env Rscript

# AIXLab R分析服务
# 注意: 需要安装以下R包: plumber, jsonlite, ggplot2, base64enc

# 加载必要的库
library(plumber)
library(jsonlite)
library(ggplot2)
library(base64enc)

#* @apiTitle AIXLab R分析服务
#* @apiDescription R数据分析与可视化API服务

# 健康检查端点
#* @get /api/r452/health
function() {
  list(
    status = "healthy", 
    service = "r452_service",
    version = "0.1.0",
    timestamp = Sys.time()
  )
}