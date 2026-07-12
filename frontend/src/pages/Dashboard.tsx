import React, { useState, useEffect, useCallback } from 'react';
import { useNavigate } from 'react-router-dom';
import {
  Container,
  Box,
  Typography,
  Grid,
  Paper,
  TextField,
  InputAdornment,
  CircularProgress,
  Button,
} from '@mui/material';
import {
  Search as SearchIcon,
  School,
  TrendingUp,
  EmojiEvents,
  ArrowForward,
} from '@mui/icons-material';
import { useAuth } from '../context/AuthContext';
import { getCourses, Course } from '../api/courses';
import { getMyEnrollments, enrollInCourse } from '../api/enrollments';
import CourseCard from '../components/common/CourseCard';
import AuthModal from '../components/auth/AuthModal';
import { toast } from 'react-toastify';

const Dashboard: React.FC = () => {
  const { user } = useAuth();
  const navigate = useNavigate();
  const [courses, setCourses] = useState<Course[]>([]);
  const [enrollments, setEnrollments] = useState<number[]>([]);
  const [loading, setLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedCourseId, setSelectedCourseId] = useState<number | null>(null);
  const [showAuthModal, setShowAuthModal] = useState(false);

   
  const fetchData = useCallback(async () => {
    try {
      
      const coursesData = await getCourses();
      setCourses(coursesData);
      
      
      if (user) {
        const enrollmentsData = await getMyEnrollments();
        setEnrollments(enrollmentsData);
      } else {
        setEnrollments([]);
      }
    } catch (error) {
      console.error('Error fetching data:', error);
    } finally {
      setLoading(false);
    }
  }, [user]);

  useEffect(() => {
    fetchData();
  }, [fetchData]);

  const handleEnroll = async (courseId: number) => {
    if (!user) {
      setSelectedCourseId(courseId);
      setShowAuthModal(true);
      return;
    }

    try {
      await enrollInCourse(courseId);
      toast.success('Enrolled successfully!');
      setEnrollments([...enrollments, courseId]);
      await fetchData();
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

  const handleAuthSuccess = async () => {
    if (selectedCourseId) {
      try {
        await enrollInCourse(selectedCourseId);
        toast.success('Enrolled successfully!');
        const enrollmentsData = await getMyEnrollments();
        setEnrollments(enrollmentsData);
        setSelectedCourseId(null);
        await fetchData();
      } catch (error) {
        toast.error('Failed to enroll');
      }
    }
    setShowAuthModal(false);
  };

  const filteredCourses = courses.filter((course: Course) =>
    course.title.toLowerCase().includes(searchTerm.toLowerCase()) ||
    course.category.toLowerCase().includes(searchTerm.toLowerCase())
  );

  const enrolledCourses = courses.filter((c) => enrollments.includes(c.id));
  const recommendedCourses = courses.filter((c) => !enrollments.includes(c.id)).slice(0, 3);

  if (loading) {
    return (
      <Box sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '80vh' }}>
        <CircularProgress />
      </Box>
    );
  }

  return (
    <Box sx={{ bgcolor: '#F8F9FE', minHeight: '100vh', pb: 6 }}>
      <Container maxWidth="lg">
        {/* Welcome Section */}
        <Box sx={{ pt: 4, pb: 3 }}>
          <Typography
            variant="h4"
            sx={{ fontWeight: 800, color: '#1A1A2E', mb: 0.5 }}
          >
            Welcome back, {user?.full_name?.split(' ')[0] || 'Student'} 👋
          </Typography>
          <Typography variant="body1" color="text.secondary">
            {user ? 'Continue your learning journey with Mentora' : 'Login to enroll in courses and track your progress'}
          </Typography>
        </Box>

       
        {user && (
          <Grid container spacing={3} sx={{ mb: 4 }}>
            <Grid size={{ xs: 12, sm: 6, md: 3 }}>
              <Paper sx={{ p: 3, textAlign: 'center', bgcolor: 'white' }}>
                <School sx={{ fontSize: 32, color: '#6C63FF', mb: 1 }} />
                <Typography variant="h4" sx={{ fontWeight: 700 }}>{enrollments.length}</Typography>
                <Typography variant="body2" color="text.secondary">Enrolled Courses</Typography>
              </Paper>
            </Grid>
            <Grid size={{ xs: 12, sm: 6, md: 3 }}>
              <Paper sx={{ p: 3, textAlign: 'center', bgcolor: 'white' }}>
                <TrendingUp sx={{ fontSize: 32, color: '#2ECC71', mb: 1 }} />
                <Typography variant="h4" sx={{ fontWeight: 700 }}>75%</Typography>
                <Typography variant="body2" color="text.secondary">Average Progress</Typography>
              </Paper>
            </Grid>
            <Grid size={{ xs: 12, sm: 6, md: 3 }}>
              <Paper sx={{ p: 3, textAlign: 'center', bgcolor: 'white' }}>
                <EmojiEvents sx={{ fontSize: 32, color: '#F39C12', mb: 1 }} />
                <Typography variant="h4" sx={{ fontWeight: 700 }}>4</Typography>
                <Typography variant="body2" color="text.secondary">Certificates</Typography>
              </Paper>
            </Grid>
            <Grid size={{ xs: 12, sm: 6, md: 3 }}>
              <Paper sx={{ p: 3, textAlign: 'center', bgcolor: 'white' }}>
                <Box sx={{ fontSize: 32, mb: 1 }}>🔥</Box>
                <Typography variant="h4" sx={{ fontWeight: 700 }}>12</Typography>
                <Typography variant="body2" color="text.secondary">Day Streak</Typography>
              </Paper>
            </Grid>
          </Grid>
        )}

       
        {user && enrollments.length > 0 && (
          <Box sx={{ mb: 4 }}>
            <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 2 }}>
              <Typography variant="h5" sx={{ fontWeight: 700 }}>📚 My Learning</Typography>
              <Button
                endIcon={<ArrowForward />}
                sx={{ color: '#6C63FF' }}
                onClick={() => navigate('/my-courses')}
              >
                View All
              </Button>
            </Box>
            <Grid container spacing={3}>
              {enrolledCourses.slice(0, 3).map((course) => (
                <Grid size={{ xs: 12, md: 4 }} key={course.id}>
                  <CourseCard
                    course={course}
                    isEnrolled={true}
                    progress={Math.floor(Math.random() * 100)}
                    onEnroll={() => {}}
                    onClick={() => handleCourseClick(course.id)}
                  />
                </Grid>
              ))}
            </Grid>
          </Box>
        )}

        {/* All Courses Section -all time*/}
        <Box>
          <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 2 }}>
            <Typography variant="h5" sx={{ fontWeight: 700 }}>🎯 All Courses</Typography>
            <Typography variant="body2" color="text.secondary">
              {filteredCourses.length} courses available
            </Typography>
          </Box>

          <TextField
            fullWidth
            placeholder="Search courses by title or category..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            sx={{ mb: 4 }}
            slotProps={{
              input: {
                startAdornment: (
                  <InputAdornment position="start">
                    <SearchIcon sx={{ color: '#9CA3AF' }} />
                  </InputAdornment>
                ),
                sx: {
                  bgcolor: 'white',
                  borderRadius: 3,
                  '&:hover': { boxShadow: '0 4px 12px rgba(108, 99, 255, 0.08)' },
                },
              },
            }}
          />

          <Grid container spacing={3}>
            {filteredCourses.length === 0 ? (
              <Grid size={{ xs: 12 }}>
                <Paper sx={{ p: 6, textAlign: 'center', bgcolor: 'white' }}>
                  <Typography variant="h6" color="text.secondary">
                    No courses found matching your search
                  </Typography>
                </Paper>
              </Grid>
            ) : (
              filteredCourses.map((course: Course) => (
                <Grid size={{ xs: 12, sm: 6, md: 4 }} key={course.id}>
                  <CourseCard
                    course={course}
                    isEnrolled={enrollments.includes(course.id)}
                    progress={Math.floor(Math.random() * 100)}
                    onEnroll={() => handleEnroll(course.id)}
                    onClick={() => handleCourseClick(course.id)}
                  />
                </Grid>
              ))
            )}
          </Grid>
        </Box>

        {/* Recommended Courses -*/}
        {!user && recommendedCourses.length > 0 && (
          <Box sx={{ mt: 4 }}>
            <Typography variant="h5" sx={{ fontWeight: 700, mb: 2 }}>
              🔥 Recommended for You
            </Typography>
            <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
              Login to enroll in these courses
            </Typography>
            <Grid container spacing={3}>
              {recommendedCourses.map((course) => (
                <Grid size={{ xs: 12, md: 4 }} key={course.id}>
                  <CourseCard
                    course={course}
                    isEnrolled={false}
                    onEnroll={() => handleEnroll(course.id)}
                    onClick={() => handleCourseClick(course.id)}
                  />
                </Grid>
              ))}
            </Grid>
          </Box>
        )}

        {/* Auth Modal */}
        <AuthModal
          open={showAuthModal}
          onClose={() => setShowAuthModal(false)}
          onSuccess={handleAuthSuccess}
        />
      </Container>
    </Box>
  );
};

export default Dashboard;