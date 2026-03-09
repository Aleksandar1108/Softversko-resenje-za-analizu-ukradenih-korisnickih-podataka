import React, { useState } from 'react'
import {
  Box,
  Container,
  Typography,
  TextField,
  Button,
  Card,
  CardContent,
  Alert,
  CircularProgress,
  LinearProgress,
  Chip,
  List,
  ListItem,
  ListItemIcon,
  ListItemText,
} from '@mui/material'
import {
  Security as SecurityIcon,
  CheckCircle as CheckCircleIcon,
  Error as ErrorIcon,
  Warning as WarningIcon,
} from '@mui/icons-material'
import { passwordAnalysisAPI, emailCheckAPI } from '../../services/api'

const PasswordAnalysis = () => {
  const [password, setPassword] = useState('')
  const [loading, setLoading] = useState(false)
  const [result, setResult] = useState(null)
  const [error, setError] = useState(null)
  const [passwordBreachCheck, setPasswordBreachCheck] = useState(null)

  const handleAnalyze = async () => {
    if (!password) {
      setError('Molimo unesite lozinku')
      return
    }

    setLoading(true)
    setError(null)
    setResult(null)
    setPasswordBreachCheck(null)

    try {
      // Check password breach first
      try {
        const breachResponse = await emailCheckAPI.checkPassword(password)
        setPasswordBreachCheck(breachResponse.data?.data || null)
      } catch (breachErr) {
        console.error('Password breach check error:', breachErr)
        // Continue with analysis even if breach check fails
      }

      // Then analyze password
      const response = await passwordAnalysisAPI.analyzePassword({
        password,
        breach_count: passwordBreachCheck?.count || 0,
      })
      setResult(response.data)
    } catch (err) {
      setError(err.response?.data?.error?.message || 'Greška pri analizi lozinke')
    } finally {
      setLoading(false)
    }
  }

  const getRiskColor = (level) => {
    switch (level) {
      case 'LOW':
        return 'success'
      case 'MEDIUM':
        return 'warning'
      case 'HIGH':
        return 'error'
      default:
        return 'default'
    }
  }

  const getRiskIcon = (level) => {
    switch (level) {
      case 'LOW':
        return <CheckCircleIcon />
      case 'MEDIUM':
        return <WarningIcon />
      case 'HIGH':
        return <ErrorIcon />
      default:
        return <SecurityIcon />
    }
  }

  return (
    <Container maxWidth="md">
      <Box sx={{ my: 4 }}>
        <Typography variant="h4" component="h1" gutterBottom>
          Analiza Lozinke
        </Typography>
        <Typography variant="body1" color="text.secondary" paragraph>
          Unesite lozinku da biste dobili analizu snage i preporuke za poboljšanje
        </Typography>

        <Card sx={{ mb: 4 }}>
          <CardContent>
            <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2 }}>
              <TextField
                fullWidth
                label="Lozinka"
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                placeholder="Unesite lozinku za analizu"
                onKeyPress={(e) => {
                  if (e.key === 'Enter') {
                    handleAnalyze()
                  }
                }}
              />
              <Button
                variant="contained"
                onClick={handleAnalyze}
                disabled={loading || !password}
                startIcon={loading ? <CircularProgress size={20} /> : <SecurityIcon />}
                size="large"
              >
                {loading ? 'Analiziram...' : 'Analiziraj Lozinku'}
              </Button>
            </Box>
          </CardContent>
        </Card>

        {error && (
          <Alert severity="error" sx={{ mb: 2 }}>
            {error}
          </Alert>
        )}

        {passwordBreachCheck && (
          <Alert 
            severity={passwordBreachCheck.is_breached ? "error" : "success"} 
            sx={{ mb: 2 }}
            icon={passwordBreachCheck.is_breached ? <ErrorIcon /> : <CheckCircleIcon />}
          >
            <Typography variant="h6" gutterBottom>
              {passwordBreachCheck.is_breached ? "⚠️ Lozinka je kompromitovana!" : "✓ Lozinka nije kompromitovana"}
            </Typography>
            <Typography variant="body2">
              {passwordBreachCheck.message}
              {passwordBreachCheck.is_breached && passwordBreachCheck.count > 0 && (
                <> Pronađena u <strong>{passwordBreachCheck.count.toLocaleString()}</strong> data breach-ova!</>
              )}
            </Typography>
          </Alert>
        )}

        {result && (
          <Card>
            <CardContent>
              <Box sx={{ mb: 3 }}>
                <Typography variant="h6" gutterBottom>
                  Rezultati Analize
                </Typography>

                <Box sx={{ my: 3 }}>
                  <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 1 }}>
                    <Typography variant="body2">Risk Score</Typography>
                    <Typography variant="body2" fontWeight="bold">
                      {result.risk_score}/100
                    </Typography>
                  </Box>
                  <LinearProgress
                    variant="determinate"
                    value={result.risk_score}
                    color={getRiskColor(result.risk_level)}
                    sx={{ height: 10, borderRadius: 5 }}
                  />
                </Box>

                <Box sx={{ display: 'flex', gap: 2, mb: 2 }}>
                  <Chip
                    icon={getRiskIcon(result.risk_level)}
                    label={`Risk Level: ${result.risk_level}`}
                    color={getRiskColor(result.risk_level)}
                    size="large"
                  />
                  {result.is_weak && (
                    <Chip
                      label="Slaba Lozinka"
                      color="error"
                      size="large"
                    />
                  )}
                </Box>
              </Box>

              {result.recommendations && result.recommendations.length > 0 && (
                <>
                  <Typography variant="h6" gutterBottom>
                    Preporuke za Poboljšanje:
                  </Typography>
                  <List>
                    {result.recommendations.map((rec, index) => (
                      <ListItem key={index}>
                        <ListItemIcon>
                          {rec.startsWith('⚠️') ? (
                            <ErrorIcon color="error" />
                          ) : rec.startsWith('✓') ? (
                            <CheckCircleIcon color="success" />
                          ) : (
                            <WarningIcon color="warning" />
                          )}
                        </ListItemIcon>
                        <ListItemText primary={rec} />
                      </ListItem>
                    ))}
                  </List>
                </>
              )}

              {result.features && (
                <Box sx={{ mt: 3 }}>
                  <Typography variant="h6" gutterBottom>
                    Detalji Analize:
                  </Typography>
                  <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 1, mt: 1 }}>
                    <Chip
                      label={`Dužina: ${result.features.length || 0}`}
                      size="small"
                    />
                    <Chip
                      label={`Entropija: ${result.features.entropy?.toFixed(2) || 0}`}
                      size="small"
                    />
                    {result.features.has_uppercase > 0 && (
                      <Chip label="Velika slova" size="small" color="primary" />
                    )}
                    {result.features.has_lowercase > 0 && (
                      <Chip label="Mala slova" size="small" color="primary" />
                    )}
                    {result.features.has_digits > 0 && (
                      <Chip label="Brojevi" size="small" color="primary" />
                    )}
                    {result.features.has_special > 0 && (
                      <Chip label="Specijalni karakteri" size="small" color="primary" />
                    )}
                    {result.features.is_common > 0 && (
                      <Chip label="Common password" size="small" color="error" />
                    )}
                  </Box>
                </Box>
              )}
            </CardContent>
          </Card>
        )}
      </Box>
    </Container>
  )
}

export default PasswordAnalysis
