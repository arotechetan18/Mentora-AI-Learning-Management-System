import React from 'react';
import { Link } from 'react-router-dom';
import { Container, Box, Typography, Button, Paper } from '@mui/material';

const Home: React.FC = () => {
  return (
    <Container>
      <Box sx={{ mt: 8, textAlign: 'center' }}>
        <Paper elevation={3} sx={{ p: 6 }}>
          <Typography variant="h2" gutterBottom>
            🎓 AI Learning Management System
          </Typography>
          {/* ✅ paragraph ऐवजी sx वापरा */}
          <Typography variant="h5" color="text.secondary" sx={{ mb: 2 }}>
            Learn, Practice, and Grow with AI-powered assistance
          </Typography>
          <Box sx={{ mt: 4, display: 'flex', gap: 2, justifyContent: 'center' }}>
            <Button
              component={Link}
              to="/register"
              variant="contained"
              size="large"
            >
              Get Started
            </Button>
            <Button
              component={Link}
              to="/login"
              variant="outlined"
              size="large"
            >
              Login
            </Button>
          </Box>
        </Paper>
      </Box>
    </Container>
  );
};

export default Home;