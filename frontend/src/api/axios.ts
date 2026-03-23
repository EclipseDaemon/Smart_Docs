import axios from 'axios'
import Cookies from 'js-cookie'

const TOKEN_KEY = 'smartdocs_token'

const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL,
  headers: {
    'Content-Type': 'application/json'
  },
  withCredentials: true
})


api.interceptors.request.use(
  (config) => {
    const token = Cookies.get(TOKEN_KEY)
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => Promise.reject(error)
)


api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      Cookies.remove(TOKEN_KEY)
      window.location.href = '/login'
    }
    return Promise.reject(error)
  }
)

export const setToken = (token: string) => {
  Cookies.set(TOKEN_KEY, token, {
    expires: 1,
    secure: window.location.protocol === 'https:',
    sameSite: 'strict'
  })
}

export const removeToken = () => {
  Cookies.remove(TOKEN_KEY)
}

export const getToken = () => Cookies.get(TOKEN_KEY)

export default api