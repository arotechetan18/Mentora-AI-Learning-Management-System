import React from 'react';
import { Container, Box, Typography, Paper, Grid, Card, CardContent } from '@mui/material';
import { useAuth } from '../context/AuthContext';

const Dashboard: React.FC = () => {
  const { user } = useAuth();

  return (
    <Container>
      <Box sx={{ mt: 4 }}>
        <Typography variant="h4" gutterBottom>
          Dashboard
        </Typography>
        <Paper elevation={3} sx={{ p: 3, mb: 3 }}>
          <Typography variant="h6">
            Welcome, {user?.full_name}! 👋
          </Typography>
          <Typography color="text.secondary">
            Role: {user?.role}
          </Typography>
        </Paper>

        {/* ✅ Grid2 वापरा किंवा Grid container मध्ये item वापरा */}
        <Grid container spacing={3}>
          <Grid size={{ xs: 12, md: 4 }}>
            <Card>
              <CardContent>
                <Typography variant="h5">📚 Courses</Typography>
                <Typography variant="h3">0</Typography>
                <Typography color="text.secondary">Enrolled Courses</Typography>
              </CardContent>
            </Card>
          </Grid>
          <Grid size={{ xs: 12, md: 4 }}>
            <Card>
              <CardContent>
                <Typography variant="h5">✅ Quizzes</Typography>
                <Typography variant="h3">0</Typography>
                <Typography color="text.secondary">Completed Quizzes</Typography>
              </CardContent>
            </Card>
          </Grid>
          <Grid size={{ xs: 12, md: 4 }}>
            <Card>
              <CardContent>
                <Typography variant="h5">🎯 Progress</Typography>
                <Typography variant="h3">0%</Typography>
                <Typography color="text.secondary">Overall Progress</Typography>
              </CardContent>
            </Card>
          </Grid>
        </Grid>
      </Box>
    </Container>
  );
};

export default Dashboard;