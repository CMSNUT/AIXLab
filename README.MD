# 项目规划
- 前后端分离
- 前端：vue3 + vite + element-plus + pinia + router
- 后端: FastAPI + plumber + MySQL

## 项目需求
- 后端数据管理的前端界面
- 后端分为：主服务 fastapi + 子服务 fastapi + plumber

## 项目结构
```text
AIXLAB\
|
```

# 主后端（FastAPI主后端）依赖

## Web框架和服务器
- fastapi[all]
- uvicorn[standard]

## 数据库连接和ORM
- sqlalchemy
- aiomysql 用于异步MySQL
- databases（SQLAlchemy的异步支持）

## 认证和安全性
- passlib[bcrypt]
- python-jose[cryptography]（用于JWT令牌）
- python-multipart （用于表单数据，包括文件上传）
- email-validator（用于验证邮箱格式）

## 配置和环境变量
- pydantic（FastAPI已经依赖）
- python-dotenv

## 异步任务和消息队列
- celery（如果需要分布式任务队列）
- redis（作为celery的broker）

## 安装
```bash
conda activate py314_fastapi
pip install "fastapi[all]" "uvicorn[standard]" sqlalchemy aiomysql passlib[bcrypt] python-jose[cryptography] python-multipart email-validator tzdata celery redis databases loguru

conda env export -n py314_aix > G:\\AIXLAB\\backend\\env_exports\\py314_fastapi_env.yaml
pip freeze > G:\\AIXLAB\\backend\\main_backend\\requirements.txt
conda deactivate
```

# 子服务端：py314_service
## 功能包
# Python科学计算相关功能包分类汇总

## 📊 数据处理
| 包的名称及官方/核心链接 | 功能简介 |
|---|---|
| [pandas](https://pandas.pydata.org/) | Python数据处理核心包，支持表格数据清洗、筛选、聚合，兼容多格式数据导入导出。 |
| [NumPy](https://numpy.org/) | 数值计算基础库，提供高性能多维数组和矩阵运算，是科学计算包的底层依赖。 |
| [SciPy](https://www.scipy.org/) | 基于NumPy的科学计算库，包含线性代数、积分、优化等模块，解决工程/科学计算问题。 |
| [Polars](https://pola.rs/) | 高性能DataFrame库，适合大数据处理 |
| [Dask](https://www.dask.org/) | 并行计算框架，支持大规模数据分析 |
| [Vaex](https://vaex.io/) | 用于懒加载、内存高效的大数据集处理 |

## 📈 图形绘制
| 包的名称及官方/核心链接 | 功能简介 |
|---|---|
| [Matplotlib](https://matplotlib.org/) | Python绘图基础库，支持静态/动态图表绘制，可自定义样式，是可视化核心。 |
| [Seaborn](https://seaborn.pydata.org/) | 基于Matplotlib的统计可视化库，内置美观样式，专注统计图表绘制。 |
| [Plotly](https://plotly.com/python/) | 交互式可视化库，支持可交互图表，适合网页展示和动态分析。 |
| [Bokeh](https://bokeh.org/) | 交互式可视化库，适合Web应用 |
| [Altair](https://altair-viz.github.io/) | 声明式统计可视化库，基于Vega-Lite |

## 🤖 机器学习（传统+通用深度学习）
### 模型构建
| 包的名称及官方/核心链接 | 功能简介 |
|---|---|
| [scikit-learn](https://scikit-learn.org/stable/) | 经典机器学习包，封装分类、回归、聚类、降维等算法，API简洁，适合入门和传统任务。 |
| [XGBoost](https://xgboost.readthedocs.io/) | 高性能梯度提升树库，对结构化数据效果优异，常用于数据竞赛和工业建模。 |
| [LightGBM](https://lightgbm.readthedocs.io/en/stable/) | 轻量级梯度提升树库，训练速度更快、内存占用更低，对小样本和类别特征友好。 |
| [CatBoost](https://catboost.ai/) | 自动处理类别特征的梯度提升树库，减少特征预处理成本，抗过拟合能力强。 |
| [PyTorch](https://pytorch.org/) | 灵活的深度学习框架，动态计算图，支持GPU加速，适配科研场景的模型开发。 |
| [TensorFlow/Keras](https://www.tensorflow.org/) | TensorFlow是谷歌深度学习框架，Keras是其高层API，简化神经网络构建，适合生产部署。 |
| [PyTorch Lightning](https://www.pytorchlightning.ai/) | 封装PyTorch，简化训练循环、分布式训练等流程，专注模型研发而非工程代码。 |
| [Hugging Face Transformers](https://huggingface.co/docs/transformers/index) | 预训练模型库，包含BERT/Transformer等，支持NLP/分子序列/分子图等多场景迁移学习。 |

### 堆叠/集成学习
| 包的名称及官方/核心链接 | 功能简介 |
|---|---|
| [scikit-learn Stacking](https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.StackingClassifier.html) | scikit-learn内置的堆叠分类器和回归器，支持多层级堆叠和交叉验证 |
| [ML-Ensemble](http://ml-ensemble.com/) | 专门用于大规模集成学习的库，支持并行计算和内存优化 |
| [StackNet](https://github.com/kaz-Anova/StackNet) | 竞赛选手开发的堆叠框架，支持深度学习与浅层模型堆叠 |
| [VecStack](https://github.com/vecxoz/vecstack) | 轻量级堆叠库，支持自定义基学习器和元学习器 |
| [H2O AutoML](http://docs.h2o.ai/h2o/latest-stable/h2o-docs/automl.html) | 自动机器学习框架，内置堆叠集成，支持大规模数据 |

### 特征选择
| 包的名称及官方/核心链接 | 功能简介 |
|---|---|
| [scikit-learn feature_selection](https://scikit-learn.org/stable/modules/classes.html#module-sklearn.feature_selection) | scikit-learn特征选择模块，包含过滤法、包裹法、嵌入法 |
| [Feature-engine](https://feature-engine.readthedocs.io/) | 专门的特征工程库，提供多种特征选择方法 |
| [Boruta](https://github.com/scikit-learn-contrib/boruta_py) | 基于随机森林的特征选择算法，识别所有相关特征 |
| [MRMR](https://github.com/smazzanti/mrmr) | 最大相关最小冗余特征选择算法，兼顾相关性和冗余度 |
| [TPOT](https://epistasislab.github.io/tpot/) | 基于遗传编程的自动机器学习，包含特征选择 |
| [RFECV](https://scikit-learn.org/stable/modules/generated/sklearn.feature_selection.RFECV.html) | 递归特征消除交叉验证，自动选择最优特征数 |

### 模型验证
| 包的名称及官方/核心链接 | 功能简介 |
|---|---|
| [scikit-learn model_selection](https://scikit-learn.org/stable/modules/classes.html#module-sklearn.model_selection) | scikit-learn模型选择模块，包含交叉验证、超参数调优 |
| [scikit-optimize](https://scikit-optimize.github.io/) | 贝叶斯优化库，用于超参数调优 |
| [Optuna](https://optuna.org/) | 自动超参数优化框架，支持剪枝、并行优化 |
| [Hyperopt](http://hyperopt.github.io/hyperopt/) | 分布式异步超参数优化库 |
| [TensorBoard](https://www.tensorflow.org/tensorboard) | TensorFlow可视化工具，用于模型训练监控 |
| [Weights & Biases](https://wandb.ai/site) | 机器学习实验跟踪平台，支持超参数调优 |
| [MLflow](https://mlflow.org/) | 机器学习生命周期管理平台，包含模型验证 |

### 模型解释
| 包的名称及官方/核心链接 | 功能简介 |
|---|---|
| [SHAP](https://shap.readthedocs.io/) | 基于SHAP值的模型可解释性工具，量化特征对预测结果的贡献。 |
| [LIME](https://lime-ml.readthedocs.io/) | 局部可解释性模型工具，解释单个预测结果的决策逻辑。 |
| [Eli5](https://eli5.readthedocs.io/) | 机器学习模型调试和解释库 |
| [InterpretML](https://interpret.ml/) | 微软开发的模型解释统一框架 |
| [Captum](https://captum.ai/) | PyTorch模型解释库 |

## 🧪 化学计量学
### 基础化学计量学包（已列出）
| 包的名称及官方/核心链接 | 功能简介 |
|---|---|
| [chemometrics](https://pypi.org/project/chemometrics/) | 化学计量学专用包，封装PCA、PLS等多元统计方法，适配化学数据。 |
| [PyChem](http://pychem.sourceforge.net/) | 多元分析化学计量学工具 |
| [mdatools](https://mdatools.readthedocs.io/) | 多元数据分析工具包 |

### 🔬 MCR-ALS（多元曲线分辨-交替最小二乘）
| 包的名称及官方/核心链接 | 功能简介 |
|---|---|
| [pyMCR](https://github.com/CCampJr/PyMCR) | 多元曲线分辨率（MCR）Python实现，支持ALS、NMF等多种算法 |
| [MCRpy](https://github.com/NEFM-TUDresden/MCRpy) | MCR-ALS算法的另一种实现，专注于光谱数据解析 |
| [hyperspy](https://hyperspy.org/) | 电子显微镜数据分析库，包含MCR-ALS等多元分析功能 |
| [Spectra](https://spectra.readthedocs.io/) | 光谱处理库，支持MCR等化学计量学方法 |

### 📊 2DCOS（二维相关光谱）
| 包的名称及官方/核心链接 | 功能简介 |
|---|---|
| [py2Dcos](https://github.com/jianboq/py2Dcos) | 二维相关光谱分析的Python实现 |
| [2Dcos](https://pypi.org/project/2Dcos/) | 二维相关光谱计算和可视化工具 |
| [spectrochempy](https://www.spectrochempy.fr/) | 光谱化学计量学平台，包含2DCOS、MCR-ALS等功能 |

### 🔧 其他相关化学计量学工具
| 包的名称及官方/核心链接 | 功能简介 |
|---|---|
| [scikit-chem](https://github.com/lewisacidic/scikit-chem) | 化学信息学和化学计量学库，扩展scikit-learn |
| [ChemometricsTools](https://github.com/HegemanLab/ChemometricsTools) | 化学计量学工具集，包含PLS-DA、OPLS等 |
| [PyPLS](https://pypi.org/project/PyPLS/) | 偏最小二乘回归的Python实现 |
| [orthogonal-PLS](https://github.com/CEA-CESTA/orthogonal-PLS) | 正交偏最小二乘（OPLS）算法实现 |

### 📊 谱图处理
| 包的名称及官方/核心链接 | 功能简介 |
|---|---|
| [PyMassSpec](https://pymassspec.github.io/) | 质谱数据处理专用库，支持峰检测、谱图比对、格式转换等。 |
| [NMRglue](https://nmrglue.readthedocs.io/) | 核磁共振谱图处理工具，支持数据读取、基线校正、峰拟合。 |
| [SpectraPy](https://spectrapy.readthedocs.io/) | 通用光谱处理库，支持红外/拉曼/紫外-可见光谱数据预处理。 |
| [Spectra](https://spectra.readthedocs.io/) | 光谱数据处理和分析 |
| [lmfit](https://lmfit.github.io/lmfit-py/) | 非线性最小二乘拟合，用于谱图分析 |
| [PySpectra](https://github.com/fujiisoup/pyspectra) | 光谱分析工具|

## 🧬 生信分析
| 包的名称及官方/核心链接 | 功能简介 |
|---|---|
| [Biopython](https://biopython.org/) | 生物信息学基础库，支持DNA/蛋白质序列处理、进化树构建等。 |
| [scikit-bio](http://scikit-bio.org/) | 生物信息学统计分析库 |
| [PyRanges](https://github.com/biocore-ntnu/pyranges) | 基因组区间处理库 |
| [PyVCF](https://pyvcf.readthedocs.io/) | VCF文件解析和操作 |

## 💊 分子设计
| 包的名称及官方/核心链接 | 功能简介 |
|---|---|
| [RDKit](https://www.rdkit.org/) | cheminformatics核心包，支持分子结构解析、绘制、性质预测等。 |
| [DeepChem](https://deepchem.io/) | 化学/生物领域深度学习库，封装分子性质预测、药物发现等基础模型。 |
| [Open Babel](https://openbabel.org/) | 化学数据格式转换和计算工具 |
| [PyMOL](https://pymol.org/) | 分子可视化系统，Python API可用 |
| [MDAnalysis](https://www.mdanalysis.org/) | 分子动力学轨迹分析工具 |
| [AutoDock Vina](https://vina.scripps.edu/) | 分子对接核心工具，Python接口支持小分子-靶蛋白对接，评估结合亲和力。 |
| [ChemBL_webresource_client](https://github.com/chembl/ChemBL_webresource_client) | 对接ChemBL数据库，获取药物分子活性、靶点信息，辅助药物候选分子筛选。 |
| [MolFormer](https://github.com/facebookresearch/MolFormer) | 开源分子预训练模型，支持药物分子性质预测、生成，适配深度学习驱动的药物设计。 |
| [DeepChem](https://deepchem.io/) | 深度学习药物发现平台 |
| [MoleculeNet](https://moleculenet.org/) | 分子机器学习基准数据集 |
| [TorchDrug](https://torchdrug.ai/) | 基于PyTorch的药物发现深度学习库，封装分子生成、对接、性质预测等专用模型。 |
| [ChemBERTa](https://huggingface.co/seyonec/ChemBERTa-zinc-base-v1) | 基于BERT的分子SMILES序列预训练模型，适配分子性质预测、生成任务。 |
| [DGL-LifeSci](https://lifesci.dgl.ai/) | 深度图库（DGL）的生命科学分支，专注分子图神经网络（GNN），支持分子图建模。 |
| [Chemprop](https://github.com/chemprop/chemprop) | 基于PyTorch的分子性质预测库，专为小分子性质（活性、溶解度）预测优化。 |
| [Equiformer](https://github.com/atomicarchitects/equiformer-pytorch) | 3D分子结构的等变Transformer模型，精准建模分子空间结构与性质的关系。 |
| [GeoMol](https://github.com/jensengroup/geomol) | 3D分子生成模型，支持从2D SMILES生成合理的3D分子构象，适配药物分子设计。 |
| [PyTorch Geometric](https://pytorch-geometric.readthedocs.io/) | 图神经网络库，用于分子表示 |
| [TensorFlow Quantum](https://www.tensorflow.org/quantum) | 量子机器学习库，可用于分子模拟 |

## 🏗️ 材料设计
| 包的名称及官方/核心链接 | 功能简介 |
|---|---|
| [pymatgen](https://pymatgen.org/) | 材料基因组学核心包，支持晶体结构解析、相图计算、DFT接口等。 |
| [ASE](https://wiki.fysik.dtu.dk/ase/) | 原子模拟环境，支持分子动力学、量子化学计算、晶体结构优化。 |
| [FireWorks](https://materialsproject.github.io/fireworks/) | 高通量计算工作流管理 |
| [Matminer](https://hackingmaterials.lbl.gov/matminer/) | 材料信息学数据挖掘工具 |
| [SchNetPack](https://schnetpack.readthedocs.io/) | 基于PyTorch的深度学习包，专注材料分子性质预测（能量、弹性模量等）。 |
| [AtomicSimulator](https://github.com/AtomicSimulator/AtomicSimulator) | 轻量级原子模拟包，支持材料分子结构优化、分子动力学模拟，适配小分子材料设计。 |
| [PyXAID](https://github.com/CMS-KULeuven/PyXAID) | 材料分子激发态计算工具，支持光化学/光物理性质模拟，适配光电材料分子设计。 |
| [MatDeepLearn](https://github.com/ulissigroup/matdeeplearn) | 材料深度学习工具 |
| [Amp](https://amp.readthedocs.io/) | 原子机器学习势函数 |
| [DeePMD-kit](https://github.com/deepmodeling/deepmd-kit) | 深度分子动力学软件包 |

## 📝 科学论文写作
| 包的名称及官方/核心链接 | 功能简介 |
|---|---|
| [papermill](https://papermill.readthedocs.io/) | 批量执行Jupyter Notebook，整合代码/结果到论文草稿，实现可复现的论文写作。 |
| [pylatex](https://jelmerro.github.io/PyLaTeX/) | Python生成LaTeX代码，自动化构建论文结构（摘要/图表/参考文献），适配LaTeX撰写。 |
| [pandoc](https://pandoc.org/) | 格式转换工具（Python可调用），支持Markdown/LaTeX/Word/PDF互转，适配论文多格式输出。 |
| [Jupyter](https://jupyter.org/) | 交互式笔记本，支持代码、文本和可视化 |
| [Manim](https://www.manim.community/) | 数学动画引擎，创建解释性视频 |
| [Graphviz](https://graphviz.org/) | 流程图核心工具，Python接口（pydot/graphviz）支持绘制结构化流程图、算法框图，符合学术规范。 |
| [Mermaid](https://mermaid.js.org/) | 文本式绘图工具（Python可调用），用简单语法绘制流程图/时序图，可嵌入Jupyter/LaTeX，轻量化易维护。 |
| [drawSvg](https://drawsvg.readthedocs.io/) | 纯Python绘制SVG矢量图，精准控制图形元素，适合绘制自定义科学示意图（分子结构/实验装置）。 |
| [Inkscape](https://inkscape.org/)（Python接口：inkex） | 矢量图编辑工具，Python接口支持高精度科学示意图绘制，导出高分辨率PDF适配论文。 |
| [Diagrams](https://diagrams.mingrammer.com/) | 用Python代码绘制云系统架构图 |
| [NetworkX](https://networkx.org/) | 复杂网络分析、设计和可视化 |


---

## 安装
```bash
conda activate py314_aix

# 数据处理
pip install numpy pandas polars dask

# 图形绘制
pip install matplotlib seaborn plotly bokeh "altair[all]"

# 机器学习与深度学习
pip install scikit-learn xgboost-cpu 
# catboost ipywidgets
pip3 install torch torchvision
pip install transformers 

pip install optunahub cmaes

## 特征选择
pip install mrmr_selection Boruta

## 堆叠集成
pip install mlens vecstack

# 模型解释
pip install shap lime eli5 captum interpret


conda env export -n py314_aix > G:\\AIXLAB\\backend\\env_exports\\py314_aix_env.yaml
pip freeze > G:\\AIXLAB\\backend\\python_services\\py314_service\\requirements.txt
conda deactivate
```



