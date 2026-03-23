import { Navigate } from 'react-router-dom'
import { useAuthStore } from '../store/authStore'
import { getToken } from '../api/axios'

interface Props {
  children: React.ReactNode
}

const ProtectedRoute = ({ children }: Props) => {
  const { isAuthenticated } = useAuthStore()
  const token = getToken()

  if (!isAuthenticated || !token) {
    return <Navigate to="/login" replace />
  }

  return <>{children}</>
}

export default ProtectedRoute