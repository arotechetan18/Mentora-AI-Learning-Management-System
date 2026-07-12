import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import {
  Container,
  Grid,
  Typography,
  TextField,
  Box,
  InputAdornment,
} from '@mui/material';
import SearchIcon from '@mui/icons-material/Search';
import { getCourses, Course } from '../api/courses';
import CourseCard from '../components/common/CourseCard';
import { useAuth } from '../context/AuthContext';
import { enrollInCourse } from '../api/enrollments';
import { toast } from 'react-toastify';

const Courses: React.FC = () => {
  const navigate = useNavigate();
  const { user } = useAuth();
  const [courses, setCourses] = useState<Course[]>([]);
  const [loading, setLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState('');

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

  // ✅ handleEnroll function with courseId parameter
  const handleEnroll = async (courseId: number) => {
    if (!user) {
      toast.info('Please login to enroll');
      navigate('/login');
      return;
    }

    try {
      await enrollInCourse(courseId);
      toast.success('Enrolled successfully!');
      await fetchCourses();
    } catch (error: any) {
      if (error.response?.data?.detail === 'Already enrolled') {
        toast.info('Already enrolled in this course');
      } else {
        toast.error('Failed to enroll');
      }
    }
  };

  const handleCourseClick = (courseId: number) => {
    navigate(`/course/${courseId}`);
  };

  const filteredCourses = courses.filter((course: Course) =>
    course.title.toLowerCase().includes(searchTerm.toLowerCase()) ||
    course.category.toLowerCase().includes(searchTerm.toLowerCase())
  );

  if (loading) {
    return (
      <Box sx={{ p: 4, textAlign: 'center' }}>
        <Typography>Loading courses...</Typography>
      </Box>
    );
  }

  return (
    <Container maxWidth="lg">
      <Box sx={{ mt: 4, mb: 4 }}>
        <Typography variant="h4" gutterBottom>
          All Courses
        </Typography>

        <TextField
          fullWidth
          placeholder="Search courses..."
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
          sx={{ mb: 4 }}
          slotProps={{
            input: {
              startAdornment: (
                <InputAdornment position="start">
                  <SearchIcon />
                </InputAdornment>
              ),
            },
          }}
        />

        <Grid container spacing={3}>
          {filteredCourses.length === 0 ? (
            <Grid size={{ xs: 12 }}>
              <Typography align="center" color="text.secondary">
                No courses found
              </Typography>
            </Grid>
          ) : (
            filteredCourses.map((course: Course) => (
              <Grid size={{ xs: 12, sm: 6, md: 4 }} key={course.id}>
                <CourseCard
                  course={course}
                  onEnroll={() => handleEnroll(course.id)}
                  onClick={() => handleCourseClick(course.id)}
                  isEnrolled={false}
                />
              </Grid>
            ))
          )}
        </Grid>
      </Box>
    </Container>
  );
};

export default Courses;