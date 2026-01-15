import request from '@/utils/request'
import type {
  LoginRequest,
  RegisterRequest,
  User,
  ApiResponse
} from '@/types/auth'

export const authApi = {
  login(data: LoginRequest): Promise<ApiResponse<{ token: string; user: User }>> {
    return request.post('/auth/login', data)
  },

  register(data: RegisterRequest): Promise<ApiResponse<void>> {
    return request.post('/auth/register', data)
  },

  getProfile(): Promise<ApiResponse<User>> {
    return request.get('/auth/profile')
  },

  logout(): Promise<ApiResponse<void>> {
    return request.post('/auth/logout')
  }
}