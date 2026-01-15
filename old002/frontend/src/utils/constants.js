// 绘图类型常量
export const PLOT_TYPES = [
  { value: 'scatter', label: '散点图', icon: 'ScatterPlot' },
  { value: 'line', label: '折线图', icon: 'TrendCharts' },
  { value: 'histogram', label: '直方图', icon: 'Histogram' },
  { value: 'boxplot', label: '箱线图', icon: 'BoxPlot' }
]

// 绘图类型名称映射
export const PLOT_TYPE_NAMES = {
  scatter: '散点图',
  line: '折线图',
  histogram: '直方图',
  boxplot: '箱线图'
}

// 服务状态类型
export const SERVICE_STATUS = {
  HEALTHY: 'healthy',
  UNREACHABLE: 'unreachable',
  ERROR: 'error'
}

// 语言类型
export const LANGUAGE_TYPE = {
  PYTHON: 'python',
  R: 'r'
}

// API 端点
export const API_ENDPOINTS = {
  HEALTH: '/api/health',
  PLOT: '/api/plot',
  TEST_PYTHON: '/api/test/python-plot',
  TEST_R: '/api/test/r-plot'
}

// 默认配置
export const DEFAULT_CONFIG = {
  AUTO_CHECK_INTERVAL: 30000, // 30秒
  MAX_HISTORY_ITEMS: 50,
  PLOT_IMAGE_MAX_HEIGHT: 450
}