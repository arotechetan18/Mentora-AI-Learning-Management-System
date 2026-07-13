import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import {
  Container,
  Box,
  Typography,
  Grid,
  CircularProgress,
  Alert,
} from '@mui/material';
import { useAuth } from '../context/AuthContext';
import { getCourses, Course } from '../api/courses';
import { getMyEnrollments } from '../api/enrollments';
import CourseCard from '../components/common/CourseCard';

const MyCourses: React.FC = () => {
  const { user } = useAuth();
  const navigate = useNavigate();
  const [courses, setCourses] = useState<Course[]>([]);
  const [enrollments, setEnrollments] = useState<number[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    if (!user) {
      navigate('/login');
      return;
    }
    fetchMyCourses();
  }, [user]);

  const fetchMyCourses = async () => {
    try {
      const [coursesData, enrollmentsData] = await Promise.all([
        getCourses(),
        getMyEnrollments(),
      ]);
      
      // Filter only enrolled courses
      const myCourses = coursesData.filter((c: Course) => 
        enrollmentsData.includes(c.id)
      );
      
      setCourses(myCourses);
      setEnrollments(enrollmentsData);
    } catch (err) {
      setError('Failed to load your courses');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleCourseClick = (courseId: number) => {
    navigate(`/course/${courseId}`);
  };

  if (loading) {
    return (
      <Box sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '80vh' }}>
        <CircularProgress />
      </Box>
    );
  }

  return (
    <Container maxWidth="lg">
      <Box sx={{ mt: 4, mb: 4 }}>
        <Typography variant="h4" gutterBottom sx={{ fontWeight: 700 }}>
          📚 My Learning
        </Typography>
        <Typography variant="body1" color="text.secondary" sx={{ mb: 3 }}>
          {courses.length} courses enrolled
        </Typography>

        {error && <Alert severity="error" sx={{ mb: 3 }}>{error}</Alert>}

        {courses.length === 0 ? (
          <Box sx={{ textAlign: 'center', py: 8 }}>
            <Typography variant="h6" color="text.secondary">
              You haven't enrolled in any courses yet.
            </Typography>
            <Typography variant="body2" color="text.secondary" sx={{ mt: 1 }}>
              Browse our courses and start learning today!
            </Typography>
          </Box>
        ) : (
          <Grid container spacing={3}>
            {courses.map((course: Course) => (
              <Grid size={{ xs: 12, sm: 6, md: 4 }} key={course.id}>
                <CourseCard
                  course={course}
                  isEnrolled={true}
                  progress={course.progress || 0}
                  onEnroll={() => {}}
                  onClick={() => handleCourseClick(course.id)}
                />
              </Grid>
            ))}
          </Grid>
        )}
      </Box>
    </Container>
  );
};

export default MyCourses;