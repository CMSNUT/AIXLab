#!/usr/bin/env Rscript

# AIXLab R分析服务
# 注意：需要安装以下R包：plumber, jsonlite, ggplot2, base64enc

# 加载必要的库
library(plumber)
library(jsonlite)
library(ggplot2)
library(base64enc)

#* @apiTitle AIXLab R分析服务
#* @apiDescription R数据分析与可视化API服务

# 健康检查端点
#* @get /api/r/health
function() {
  return(list(
    status = "healthy", 
    service = "r-analysis",
    version = "1.0.0",
    timestamp = Sys.time()
  ))
}

# 执行R代码端点
#* @post /api/r/plot
function(dataset_path = NULL, plot_type = "scatter", parameters = list()) {
  tryCatch({
    cat("收到绘图请求:\n")
    cat("  plot_type:", plot_type, "\n")
    cat("  dataset_path:", dataset_path, "\n")
    
    # 读取数据
    if (!is.null(dataset_path) && file.exists(dataset_path)) {
      df <- read.csv(dataset_path)
      cat("  从文件读取数据，行数:", nrow(df), "列数:", ncol(df), "\n")
    } else {
      # 使用内置iris数据集
      cat("  文件不存在或未指定，使用内置iris数据集\n")
      df <- iris
      # 重命名列以匹配预期
      names(df) <- c("sepal_length", "sepal_width", "petal_length", "petal_width", "species")
    }
    
    # 创建图表
    p <- NULL
    
    if (plot_type == "scatter") {
      p <- ggplot(df, aes(x = sepal_length, y = sepal_width, color = species)) +
        geom_point(size = 3, alpha = 0.7) +
        labs(title = "R ggplot2 - 散点图", 
             x = "萼片长度", 
             y = "萼片宽度") +
        theme_minimal()
      
    } else if (plot_type == "line") {
      # 为折线图创建数据
      line_data <- data.frame(
        x = 1:nrow(df),
        y = df$sepal_length
      )
      
      p <- ggplot(line_data, aes(x = x, y = y)) +
        geom_line(color = "blue", linewidth = 1.5) +
        geom_point(color = "red", size = 2) +
        labs(title = "R ggplot2 - 折线图", 
             x = "索引", 
             y = "萼片长度") +
        theme_minimal()
      
    } else if (plot_type == "histogram") {
      p <- ggplot(df, aes(x = sepal_length)) +
        geom_histogram(bins = 20, fill = "skyblue", color = "black", alpha = 0.7) +
        labs(title = "R ggplot2 - 直方图", 
             x = "萼片长度", 
             y = "频率") +
        theme_minimal()
      
    } else if (plot_type == "boxplot") {
      p <- ggplot(df, aes(x = species, y = sepal_length, fill = species)) +
        geom_boxplot(alpha = 0.7) +
        labs(title = "R ggplot2 - 箱线图", 
             x = "种类", 
             y = "萼片长度") +
        theme_minimal() +
        theme(legend.position = "none")
      
    } else {
      # 默认散点图
      p <- ggplot(df, aes(x = sepal_length, y = sepal_width, color = species)) +
        geom_point(size = 3, alpha = 0.7) +
        labs(title = "R ggplot2 - 默认散点图", 
             x = "萼片长度", 
             y = "萼片宽度") +
        theme_minimal()
    }
    
    # 保存为临时文件
    temp_file <- tempfile(fileext = ".png")
    ggsave(temp_file, plot = p, width = 8, height = 6, dpi = 100)
    
    # 转换为base64
    img_data <- base64enc::base64encode(temp_file)
    
    # 清理临时文件
    unlink(temp_file)
    
    # 返回结果
    list(
      success = TRUE,
      plot_type = plot_type,
      image = as.character(img_data),
      image_info = list(
        width = 800,
        height = 600,
        format = "png"
      ),
      data_info = list(
        rows = nrow(df),
        columns = ncol(df),
        shape = c(nrow(df), ncol(df))
      )
    )
    
  }, error = function(e) {
    list(
      success = FALSE,
      error = conditionMessage(e)
    )
  })
}

# 测试端点
#* @get /api/r/test
function() {
  tryCatch({
    # 创建测试图表
    test_data <- data.frame(
      x = 1:10,
      y = (1:10)^2,
      group = rep(c("A", "B"), each = 5)
    )
    
    p <- ggplot(test_data, aes(x = x, y = y, color = group)) +
      geom_point(size = 4) +
      geom_line(linewidth = 1.5) +
      labs(title = "R测试图表", x = "X轴", y = "Y轴") +
      theme_minimal()
    
    temp_file <- tempfile(fileext = ".png")
    ggsave(temp_file, plot = p, width = 8, height = 6, dpi = 100)
    
    img_data <- base64enc::base64encode(temp_file)
    unlink(temp_file)
    
    list(
      success = TRUE,
      message = "R测试图表生成成功",
      image = as.character(img_data)
    )
    
  }, error = function(e) {
    list(
      success = FALSE,
      error = conditionMessage(e)
    )
  })
}