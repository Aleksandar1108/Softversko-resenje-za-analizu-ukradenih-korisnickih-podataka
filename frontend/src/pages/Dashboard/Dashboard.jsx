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
} from '@mui/material'
import {
  BarChart,
  Bar,
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
} from 'recharts'
import { reportingAPI } from '../../services/api'

const Dashboard = () => {
  const [statistics, setStatistics] = useState(null)
  const [trends, setTrends] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  useEffect(() => {
    loadData()
  }, [])

  const loadData = async () => {
    try {
      setLoading(true)
      const [statsResponse, trendsResponse] = await Promise.all([
        reportingAPI.getStatistics(),
        reportingAPI.getTrends(30),
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

  const COLORS = ['#0088FE', '#00C49F', '#FFBB28', '#FF8042']

  return (
    <Container maxWidth="lg">
      <Box sx={{ my: 4 }}>
        <Typography variant="h4" component="h1" gutterBottom>
          Dashboard - Statistike Breach Podataka
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
                    Slabe Lozinke
                  </Typography>
                  <Typography variant="h4" color="error">
                    {statistics.weak_passwords?.count || 0}
                  </Typography>
                  <Typography variant="body2" color="text.secondary">
                    {statistics.weak_passwords?.percentage || 0}%
                  </Typography>
                </CardContent>
              </Card>
            </Grid>
            <Grid item xs={12} sm={6} md={3}>
              <Card>
                <CardContent>
                  <Typography color="text.secondary" gutterBottom>
                    Visok Rizik
                  </Typography>
                  <Typography variant="h4" color="warning.main">
                    {statistics.high_risk_credentials?.count || 0}
                  </Typography>
                  <Typography variant="body2" color="text.secondary">
                    {statistics.high_risk_credentials?.percentage || 0}%
                  </Typography>
                </CardContent>
              </Card>
            </Grid>
          </Grid>
        )}

        {trends && (
          <Grid container spacing={3} sx={{ mt: 2 }}>
            <Grid item xs={12} md={6}>
              <Card>
                <CardContent>
                  <Typography variant="h6" gutterBottom>
                    Trend Breach-ova (Poslednjih {trends.period_days} dana)
                  </Typography>
                  <ResponsiveContainer width="100%" height={300}>
                    <LineChart data={Object.entries(trends.monthly_trends || {}).map(([month, data]) => ({
                      month,
                      breaches: data.breaches || 0,
                    }))}>
                      <CartesianGrid strokeDasharray="3 3" />
                      <XAxis dataKey="month" />
                      <YAxis />
                      <Tooltip />
                      <Legend />
                      <Line type="monotone" dataKey="breaches" stroke="#8884d8" />
                    </LineChart>
                  </ResponsiveContainer>
                </CardContent>
              </Card>
            </Grid>

            <Grid item xs={12} md={6}>
              <Card>
                <CardContent>
                  <Typography variant="h6" gutterBottom>
                    Top Tipovi Podataka
                  </Typography>
                  <ResponsiveContainer width="100%" height={300}>
                    <PieChart>
                      <Pie
                        data={trends.top_data_classes || []}
                        dataKey="count"
                        nameKey="class"
                        cx="50%"
                        cy="50%"
                        outerRadius={80}
                        label
                      >
                        {(trends.top_data_classes || []).map((entry, index) => (
                          <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                        ))}
                      </Pie>
                      <Tooltip />
                    </PieChart>
                  </ResponsiveContainer>
                </CardContent>
              </Card>
            </Grid>
          </Grid>
        )}

        {statistics?.breach_sources && (
          <Card sx={{ mt: 3 }}>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Izvori Breach-ova
              </Typography>
              <Grid container spacing={2}>
                <Grid item xs={6}>
                  <Typography variant="body1">
                    HIBP: {statistics.breach_sources.hibp || 0}
                  </Typography>
                </Grid>
                <Grid item xs={6}>
                  <Typography variant="body1">
                    Scraped: {statistics.breach_sources.scraped || 0}
                  </Typography>
                </Grid>
              </Grid>
            </CardContent>
          </Card>
        )}
      </Box>
    </Container>
  )
}

export default Dashboard
