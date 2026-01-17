from fastapi import FastAPI
import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn.datasets import load_iris
import matplotlib.pyplot as plt
import base64
import io

app = FastAPI(title="Python Analysis API")

# 加载Iris数据
def load_iris_data():
    iris = load_iris()
    df = pd.DataFrame(iris.data, columns=[
        'sepal_length', 'sepal_width', 
        'petal_length', 'petal_width'
    ])
    df['species'] = pd.Categorical.from_codes(iris.target, iris.target_names)
    return df

# 健康检查
@app.get("/")
async def root():
    return {"service": "Python Analysis API", "status": "running"}

@app.get("/health")
async def health():
    return {"status": "ok"}

# 查看数据
@app.post("/iris/view")
async def view_iris():
    df = load_iris_data()
    return {
        "rows": df.head(10).to_dict(orient="records"),
        "summary": df.describe().to_dict(),
        "species_counts": df['species'].value_counts().to_dict()
    }

# 聚类分析
@app.post("/iris/cluster")
async def cluster_iris(data: dict):
    n_clusters = data.get("n_clusters", 3)
    df = load_iris_data()
    
    # 准备数据
    X = df[['sepal_length', 'sepal_width', 'petal_length', 'petal_width']].values
    
    # K-means聚类
    kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
    clusters = kmeans.fit_predict(X)
    
    # 计算轮廓系数
    from sklearn.metrics import silhouette_score
    score = silhouette_score(X, clusters)
    
    # 每个簇的统计
    df['cluster'] = clusters
    cluster_stats = {}
    for i in range(n_clusters):
        cluster_data = df[df['cluster'] == i]
        cluster_stats[i] = {
            "size": len(cluster_data),
            "sepal_length_mean": float(cluster_data['sepal_length'].mean()),
            "sepal_width_mean": float(cluster_data['sepal_width'].mean()),
            "petal_length_mean": float(cluster_data['petal_length'].mean()),
            "petal_width_mean": float(cluster_data['petal_width'].mean()),
        }
    
    return {
        "algorithm": "K-means",
        "n_clusters": n_clusters,
        "silhouette_score": float(score),
        "inertia": float(kmeans.inertia_),
        "cluster_assignments": clusters.tolist(),
        "cluster_stats": cluster_stats
    }

# 绘图
@app.post("/iris/plot")
async def plot_iris(data: dict):
    plot_type = data.get("plot_type", "scatter")
    x_col = data.get("x_col", "sepal_length")
    y_col = data.get("y_col", "sepal_width")
    
    df = load_iris_data()
    
    # 创建图表
    plt.figure(figsize=(8, 6))
    
    if plot_type == "scatter":
        colors = {'setosa': 'red', 'versicolor': 'green', 'virginica': 'blue'}
        for species, color in colors.items():
            species_data = df[df['species'] == species]
            plt.scatter(species_data[x_col], species_data[y_col], 
                       color=color, label=species, alpha=0.7)
        
        plt.xlabel(x_col)
        plt.ylabel(y_col)
        plt.title(f'Iris Dataset: {y_col} vs {x_col}')
        plt.legend()
        plt.grid(True, alpha=0.3)
    
    elif plot_type == "boxplot":
        data_to_plot = [df[df['species'] == species][x_col].values 
                       for species in df['species'].unique()]
        plt.boxplot(data_to_plot, labels=df['species'].unique())
        plt.ylabel(x_col)
        plt.title(f'Distribution of {x_col} by Species')
    
    # 转换为base64
    buf = io.BytesIO()
    plt.tight_layout()
    plt.savefig(buf, format='png', dpi=100)
    plt.close()
    buf.seek(0)
    img_base64 = base64.b64encode(buf.read()).decode('utf-8')
    
    return {
        "plot_type": plot_type,
        "image_format": "png",
        "image_base64": img_base64,
        "x_column": x_col,
        "y_column": y_col
    }