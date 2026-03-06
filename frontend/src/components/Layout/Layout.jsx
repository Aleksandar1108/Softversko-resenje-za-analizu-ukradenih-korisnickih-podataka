import React, { useState } from 'react'
import { Outlet, useNavigate, useLocation } from 'react-router-dom'
import {
  AppBar,
  Box,
  Drawer,
  IconButton,
  List,
  ListItem,
  ListItemButton,
  ListItemIcon,
  ListItemText,
  Toolbar,
  Typography,
  Avatar,
  Menu,
  MenuItem,
  Badge,
} from '@mui/material'
import {
  Menu as MenuIcon,
  Home as HomeIcon,
  Email as EmailIcon,
  Dashboard as DashboardIcon,
  Lock as LockIcon,
  Security as SecurityIcon,
  Person as PersonIcon,
  Notifications as NotificationsIcon,
  Logout as LogoutIcon,
} from '@mui/icons-material'
import { useAuth } from '../../contexts/AuthContext'
import { Button } from '@mui/material'

const drawerWidth = 240

// Javni menu items (bez autentifikacije)
const publicMenuItems = [
  { text: 'Home', icon: <HomeIcon />, path: '/' },
  { text: 'Provera Email-a', icon: <EmailIcon />, path: '/email-check' },
]

// Zaštićeni menu items (zahtevaju autentifikaciju)
const protectedMenuItems = [
  { text: 'Dashboard', icon: <DashboardIcon />, path: '/dashboard' },
  { text: 'Analiza Lozinke', icon: <LockIcon />, path: '/password-analysis' },
  { text: 'Preporuke', icon: <SecurityIcon />, path: '/recommendations' },
  { text: 'Notifikacije', icon: <NotificationsIcon />, path: '/notifications' },
  { text: 'Profil', icon: <PersonIcon />, path: '/profile' },
]

const Layout = () => {
  const [mobileOpen, setMobileOpen] = useState(false)
  const [anchorEl, setAnchorEl] = useState(null)
  const navigate = useNavigate()
  const location = useLocation()
  const { user, logout } = useAuth()

  const handleDrawerToggle = () => {
    setMobileOpen(!mobileOpen)
  }

  const handleMenuOpen = (event) => {
    setAnchorEl(event.currentTarget)
  }

  const handleMenuClose = () => {
    setAnchorEl(null)
  }

  const handleLogout = () => {
    logout()
    navigate('/')
    handleMenuClose()
  }

  const drawer = (
    <Box>
      <Toolbar>
        <Typography 
          variant="h6" 
          noWrap 
          component="div"
          sx={{
            color: '#00ff41',
            textShadow: '0 0 10px #00ff41, 0 0 20px #00ff41',
            fontFamily: '"Courier New", monospace',
            fontWeight: 700,
          }}
        >
          &gt; BREACH_ANALYZER.exe
        </Typography>
      </Toolbar>
      <List>
        {/* Javni menu items - uvek vidljivi */}
        {publicMenuItems.map((item) => (
          <ListItem key={item.text} disablePadding>
            <ListItemButton
              selected={location.pathname === item.path}
              onClick={() => {
                navigate(item.path)
                setMobileOpen(false)
              }}
            >
              <ListItemIcon>{item.icon}</ListItemIcon>
              <ListItemText primary={item.text} />
            </ListItemButton>
          </ListItem>
        ))}
        
        {/* Zaštićeni menu items - samo za prijavljene korisnike */}
        {user && protectedMenuItems.map((item) => (
          <ListItem key={item.text} disablePadding>
            <ListItemButton
              selected={location.pathname === item.path}
              onClick={() => {
                navigate(item.path)
                setMobileOpen(false)
              }}
            >
              <ListItemIcon>{item.icon}</ListItemIcon>
              <ListItemText primary={item.text} />
            </ListItemButton>
          </ListItem>
        ))}
        
        {/* Ako korisnik nije prijavljen, prikaži opciju za registraciju */}
        {!user && (
          <ListItem disablePadding>
            <Box sx={{ p: 2, width: '100%' }}>
              <Button
                fullWidth
                variant="contained"
                onClick={() => {
                  navigate('/register')
                  setMobileOpen(false)
                }}
                sx={{ mb: 1 }}
              >
                Registruj se
              </Button>
              <Button
                fullWidth
                variant="outlined"
                onClick={() => {
                  navigate('/login')
                  setMobileOpen(false)
                }}
              >
                Prijavi se
              </Button>
            </Box>
          </ListItem>
        )}
      </List>
    </Box>
  )

  return (
    <Box sx={{ display: 'flex' }}>
      <AppBar
        position="fixed"
        sx={{
          width: { sm: `calc(100% - ${drawerWidth}px)` },
          ml: { sm: `${drawerWidth}px` },
        }}
      >
        <Toolbar>
          <IconButton
            color="inherit"
            aria-label="open drawer"
            edge="start"
            onClick={handleDrawerToggle}
            sx={{ mr: 2, display: { sm: 'none' } }}
          >
            <MenuIcon />
          </IconButton>
          <Typography 
            variant="h6" 
            noWrap 
            component="div" 
            sx={{ 
              flexGrow: 1,
              color: '#00ff41',
              textShadow: '0 0 10px #00ff41',
              fontFamily: '"Courier New", monospace',
              fontWeight: 700,
            }}
          >
            &gt; ANALIZA_KREDENCIJALA.exe
          </Typography>
          <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
            {user ? (
              <>
                <IconButton
                  color="inherit"
                  onClick={() => navigate('/notifications')}
                >
                  <Badge badgeContent={0} color="error">
                    <NotificationsIcon />
                  </Badge>
                </IconButton>
                <IconButton onClick={handleMenuOpen} sx={{ p: 0 }}>
                  <Avatar sx={{ bgcolor: 'secondary.main' }}>
                    {user?.email?.charAt(0).toUpperCase() || 'U'}
                  </Avatar>
                </IconButton>
                <Menu
                  anchorEl={anchorEl}
                  open={Boolean(anchorEl)}
                  onClose={handleMenuClose}
                >
                  <MenuItem onClick={() => { navigate('/profile'); handleMenuClose(); }}>
                    <PersonIcon sx={{ mr: 1 }} />
                    Profil
                  </MenuItem>
                  <MenuItem onClick={handleLogout}>
                    <LogoutIcon sx={{ mr: 1 }} />
                    Odjavi se
                  </MenuItem>
                </Menu>
              </>
            ) : (
              <>
                <Button color="inherit" onClick={() => navigate('/login')}>
                  Prijava
                </Button>
                <Button 
                  color="inherit" 
                  variant="outlined" 
                  onClick={() => navigate('/register')}
                  sx={{ borderColor: 'white', color: 'white' }}
                >
                  Registracija
                </Button>
              </>
            )}
          </Box>
        </Toolbar>
      </AppBar>
      <Box
        component="nav"
        sx={{ width: { sm: drawerWidth }, flexShrink: { sm: 0 } }}
      >
        <Drawer
          variant="temporary"
          open={mobileOpen}
          onClose={handleDrawerToggle}
          ModalProps={{
            keepMounted: true,
          }}
          sx={{
            display: { xs: 'block', sm: 'none' },
            '& .MuiDrawer-paper': { boxSizing: 'border-box', width: drawerWidth },
          }}
        >
          {drawer}
        </Drawer>
        <Drawer
          variant="permanent"
          sx={{
            display: { xs: 'none', sm: 'block' },
            '& .MuiDrawer-paper': { boxSizing: 'border-box', width: drawerWidth },
          }}
          open
        >
          {drawer}
        </Drawer>
      </Box>
      <Box
        component="main"
        sx={{
          flexGrow: 1,
          p: 3,
          width: { sm: `calc(100% - ${drawerWidth}px)` },
          mt: 8,
        }}
      >
        <Outlet />
      </Box>
    </Box>
  )
}

export default Layout
