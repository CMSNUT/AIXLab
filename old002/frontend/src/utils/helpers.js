/**
 * 格式化服务状态显示文本
 * @param {string} status - 状态值
 * @returns {string}
 */
export const formatServiceStatus = (status) => {
  const statusMap = {
    healthy: '正常',
    unreachable: '未启动',
    error: '异常'
  }
  return statusMap[status] || '未知'
}

/**
 * 获取服务状态对应的 Tag 类型
 * @param {string} status - 状态值
 * @returns {string}
 */
export const getServiceStatusType = (status) => {
  const typeMap = {
    healthy: 'success',
    unreachable: 'warning',
    error: 'danger'
  }
  return typeMap[status] || 'info'
}

/**
 * 获取语言对应的 Tag 类型
 * @param {string} language - 语言
 * @returns {string}
 */
export const getLanguageTagType = (language) => {
  return language === 'python' ? 'primary' : 'success'
}

/**
 * 格式化时间
 * @param {Date|string} date - 日期
 * @returns {string}
 */
export const formatTime = (date) => {
  if (!date) return ''
  const d = new Date(date)
  return d.toLocaleString('zh-CN')
}