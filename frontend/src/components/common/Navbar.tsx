// src/components/common/Navbar.tsx
import React from 'react';
import { 
  AppBar, 
  Toolbar, 
  Typography, 
  Button, 
  Box, 
  Avatar, 
  Chip, 
  Menu, 
  MenuItem,
  Divider,
  ListItemIcon,
  IconButton,
  Tooltip,
} from '@mui/material';
import { 
  Link, 
  useNavigate 
} from 'react-router-dom';
import { 
  Person, 
  Settings, 
  Logout, 
  Dashboard as DashboardIcon,
  School,
} from '@mui/icons-material';
import { useAuth } from '../../context/AuthContext';

const Navbar: React.FC = () => {
  const { user, logout } = useAuth();
  const navigate = useNavigate();
  const [anchorEl, setAnchorEl] = React.useState<null | HTMLElement>(null);

  const handleMenuOpen = (event: React.MouseEvent<HTMLElement>) => {
    setAnchorEl(event.currentTarget);
  };

  const handleMenuClose = () => {
    setAnchorEl(null);
  };

  const handleLogout = () => {
    logout();
    navigate('/login');
    handleMenuClose();
  };

  const handleProfile = () => {
    navigate('/profile');
    handleMenuClose();
  };

  const handleDashboard = () => {
    navigate('/dashboard');
    handleMenuClose();
  };

  return (
    <AppBar
      position="sticky"
      elevation={0}
      sx={{
        background: 'rgba(255, 255, 255, 0.95)',
        backdropFilter: 'blur(20px)',
        borderBottom: '1px solid rgba(108, 99, 255, 0.08)',
      }}
    >
      <Toolbar sx={{ justifyContent: 'space-between', py: 1 }}>
        {/* Logo */}
        <Box 
          component={Link}
          to="/dashboard"
          sx={{ 
            display: 'flex', 
            alignItems: 'center', 
            gap: 1,
            textDecoration: 'none',
            cursor: 'pointer',
          }}
        >
          <Box
            sx={{
              width: 40,
              height: 40,
              background: 'linear-gradient(135deg, #6C63FF 0%, #4A42D9 100%)',
              borderRadius: 2,
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              fontSize: 20,
              fontWeight: 700,
              color: 'white',
            }}
          >
            M
          </Box>
          <Typography
            variant="h6"
            sx={{
              fontWeight: 800,
              color: '#1A1A2E',
              letterSpacing: '-0.5px',
            }}
          >
            Mentora
            <Typography component="span" sx={{ color: '#6C63FF', fontWeight: 700 }}>
              .
            </Typography>
          </Typography>
        </Box>

        {/* Navigation */}
        <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
          {user ? (
            <>
              {/* Dashboard Button */}
              <Button
                color="inherit"
                onClick={() => navigate('/dashboard')}
                startIcon={<School />}
                sx={{ 
                  color: '#1A1A2E', 
                  fontWeight: 500,
                  '&:hover': { bgcolor: 'rgba(108, 99, 255, 0.08)' },
                  display: { xs: 'none', sm: 'flex' }
                }}
              >
                Dashboard
              </Button>

              {/* Profile Chip with Menu */}
              <Chip
                avatar={
                  <Avatar sx={{ bgcolor: '#6C63FF', width: 32, height: 32 }}>
                    {user.full_name?.charAt(0)?.toUpperCase() || 'U'}
                  </Avatar>
                }
                label={user.full_name}
                onClick={handleMenuOpen}
                sx={{ 
                  cursor: 'pointer', 
                  fontWeight: 500,
                  bgcolor: 'rgba(108, 99, 255, 0.08)',
                  '&:hover': { bgcolor: 'rgba(108, 99, 255, 0.15)' },
                  px: 1,
                }}
              />

              {/* Profile Dropdown Menu */}
              <Menu
                anchorEl={anchorEl}
                open={Boolean(anchorEl)}
                onClose={handleMenuClose}
                transformOrigin={{ horizontal: 'right', vertical: 'top' }}
                anchorOrigin={{ horizontal: 'right', vertical: 'bottom' }}
                sx={{
                  mt: 1,
                  '& .MuiPaper-root': {
                    minWidth: 200,
                    borderRadius: 2,
                    boxShadow: '0 4px 20px rgba(0,0,0,0.1)',
                  }
                }}
              >
                <Box sx={{ px: 2, py: 1.5 }}>
                  <Typography variant="subtitle1" sx={{ fontWeight: 600 }}>
                    {user.full_name}
                  </Typography>
                  <Typography variant="body2" color="text.secondary" sx={{ fontSize: 12 }}>
                    {user.email}
                  </Typography>
                  <Typography variant="caption" sx={{
                    bgcolor: '#6C63FF',
                    color: 'white',
                    px: 1,
                    py: 0.3,
                    borderRadius: 1,
                    display: 'inline-block',
                    mt: 0.5,
                    fontSize: 10,
                    textTransform: 'uppercase',
                  }}>
                    {user.role || 'STUDENT'}
                  </Typography>
                </Box>
                <Divider />
                <MenuItem onClick={handleProfile}>
                  <ListItemIcon>
                    <Person fontSize="small" sx={{ color: '#6C63FF' }} />
                  </ListItemIcon>
                  My Profile
                </MenuItem>
                <MenuItem onClick={handleDashboard}>
                  <ListItemIcon>
                    <DashboardIcon fontSize="small" sx={{ color: '#6C63FF' }} />
                  </ListItemIcon>
                  Dashboard
                </MenuItem>
                <MenuItem onClick={handleProfile}>
                  <ListItemIcon>
                    <Settings fontSize="small" sx={{ color: '#6C63FF' }} />
                  </ListItemIcon>
                  Settings
                </MenuItem>
                <Divider />
                <MenuItem onClick={handleLogout} sx={{ color: '#FF4444' }}>
                  <ListItemIcon>
                    <Logout fontSize="small" sx={{ color: '#FF4444' }} />
                  </ListItemIcon>
                  Logout
                </MenuItem>
              </Menu>
            </>
          ) : (
            <>
              <Button
                onClick={() => navigate('/login')}
                sx={{ 
                  color: '#1A1A2E', 
                  fontWeight: 500,
                  '&:hover': { bgcolor: 'rgba(108, 99, 255, 0.08)' },
                }}
              >
                Login
              </Button>
              <Button
                onClick={() => navigate('/register')}
                variant="contained"
                sx={{ 
                  fontWeight: 600,
                  bgcolor: '#6C63FF',
                  '&:hover': { bgcolor: '#5A52D9' },
                }}
              >
                Get Started
              </Button>
            </>
          )}
        </Box>
      </Toolbar>
    </AppBar>
  );
};

export default Navbar;