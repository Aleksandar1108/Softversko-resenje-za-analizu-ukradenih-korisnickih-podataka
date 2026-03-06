import React, { useState } from 'react'
import {
  Box,
  Container,
  Typography,
  Grid,
  Card,
  CardContent,
  Button,
  Alert,
  TextField,
  CircularProgress,
  Chip,
  Link,
} from '@mui/material'
import {
  Email as EmailIcon,
  Dashboard as DashboardIcon,
  Lock as LockIcon,
  Security as SecurityIcon,
  CheckCircle as CheckCircleIcon,
  Warning as WarningIcon,
} from '@mui/icons-material'
import { useNavigate } from 'react-router-dom'
import { emailCheckAPI } from '../../services/api'
import { useAuth } from '../../contexts/AuthContext'

const Home = () => {
  const navigate = useNavigate()
  const { user } = useAuth()
  const [email, setEmail] = useState('')
  const [loading, setLoading] = useState(false)
  const [checkResult, setCheckResult] = useState(null)
  const [error, setError] = useState(null)

  const handleEmailCheck = async () => {
    if (!email) {
      setError('Molimo unesite email adresu')
      return
    }

    setLoading(true)
    setError(null)
    setCheckResult(null)

    try {
      const response = await emailCheckAPI.checkEmail(email)
      setCheckResult(response.data.data)
    } catch (err) {
      setError(err.response?.data?.error?.message || 'Greška pri proveri email-a')
    } finally {
      setLoading(false)
    }
  }

  const quickActions = [
    {
      title: 'Provera Email-a',
      description: 'Proverite da li je vaš email kompromitovan u breach-ovima',
      icon: <EmailIcon sx={{ fontSize: 40 }} />,
      path: '/email-check',
      color: '#00ff41',
    },
    {
      title: 'Analiza Lozinke',
      description: 'Analizirajte snagu vaše lozinke i dobijte preporuke',
      icon: <LockIcon sx={{ fontSize: 40 }} />,
      path: '/password-analysis',
      color: '#ff0080',
    },
    {
      title: 'Dashboard',
      description: 'Pregled statistika i trendova breach podataka',
      icon: <DashboardIcon sx={{ fontSize: 40 }} />,
      path: '/dashboard',
      color: '#00ffff',
    },
    {
      title: 'Preporuke',
      description: 'Personalizovane preporuke za poboljšanje bezbednosti',
      icon: <SecurityIcon sx={{ fontSize: 40 }} />,
      path: '/recommendations',
      color: '#ffaa00',
    },
  ]

  return (
    <Container maxWidth="lg">
      <Box sx={{ my: 4 }}>
        <Typography 
          variant="h3" 
          component="h1" 
          gutterBottom
          sx={{
            color: '#00ff41',
            textShadow: '0 0 10px #00ff41, 0 0 20px #00ff41, 0 0 30px #00ff41',
            fontFamily: '"Courier New", monospace',
            fontWeight: 700,
          }}
        >
          &gt; DOBRODOSLI_U_BREACH_ANALYZER.exe
        </Typography>
        <Typography 
          variant="h6" 
          paragraph
          sx={{
            color: '#00ffff',
            textShadow: '0 0 8px #00ffff',
            fontFamily: '"Courier New", monospace',
          }}
        >
          [SYSTEM] Analiza kompromitovanih kredencijala i procena rizika
        </Typography>

        <Alert 
          severity="info" 
          sx={{ 
            mb: 4,
            bgcolor: 'rgba(0, 255, 255, 0.1)',
            border: '1px solid #00ffff',
            color: '#00ffff',
            boxShadow: '0 0 20px rgba(0, 255, 255, 0.3)',
          }}
        >
          <Typography variant="body1" gutterBottom sx={{ fontFamily: '"Courier New", monospace' }}>
            <strong>[INFO] Anonimna provera email-a</strong> - Proverite da li je vaš email kompromitovan bez potrebe za registracijom.
          </Typography>
          <Typography variant="body2" sx={{ fontFamily: '"Courier New", monospace' }}>
            [NOTE] Registracija je opciona i omogućava notifikacije, istoriju provera i personalizovane preporuke.
          </Typography>
        </Alert>

        {/* Anonimna Email Provera */}
        <Card sx={{ 
          mb: 4, 
          background: 'linear-gradient(135deg, rgba(0, 255, 65, 0.1) 0%, rgba(0, 255, 255, 0.1) 100%)',
          border: '2px solid #00ff41',
          boxShadow: '0 0 30px rgba(0, 255, 65, 0.5), inset 0 0 30px rgba(0, 255, 65, 0.1)',
        }}>
          <CardContent>
            <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
              <EmailIcon sx={{ fontSize: 40, mr: 2 }} />
              <Box>
                <Typography 
                  variant="h5" 
                  gutterBottom
                  sx={{
                    color: '#00ff41',
                    textShadow: '0 0 10px #00ff41',
                    fontFamily: '"Courier New", monospace',
                    fontWeight: 700,
                  }}
                >
                  &gt; BRZA_PROVERA_EMAIL.exe
                </Typography>
                <Typography 
                  variant="body2"
                  sx={{
                    color: '#00ffff',
                    fontFamily: '"Courier New", monospace',
                  }}
                >
                  [INPUT] Unesite email adresu za proveru kompromitovanosti
                </Typography>
              </Box>
            </Box>

            <Box sx={{ display: 'flex', gap: 2, mb: 2 }}>
              <TextField
                fullWidth
                label="Email adresa"
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                placeholder="example@email.com"
                onKeyPress={(e) => {
                  if (e.key === 'Enter') {
                    handleEmailCheck()
                  }
                }}
                sx={{
                  bgcolor: 'background.paper',
                  '& .MuiOutlinedInput-root': {
                    bgcolor: 'background.paper',
                  },
                }}
              />
              <Button
                variant="contained"
                onClick={handleEmailCheck}
                disabled={loading}
                startIcon={loading ? <CircularProgress size={20} color="inherit" /> : <EmailIcon />}
                sx={{ 
                  minWidth: 150, 
                  bgcolor: '#00ff41',
                  color: '#0a0a0a',
                  fontFamily: '"Courier New", monospace',
                  fontWeight: 700,
                  boxShadow: '0 0 20px #00ff41',
                  '&:hover': {
                    bgcolor: '#00ffff',
                    boxShadow: '0 0 30px #00ffff',
                  },
                }}
              >
                {loading ? 'Proveravam...' : 'Proveri'}
              </Button>
            </Box>

            {error && (
              <Alert severity="error" sx={{ mt: 2 }}>
                {error}
              </Alert>
            )}

            {checkResult && (
              <Box sx={{ mt: 3, bgcolor: 'background.paper', p: 2, borderRadius: 1 }}>
                <Typography variant="h6" gutterBottom color="text.primary">
                  Rezultati provere za: {checkResult.email}
                </Typography>
                {checkResult.is_breached ? (
                  <Alert
                    severity="error"
                    icon={<WarningIcon />}
                    sx={{ mt: 2 }}
                  >
                    <Typography variant="h6">
                      Vaš email je pronađen u {checkResult.total_breaches} breach-ova!
                    </Typography>
                    <Typography variant="body2" sx={{ mt: 1 }}>
                      {checkResult.breaches.length > 0 && (
                        <>
                          Breach-ovi: {checkResult.breaches.map(b => b.name).join(', ')}
                        </>
                      )}
                    </Typography>
                  </Alert>
                ) : (
                  <Alert severity="success" icon={<CheckCircleIcon />} sx={{ mt: 2 }}>
                    Vaš email nije pronađen u breach bazama podataka.
                  </Alert>
                )}

                {!user && checkResult.is_breached && (
                  <Alert severity="info" sx={{ mt: 2 }}>
                    <Typography variant="body2">
                      <strong>Želite notifikacije o novim breach-ovima?</strong>
                    </Typography>
                    <Button
                      variant="outlined"
                      size="small"
                      onClick={() => navigate('/register')}
                      sx={{ mt: 1 }}
                    >
                      Registrujte se besplatno
                    </Button>
                  </Alert>
                )}
              </Box>
            )}
          </CardContent>
        </Card>

        <Grid container spacing={3} sx={{ mt: 2 }}>
          {quickActions.map((action, index) => (
            <Grid item xs={12} sm={6} md={3} key={index}>
              <Card
                sx={{
                  height: '100%',
                  display: 'flex',
                  flexDirection: 'column',
                  cursor: 'pointer',
                  transition: 'transform 0.2s',
                  '&:hover': {
                    transform: 'translateY(-4px)',
                    boxShadow: '0 0 40px currentColor, 0 0 60px currentColor',
                    borderColor: '#00ffff',
                  },
                }}
                onClick={() => navigate(action.path)}
              >
                <CardContent sx={{ flexGrow: 1, textAlign: 'center' }}>
                  <Box sx={{ color: action.color, mb: 2 }}>{action.icon}</Box>
                  <Typography variant="h6" component="h2" gutterBottom>
                    {action.title}
                  </Typography>
                  <Typography variant="body2" color="text.secondary">
                    {action.description}
                  </Typography>
                </CardContent>
                <Box sx={{ p: 2, pt: 0 }}>
                  <Button
                    fullWidth
                    variant="contained"
                    onClick={() => navigate(action.path)}
                    sx={{ 
                      bgcolor: action.color,
                      color: '#0a0a0a',
                      fontFamily: '"Courier New", monospace',
                      fontWeight: 700,
                      boxShadow: `0 0 15px ${action.color}`,
                      '&:hover': {
                        boxShadow: `0 0 25px ${action.color}, 0 0 35px ${action.color}`,
                      },
                    }}
                  >
                    Otvori
                  </Button>
                </Box>
              </Card>
            </Grid>
          ))}
        </Grid>

        <Box sx={{ mt: 6 }}>
          <Typography variant="h5" gutterBottom>
            Funkcionalnosti sistema
          </Typography>
          <Grid container spacing={2} sx={{ mt: 1 }}>
            <Grid item xs={12} md={6}>
              <Typography 
                variant="body1" 
                paragraph
                sx={{ 
                  color: '#00ffff',
                  fontFamily: '"Courier New", monospace',
                }}
              >
                <strong style={{ color: '#00ff41' }}>[FUNC] Provera kompromitovanih email adresa</strong> - Proverite da li
                je vaš email pronađen u javnim breach bazama podataka
              </Typography>
              <Typography 
                variant="body1" 
                paragraph
                sx={{ 
                  color: '#00ffff',
                  fontFamily: '"Courier New", monospace',
                }}
              >
                <strong style={{ color: '#00ff41' }}>[FUNC] Analiza lozinki</strong> - ML model analizira snagu vaše lozinke
                i detektuje slabe obrasce
              </Typography>
            </Grid>
            <Grid item xs={12} md={6}>
              <Typography 
                variant="body1" 
                paragraph
                sx={{ 
                  color: '#00ffff',
                  fontFamily: '"Courier New", monospace',
                }}
              >
                <strong style={{ color: '#00ff41' }}>[FUNC] Procena rizika</strong> - Automatska procena rizika za svaki
                kompromitovani kredencijal
              </Typography>
              <Typography 
                variant="body1" 
                paragraph
                sx={{ 
                  color: '#00ffff',
                  fontFamily: '"Courier New", monospace',
                }}
              >
                <strong style={{ color: '#00ff41' }}>[FUNC] Personalizovane preporuke</strong> - Dobijte konkretne preporuke
                za poboljšanje bezbednosti vaših naloga
              </Typography>
            </Grid>
          </Grid>
        </Box>
      </Box>
    </Container>
  )
}

export default Home
