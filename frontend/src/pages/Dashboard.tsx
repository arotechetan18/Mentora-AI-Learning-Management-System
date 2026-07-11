import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import {
  Container,
  Box,
  Typography,
  Grid,
  Card,
  CardContent,
  Paper,
  LinearProgress,
  Button,
} from '@mui/material';
import { useAuth } from '../context/AuthContext';
import { getCourses } from '../api/courses';

const Dashboard: React.FC = () => {
  const { user } = useAuth();
  const navigate = useNavigate();
  const [courses, setCourses] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchCourses();
  }, []);

  const fetchCourses = async () => {
    try {
      const data = await getCourses();
      setCourses(data);
    } catch (error) {
      console.error('Error fetching courses:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleCourseClick = (courseId: number) => {
    navigate(`/course/${courseId}`);
  };

  if (loading) return <Box sx={{ p: 4 }}><Typography>Loading...</Typography></Box>;

  return (
    <Container>
      <Box sx={{ mt: 4 }}>
        <Typography variant="h4" gutterBottom>
          Dashboard
        </Typography>
        <Paper elevation={3} sx={{ p: 3, mb: 3 }}>
          <Typography variant="h6">
            Welcome, {user?.full_name || 'Student'}! 👋
          </Typography>
          <Typography color="text.secondary">
            Role: {user?.role} | You are enrolled in {courses.length} courses
          </Typography>
        </Paper>

        <Typography variant="h5" gutterBottom>
          Your Courses
        </Typography>
        <Grid container spacing={3}>
          {courses.map((course) => (
            <Grid size={{ xs: 12, md: 6 }} key={course.id}>
              <Card
                sx={{
                  cursor: 'pointer',
                  '&:hover': { boxShadow: 6 },
                }}
                onClick={() => handleCourseClick(course.id)}
              >
                <CardContent>
                  <Typography variant="h6">{course.title}</Typography>
                  <Typography color="text.secondary" gutterBottom>
                    {course.category} • {course.difficulty}
                  </Typography>
                  <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
                    <LinearProgress
                      variant="determinate"
                      value={course.progress || 0}
                      sx={{ flex: 1 }}
                    />
                    <Typography variant="body2">
                      {course.progress || 0}%
                    </Typography>
                  </Box>
                  <Button size="small" sx={{ mt: 2 }}>
                    Continue Learning
                  </Button>
                </CardContent>
              </Card>
            </Grid>
          ))}
        </Grid>
      </Box>
    </Container>
  );
};

export default Dashboard;