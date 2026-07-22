import React, { useState, useEffect, useCallback } from 'react';
import { useNavigate } from 'react-router-dom';
import { motion } from 'framer-motion';
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
  Avatar,
  Menu,
  MenuItem,
  IconButton,
  Divider,
  ListItemIcon,
  Tooltip,
  Card,
  CardContent,
  LinearProgress,
  Chip,
  useTheme,
} from '@mui/material';
import {
  Search as SearchIcon,
  School,
  TrendingUp,
  EmojiEvents,
  ArrowForward,
  Login as LoginIcon,
  Rocket as RocketIcon,
  Person,
  Settings,
  Logout,
  Dashboard as DashboardIcon,
  VideoLibrary,
  Assignment,
  Quiz,
  Star,
  AccessTime,
  CheckCircle,
  PlayCircle,
  Whatshot,
  AutoAwesome,
} from '@mui/icons-material';
import { useAuth } from '../context/AuthContext';
import { getCourses, Course } from '../api/courses';
import { getMyEnrollments, enrollInCourse } from '../api/enrollments';
import { getCourseProgress } from '../api/progress';
import CourseCard from '../components/common/CourseCard';
import AuthModal from '../components/auth/AuthModal';
import { toast } from 'react-toastify';

const Dashboard: React.FC = () => {
  const { user, logout } = useAuth();
  const navigate = useNavigate();
  const theme = useTheme();
  
  const [courses, setCourses] = useState<Course[]>([]);
  const [enrollments, setEnrollments] = useState<number[]>([]);
  const [loading, setLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedCourseId, setSelectedCourseId] = useState<number | null>(null);
  const [showAuthModal, setShowAuthModal] = useState(false);
  
  // Profile Menu
  const [anchorEl, setAnchorEl] = useState<null | HTMLElement>(null);
  const open = Boolean(anchorEl);

  // Stats
  const [stats, setStats] = useState({
    enrolledCourses: 0,
    averageProgress: 0,
    certificates: 0,
    streak: 0,
    totalHours: 0,
    completedLessons: 0,
  });

  const handleMenuClick = (event: React.MouseEvent<HTMLElement>) => {
    setAnchorEl(event.currentTarget);
  };

  const handleMenuClose = () => {
    setAnchorEl(null);
  };

  const handleLogout = () => {
    logout();
    handleMenuClose();
    navigate('/login');
  };

  const handleProfile = () => {
    handleMenuClose();
    navigate('/profile');
  };



const fetchData = useCallback(async () => {
  try {
    console.log("🔄 Fetching courses...");
    const coursesData = await getCourses();
    console.log("✅ Courses Data:", coursesData);
    
    if (user) {
      const enrollmentsData = await getMyEnrollments();
      console.log("✅ Enrollments:", enrollmentsData);
      setEnrollments(enrollmentsData);
      
      // ✅ Only course progress (not module)
      const progressPromises = enrollmentsData.map(async (courseId: number) => {
        try {
          const progress = await getCourseProgress(courseId);
          console.log(`📊 Course ${courseId} Progress:`, progress);
          return { courseId, progress: progress.progress || 0 };
        } catch (err) {
          console.error(`❌ Error fetching progress for course ${courseId}:`, err);
          return { courseId, progress: 0 };
        }
      });
      
      const progressResults = await Promise.all(progressPromises);
      const progressMap: { [key: number]: number } = {};
      let totalProgress = 0;
      
      progressResults.forEach((p) => {
        progressMap[p.courseId] = p.progress;
        totalProgress += p.progress;
      });
      
      // ✅ Add course progress
      setCourses(coursesData.map((c: Course) => ({
        ...c,
        progress: progressMap[c.id] || 0  // ✅ Course progress
      })));
      
      // ✅ Stats
      setStats({
        enrolledCourses: enrollmentsData.length,
        averageProgress: enrollmentsData.length > 0 ? Math.round(totalProgress / enrollmentsData.length) : 0,
        certificates: 0,
        streak: 12,
        totalHours: 0,
        completedLessons: 0,
      });
    } else {
      setCourses(coursesData);
      setEnrollments([]);
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
      toast.success('🎉 Enrolled successfully!');
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
        toast.success('🎉 Enrolled successfully!');
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

  // Animation variants
  const containerVariants = {
    hidden: { opacity: 0 },
    visible: {
      opacity: 1,
      transition: { staggerChildren: 0.1 }
    }
  };

  const itemVariants = {
    hidden: { opacity: 0, y: 20 },
    visible: { opacity: 1, y: 0 }
  };

  if (loading) {
    return (
      <Box sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '80vh' }}>
        <CircularProgress />
      </Box>
    );
  }

  return (
    <Box sx={{ bgcolor: '#F8F9FE', minHeight: '100vh', pb: 6 }}>
      <Container maxWidth="xl">
        {/* Welcome Section */}
        <motion.div
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5 }}
        >
          <Box sx={{ pt: 4, pb: 3, display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
            <Box>
              {user ? (
                <>
                  <Typography variant="h3" sx={{ fontWeight: 800, color: '#1A1A2E', mb: 0.5 }}>
                    Welcome back, {user?.full_name?.split(' ')[0] || 'Student'}! 👋
                  </Typography>
                  <Typography variant="body1" color="text.secondary" sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                    <AutoAwesome sx={{ color: '#6C63FF', fontSize: 16 }} />
                    Continue your learning journey with Mentora
                  </Typography>
                </>
              ) : (
                <Box sx={{ p: 4, background: 'linear-gradient(135deg, #6C63FF 0%, #4A42D9 100%)', borderRadius: 3, color: 'white', width: '100%' }}>
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

            {/* Profile Avatar */}
            {user && (
              <Box>
                <Tooltip title="Profile">
                  <IconButton
                    onClick={handleMenuClick}
                    size="medium"
                    sx={{ 
                      bgcolor: '#6C63FF', 
                      color: 'white',
                      '&:hover': { bgcolor: '#5A52D9' },
                      width: 48,
                      height: 48,
                    }}
                  >
                    <Avatar sx={{ bgcolor: 'transparent', width: 40, height: 40 }}>
                      {user?.full_name?.charAt(0) || 'U'}
                    </Avatar>
                  </IconButton>
                </Tooltip>

                <Menu
                  anchorEl={anchorEl}
                  open={open}
                  onClose={handleMenuClose}
                  onClick={handleMenuClose}
                  transformOrigin={{ horizontal: 'right', vertical: 'top' }}
                  anchorOrigin={{ horizontal: 'right', vertical: 'bottom' }}
                  sx={{ 
                    mt: 1,
                    '& .MuiPaper-root': {
                      minWidth: 220,
                      borderRadius: 2,
                      boxShadow: '0 4px 20px rgba(0,0,0,0.1)',
                    }
                  }}
                >
                  <Box sx={{ px: 2, py: 1.5 }}>
                    <Typography variant="subtitle1" sx={{ fontWeight: 600 }}>
                      {user?.full_name}
                    </Typography>
                    <Typography variant="body2" color="text.secondary" sx={{ fontSize: 12 }}>
                      {user?.email}
                    </Typography>
                    <Chip
                      label={user?.role || 'STUDENT'}
                      size="small"
                      sx={{ bgcolor: '#6C63FF', color: 'white', mt: 0.5, fontSize: 10, textTransform: 'uppercase' }}
                    />
                  </Box>
                  <Divider />
                  <MenuItem onClick={handleProfile}>
                    <ListItemIcon><Person fontSize="small" sx={{ color: '#6C63FF' }} /></ListItemIcon>
                    My Profile
                  </MenuItem>
                  <MenuItem onClick={() => { handleMenuClose(); navigate('/dashboard'); }}>
                    <ListItemIcon><DashboardIcon fontSize="small" sx={{ color: '#6C63FF' }} /></ListItemIcon>
                    Dashboard
                  </MenuItem>
                  <Divider />
                  <MenuItem onClick={handleLogout} sx={{ color: '#FF4444' }}>
                    <ListItemIcon><Logout fontSize="small" sx={{ color: '#FF4444' }} /></ListItemIcon>
                    Logout
                  </MenuItem>
                </Menu>
              </Box>
            )}
          </Box>
        </motion.div>

        {/* Stats Cards */}
        {user && (
          <motion.div
            variants={containerVariants}
            initial="hidden"
            animate="visible"
          >
            <Grid container spacing={3} sx={{ mb: 4 }}>
              <Grid size={{ xs: 12, sm: 6, md: 2.4 }}>
                <motion.div variants={itemVariants}>
                  <Paper sx={{ p: 2.5, textAlign: 'center', bgcolor: 'white', borderRadius: 2, position: 'relative', overflow: 'hidden' }}>
                    <Box sx={{ position: 'absolute', top: 0, left: 0, right: 0, height: 3, bgcolor: '#6C63FF' }} />
                    <School sx={{ fontSize: 32, color: '#6C63FF', mb: 0.5 }} />
                    <Typography variant="h4" sx={{ fontWeight: 700 }}>{stats.enrolledCourses}</Typography>
                    <Typography variant="body2" color="text.secondary">Enrolled Courses</Typography>
                  </Paper>
                </motion.div>
              </Grid>
              <Grid size={{ xs: 12, sm: 6, md: 2.4 }}>
                <motion.div variants={itemVariants}>
                  <Paper sx={{ p: 2.5, textAlign: 'center', bgcolor: 'white', borderRadius: 2, position: 'relative', overflow: 'hidden' }}>
                    <Box sx={{ position: 'absolute', top: 0, left: 0, right: 0, height: 3, bgcolor: '#2ECC71' }} />
                    <TrendingUp sx={{ fontSize: 32, color: '#2ECC71', mb: 0.5 }} />
                    <Typography variant="h4" sx={{ fontWeight: 700 }}>{stats.averageProgress}%</Typography>
                    <Typography variant="body2" color="text.secondary">Average Progress</Typography>
                  </Paper>
                </motion.div>
              </Grid>
              <Grid size={{ xs: 12, sm: 6, md: 2.4 }}>
                <motion.div variants={itemVariants}>
                  <Paper sx={{ p: 2.5, textAlign: 'center', bgcolor: 'white', borderRadius: 2, position: 'relative', overflow: 'hidden' }}>
                    <Box sx={{ position: 'absolute', top: 0, left: 0, right: 0, height: 3, bgcolor: '#F39C12' }} />
                    <EmojiEvents sx={{ fontSize: 32, color: '#F39C12', mb: 0.5 }} />
                    <Typography variant="h4" sx={{ fontWeight: 700 }}>{stats.certificates}</Typography>
                    <Typography variant="body2" color="text.secondary">Certificates</Typography>
                  </Paper>
                </motion.div>
              </Grid>
              <Grid size={{ xs: 12, sm: 6, md: 2.4 }}>
                <motion.div variants={itemVariants}>
                  <Paper sx={{ p: 2.5, textAlign: 'center', bgcolor: 'white', borderRadius: 2, position: 'relative', overflow: 'hidden' }}>
                    <Box sx={{ position: 'absolute', top: 0, left: 0, right: 0, height: 3, bgcolor: '#FF6B6B' }} />
                    <Whatshot sx={{ fontSize: 32, color: '#FF6B6B', mb: 0.5 }} />
                    <Typography variant="h4" sx={{ fontWeight: 700 }}>{stats.streak}</Typography>
                    <Typography variant="body2" color="text.secondary">Day Streak</Typography>
                  </Paper>
                </motion.div>
              </Grid>
              <Grid size={{ xs: 12, sm: 6, md: 2.4 }}>
                <motion.div variants={itemVariants}>
                  <Paper sx={{ p: 2.5, textAlign: 'center', bgcolor: 'white', borderRadius: 2, position: 'relative', overflow: 'hidden' }}>
                    <Box sx={{ position: 'absolute', top: 0, left: 0, right: 0, height: 3, bgcolor: '#9B59B6' }} />
                    <AccessTime sx={{ fontSize: 32, color: '#9B59B6', mb: 0.5 }} />
                    <Typography variant="h4" sx={{ fontWeight: 700 }}>{stats.totalHours}h</Typography>
                    <Typography variant="body2" color="text.secondary">Total Hours</Typography>
                  </Paper>
                </motion.div>
              </Grid>
            </Grid>
          </motion.div>
        )}

        {/* My Learning Section */}
        {user && enrolledCourses.length > 0 && (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5, delay: 0.3 }}
          >
            <Box sx={{ mb: 4 }}>
              <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 2 }}>
                <Typography variant="h5" sx={{ fontWeight: 700, display: 'flex', alignItems: 'center', gap: 1 }}>
                  <VideoLibrary sx={{ color: '#6C63FF' }} />
                  My Learning
                </Typography>
                <Button endIcon={<ArrowForward />} sx={{ color: '#6C63FF' }} onClick={() => navigate('/my-courses')}>
                  View All
                </Button>
              </Box>
              <Grid container spacing={3}>
                {enrolledCourses.slice(0, 3).map((course: Course) => (
                  <Grid size={{ xs: 12, md: 4 }} key={course.id}>
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
            </Box>
          </motion.div>
        )}

        {/* All Courses Section */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5, delay: 0.5 }}
        >
          <Box>
            <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 2 }}>
              <Typography variant="h5" sx={{ fontWeight: 700, display: 'flex', alignItems: 'center', gap: 1 }}>
                <AutoAwesome sx={{ color: '#6C63FF' }} />
                All Courses
              </Typography>
              <Typography variant="body2" color="text.secondary">{filteredCourses.length} courses available</Typography>
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
                    progress={course.progress || 0}
                    onEnroll={() => handleEnroll(course.id)}
                    onClick={() => handleCourseClick(course.id)}
                  />
                </Grid>
              ))}
            </Grid>
          </Box>
        </motion.div>

        <AuthModal open={showAuthModal} onClose={() => setShowAuthModal(false)} onSuccess={handleAuthSuccess} />
      </Container>
    </Box>
  );
};

export default Dashboard;