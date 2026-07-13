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
} from '@mui/material';
import {
  ExpandMore,
  PlayArrow,
  Lock,
  School,
  Timer,
  Language,
  AttachMoney,
  DoneAll,              // ✅ Double Tick (Completed)
  RadioButtonUnchecked, // ⚪ Empty Circle (Not Completed)
} from '@mui/icons-material';
import { useAuth } from '../context/AuthContext';
import { getCourse, getCourseModules, Course, Module, Lesson } from '../api/courses';
import { enrollInCourse, getMyEnrollments } from '../api/enrollments';
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

  useEffect(() => {
    if (id) {
      fetchCourseDetails(Number(id));
    }
  }, [id, user]);

const fetchCourseDetails = async (courseId: number) => {
  try {
    const [courseData, modulesData, enrollmentsData] = await Promise.all([
      getCourse(courseId),
      getCourseModules(courseId),
      user ? getMyEnrollments() : Promise.resolve([]),
    ]);
    setCourse(courseData);
    
    
    console.log("Modules Data:", modulesData);  // Debug log
    setModules(modulesData);
    setIsEnrolled(enrollmentsData.includes(courseId));
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
        {/* Course Header */}
        <Paper elevation={3} sx={{ p: 4, mb: 4 }}>
          <Typography variant="h4" gutterBottom sx={{ fontWeight: 700 }}>
            {course.title}
          </Typography>
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

          {/* What you will learn */}
          <Typography variant="h6" sx={{ fontWeight: 600, mb: 2 }}>
            📝 What you will learn
          </Typography>
          <Box sx={{ p: 3, bgcolor: '#f8f9fa', borderRadius: 2, mb: 3 }}>
            <Typography variant="body2">
              • Provide insights into basics of programming
              <br />
              • Introduce fundamentals of Java programming
              <br />
              • Discuss various control structures in Java
              <br />
              • Provide insights into basics of object oriented programming
              <br />
              • Introduce class and objects
              <br />
              • Discuss Encapsulation and need for encapsulation
            </Typography>
          </Box>

          {/* Skills you will gain */}
          <Typography variant="h6" sx={{ fontWeight: 600, mb: 2 }}>
            🎯 Skills you will gain
          </Typography>
          <Box sx={{ display: 'flex', gap: 1, flexWrap: 'wrap', mb: 3 }}>
            <Chip label="Java - ALL" sx={{ bgcolor: '#6C63FF', color: 'white' }} />
            <Chip label="Programming" variant="outlined" />
            <Chip label="Object Oriented Programming" variant="outlined" />
          </Box>

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
                          bgcolor: lesson.is_completed ? 'success.light' : 'transparent',
                          '&:hover': {
                            bgcolor: isEnrolled ? 'action.hover' : 'transparent',
                          },
                        }}
                      >
                        {/* ✅ WhatsApp Style Double Tick */}
                        <ListItemIcon sx={{ minWidth: 36 }}>
                          {lesson.is_completed ? (
                            <DoneAll sx={{ color: '#6C63FF' }} />   // ✅ Blue Double Tick
                          ) : (
                            <RadioButtonUnchecked sx={{ color: '#9CA3AF' }} /> // ⚪ Gray Circle
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