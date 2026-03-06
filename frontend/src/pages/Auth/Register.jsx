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
  Grid,
} from '@mui/material'
import { PersonAdd as PersonAddIcon } from '@mui/icons-material'
import { useAuth } from '../../contexts/AuthContext'

const Register = () => {
  const [formData, setFormData] = useState({
    email: '',
    password: '',
    confirmPassword: '',
    first_name: '',
    last_name: '',
  })
  const [error, setError] = useState(null)
  const [loading, setLoading] = useState(false)
  const { register } = useAuth()
  const navigate = useNavigate()

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    })
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    setError(null)

    if (formData.password !== formData.confirmPassword) {
      setError('Lozinke se ne poklapaju')
      return
    }

    if (formData.password.length < 8) {
      setError('Lozinka mora imati najmanje 8 karaktera')
      return
    }

    setLoading(true)

    const { confirmPassword, ...registerData } = formData
    const result = await register(registerData)

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
              <PersonAddIcon sx={{ fontSize: 40, color: 'primary.main', mb: 1 }} />
              <Typography component="h1" variant="h5">
                Registracija
              </Typography>
            </Box>

            {error && (
              <Alert severity="error" sx={{ mb: 2 }}>
                {error}
              </Alert>
            )}

            <Box component="form" onSubmit={handleSubmit} sx={{ mt: 1 }}>
              <Grid container spacing={2}>
                <Grid item xs={12} sm={6}>
                  <TextField
                    autoComplete="given-name"
                    name="first_name"
                    required
                    fullWidth
                    id="first_name"
                    label="Ime"
                    autoFocus
                    value={formData.first_name}
                    onChange={handleChange}
                  />
                </Grid>
                <Grid item xs={12} sm={6}>
                  <TextField
                    required
                    fullWidth
                    id="last_name"
                    label="Prezime"
                    name="last_name"
                    autoComplete="family-name"
                    value={formData.last_name}
                    onChange={handleChange}
                  />
                </Grid>
                <Grid item xs={12}>
                  <TextField
                    required
                    fullWidth
                    id="email"
                    label="Email adresa"
                    name="email"
                    autoComplete="email"
                    type="email"
                    value={formData.email}
                    onChange={handleChange}
                  />
                </Grid>
                <Grid item xs={12}>
                  <TextField
                    required
                    fullWidth
                    name="password"
                    label="Lozinka"
                    type="password"
                    id="password"
                    autoComplete="new-password"
                    value={formData.password}
                    onChange={handleChange}
                  />
                </Grid>
                <Grid item xs={12}>
                  <TextField
                    required
                    fullWidth
                    name="confirmPassword"
                    label="Potvrdi lozinku"
                    type="password"
                    id="confirmPassword"
                    value={formData.confirmPassword}
                    onChange={handleChange}
                  />
                </Grid>
              </Grid>
              <Button
                type="submit"
                fullWidth
                variant="contained"
                sx={{ mt: 3, mb: 2 }}
                disabled={loading}
                startIcon={loading ? <CircularProgress size={20} /> : <PersonAddIcon />}
              >
                {loading ? 'Registracija...' : 'Registruj se'}
              </Button>
              <Box sx={{ textAlign: 'center' }}>
                <Link to="/login" style={{ textDecoration: 'none' }}>
                  <Typography variant="body2" color="primary">
                    Već imate nalog? Prijavite se
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

export default Register
