// 绘图相关 API
import request from '@/utils/request'

/**
 * 生成图表
 * @param {Object} params - 参数
 * @param {string} params.language - 语言 (python/r)
 * @param {string} params.plot_type - 图表类型
 * @returns {Promise}
 */
export const generatePlot = (params) => {
  return request.post('/api/plot', params)
}

/**
 * 测试 Python 图表
 * @returns {Promise}
 */
export const testPythonPlot = () => {
  return request.get('/api/test/python-plot')
}

/**
 * 测试 R 图表
 * @returns {Promise}
 */
export const testRPlot = () => {
  return request.get('/api/test/r-plot')
}