import React, { useState, useEffect } from 'react'
import {
  Box,
  Container,
  Typography,
  Card,
  CardContent,
  CircularProgress,
  Alert,
  List,
  ListItem,
  ListItemIcon,
  ListItemText,
  Chip,
  Divider,
} from '@mui/material'
import {
  CheckCircle as CheckCircleIcon,
  Error as ErrorIcon,
  Warning as WarningIcon,
  Security as SecurityIcon,
} from '@mui/icons-material'
import { recommendationsAPI } from '../../services/api'

const Recommendations = () => {
  const [recommendations, setRecommendations] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  useEffect(() => {
    loadRecommendations()
  }, [])

  const loadRecommendations = async () => {
    try {
      setLoading(true)
      const response = await recommendationsAPI.getRecommendations()
      setRecommendations(response.data || [])
    } catch (err) {
      setError(err.response?.data?.error?.message || 'Greška pri učitavanju preporuka')
    } finally {
      setLoading(false)
    }
  }

  const getIcon = (rec) => {
    if (rec.includes('CRITICAL') || rec.includes('immediately')) {
      return <ErrorIcon color="error" />
    } else if (rec.includes('Consider') || rec.includes('recommend')) {
      return <WarningIcon color="warning" />
    } else {
      return <CheckCircleIcon color="success" />
    }
  }

  if (loading) {
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
          Preporuke za Bezbednost
        </Typography>
        <Typography variant="body1" color="text.secondary" paragraph>
          Personalizovane preporuke za poboljšanje bezbednosti vaših naloga
        </Typography>

        {error && (
          <Alert severity="error" sx={{ mb: 2 }}>
            {error}
          </Alert>
        )}

        {recommendations.length === 0 && !error && (
          <Card>
            <CardContent>
              <Box sx={{ textAlign: 'center', py: 4 }}>
                <SecurityIcon sx={{ fontSize: 60, color: 'success.main', mb: 2 }} />
                <Typography variant="h6" gutterBottom>
                  Vaši kredencijali izgledaju sigurno!
                </Typography>
                <Typography variant="body2" color="text.secondary">
                  Nastavite da koristite jake, jedinstvene lozinke za svaki nalog.
                </Typography>
              </Box>
            </CardContent>
          </Card>
        )}

        {recommendations.length > 0 && (
          <Card>
            <CardContent>
              <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                <SecurityIcon sx={{ mr: 1, color: 'primary.main' }} />
                <Typography variant="h6">
                  Preporuke ({recommendations.length})
                </Typography>
              </Box>
              <List>
                {recommendations.map((rec, index) => (
                  <React.Fragment key={index}>
                    <ListItem>
                      <ListItemIcon>{getIcon(rec)}</ListItemIcon>
                      <ListItemText
                        primary={rec}
                        primaryTypographyProps={{
                          variant: 'body1',
                          color: rec.includes('CRITICAL') || rec.includes('immediately')
                            ? 'error.main'
                            : 'text.primary',
                        }}
                      />
                    </ListItem>
                    {index < recommendations.length - 1 && <Divider />}
                  </React.Fragment>
                ))}
              </List>
            </CardContent>
          </Card>
        )}

        <Card sx={{ mt: 3 }}>
          <CardContent>
            <Typography variant="h6" gutterBottom>
              Opšti Saveti za Bezbednost:
            </Typography>
            <List>
              <ListItem>
                <ListItemIcon>
                  <CheckCircleIcon color="success" />
                </ListItemIcon>
                <ListItemText
                  primary="Koristite jedinstvene lozinke za svaki nalog"
                  secondary="Nikada ne koristite istu lozinku na više mesta"
                />
              </ListItem>
              <ListItem>
                <ListItemIcon>
                  <CheckCircleIcon color="success" />
                </ListItemIcon>
                <ListItemText
                  primary="Koristite password manager"
                  secondary="Password manager vam pomaže da generišete i čuvate jake lozinke"
                />
              </ListItem>
              <ListItem>
                <ListItemIcon>
                  <CheckCircleIcon color="success" />
                </ListItemIcon>
                <ListItemText
                  primary="Omogućite two-factor authentication (2FA)"
                  secondary="Dodatni sloj zaštite za vaše naloge"
                />
              </ListItem>
              <ListItem>
                <ListItemIcon>
                  <CheckCircleIcon color="success" />
                </ListItemIcon>
                <ListItemText
                  primary="Redovno proveravajte breach podatke"
                  secondary="Budite svesni kada su vaši podaci kompromitovani"
                />
              </ListItem>
            </List>
          </CardContent>
        </Card>
      </Box>
    </Container>
  )
}

export default Recommendations
