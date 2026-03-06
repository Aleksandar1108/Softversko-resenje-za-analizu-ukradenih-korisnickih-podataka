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
  Chip,
  List,
  ListItem,
  ListItemText,
  Divider,
} from '@mui/material'
import { Search as SearchIcon, Warning as WarningIcon } from '@mui/icons-material'
import { emailCheckAPI } from '../../services/api'

const EmailCheck = () => {
  const [email, setEmail] = useState('')
  const [loading, setLoading] = useState(false)
  const [result, setResult] = useState(null)
  const [error, setError] = useState(null)

  const handleCheck = async () => {
    if (!email) {
      setError('Molimo unesite email adresu')
      return
    }

    setLoading(true)
    setError(null)
    setResult(null)

    try {
      const response = await emailCheckAPI.checkEmail(email)
      setResult(response.data.data)
    } catch (err) {
      setError(err.response?.data?.error?.message || 'Greška pri proveri email-a')
    } finally {
      setLoading(false)
    }
  }

  return (
    <Container maxWidth="md">
      <Box sx={{ my: 4 }}>
        <Typography variant="h4" component="h1" gutterBottom>
          Provera Kompromitovanog Email-a
        </Typography>
        <Typography variant="body1" color="text.secondary" paragraph>
          Unesite vašu email adresu da proverite da li je kompromitovana u data breach-ovima
        </Typography>

        <Card sx={{ mb: 4 }}>
          <CardContent>
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
                    handleCheck()
                  }
                }}
              />
              <Button
                variant="contained"
                onClick={handleCheck}
                disabled={loading}
                startIcon={loading ? <CircularProgress size={20} /> : <SearchIcon />}
                sx={{ minWidth: 150 }}
              >
                {loading ? 'Proveravam...' : 'Proveri'}
              </Button>
            </Box>
          </CardContent>
        </Card>

        {error && (
          <Alert severity="error" sx={{ mb: 2 }}>
            {error}
          </Alert>
        )}

        {result && (
          <Card>
            <CardContent>
              <Box sx={{ mb: 3 }}>
                <Typography variant="h6" gutterBottom>
                  Rezultati provere za: {result.email}
                </Typography>
                {result.is_breached ? (
                  <Alert
                    severity="error"
                    icon={<WarningIcon />}
                    sx={{ mt: 2 }}
                  >
                    <Typography variant="h6">
                      Vaš email je pronađen u {result.total_breaches} breach-ova!
                    </Typography>
                  </Alert>
                ) : (
                  <Alert severity="success" sx={{ mt: 2 }}>
                    Vaš email nije pronađen u breach bazama podataka.
                  </Alert>
                )}
              </Box>

              {result.is_breached && (
                <>
                  <Divider sx={{ my: 2 }} />
                  <Typography variant="h6" gutterBottom>
                    Detalji breach-ova:
                  </Typography>
                  <List>
                    {result.breaches.map((breach, index) => (
                      <React.Fragment key={index}>
                        <ListItem>
                          <ListItemText
                            primary={breach.name}
                            secondary={
                              <Box>
                                <Typography variant="body2" color="text.secondary">
                                  Domen: {breach.domain || 'N/A'}
                                </Typography>
                                {breach.breach_date && (
                                  <Typography variant="body2" color="text.secondary">
                                    Datum: {new Date(breach.breach_date).toLocaleDateString()}
                                  </Typography>
                                )}
                                {breach.data_classes && breach.data_classes.length > 0 && (
                                  <Box sx={{ mt: 1 }}>
                                    {breach.data_classes.map((dataClass, i) => (
                                      <Chip
                                        key={i}
                                        label={dataClass}
                                        size="small"
                                        sx={{ mr: 0.5, mb: 0.5 }}
                                      />
                                    ))}
                                  </Box>
                                )}
                              </Box>
                            }
                          />
                        </ListItem>
                        {index < result.breaches.length - 1 && <Divider />}
                      </React.Fragment>
                    ))}
                  </List>

                  {result.statistics && (
                    <>
                      <Divider sx={{ my: 2 }} />
                      <Typography variant="h6" gutterBottom>
                        Statistike:
                      </Typography>
                      <Box sx={{ display: 'flex', gap: 2, flexWrap: 'wrap' }}>
                        <Chip
                          label={`Ukupno kredencijala: ${result.statistics.total_credentials || 0}`}
                          color="primary"
                        />
                        <Chip
                          label={`Slabe lozinke: ${result.statistics.weak_passwords || 0}`}
                          color="error"
                        />
                        <Chip
                          label={`Visok rizik: ${result.statistics.high_risk_credentials || 0}`}
                          color="warning"
                        />
                      </Box>
                    </>
                  )}
                </>
              )}
            </CardContent>
          </Card>
        )}
      </Box>
    </Container>
  )
}

export default EmailCheck
