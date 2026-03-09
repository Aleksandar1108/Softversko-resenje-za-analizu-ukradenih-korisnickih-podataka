import React, { useState, useEffect } from 'react'
import {
  Box,
  Container,
  Typography,
  Grid,
  Card,
  CardContent,
  CircularProgress,
  Alert,
  Chip,
  List,
  ListItem,
  ListItemText,
  Divider,
} from '@mui/material'
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
  PieChart,
  Pie,
  Cell,
  BarChart,
  Bar,
} from 'recharts'
import { reportingAPI } from '../../services/api'
import { useAuth } from '../../contexts/AuthContext'

const Dashboard = () => {
  const { isAuthenticated } = useAuth()
  const [statistics, setStatistics] = useState(null)
  const [trends, setTrends] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  useEffect(() => {
    loadData()
  }, [isAuthenticated])

  const loadData = async () => {
    try {
      setLoading(true)
      const [statsResponse, trendsResponse] = await Promise.all([
        reportingAPI.getStatistics(),
        reportingAPI.getTrends(30).catch(() => ({ data: { data: null } })),
      ])
      setStatistics(statsResponse.data.data)
      setTrends(trendsResponse.data.data)
    } catch (err) {
      setError(err.response?.data?.error?.message || 'Greška pri učitavanju podataka')
    } finally {
      setLoading(false)
    }
  }

  if (loading) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" minHeight="400px">
        <CircularProgress />
      </Box>
    )
  }

  if (error) {
    return (
      <Container maxWidth="lg">
        <Alert severity="error">{error}</Alert>
      </Container>
    )
  }

  const COLORS = ['#0088FE', '#00C49F', '#FFBB28', '#FF8042', '#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4']

  // Get risk level color
  const getRiskLevelColor = (riskLevel) => {
    switch (riskLevel) {
      case 'low':
        return 'success'
      case 'medium':
        return 'warning'
      case 'high':
        return 'error'
      default:
        return 'default'
    }
  }

  // Get risk level text
  const getRiskLevelText = (riskLevel) => {
    switch (riskLevel) {
      case 'low':
        return 'Nizak'
      case 'medium':
        return 'Srednji'
      case 'high':
        return 'Visok'
      default:
        return 'Nepoznat'
    }
  }

  // Prepare trend data from breaches
  const prepareTrendData = () => {
    if (!statistics?.breaches || statistics.breaches.length === 0) {
      return []
    }

    // Group breaches by year
    const breachesByYear = {}
    statistics.breaches.forEach((breach) => {
      if (breach.breach_date) {
        const year = new Date(breach.breach_date).getFullYear()
        breachesByYear[year] = (breachesByYear[year] || 0) + 1
      }
    })

    // Convert to array and sort by year
    return Object.entries(breachesByYear)
      .map(([year, count]) => ({ year, breaches: count }))
      .sort((a, b) => a.year - b.year)
  }

  // Prepare data types chart data
  const prepareDataTypesData = () => {
    if (!statistics?.data_types_count) {
      return []
    }

    return Object.entries(statistics.data_types_count).map(([name, count]) => ({
      name,
      count,
    }))
  }

  const trendData = prepareTrendData()
  const dataTypesData = prepareDataTypesData()

  return (
    <Container maxWidth="lg">
      <Box sx={{ my: 4 }}>
        <Typography variant="h4" component="h1" gutterBottom>
          {isAuthenticated ? 'Moj Dashboard' : 'Dashboard - Statistike Breach Podataka'}
        </Typography>

        {statistics && (
          <Grid container spacing={3} sx={{ mt: 2 }}>
            <Grid item xs={12} sm={6} md={3}>
              <Card>
                <CardContent>
                  <Typography color="text.secondary" gutterBottom>
                    Ukupno Breach-ova
                  </Typography>
                  <Typography variant="h4">{statistics.total_breaches || 0}</Typography>
                </CardContent>
              </Card>
            </Grid>
            <Grid item xs={12} sm={6} md={3}>
              <Card>
                <CardContent>
                  <Typography color="text.secondary" gutterBottom>
                    Nivo Rizika
                  </Typography>
                  <Chip
                    label={getRiskLevelText(statistics.risk_level || 'low')}
                    color={getRiskLevelColor(statistics.risk_level || 'low')}
                    sx={{ mt: 1 }}
                  />
                </CardContent>
              </Card>
            </Grid>
            <Grid item xs={12} sm={6} md={3}>
              <Card>
                <CardContent>
                  <Typography color="text.secondary" gutterBottom>
                    Ukupno Kredencijala
                  </Typography>
                  <Typography variant="h4">{statistics.total_credentials || 0}</Typography>
                </CardContent>
              </Card>
            </Grid>
            <Grid item xs={12} sm={6} md={3}>
              <Card>
                <CardContent>
                  <Typography color="text.secondary" gutterBottom>
                    Tipovi Podataka
                  </Typography>
                  <Typography variant="h4">{Object.keys(statistics.data_types_count || {}).length || 0}</Typography>
                </CardContent>
              </Card>
            </Grid>
          </Grid>
        )}

        {/* Breaches List */}
        {statistics?.breaches && statistics.breaches.length > 0 && (
          <Card sx={{ mt: 3 }}>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Lista Breach-ova
              </Typography>
              <List>
                {statistics.breaches.map((breach, index) => (
                  <React.Fragment key={breach.id || index}>
                    <ListItem>
                      <ListItemText
                        primary={
                          <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                            <Typography variant="subtitle1">{breach.name}</Typography>
                            {breach.domain && (
                              <Chip label={breach.domain} size="small" variant="outlined" />
                            )}
                          </Box>
                        }
                        secondary={
                          <Box>
                            {breach.breach_date && (
                              <Typography variant="body2" color="text.secondary">
                                Datum: {new Date(breach.breach_date).toLocaleDateString('sr-RS')}
                              </Typography>
                            )}
                            {breach.data_classes && breach.data_classes.length > 0 && (
                              <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 0.5, mt: 1 }}>
                                {breach.data_classes.map((dataClass, idx) => (
                                  <Chip
                                    key={idx}
                                    label={dataClass}
                                    size="small"
                                    color="primary"
                                    variant="outlined"
                                  />
                                ))}
                              </Box>
                            )}
                          </Box>
                        }
                      />
                    </ListItem>
                    {index < statistics.breaches.length - 1 && <Divider />}
                  </React.Fragment>
                ))}
              </List>
            </CardContent>
          </Card>
        )}

        {/* Charts */}
        <Grid container spacing={3} sx={{ mt: 2 }}>
          {/* Trend Chart */}
          {trendData.length > 0 && (
            <Grid item xs={12} md={6}>
              <Card>
                <CardContent>
                  <Typography variant="h6" gutterBottom>
                    Trend Breach-ova kroz Vreme
                  </Typography>
                  <ResponsiveContainer width="100%" height={300}>
                    <LineChart data={trendData}>
                      <CartesianGrid strokeDasharray="3 3" />
                      <XAxis dataKey="year" />
                      <YAxis />
                      <Tooltip />
                      <Legend />
                      <Line type="monotone" dataKey="breaches" stroke="#8884d8" strokeWidth={2} />
                    </LineChart>
                  </ResponsiveContainer>
                </CardContent>
              </Card>
            </Grid>
          )}

          {/* Data Types Chart */}
          {dataTypesData.length > 0 && (
            <Grid item xs={12} md={6}>
              <Card>
                <CardContent>
                  <Typography variant="h6" gutterBottom>
                    Tipovi Kompromitovanih Podataka
                  </Typography>
                  <ResponsiveContainer width="100%" height={300}>
                    <PieChart>
                      <Pie
                        data={dataTypesData}
                        dataKey="count"
                        nameKey="name"
                        cx="50%"
                        cy="50%"
                        outerRadius={80}
                        label={({ name, count }) => `${name}: ${count}`}
                      >
                        {dataTypesData.map((entry, index) => (
                          <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                        ))}
                      </Pie>
                      <Tooltip />
                    </PieChart>
                  </ResponsiveContainer>
                </CardContent>
              </Card>
            </Grid>
          )}

          {/* Data Types Bar Chart */}
          {dataTypesData.length > 0 && (
            <Grid item xs={12}>
              <Card>
                <CardContent>
                  <Typography variant="h6" gutterBottom>
                    Broj Kompromitovanih Tipova Podataka
                  </Typography>
                  <ResponsiveContainer width="100%" height={300}>
                    <BarChart data={dataTypesData}>
                      <CartesianGrid strokeDasharray="3 3" />
                      <XAxis dataKey="name" />
                      <YAxis />
                      <Tooltip />
                      <Legend />
                      <Bar dataKey="count" fill="#8884d8" />
                    </BarChart>
                  </ResponsiveContainer>
                </CardContent>
              </Card>
            </Grid>
          )}
        </Grid>

        {/* Additional Statistics */}
        {statistics && (
          <Grid container spacing={3} sx={{ mt: 2 }}>
            {statistics.weak_passwords && (
              <Grid item xs={12} sm={6} md={3}>
                <Card>
                  <CardContent>
                    <Typography color="text.secondary" gutterBottom>
                      Slabe Lozinke
                    </Typography>
                    <Typography variant="h4" color="error">
                      {statistics.weak_passwords.count || 0}
                    </Typography>
                    <Typography variant="body2" color="text.secondary">
                      {statistics.weak_passwords.percentage || 0}%
                    </Typography>
                  </CardContent>
                </Card>
              </Grid>
            )}
            {statistics.high_risk_credentials && (
              <Grid item xs={12} sm={6} md={3}>
                <Card>
                  <CardContent>
                    <Typography color="text.secondary" gutterBottom>
                      Visok Rizik
                    </Typography>
                    <Typography variant="h4" color="warning.main">
                      {statistics.high_risk_credentials.count || 0}
                    </Typography>
                    <Typography variant="body2" color="text.secondary">
                      {statistics.high_risk_credentials.percentage || 0}%
                    </Typography>
                  </CardContent>
                </Card>
              </Grid>
            )}
            {statistics.breach_sources && (
              <Grid item xs={12} sm={6} md={3}>
                <Card>
                  <CardContent>
                    <Typography color="text.secondary" gutterBottom>
                      Izvor: HIBP
                    </Typography>
                    <Typography variant="h4">{statistics.breach_sources.hibp || 0}</Typography>
                  </CardContent>
                </Card>
              </Grid>
            )}
            {statistics.breach_sources && (
              <Grid item xs={12} sm={6} md={3}>
                <Card>
                  <CardContent>
                    <Typography color="text.secondary" gutterBottom>
                      Izvor: Scraped
                    </Typography>
                    <Typography variant="h4">{statistics.breach_sources.scraped || 0}</Typography>
                  </CardContent>
                </Card>
              </Grid>
            )}
          </Grid>
        )}

        {/* Empty State */}
        {statistics && statistics.total_breaches === 0 && (
          <Card sx={{ mt: 3 }}>
            <CardContent>
              <Box sx={{ textAlign: 'center', py: 4 }}>
                <Typography variant="h6" gutterBottom>
                  Nema pronađenih breach-ova
                </Typography>
                <Typography variant="body2" color="text.secondary">
                  Vaš email nije pronađen u nijednom poznatom data breach-u.
                </Typography>
              </Box>
            </CardContent>
          </Card>
        )}
      </Box>
    </Container>
  )
}

export default Dashboard
