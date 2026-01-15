import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import type { User, LoginRequest, RegisterRequest } from '@/types/auth'
import { authApi } from '@/api/auth'
import Cookies from 'js-cookie'

export const useAuthStore = defineStore('auth', () => {
  const user = ref<User | null>(null)
  const token = ref<string | null>(Cookies.get('token') || null)

  const isAuthenticated = computed(() => !!token.value)

  const login = async (credentials: LoginRequest) => {
    try {
      const response = await authApi.login(credentials)
      token.value = response.data.token
      user.value = response.data.user
      Cookies.set('token', token.value, { expires: 7 })
      return response
    } catch (error) {
      throw error
    }
  }

  const register = async (data: RegisterRequest) => {
    try {
      const response = await authApi.register(data)
      return response
    } catch (error) {
      throw error
    }
  }

  const logout = () => {
    token.value = null
    user.value = null
    Cookies.remove('token')
  }

  const fetchUser = async () => {
    if (!token.value) return
    try {
      const response = await authApi.getProfile()
      user.value = response.data
    } catch (error) {
      logout()
    }
  }

  return {
    user,
    token,
    isAuthenticated,
    login,
    register,
    logout,
    fetchUser
  }
})