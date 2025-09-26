import { createTheme } from '@mui/material/styles';

const theme = createTheme({
  palette: {
    primary: {
      main: '#111111',
      light: '#3f3f3f',
      dark: '#000000'
    },
    secondary: {
      main: '#4b5563',
      light: '#6b7280',
      dark: '#1f2937'
    },
    background: {
      default: '#ffffff',
      paper: '#ffffff'
    },
    text: {
      primary: '#0f172a',
      secondary: '#4b5563'
    },
    divider: '#e2e8f0',
    success: {
      main: '#16a34a',
      light: '#dcfce7',
      dark: '#15803d'
    },
    warning: {
      main: '#f97316'
    }
  },
  typography: {
    fontFamily: '"Inter", "Roboto", "Helvetica", "Arial", sans-serif',
    h4: {
      fontWeight: 700
    },
    h5: {
      fontWeight: 600
    }
  },
  shape: {
    borderRadius: 12
  },
  components: {
    MuiButton: {
      styleOverrides: {
        root: {
          textTransform: 'none',
          borderRadius: 8,
          padding: '8px 16px'
        }
      }
    },
    MuiPaper: {
      styleOverrides: {
        root: {
          borderRadius: 12
        }
      }
    }
  }
});

export default theme;
