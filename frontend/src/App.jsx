import React from 'react'
import { Routes, Route, Navigate } from 'react-router-dom'
import { AuthProvider } from './contexts/AuthContext'
import Layout from './components/Layout/Layout'
import Home from './pages/Home/Home'
import EmailCheck from './pages/EmailCheck/EmailCheck'
import Dashboard from './pages/Dashboard/Dashboard'
import PasswordAnalysis from './pages/PasswordAnalysis/PasswordAnalysis'
import Recommendations from './pages/Recommendations/Recommendations'
import Profile from './pages/Profile/Profile'
import Notifications from './pages/Notifications/Notifications'
import Login from './pages/Auth/Login'
import Register from './pages/Auth/Register'
import ProtectedRoute from './components/ProtectedRoute/ProtectedRoute'

function App() {
  return (
    <AuthProvider>
      <Routes>
        {/* Javne rute - ne zahtevaju autentifikaciju */}
        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<Register />} />
        <Route
          path="/"
          element={<Layout />}
        >
          {/* Javne stranice - anonimna provera */}
          <Route index element={<Home />} />
          <Route path="email-check" element={<EmailCheck />} />
          
          {/* Zaštićene stranice - zahtevaju autentifikaciju */}
          <Route
            path="dashboard"
            element={
              <ProtectedRoute>
                <Dashboard />
              </ProtectedRoute>
            }
          />
          <Route
            path="password-analysis"
            element={
              <ProtectedRoute>
                <PasswordAnalysis />
              </ProtectedRoute>
            }
          />
          <Route
            path="recommendations"
            element={
              <ProtectedRoute>
                <Recommendations />
              </ProtectedRoute>
            }
          />
          <Route
            path="profile"
            element={
              <ProtectedRoute>
                <Profile />
              </ProtectedRoute>
            }
          />
          <Route
            path="notifications"
            element={
              <ProtectedRoute>
                <Notifications />
              </ProtectedRoute>
            }
          />
        </Route>
        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </AuthProvider>
  )
}

export default App
