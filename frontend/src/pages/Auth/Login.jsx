import React, { useState } from 'react'
import { useNavigate, Link } from 'react-router-dom'
import {
  Box,
  Container,
  Card,
  CardContent,
  TextField,
  Button,
  Typography,
  Alert,
  CircularProgress,
} from '@mui/material'
import { Login as LoginIcon } from '@mui/icons-material'
import { useAuth } from '../../contexts/AuthContext'

const Login = () => {
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState(null)
  const [loading, setLoading] = useState(false)
  const { login } = useAuth()
  const navigate = useNavigate()

  const handleSubmit = async (e) => {
    e.preventDefault()
    setError(null)
    setLoading(true)

    const result = await login(email, password)

    if (result.success) {
      navigate('/')
    } else {
      setError(result.error)
    }

    setLoading(false)
  }

  return (
    <Container component="main" maxWidth="xs">
      <Box
        sx={{
          marginTop: 8,
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
        }}
      >
        <Card sx={{ width: '100%' }}>
          <CardContent>
            <Box sx={{ display: 'flex', flexDirection: 'column', alignItems: 'center', mb: 2 }}>
              <LoginIcon sx={{ fontSize: 40, color: 'primary.main', mb: 1 }} />
              <Typography component="h1" variant="h5">
                Prijava
              </Typography>
            </Box>

            {error && (
              <Alert severity="error" sx={{ mb: 2 }}>
                {error}
              </Alert>
            )}

            <Box component="form" onSubmit={handleSubmit} sx={{ mt: 1 }}>
              <TextField
                margin="normal"
                required
                fullWidth
                id="email"
                label="Email adresa"
                name="email"
                autoComplete="email"
                autoFocus
                value={email}
                onChange={(e) => setEmail(e.target.value)}
              />
              <TextField
                margin="normal"
                required
                fullWidth
                name="password"
                label="Lozinka"
                type="password"
                id="password"
                autoComplete="current-password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
              />
              <Button
                type="submit"
                fullWidth
                variant="contained"
                sx={{ mt: 3, mb: 2 }}
                disabled={loading}
                startIcon={loading ? <CircularProgress size={20} /> : <LoginIcon />}
              >
                {loading ? 'Prijavljivanje...' : 'Prijavi se'}
              </Button>
              <Box sx={{ textAlign: 'center' }}>
                <Link to="/register" style={{ textDecoration: 'none' }}>
                  <Typography variant="body2" color="primary">
                    Nemate nalog? Registrujte se
                  </Typography>
                </Link>
              </Box>
            </Box>
          </CardContent>
        </Card>
      </Box>
    </Container>
  )
}

export default Login
