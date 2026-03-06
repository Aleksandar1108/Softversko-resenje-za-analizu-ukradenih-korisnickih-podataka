import React, { useState, useEffect } from 'react'
import {
  Box,
  Container,
  Typography,
  Card,
  CardContent,
  TextField,
  Button,
  Grid,
  Alert,
  CircularProgress,
  Divider,
} from '@mui/material'
import { Save as SaveIcon } from '@mui/icons-material'
import { useAuth } from '../../contexts/AuthContext'
import { authAPI } from '../../services/api'

const Profile = () => {
  const { user, logout } = useAuth()
  const [loading, setLoading] = useState(false)
  const [success, setSuccess] = useState(false)
  const [error, setError] = useState(null)
  const [formData, setFormData] = useState({
    first_name: '',
    last_name: '',
    email: '',
  })

  useEffect(() => {
    if (user) {
      setFormData({
        first_name: user.first_name || '',
        last_name: user.last_name || '',
        email: user.email || '',
      })
    }
  }, [user])

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    })
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    setLoading(true)
    setError(null)
    setSuccess(false)

    try {
      // Update user profile
      // Note: This endpoint might need to be implemented in backend
      await authAPI.getCurrentUser() // Placeholder
      setSuccess(true)
    } catch (err) {
      setError(err.response?.data?.error?.message || 'Greška pri ažuriranju profila')
    } finally {
      setLoading(false)
    }
  }

  if (!user) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" minHeight="400px">
        <CircularProgress />
      </Box>
    )
  }

  return (
    <Container maxWidth="md">
      <Box sx={{ my: 4 }}>
        <Typography variant="h4" component="h1" gutterBottom>
          Profil Korisnika
        </Typography>

        <Card sx={{ mb: 3 }}>
          <CardContent>
            <Typography variant="h6" gutterBottom>
              Lični Podaci
            </Typography>
            <Divider sx={{ my: 2 }} />
            <form onSubmit={handleSubmit}>
              <Grid container spacing={2}>
                <Grid item xs={12} sm={6}>
                  <TextField
                    fullWidth
                    label="Ime"
                    name="first_name"
                    value={formData.first_name}
                    onChange={handleChange}
                  />
                </Grid>
                <Grid item xs={12} sm={6}>
                  <TextField
                    fullWidth
                    label="Prezime"
                    name="last_name"
                    value={formData.last_name}
                    onChange={handleChange}
                  />
                </Grid>
                <Grid item xs={12}>
                  <TextField
                    fullWidth
                    label="Email"
                    name="email"
                    type="email"
                    value={formData.email}
                    onChange={handleChange}
                    disabled
                  />
                </Grid>
                <Grid item xs={12}>
                  <Button
                    type="submit"
                    variant="contained"
                    startIcon={loading ? <CircularProgress size={20} /> : <SaveIcon />}
                    disabled={loading}
                  >
                    {loading ? 'Čuvam...' : 'Sačuvaj Promene'}
                  </Button>
                </Grid>
              </Grid>
            </form>

            {success && (
              <Alert severity="success" sx={{ mt: 2 }}>
                Profil je uspešno ažuriran!
              </Alert>
            )}

            {error && (
              <Alert severity="error" sx={{ mt: 2 }}>
                {error}
              </Alert>
            )}
          </CardContent>
        </Card>

        <Card>
          <CardContent>
            <Typography variant="h6" gutterBottom>
              Informacije o Nalogu
            </Typography>
            <Divider sx={{ my: 2 }} />
            <Grid container spacing={2}>
              <Grid item xs={12} sm={6}>
                <Typography variant="body2" color="text.secondary">
                  Status
                </Typography>
                <Typography variant="body1">
                  {user.is_active ? 'Aktivan' : 'Neaktivan'}
                </Typography>
              </Grid>
              <Grid item xs={12} sm={6}>
                <Typography variant="body2" color="text.secondary">
                  Email Verifikovan
                </Typography>
                <Typography variant="body1">
                  {user.email_verified ? 'Da' : 'Ne'}
                </Typography>
              </Grid>
              <Grid item xs={12} sm={6}>
                <Typography variant="body2" color="text.secondary">
                  Datum Registracije
                </Typography>
                <Typography variant="body1">
                  {user.created_at
                    ? new Date(user.created_at).toLocaleDateString()
                    : 'N/A'}
                </Typography>
              </Grid>
              {user.last_login && (
                <Grid item xs={12} sm={6}>
                  <Typography variant="body2" color="text.secondary">
                    Poslednja Prijava
                  </Typography>
                  <Typography variant="body1">
                    {new Date(user.last_login).toLocaleString()}
                  </Typography>
                </Grid>
              )}
            </Grid>
          </CardContent>
        </Card>
      </Box>
    </Container>
  )
}

export default Profile
