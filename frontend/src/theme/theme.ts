import { createTheme } from '@mui/material';

// 🎨 Mentora Brand Colors
const brandColors = {
  primary: {
    main: '#6C63FF',
    light: '#8B83FF',
    dark: '#4A42D9',
    gradient: 'linear-gradient(135deg, #6C63FF 0%, #4A42D9 100%)',
  },
  secondary: {
    main: '#FF6B6B',
    light: '#FF8E8E',
    dark: '#E55555',
  },
  success: {
    main: '#2ECC71',
    light: '#58D68D',
    dark: '#27AE60',
  },
  warning: {
    main: '#F39C12',
    light: '#F5B041',
    dark: '#D68910',
  },
  background: {
    default: '#F8F9FE',
    paper: '#FFFFFF',
    gradient: 'linear-gradient(135deg, #F8F9FE 0%, #EEF1FA 100%)',
  },
  text: {
    primary: '#1A1A2E',
    secondary: '#6B7280',
    light: '#9CA3AF',
  },
};

export const theme = createTheme({
  palette: {
    primary: brandColors.primary,
    secondary: brandColors.secondary,
    success: brandColors.success,
    warning: brandColors.warning,
    background: {
      default: brandColors.background.default,
      paper: brandColors.background.paper,
    },
    text: {
      primary: brandColors.text.primary,
      secondary: brandColors.text.secondary,
    },
  },
  typography: {
    fontFamily: '"Inter", "Segoe UI", "Roboto", sans-serif',
    h1: { fontWeight: 700, fontSize: '2.5rem' },
    h2: { fontWeight: 700, fontSize: '2rem' },
    h3: { fontWeight: 600, fontSize: '1.75rem' },
    h4: { fontWeight: 600, fontSize: '1.5rem' },
    h5: { fontWeight: 600, fontSize: '1.25rem' },
    h6: { fontWeight: 600, fontSize: '1rem' },
    body1: { fontSize: '1rem', lineHeight: 1.6 },
    body2: { fontSize: '0.875rem', lineHeight: 1.6 },
  },
  shape: {
    borderRadius: 12,
  },
  components: {
    MuiCard: {
      styleOverrides: {
        root: {
          borderRadius: 16,
          boxShadow: '0 4px 20px rgba(108, 99, 255, 0.08)',
          transition: 'all 0.3s ease',
          '&:hover': {
            boxShadow: '0 8px 40px rgba(108, 99, 255, 0.15)',
            transform: 'translateY(-4px)',
          },
        },
      },
    },
    MuiButton: {
      styleOverrides: {
        root: {
          borderRadius: 8,
          textTransform: 'none',
          fontWeight: 600,
          padding: '10px 24px',
        },
        // ✅ v7 syntax: containedPrimary ऐवजी containedPrimary वापरा पण नाव बदला
      },
    },
    MuiPaper: {
      styleOverrides: {
        root: {
          borderRadius: 16,
        },
      },
    },
    MuiChip: {
      styleOverrides: {
        root: {
          borderRadius: 8,
        },
      },
    },
  },
});

// ✅ Button variant override
export const buttonOverrides = {
  MuiButton: {
    variants: [
      {
        props: { variant: 'contained', color: 'primary' },
        style: {
          background: 'linear-gradient(135deg, #6C63FF 0%, #4A42D9 100%)',
          '&:hover': {
            background: 'linear-gradient(135deg, #5A52E6 0%, #3A32C9 100%)',
          },
        },
      },
    ],
  },
};

export default theme;