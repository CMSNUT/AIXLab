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

# 加法API - 接收JSON格式的data
#* @post /api/r452/add
function(req) {
  # 解析请求体
  body <- tryCatch({
    jsonlite::fromJSON(req$postBody)
  }, error = function(e) {
    return(list(error = "JSON解析失败"))
  })
  
  # 提取data中的a和b
  if (is.null(body$data)) {
    return(list(
      success = FALSE,
      error = "请求格式错误",
      required_format = list(data = list(a = "number", b = "number"))
    ))
  }
  
  data <- body$data
  a <- data$a
  b <- data$b
  
  # 验证参数
  if (is.null(a) || is.null(b)) {
    return(list(
      success = FALSE,
      error = "缺少参数a或b"
    ))
  }
  
  # 转换为数值
  a_num <- as.numeric(a)
  b_num <- as.numeric(b)
  
  if (is.na(a_num) || is.na(b_num)) {
    return(list(
      success = FALSE,
      error = "参数必须是有效的数字"
    ))
  }
  
  # 执行计算
  result <- a_num + b_num
  
  # 返回结果
  list(
    success = TRUE,
    operation = "addition",
    data = list(
      a = a_num,
      b = b_num,
      result = result
    ),
    computed_in = "R",
    timestamp = as.character(Sys.time())
  )
}

# 批量计算API
#* @post /api/r452/batch_add
function(req) {
  # ========== 核心修改1：统一接口返回格式，定义基础返回体 ==========
  # 无论成功/失败，都返回固定格式，让Python端解析不报错
  res <- list(
    success = FALSE,
    operations = NULL,
    results = NULL,
    computed_in = "R",
    timestamp = format(Sys.time(), "%Y-%m-%d %H:%M:%S"), # 格式化时间为字符串，Python解析更友好
    error = NULL # 新增错误描述字段，精准反馈问题
  )
  
  # ========== 步骤1：解析JSON请求体，完善解析失败的容错 ==========
  body <- tryCatch({
    # 强制解析为列表，避免返回原子向量
    jsonlite::fromJSON(req$postBody, simplifyVector = FALSE)
  }, error = function(e) {
    # 解析失败返回统一格式，而非单独的error列表
    res$error <- paste0("JSON解析失败: ", e$message)
    return(res)
  })
  
  # ========== 核心修改2：校验body$operations的合法性（杜绝循环内报错） ==========
  # 1. 检查operations是否存在 2. 检查是否为列表/向量（数组） 3. 检查是否非空
  if (is.null(body$operations) || !is.vector(body$operations) || length(body$operations) == 0) {
    res$error <- "缺少有效的operations数组（必须是非空的数组/列表）"
    return(res)
  }
  
  # 赋值合法的operations到返回体
  res$operations <- body$operations
  # 初始化结果列表，长度和operations一致
  results <- vector("list", length(body$operations))
  
  # ========== 步骤2：循环处理每个操作，核心加op的类型+字段校验 ==========
  for (i in seq_along(body$operations)) {
    op <- body$operations[[i]]
    # 初始化单个操作的结果
    op_res <- list(
      success = FALSE,
      operation = op, # 回传原操作，方便前端定位错误
      error = NULL,
      result = NULL
    )
    
    # ========== 核心修改3：校验op的类型，杜绝原子向量用$取值 ==========
    # 强制要求op是列表（只有列表才能用$取字段），否则直接标记错误
    if (!is.list(op)) {
      op_res$error <- paste0("操作", i, "格式错误：非列表类型（禁止原子向量/标量）")
      results[[i]] <- op_res
      next # 跳过当前错误操作，继续处理下一个（批量接口核心）
    }
    
    # ========== 核心修改4：校验op的必传字段（type/a/b） ==========
    required_fields <- c("type", "a", "b")
    missing_fields <- setdiff(required_fields, names(op))
    if (length(missing_fields) > 0) {
      op_res$error <- paste0("操作", i, "缺少必传字段：", paste(missing_fields, collapse = "、"))
      results[[i]] <- op_res
      next
    }
    
    # ========== 步骤3：处理具体的计算逻辑，保留原逻辑+完善容错 ==========
    tryCatch({
      # 转换为数值型，原逻辑保留
      a <- as.numeric(op$a)
      b <- as.numeric(op$b)
      
      # 检查数值是否有效（NA/NaN都算无效）
      if (is.na(a) || is.na(b) || is.nan(a) || is.nan(b)) {
        op_res$error <- paste0("操作", i, "数值无效：a=", op$a, "，b=", op$b, "（必须是数字）")
        results[[i]] <- op_res
        next
      }
      
      # 加法/乘法计算，原逻辑保留
      if (op$type == "add") {
        op_res$result <- a + b
        op_res$type <- "add"
        op_res$success <- TRUE
      } else if (op$type == "multiply") {
        op_res$result <- a * b
        op_res$type <- "multiply"
        op_res$success <- TRUE
      } else {
        op_res$error <- paste0("操作", i, "类型不支持：仅支持add（加法）、multiply（乘法）")
      }
    }, error = function(e) {
      # 捕获计算过程中的意外错误（比如数值溢出等）
      op_res$error <- paste0("操作", i, "计算失败：", e$message)
    })
    
    # 将单个操作结果加入总结果
    results[[i]] <- op_res
  }
  
  # ========== 步骤3：最终结果赋值，标记整体成功状态 ==========
  res$results <- results
  # 整体成功：所有操作都成功 ｜ 宽松版：至少有一个操作成功（根据需求选一个）
  # 严格版（推荐）：所有操作成功，整体才成功
  res$success <- all(sapply(results, function(x) x$success))
  # 宽松版：只要有一个操作成功，整体就成功（如需开启，注释上面一行，打开下面一行）
  # res$success <- any(sapply(results, function(x) x$success))
  
  # 返回最终结果
  return(res)
}

