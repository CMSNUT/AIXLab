from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, Dict, Any
import uvicorn
import pandas as pd
import matplotlib
matplotlib.use('Agg')  # 使用非交互式后端
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
import numpy as np
import io
import base64
import os
import traceback

app = FastAPI(title="AIXLab Python分析服务")

# CORS配置
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 允许所有源，实际生产环境应限制
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 数据模型
class PlotRequest(BaseModel):
    dataset_path: str
    plot_type: str = "scatter"
    parameters: Optional[Dict[str, Any]] = None

class ExecuteRequest(BaseModel):
    dataset_path: str
    code: str
    parameters: Optional[Dict[str, Any]] = None

def read_dataset(file_path: str):
    """读取数据集"""
    try:
        # 检查文件是否存在
        if not os.path.exists(file_path):
            # 尝试从data目录查找
            alt_path = os.path.join("data", os.path.basename(file_path))
            if os.path.exists(alt_path):
                file_path = alt_path
            else:
                # 尝试从backend/data目录查找
                alt_path2 = os.path.join("..", "backend", "data", os.path.basename(file_path))
                if os.path.exists(alt_path2):
                    file_path = alt_path2
                else:
                    print(f"文件不存在: {file_path}，使用示例数据")
                    return create_sample_data()
        
        # 读取文件
        if file_path.endswith('.csv'):
            return pd.read_csv(file_path)
        elif file_path.endswith('.json'):
            return pd.read_json(file_path)
        else:
            # 尝试作为CSV读取
            return pd.read_csv(file_path)
            
    except Exception as e:
        print(f"读取数据失败: {e}")
        return create_sample_data()

def create_sample_data():
    """创建示例数据"""
    np.random.seed(42)
    n = 150
    data = {
        'sepal_length': np.random.normal(5.8, 0.8, n),
        'sepal_width': np.random.normal(3.0, 0.4, n),
        'petal_length': np.random.normal(3.8, 1.8, n),
        'petal_width': np.random.normal(1.2, 0.8, n),
        'species': np.repeat(['setosa', 'versicolor', 'virginica'], n//3)
    }
    return pd.DataFrame(data)

# 设置中文字体
def setup_chinese_font():
    """
    设置中文字体，支持 Windows、Linux、macOS
    """
    try:
        # 尝试多种字体，按优先级排序
        font_options = [
            # Windows 字体
            'Microsoft YaHei',      # 微软雅黑
            'SimHei',               # 黑体
            'SimSun',               # 宋体
            # macOS 字体
            'PingFang SC',          # 苹方
            'Heiti SC',             # 黑体-简
            # Linux 字体
            'DejaVu Sans',          # 常用开源字体
            'WenQuanYi Micro Hei',  # 文泉驿微米黑
            'Noto Sans CJK SC',     # Google Noto 字体
            'AR PL UMing CN',       # 文鼎明体
        ]
        
        # 首先尝试使用系统字体
        for font_name in font_options:
            try:
                # 检查字体是否存在
                font_path = matplotlib.font_manager.findfont(font_name)
                if font_path:
                    print(f"找到字体: {font_name}, 路径: {font_path}")
                    
                    # 设置 matplotlib 默认字体
                    plt.rcParams['font.sans-serif'] = [font_name]
                    plt.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题
                    
                    # 设置全局字体属性
                    matplotlib.rcParams['font.family'] = font_name
                    matplotlib.rcParams['font.sans-serif'] = [font_name]
                    
                    print(f"成功设置中文字体为: {font_name}")
                    return font_name
            except Exception as e:
                print(f"字体 {font_name} 设置失败: {e}")
                continue
        
        # 如果系统字体都不行，尝试下载并添加字体
        print("未找到合适的中文字体，尝试下载字体...")
        setup_custom_font()
        
    except Exception as e:
        print(f"字体设置过程中出错: {e}")
        traceback.print_exc()

def setup_custom_font():
    """
    下载并安装中文字体
    """
    try:
        import requests
        import tempfile
        
        # 字体下载URL（开源字体）
        font_urls = {
            'SimHei': 'https://github.com/googlefonts/noto-cjk/raw/main/Sans/OTF/SimplifiedChinese/NotoSansCJKsc-Regular.otf',
            'SourceHanSansSC': 'https://github.com/adobe-fonts/source-han-sans/raw/release/OTF/SimplifiedChinese/SourceHanSansSC-Regular.otf'
        }
        
        # 创建临时目录
        temp_dir = tempfile.mkdtemp()
        font_path = os.path.join(temp_dir, 'chinese_font.otf')
        
        # 下载字体
        for font_name, url in font_urls.items():
            try:
                print(f"正在下载字体: {font_name}")
                response = requests.get(url, timeout=10)
                if response.status_code == 200:
                    with open(font_path, 'wb') as f:
                        f.write(response.content)
                    
                    # 添加字体到 matplotlib
                    font_prop = FontProperties(fname=font_path)
                    font_name = font_prop.get_name()
                    
                    # 设置全局字体
                    matplotlib.font_manager.fontManager.addfont(font_path)
                    plt.rcParams['font.sans-serif'] = [font_name]
                    plt.rcParams['axes.unicode_minus'] = False
                    matplotlib.rcParams['font.family'] = font_name
                    
                    print(f"成功添加自定义字体: {font_name}")
                    return font_name
            except Exception as e:
                print(f"下载字体 {font_name} 失败: {e}")
                continue
        
        print("所有字体下载尝试都失败了")
        return None
        
    except Exception as e:
        print(f"自定义字体设置失败: {e}")
        traceback.print_exc()
        return None

# 初始化字体
chinese_font = setup_chinese_font()

def plot_to_base64():
    """将当前图表转换为base64"""
    buf = io.BytesIO()
    plt.savefig(buf, format='png', dpi=100, bbox_inches='tight')
    buf.seek(0)
    image_base64 = base64.b64encode(buf.getvalue()).decode('utf-8')
    plt.close()
    return image_base64

# ========== API端点 ==========

@app.get("/")
async def root():
    return {
        "message": "AIXLab Python分析服务运行中",
        "version": "1.0",
        "endpoints": {
            "health": "/api/python/health (GET)",
            "test": "/api/python/test (GET)",
            "plot": "/api/python/plot (POST)",
            "execute": "/api/python/execute (POST)"
        }
    }

@app.get("/api/python/health")
async def health_check():
    """健康检查端点"""
    return {
        "status": "healthy",
        "service": "python-analysis",
        "version": "1.0.0",
        "timestamp": pd.Timestamp.now().isoformat()
    }

@app.get("/api/python/test")
async def test_plot():
    """测试绘图端点"""
    try:
        # 创建测试图表
        plt.figure(figsize=(10, 6))
        
        # 创建简单图表
        x = np.linspace(0, 10, 100)
        y1 = np.sin(x)
        y2 = np.cos(x)
        
        plt.plot(x, y1, 'b-', label='sin(x)', linewidth=2)
        plt.plot(x, y2, 'r-', label='cos(x)', linewidth=2)
        plt.fill_between(x, y1, y2, alpha=0.2)
        
        plt.title('Python测试图表', fontsize=14)
        plt.xlabel('X轴', fontsize=12)
        plt.ylabel('Y轴', fontsize=12)
        plt.legend()
        plt.grid(True, alpha=0.3)
        
        # 转换为base64
        image_base64 = plot_to_base64()
        
        return {
            "success": True,
            "message": "Python测试图表生成成功",
            "image": image_base64,
            "image_info": {
                "width": 800,
                "height": 600,
                "format": "png"
            }
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "traceback": traceback.format_exc()
        }

@app.post("/api/python/plot")
async def create_plot(request: PlotRequest):
    """创建Python图表"""
    try:
        # 读取数据
        df = read_dataset(request.dataset_path)
        
        # 清理之前的图表
        plt.close('all')
        
        # 根据绘图类型创建图表
        plot_type = request.plot_type.lower()
        
        if plot_type == "scatter":
            # 散点图
            plt.figure(figsize=(10, 6))
            
            if 'species' in df.columns:
                # 按种类着色
                colors = {'setosa': 'red', 'versicolor': 'green', 'virginica': 'blue'}
                for species, color in colors.items():
                    subset = df[df['species'] == species]
                    plt.scatter(subset['sepal_length'], subset['sepal_width'], 
                               color=color, label=species, alpha=0.6, s=80)
                plt.legend(title='种类')
                plt.xlabel('萼片长度 (cm)')
                plt.ylabel('萼片宽度 (cm)')
            else:
                # 使用前两列
                cols = df.select_dtypes(include=[np.number]).columns
                if len(cols) >= 2:
                    plt.scatter(df[cols[0]], df[cols[1]], alpha=0.6, s=80)
                    plt.xlabel(cols[0])
                    plt.ylabel(cols[1])
                else:
                    plt.scatter(range(len(df)), df.iloc[:, 0], alpha=0.6, s=80)
                    plt.xlabel('索引')
                    plt.ylabel(df.columns[0])
            
            plt.title('Python Matplotlib - 散点图')
            plt.grid(True, alpha=0.3)
            
        elif plot_type == "line":
            # 折线图
            plt.figure(figsize=(10, 6))
            
            # 如果有数值列，绘制折线
            numeric_cols = df.select_dtypes(include=[np.number]).columns
            if len(numeric_cols) > 0:
                for i, col in enumerate(numeric_cols[:3]):  # 最多绘制3列
                    plt.plot(range(len(df)), df[col], label=col, linewidth=2, 
                            marker='o' if len(df) < 20 else None)
                
                plt.legend()
                plt.title('Python Matplotlib - 折线图')
                plt.xlabel('索引')
                plt.ylabel('值')
                plt.grid(True, alpha=0.3)
            else:
                # 如果没有数值列，创建简单图表
                plt.text(0.5, 0.5, '没有数值数据可绘制', 
                        ha='center', va='center', fontsize=14)
                plt.title('Python - 数据不可用')
            
        elif plot_type == "histogram":
            # 直方图
            plt.figure(figsize=(10, 6))
            
            # 选择第一个数值列
            numeric_cols = df.select_dtypes(include=[np.number]).columns
            if len(numeric_cols) > 0:
                plt.hist(df[numeric_cols[0]].dropna(), bins=20, 
                        color='skyblue', edgecolor='black', alpha=0.7)
                plt.title(f'Python Matplotlib - {numeric_cols[0]} 直方图')
                plt.xlabel(numeric_cols[0])
                plt.ylabel('频率')
                plt.grid(True, alpha=0.3, axis='y')
            else:
                plt.text(0.5, 0.5, '没有数值数据', 
                        ha='center', va='center', fontsize=14)
                plt.title('Python - 数据不可用')
                
        elif plot_type == "boxplot":
            # 箱线图
            plt.figure(figsize=(10, 6))
            
            # 如果有分类列和数值列
            if 'species' in df.columns and 'sepal_length' in df.columns:
                # 按种类分组
                data = [df[df['species'] == sp]['sepal_length'] 
                       for sp in df['species'].unique()]
                plt.boxplot(data, labels=df['species'].unique())
                plt.title('Python Matplotlib - 萼片长度箱线图')
                plt.xlabel('种类')
                plt.ylabel('萼片长度')
                plt.grid(True, alpha=0.3, axis='y')
            else:
                # 绘制所有数值列
                numeric_cols = df.select_dtypes(include=[np.number]).columns
                if len(numeric_cols) > 0:
                    plt.boxplot([df[col] for col in numeric_cols], labels=numeric_cols)
                    plt.title('Python Matplotlib - 数值列箱线图')
                    plt.xlabel('列')
                    plt.ylabel('值')
                    plt.grid(True, alpha=0.3, axis='y')
                    plt.xticks(rotation=45)
                else:
                    plt.text(0.5, 0.5, '没有数值数据', 
                            ha='center', va='center', fontsize=14)
                    plt.title('Python - 数据不可用')
        
        else:
            # 默认散点图
            plt.figure(figsize=(10, 6))
            plt.scatter(range(len(df)), range(len(df)), alpha=0.6)
            plt.title('Python Matplotlib - 默认图表')
            plt.grid(True, alpha=0.3)
        
        # 转换为base64
        image_base64 = plot_to_base64()
        
        # 返回结果
        return {
            "success": True,
            "language": "python",
            "plot_type": plot_type,
            "image": image_base64,
            "image_info": {
                "width": 800,
                "height": 600,
                "format": "png"
            },
            "data_info": {
                "rows": len(df),
                "columns": len(df.columns),
                "shape": df.shape
            }
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "traceback": traceback.format_exc(),
            "language": "python"
        }

@app.post("/api/python/execute")
async def execute_code(request: ExecuteRequest):
    """执行Python代码"""
    try:
        # 读取数据
        df = read_dataset(request.dataset_path)
        
        # 准备执行环境
        local_vars = {
            'df': df,
            'data': df,
            'pd': pd,
            'np': np,
            'plt': plt,
            'io': io,
            'base64': base64,
            'parameters': request.parameters or {}
        }
        
        # 捕获输出
        output_buffer = io.StringIO()
        result = None
        error = None
        
        try:
            import sys
            from contextlib import redirect_stdout, redirect_stderr
            
            with redirect_stdout(output_buffer), redirect_stderr(output_buffer):
                # 执行代码
                exec(request.code, {"__builtins__": __builtins__}, local_vars)
                
                # 检查是否有名为result的变量
                if 'result' in local_vars:
                    result = local_vars['result']
                    
        except Exception as e:
            error = {
                'type': type(e).__name__,
                'message': str(e),
                'traceback': traceback.format_exc()
            }
        
        # 获取输出
        output = output_buffer.getvalue()
        
        # 关闭所有matplotlib图形
        plt.close('all')
        
        # 构建响应
        response = {
            'success': error is None,
            'output': output,
            'error': error
        }
        
        # 处理结果
        if result is not None:
            if isinstance(result, pd.DataFrame):
                response['result'] = {
                    'type': 'dataframe',
                    'columns': result.columns.tolist(),
                    'data': result.head(100).to_dict(orient='records'),
                    'shape': result.shape
                }
            elif isinstance(result, dict):
                response['result'] = result
            elif isinstance(result, (list, str, int, float, bool)):
                response['result'] = result
            elif hasattr(result, 'to_dict'):
                response['result'] = result.to_dict()
        
        return response
        
    except Exception as e:
        return {
            'success': False,
            'output': '',
            'error': {
                'type': 'API Error',
                'message': str(e),
                'traceback': traceback.format_exc()
            }
        }

@app.get("/api/example/python")
async def python_example():
    """Python代码示例"""
    example_code = '''import pandas as pd
import matplotlib.pyplot as plt
import io
import base64

# 加载数据
print("数据形状:", df.shape)
print("列名:", list(df.columns))
print("\\n前5行数据:")
print(df.head())

# 创建散点图
plt.figure(figsize=(10, 6))

if 'species' in df.columns:
    # 按种类着色
    colors = {'setosa': 'red', 'versicolor': 'green', 'virginica': 'blue'}
    for species, color in colors.items():
        subset = df[df['species'] == species]
        plt.scatter(subset['sepal_length'], subset['sepal_width'], 
                   color=color, label=species, alpha=0.6, s=80)
    plt.legend(title='种类')
else:
    plt.scatter(df.iloc[:, 0], df.iloc[:, 1], alpha=0.6, s=80)

plt.title('Python散点图示例')
plt.xlabel('X轴')
plt.ylabel('Y轴')
plt.grid(True, alpha=0.3)

# 转换为base64
buf = io.BytesIO()
plt.savefig(buf, format='png', dpi=100, bbox_inches='tight')
buf.seek(0)
image_base64 = base64.b64encode(buf.getvalue()).decode('utf-8')

# 返回结果
result = {
    'image': image_base64,
    'image_info': {'width': 800, 'height': 600},
    'data_info': {'rows': len(df), 'columns': len(df.columns)}
}'''
    
    return {
        "language": "python",
        "title": "Python绘图示例",
        "description": "使用Matplotlib创建散点图",
        "code": example_code
    }

if __name__ == "__main__":
    print("=" * 60)
    print("AIXLab Python分析服务启动")
    print("=" * 60)
    print("服务端口: 8001")
    print("API文档: http://localhost:8001/docs")
    print("健康检查: http://localhost:8001/health")
    print("测试绘图: http://localhost:8001/test")
    print("=" * 60)
    
    # 确保data目录存在
    os.makedirs("data", exist_ok=True)
    
    # 启动服务
    uvicorn.run("app:app", host="0.0.0.0", port=8001, reload=True)