import React from 'react'
import ReactDOM from 'react-dom/client'
import { BrowserRouter } from 'react-router-dom'
import { ThemeProvider, createTheme } from '@mui/material/styles'
import CssBaseline from '@mui/material/CssBaseline'
import App from './App'
import './index.css'

const theme = createTheme({
  palette: {
    mode: 'dark',
    primary: {
      main: '#00ff41', // Neon zelena
      light: '#66ff7a',
      dark: '#00cc33',
    },
    secondary: {
      main: '#00ffff', // Cijan
      light: '#66ffff',
      dark: '#00cccc',
    },
    error: {
      main: '#ff0080', // Neon roza
      light: '#ff66b3',
      dark: '#cc0066',
    },
    warning: {
      main: '#ffaa00', // Neon narandžasta
      light: '#ffcc66',
      dark: '#cc8800',
    },
    info: {
      main: '#0080ff', // Neon plava
      light: '#66b3ff',
      dark: '#0066cc',
    },
    success: {
      main: '#00ff41', // Neon zelena
      light: '#66ff7a',
      dark: '#00cc33',
    },
    background: {
      default: '#0a0a0a', // Vrlo tamna pozadina
      paper: '#1a1a1a', // Tamna kartica
    },
    text: {
      primary: '#00ff41', // Neon zelena
      secondary: '#00ffff', // Cijan
    },
  },
  typography: {
    fontFamily: '"Courier New", "Monaco", "Consolas", "monospace"',
    h1: {
      fontFamily: '"Courier New", "Monaco", "Consolas", "monospace"',
      fontWeight: 700,
      textShadow: '0 0 10px #00ff41, 0 0 20px #00ff41',
    },
    h2: {
      fontFamily: '"Courier New", "Monaco", "Consolas", "monospace"',
      fontWeight: 700,
      textShadow: '0 0 8px #00ff41, 0 0 16px #00ff41',
    },
    h3: {
      fontFamily: '"Courier New", "Monaco", "Consolas", "monospace"',
      fontWeight: 700,
      textShadow: '0 0 6px #00ff41, 0 0 12px #00ff41',
    },
    h4: {
      fontFamily: '"Courier New", "Monaco", "Consolas", "monospace"',
      fontWeight: 600,
    },
    h5: {
      fontFamily: '"Courier New", "Monaco", "Consolas", "monospace"',
      fontWeight: 600,
    },
    h6: {
      fontFamily: '"Courier New", "Monaco", "Consolas", "monospace"',
      fontWeight: 600,
    },
    body1: {
      fontFamily: '"Courier New", "Monaco", "Consolas", "monospace"',
    },
    body2: {
      fontFamily: '"Courier New", "Monaco", "Consolas", "monospace"',
    },
  },
  components: {
    MuiButton: {
      styleOverrides: {
        root: {
          textTransform: 'none',
          fontWeight: 600,
          boxShadow: '0 0 10px currentColor',
          '&:hover': {
            boxShadow: '0 0 20px currentColor, 0 0 30px currentColor',
            transform: 'translateY(-2px)',
          },
          transition: 'all 0.3s ease',
        },
        contained: {
          boxShadow: '0 0 15px currentColor',
        },
      },
    },
    MuiCard: {
      styleOverrides: {
        root: {
          background: 'linear-gradient(135deg, #1a1a1a 0%, #0f0f0f 100%)',
          border: '1px solid #00ff41',
          boxShadow: '0 0 20px rgba(0, 255, 65, 0.3), inset 0 0 20px rgba(0, 255, 65, 0.1)',
          '&:hover': {
            boxShadow: '0 0 30px rgba(0, 255, 65, 0.5), inset 0 0 30px rgba(0, 255, 65, 0.2)',
            borderColor: '#00ffff',
          },
          transition: 'all 0.3s ease',
        },
      },
    },
    MuiTextField: {
      styleOverrides: {
        root: {
          '& .MuiOutlinedInput-root': {
            '& fieldset': {
              borderColor: '#00ff41',
              borderWidth: '2px',
            },
            '&:hover fieldset': {
              borderColor: '#00ffff',
              boxShadow: '0 0 10px rgba(0, 255, 255, 0.3)',
            },
            '&.Mui-focused fieldset': {
              borderColor: '#00ffff',
              boxShadow: '0 0 15px rgba(0, 255, 255, 0.5)',
            },
          },
          '& .MuiInputLabel-root': {
            color: '#00ff41',
          },
          '& .MuiInputLabel-root.Mui-focused': {
            color: '#00ffff',
          },
        },
      },
    },
    MuiAppBar: {
      styleOverrides: {
        root: {
          background: 'linear-gradient(135deg, #0a0a0a 0%, #1a1a1a 100%)',
          borderBottom: '2px solid #00ff41',
          boxShadow: '0 0 20px rgba(0, 255, 65, 0.5)',
        },
      },
    },
    MuiDrawer: {
      styleOverrides: {
        paper: {
          background: 'linear-gradient(180deg, #0a0a0a 0%, #1a1a1a 100%)',
          borderRight: '2px solid #00ff41',
          boxShadow: '0 0 20px rgba(0, 255, 65, 0.3)',
        },
      },
    },
    MuiListItemButton: {
      styleOverrides: {
        root: {
          '&:hover': {
            background: 'rgba(0, 255, 65, 0.1)',
            boxShadow: 'inset 0 0 10px rgba(0, 255, 65, 0.2)',
          },
          '&.Mui-selected': {
            background: 'rgba(0, 255, 65, 0.2)',
            borderLeft: '3px solid #00ff41',
            boxShadow: 'inset 0 0 15px rgba(0, 255, 65, 0.3)',
          },
        },
      },
    },
    MuiAlert: {
      styleOverrides: {
        root: {
          border: '1px solid currentColor',
          boxShadow: '0 0 15px rgba(0, 255, 65, 0.3)',
        },
      },
    },
  },
})

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <BrowserRouter>
      <ThemeProvider theme={theme}>
        <CssBaseline />
        <App />
      </ThemeProvider>
    </BrowserRouter>
  </React.StrictMode>,
)
