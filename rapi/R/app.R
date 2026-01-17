library(plumber)
library(ggplot2)
library(cluster)
library(datasets)
library(base64enc)

# 加载Iris数据
load_iris_data <- function() {
  data(iris)
  return(iris)
}

# 创建Plumber应用
pr <- plumber$new()

# 健康检查
pr$handle("GET", "/", function(req, res) {
  list(service = "R Analysis API", status = "running")
})

pr$handle("GET", "/health", function(req, res) {
  list(status = "ok")
})

# 查看数据
pr$handle("POST", "/iris/view", function(req, res) {
  df <- load_iris_data()
  list(
    rows = head(df, 10),
    summary = summary(df),
    species_counts = table(df$Species)
  )
})

# 聚类分析
pr$handle("POST", "/iris/cluster", function(req, res) {
  n_clusters <- req$body$n_clusters %||% 3
  df <- load_iris_data()
  
  # 准备数据
  X <- df[, 1:4]
  
  # K-means聚类
  set.seed(42)
  kmeans_result <- kmeans(X, centers = n_clusters, nstart = 10)
  
  # 轮廓系数
  silhouette <- silhouette(kmeans_result$cluster, dist(X))
  silhouette_avg <- mean(silhouette[, 3])
  
  # 每个簇的统计
  df$cluster <- kmeans_result$cluster
  cluster_stats <- list()
  
  for (i in 1:n_clusters) {
    cluster_data <- df[df$cluster == i, ]
    cluster_stats[[as.character(i)]] <- list(
      size = nrow(cluster_data),
      Sepal.Length_mean = mean(cluster_data$Sepal.Length),
      Sepal.Width_mean = mean(cluster_data$Sepal.Width),
      Petal.Length_mean = mean(cluster_data$Petal.Length),
      Petal.Width_mean = mean(cluster_data$Petal.Width)
    )
  }
  
  list(
    algorithm = "K-means",
    n_clusters = n_clusters,
    silhouette_score = silhouette_avg,
    tot.withinss = kmeans_result$tot.withinss,
    cluster_assignments = as.list(kmeans_result$cluster),
    cluster_stats = cluster_stats
  )
})

# 绘图
pr$handle("POST", "/iris/plot", function(req, res) {
  plot_type <- req$body$plot_type %||% "scatter"
  x_col <- req$body$x_col %||% "Sepal.Length"
  y_col <- req$body$y_col %||% "Sepal.Width"
  
  df <- load_iris_data()
  
  # 创建图表
  if (plot_type == "scatter") {
    p <- ggplot(df, aes_string(x = x_col, y = y_col, color = "Species")) +
      geom_point(size = 3, alpha = 0.7) +
      labs(title = paste("Iris Dataset:", y_col, "vs", x_col)) +
      theme_minimal()
  } else if (plot_type == "boxplot") {
    p <- ggplot(df, aes_string(x = "Species", y = x_col, fill = "Species")) +
      geom_boxplot(alpha = 0.7) +
      labs(title = paste("Distribution of", x_col, "by Species")) +
      theme_minimal() +
      theme(legend.position = "none")
  }
  
  # 保存为base64
  temp_file <- tempfile(fileext = ".png")
  ggsave(temp_file, p, width = 8, height = 6, dpi = 100)
  
  img_data <- readBin(temp_file, "raw", file.info(temp_file)$size)
  img_base64 <- base64enc::base64encode(img_data)
  unlink(temp_file)
  
  list(
    plot_type = plot_type,
    image_format = "png",
    image_base64 = img_base64,
    x_column = x_col,
    y_column = y_col
  )
})

# 启动服务
pr$run(host = "0.0.0.0", port = 8002)