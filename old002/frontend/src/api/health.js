// 健康检查 API
import request from '@/utils/request'

/**
 * 检查服务健康状态
 * @returns {Promise}
 */
export const checkHealth = () => {
  return request.get('/api/health')
}