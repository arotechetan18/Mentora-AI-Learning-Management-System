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
  Stack,
} from '@mui/material';
import {
  Search as SearchIcon,
  School,
  TrendingUp,
  EmojiEvents,
  ArrowForward,
  Login as LoginIcon,
  Rocket as RocketIcon,
} from '@mui/icons-material';
import { useAuth } from '../context/AuthContext';
import { getCourses, Course } from '../api/courses';
import { getMyEnrollments, enrollInCourse } from '../api/enrollments';
import { getCourseProgress } from '../api/progress';
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

  // ✅ Real progress fetch
const fetchData = useCallback(async () => {
  try {
    console.log("🔄 Fetching courses...");
    const coursesData = await getCourses();
    console.log("✅ Courses Data from API:", coursesData);  // ✅ हे Check करा
    console.log("📊 Number of courses:", coursesData.length);
    setCourses(coursesData);
    
    if (user) {
      const enrollmentsData = await getMyEnrollments();
      console.log("✅ Enrollments:", enrollmentsData);
      setEnrollments(enrollmentsData);
    }
  } catch (error) {
    console.error("❌ Error fetching data:", error);
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
        await fetchData();
        setSelectedCourseId(null);
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
          {user ? (
            <>
              <Typography variant="h4" sx={{ fontWeight: 800, color: '#1A1A2E', mb: 0.5 }}>
                Welcome back, {user?.full_name?.split(' ')[0] || 'Student'} 👋
              </Typography>
              <Typography variant="body1" color="text.secondary">
                Continue your learning journey with Mentora
              </Typography>
            </>
          ) : (
            <Box sx={{ p: 4, background: 'linear-gradient(135deg, #6C63FF 0%, #4A42D9 100%)', borderRadius: 3, color: 'white' }}>
              <Grid container spacing={3}>
                <Grid size={{ xs: 12, md: 8 }}>
                  <Typography variant="h4" sx={{ fontWeight: 700, mb: 1 }}>
                    🚀 Start Your Learning Journey
                  </Typography>
                  <Typography variant="body1" sx={{ opacity: 0.9, mb: 2 }}>
                    Join Mentora and unlock thousands of courses.
                  </Typography>
                  <Stack direction={{ xs: 'column', sm: 'row' }} spacing={2}>
                    <Button variant="contained" size="large" startIcon={<RocketIcon />} onClick={() => navigate('/register')} sx={{ bgcolor: 'white', color: '#6C63FF' }}>
                      Get Started Free
                    </Button>
                    <Button variant="outlined" size="large" startIcon={<LoginIcon />} onClick={() => navigate('/login')} sx={{ borderColor: 'white', color: 'white' }}>
                      Login
                    </Button>
                  </Stack>
                </Grid>
                <Grid size={{ xs: 12, md: 4 }} sx={{ display: { xs: 'none', md: 'block' } }}>
                  <Box sx={{ textAlign: 'center', fontSize: 64 }}>🎓</Box>
                </Grid>
              </Grid>
            </Box>
          )}
        </Box>

        {/* Stats - Login असेल तरच */}
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

        {/* My Learning */}
        {user && enrolledCourses.length > 0 && (
          <Box sx={{ mb: 4 }}>
            <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 2 }}>
              <Typography variant="h5" sx={{ fontWeight: 700 }}>📚 My Learning</Typography>
              <Button endIcon={<ArrowForward />} sx={{ color: '#6C63FF' }} onClick={() => navigate('/my-courses')}>View All</Button>
            </Box>
            <Grid container spacing={3}>
              {enrolledCourses.slice(0, 3).map((course: Course) => (
                <Grid size={{ xs: 12, md: 4 }} key={course.id}>
                  <CourseCard
                    course={course}
                    isEnrolled={true}
                    progress={course.progress || 0}  //  Real Progress
                    onEnroll={() => {}}
                    onClick={() => handleCourseClick(course.id)}
                  />
                </Grid>
              ))}
            </Grid>
          </Box>
        )}

        {/* All Courses */}
        <Box>
          <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 2 }}>
            <Typography variant="h5" sx={{ fontWeight: 700 }}>🎯 All Courses</Typography>
            <Typography variant="body2" color="text.secondary">{filteredCourses.length} courses available</Typography>
          </Box>

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
                    <SearchIcon sx={{ color: '#9CA3AF' }} />
                  </InputAdornment>
                ),
                sx: { bgcolor: 'white', borderRadius: 3 },
              },
            }}
          />

          <Grid container spacing={3}>
            {filteredCourses.map((course: Course) => (
              <Grid size={{ xs: 12, sm: 6, md: 4 }} key={course.id}>
                <CourseCard
                  course={course}
                  isEnrolled={enrollments.includes(course.id)}
                  progress={course.progress || 0}  // ✅ Real Progress
                  onEnroll={() => handleEnroll(course.id)}
                  onClick={() => handleCourseClick(course.id)}
                />
              </Grid>
            ))}
          </Grid>
        </Box>

        <AuthModal open={showAuthModal} onClose={() => setShowAuthModal(false)} onSuccess={handleAuthSuccess} />
      </Container>
    </Box>
  );
};

export default Dashboard;