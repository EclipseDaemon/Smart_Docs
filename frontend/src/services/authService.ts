import api, { setToken, removeToken } from '../api/axios'
import { useAuthStore } from '../store/authStore'
import type  { LoginCredentials, RegisterCredentials, TokenResponse, User } from '../types'

export const authService = {
  async register(credentials: RegisterCredentials): Promise<User> {
    const response = await api.post<User>('/auth/register', credentials)
    return response.data
  },

  async login(credentials: LoginCredentials): Promise<void> {
    const formData = new FormData()
    formData.append('username', credentials.email)
    formData.append('password', credentials.password)

    const response = await api.post<TokenResponse>('/auth/login', formData, {
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' }
    })

    setToken(response.data.access_token)

    const userResponse = await api.get<User>('/auth/me')
    useAuthStore.getState().setUser(userResponse.data)
  },

  async logout(): Promise<void> {
    removeToken()
    useAuthStore.getState().clearUser()
    window.location.href = '/login'
  },

  async getMe(): Promise<User> {
    const response = await api.get<User>('/auth/me')
    return response.data
  }
}