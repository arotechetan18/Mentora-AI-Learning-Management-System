import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import {
  Container,
  Box,
  Typography,
  Paper,
  Button,
  Chip,
  Grid,
  Accordion,
  AccordionSummary,
  AccordionDetails,
  List,
  ListItem,
  ListItemText,
  ListItemIcon,
  CircularProgress,
  Alert,
  Divider,
  LinearProgress,
} from '@mui/material';
import {
  ExpandMore,
  PlayArrow,
  Lock,
  School,
  Timer,
  Language,
  AttachMoney,
  DoneAll,
  RadioButtonUnchecked,
} from '@mui/icons-material';
import { useAuth } from '../context/AuthContext';
import { getCourse, getCourseModules, Course, Module, Lesson } from '../api/courses';
import { enrollInCourse, getMyEnrollments } from '../api/enrollments';
import { getCourseProgress, getCompletedLessons } from '../api/progress'; // ✅ ADD
import { toast } from 'react-toastify';

const CourseDetails: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const { user } = useAuth();
  const [course, setCourse] = useState<Course | null>(null);
  const [modules, setModules] = useState<Module[]>([]);
  const [loading, setLoading] = useState(true);
  const [isEnrolled, setIsEnrolled] = useState(false);
  const [error, setError] = useState('');
  const [courseProgress, setCourseProgress] = useState(0);

  useEffect(() => {
    if (id) {
      fetchCourseDetails(Number(id));
    }
  }, [id, user]);

  const fetchCourseDetails = async (courseId: number) => {
    try {
      setLoading(true);
      
      const [courseData, modulesData, enrollmentsData] = await Promise.all([
        getCourse(courseId),
        getCourseModules(courseId),
        user ? getMyEnrollments() : Promise.resolve([]),
      ]);
      
      setCourse(courseData);
      setIsEnrolled(enrollmentsData.includes(courseId));
      
      if (user && enrollmentsData.includes(courseId)) {
        try {
          // Get course progress
          const progress = await getCourseProgress(courseId);
          console.log("📊 Course Progress:", progress);
          setCourseProgress(progress.progress || 0);
          
          // Get completed lesson IDs
          const completedIds = await getCompletedLessons(courseId);
          console.log("✅ Completed Lessons:", completedIds);
          
          // Mark only completed lessons
          const updatedModules = modulesData.map((module: Module) => ({
            ...module,
            lessons: module.lessons?.map((lesson: Lesson) => ({
              ...lesson,
              is_completed: completedIds.includes(lesson.id)  // Only true if in list
            }))
          }));
          setModules(updatedModules);
        } catch (err) {
          console.error("❌ Error fetching progress:", err);
          setModules(modulesData);
        }
      } else {
        setModules(modulesData);
      }
      
      setLoading(false);
    } catch (err) {
      setError('Failed to load course details');
      console.error(err);
      setLoading(false);
    }
  };

  const handleEnroll = async () => {
    if (!user) {
      toast.info('Please login to enroll');
      navigate('/login');
      return;
    }

    try {
      await enrollInCourse(Number(id));
      setIsEnrolled(true);
      toast.success('Enrolled successfully!');
      fetchCourseDetails(Number(id));
    } catch (error: any) {
      if (error.response?.data?.detail === 'Already enrolled') {
        toast.info('Already enrolled in this course');
        setIsEnrolled(true);
      } else {
        toast.error('Failed to enroll');
      }
    }
  };

  const handleLessonClick = (lessonId: number) => {
    if (isEnrolled) {
      navigate(`/lesson/${lessonId}`);
    } else {
      toast.info('Please enroll to access lessons');
    }
  };

  if (loading) {
    return (
      <Box sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '80vh' }}>
        <CircularProgress />
      </Box>
    );
  }

  if (error || !course) {
    return (
      <Container>
        <Alert severity="error" sx={{ mt: 4 }}>{error || 'Course not found'}</Alert>
      </Container>
    );
  }

  return (
    <Container maxWidth="lg">
      <Box sx={{ mt: 4, mb: 4 }}>
        <Paper elevation={3} sx={{ p: 4, mb: 4 }}>
          {/* Header with Course Progress */}
          <Box sx={{ display: 'flex', alignItems: 'center', gap: 2, mb: 3, flexWrap: 'wrap' }}>
            <Typography variant="h4" sx={{ fontWeight: 700 }}>
              {course.title}
            </Typography>
            {isEnrolled && (
              <Chip
                label={`${Math.round(courseProgress)}% Complete`}
                sx={{ 
                  bgcolor: courseProgress >= 100 ? '#2ECC71' : 
                           courseProgress >= 50 ? '#F39C12' : '#6C63FF',
                  color: 'white',
                  fontWeight: 600,
                  fontSize: '14px',
                  px: 1,
                }}
              />
            )}
          </Box>

          {/* Course Progress Bar */}
          {isEnrolled && (
            <Box sx={{ mb: 4 }}>
              <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 1 }}>
                <Typography variant="body2" color="text.secondary">
                  Course Progress
                </Typography>
                <Typography variant="body2" sx={{ fontWeight: 600 }}>
                  {Math.round(courseProgress)}%
                </Typography>
              </Box>
              <LinearProgress
                variant="determinate"
                value={courseProgress}
                sx={{
                  height: 8,
                  borderRadius: 4,
                  bgcolor: 'rgba(108, 99, 255, 0.1)',
                  '& .MuiLinearProgress-bar': {
                    background: 'linear-gradient(90deg, #6C63FF 0%, #4A42D9 100%)',
                    borderRadius: 4,
                  },
                }}
              />
            </Box>
          )}

          <Typography variant="body1" color="text.secondary" sx={{ mb: 3 }}>
            {course.description}
          </Typography>

          {/* At a glance */}
          <Grid container spacing={2} sx={{ mb: 3 }}>
            <Grid size={{ xs: 6, sm: 3 }}>
              <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                <Timer sx={{ color: '#6C63FF' }} />
                <Box>
                  <Typography variant="caption" color="text.secondary">Duration</Typography>
                  <Typography variant="body2" sx={{ fontWeight: 600 }}>{course.duration}h</Typography>
                </Box>
              </Box>
            </Grid>
            <Grid size={{ xs: 6, sm: 3 }}>
              <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                <School sx={{ color: '#6C63FF' }} />
                <Box>
                  <Typography variant="caption" color="text.secondary">Level</Typography>
                  <Typography variant="body2" sx={{ fontWeight: 600, textTransform: 'capitalize' }}>
                    {course.difficulty}
                  </Typography>
                </Box>
              </Box>
            </Grid>
            <Grid size={{ xs: 6, sm: 3 }}>
              <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                <Language sx={{ color: '#6C63FF' }} />
                <Box>
                  <Typography variant="caption" color="text.secondary">Language</Typography>
                  <Typography variant="body2" sx={{ fontWeight: 600 }}>English</Typography>
                </Box>
              </Box>
            </Grid>
            <Grid size={{ xs: 6, sm: 3 }}>
              <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                <AttachMoney sx={{ color: '#6C63FF' }} />
                <Box>
                  <Typography variant="caption" color="text.secondary">Price</Typography>
                  <Typography variant="body2" sx={{ fontWeight: 600 }}>
                    {course.price === 0 ? 'Free' : `₹${course.price}`}
                  </Typography>
                </Box>
              </Box>
            </Grid>
          </Grid>

          <Divider sx={{ my: 3 }} />

          {/* Table of Contents */}
          <Typography variant="h6" sx={{ fontWeight: 600, mb: 2 }}>
            📖 Table of Contents
          </Typography>
          <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
            {modules.reduce((acc, m) => acc + (m.lessons?.length || 0), 0)} lessons • {modules.length} modules
          </Typography>

          {modules.length === 0 ? (
            <Alert severity="info">No modules available for this course yet.</Alert>
          ) : (
            modules.map((module: Module, index: number) => (
              <Accordion key={module.id} defaultExpanded={index === 0} sx={{ mb: 1 }}>
                <AccordionSummary expandIcon={<ExpandMore />}>
                  <Box sx={{ display: 'flex', alignItems: 'center', gap: 2, width: '100%' }}>
                    <Typography variant="subtitle1" sx={{ fontWeight: 600 }}>
                      {module.title}
                    </Typography>
                    <Chip
                      label={`${module.lessons?.length || 0} lessons`}
                      size="small"
                      variant="outlined"
                    />
                  </Box>
                </AccordionSummary>
                <AccordionDetails>
                  <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
                    {module.description}
                  </Typography>
                  <List>
                    {module.lessons?.map((lesson: Lesson) => (
                      <ListItem
                        key={lesson.id}
                        component="div"
                        onClick={() => handleLessonClick(lesson.id)}
                        sx={{
                          borderRadius: 1,
                          mb: 0.5,
                          cursor: isEnrolled ? 'pointer' : 'default',
                          bgcolor: lesson.is_completed ? 'rgba(46, 204, 113, 0.1)' : 'transparent',
                          '&:hover': {
                            bgcolor: isEnrolled ? 'action.hover' : 'transparent',
                          },
                        }}
                      >
                        <ListItemIcon sx={{ minWidth: 36 }}>
                          {lesson.is_completed ? (
                            <DoneAll sx={{ color: '#2ECC71' }} />
                          ) : (
                            <RadioButtonUnchecked sx={{ color: '#9CA3AF' }} />
                          )}
                        </ListItemIcon>
                        <ListItemText
                          primary={lesson.title}
                          secondary={`${lesson.duration} min`}
                        />
                        {lesson.is_completed && (
                          <Chip label="Completed" size="small" color="success" />
                        )}
                        {!isEnrolled && (
                          <Lock fontSize="small" color="action" />
                        )}
                      </ListItem>
                    ))}
                  </List>
                </AccordionDetails>
              </Accordion>
            ))
          )}

          {/* Action Button */}
          <Box sx={{ mt: 4, textAlign: 'center' }}>
            {isEnrolled ? (
              <Button
                variant="contained"
                size="large"
                startIcon={<PlayArrow />}
                onClick={() => {
                  const firstLesson = modules[0]?.lessons?.[0];
                  if (firstLesson) {
                    navigate(`/lesson/${firstLesson.id}`);
                  } else {
                    toast.info('No lessons available yet');
                  }
                }}
                sx={{ px: 6, py: 1.5 }}
              >
                Continue Learning
              </Button>
            ) : (
              <Button
                variant="contained"
                size="large"
                onClick={handleEnroll}
                sx={{ px: 6, py: 1.5 }}
              >
                Enroll Now
              </Button>
            )}
          </Box>
        </Paper>
      </Box>
    </Container>
  );
};

export default CourseDetails;