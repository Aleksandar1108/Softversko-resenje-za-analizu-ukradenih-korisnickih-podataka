import React, { useState, useEffect } from 'react'
import {
  Box,
  Container,
  Typography,
  Card,
  CardContent,
  List,
  ListItem,
  ListItemText,
  ListItemSecondaryAction,
  IconButton,
  Chip,
  CircularProgress,
  Alert,
  Divider,
} from '@mui/material'
import {
  Delete as DeleteIcon,
  Notifications as NotificationsIcon,
  Warning as WarningIcon,
  Info as InfoIcon,
  Error as ErrorIcon,
} from '@mui/icons-material'
import { notificationsAPI } from '../../services/api'
import { useAuth } from '../../contexts/AuthContext'

const Notifications = () => {
  const { isAuthenticated } = useAuth()
  const [notifications, setNotifications] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  useEffect(() => {
    if (isAuthenticated) {
      loadNotifications()
    } else {
      setLoading(false)
      setNotifications([])
    }
  }, [isAuthenticated])

  const loadNotifications = async () => {
    try {
      setLoading(true)
      setError(null)
      const response = await notificationsAPI.getAll()
      setNotifications(response.data?.data || [])
    } catch (err) {
      // If 401 or 403, user is not authenticated - show empty list
      if (err.response?.status === 401 || err.response?.status === 403) {
        setNotifications([])
      } else {
        setError(err.response?.data?.error?.message || 'Greška pri učitavanju notifikacija')
      }
    } finally {
      setLoading(false)
    }
  }

  const handleMarkAsRead = async (id) => {
    try {
      await notificationsAPI.markAsRead(id)
      setNotifications(
        notifications.map((notif) =>
          notif.id === id ? { ...notif, is_read: true } : notif
        )
      )
    } catch (err) {
      console.error('Error marking notification as read:', err)
    }
  }

  const handleDelete = async (id) => {
    try {
      await notificationsAPI.delete(id)
      setNotifications(notifications.filter((notif) => notif.id !== id))
    } catch (err) {
      console.error('Error deleting notification:', err)
    }
  }

  const getIcon = (type) => {
    switch (type) {
      case 'breach_alert':
        return <ErrorIcon color="error" />
      case 'risk_alert':
        return <WarningIcon color="warning" />
      case 'recommendation':
        return <InfoIcon color="info" />
      default:
        return <NotificationsIcon />
    }
  }

  const getPriorityColor = (priority) => {
    switch (priority) {
      case 'critical':
        return 'error'
      case 'high':
        return 'warning'
      case 'normal':
        return 'info'
      default:
        return 'default'
    }
  }

  if (loading) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" minHeight="400px">
        <CircularProgress />
      </Box>
    )
  }

  const unreadCount = notifications.filter((n) => !n.is_read).length

  return (
    <Container maxWidth="md">
      <Box sx={{ my: 4 }}>
        <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 2 }}>
          <Typography variant="h4" component="h1">
            Notifikacije
          </Typography>
          {unreadCount > 0 && (
            <Chip label={`${unreadCount} nepročitanih`} color="primary" />
          )}
        </Box>

        {error && (
          <Alert severity="error" sx={{ mb: 2 }}>
            {error}
          </Alert>
        )}

        {notifications.length === 0 && !error && (
          <Card>
            <CardContent>
              <Box sx={{ textAlign: 'center', py: 4 }}>
                <NotificationsIcon sx={{ fontSize: 60, color: 'text.secondary', mb: 2 }} />
                <Typography variant="h6" gutterBottom>
                  Nema notifikacija
                </Typography>
                <Typography variant="body2" color="text.secondary">
                  Kada budete imali nove notifikacije, pojaviće se ovde.
                </Typography>
              </Box>
            </CardContent>
          </Card>
        )}

        {notifications.length > 0 && (
          <Card>
            <CardContent>
              <List>
                {notifications.map((notif, index) => (
                  <React.Fragment key={notif.id || index}>
                    <ListItem
                      sx={{
                        bgcolor: notif.is_read ? 'transparent' : 'action.hover',
                        borderRadius: 1,
                        mb: 1,
                      }}
                    >
                      <Box sx={{ mr: 2 }}>{getIcon(notif.type)}</Box>
                      <ListItemText
                        primary={
                          <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                            <Typography variant="subtitle1">{notif.title}</Typography>
                            {!notif.is_read && (
                              <Chip label="Nova" size="small" color="primary" />
                            )}
                            <Chip
                              label={notif.priority}
                              size="small"
                              color={getPriorityColor(notif.priority)}
                            />
                          </Box>
                        }
                        secondary={
                          <Box>
                            <Typography variant="body2" color="text.secondary">
                              {notif.message}
                            </Typography>
                            {notif.created_at && (
                              <Typography variant="caption" color="text.secondary">
                                {new Date(notif.created_at).toLocaleString()}
                              </Typography>
                            )}
                          </Box>
                        }
                      />
                      <ListItemSecondaryAction>
                        {!notif.is_read && (
                          <IconButton
                            edge="end"
                            onClick={() => handleMarkAsRead(notif.id)}
                            sx={{ mr: 1 }}
                          >
                            <Chip label="Pročitano" size="small" />
                          </IconButton>
                        )}
                        <IconButton
                          edge="end"
                          onClick={() => handleDelete(notif.id)}
                          color="error"
                        >
                          <DeleteIcon />
                        </IconButton>
                      </ListItemSecondaryAction>
                    </ListItem>
                    {index < notifications.length - 1 && <Divider />}
                  </React.Fragment>
                ))}
              </List>
            </CardContent>
          </Card>
        )}
      </Box>
    </Container>
  )
}

export default Notifications
