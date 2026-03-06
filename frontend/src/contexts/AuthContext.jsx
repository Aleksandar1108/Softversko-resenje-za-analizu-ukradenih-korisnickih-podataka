import React, { createContext, useContext, useState, useEffect } from 'react'
import { authAPI } from '../services/api'

const AuthContext = createContext(null)

export const useAuth = () => {
  const context = useContext(AuthContext)
  if (!context) {
    throw new Error('useAuth must be used within AuthProvider')
  }
  return context
}

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null)
  const [loading, setLoading] = useState(true)
  const [token, setToken] = useState(localStorage.getItem('token'))

  useEffect(() => {
    const initAuth = async () => {
      const storedToken = localStorage.getItem('token')
      const storedUser = localStorage.getItem('user')

      if (storedToken && storedUser) {
        setToken(storedToken)
        setUser(JSON.parse(storedUser))
        try {
          const response = await authAPI.getCurrentUser()
          setUser(response.data.data)
        } catch (error) {
          console.error('Failed to get current user:', error)
          logout()
        }
      }
      setLoading(false)
    }

    initAuth()
  }, [])

  const login = async (email, password) => {
    try {
      const response = await authAPI.login(email, password)
      const { token: newToken, user: userData } = response.data.data || response.data

      setToken(newToken)
      setUser(userData)
      localStorage.setItem('token', newToken)
      localStorage.setItem('user', JSON.stringify(userData))

      return { success: true }
    } catch (error) {
      return {
        success: false,
        error: error.response?.data?.error?.message || 'Login failed',
      }
    }
  }

  const register = async (userData) => {
    try {
      const response = await authAPI.register(userData)
      const { token: newToken, user: newUser } = response.data.data || response.data

      setToken(newToken)
      setUser(newUser)
      localStorage.setItem('token', newToken)
      localStorage.setItem('user', JSON.stringify(newUser))

      return { success: true }
    } catch (error) {
      return {
        success: false,
        error: error.response?.data?.error?.message || 'Registration failed',
      }
    }
  }

  const logout = () => {
    setToken(null)
    setUser(null)
    localStorage.removeItem('token')
    localStorage.removeItem('user')
  }

  const value = {
    user,
    token,
    loading,
    login,
    register,
    logout,
    isAuthenticated: !!token,
  }

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>
}
