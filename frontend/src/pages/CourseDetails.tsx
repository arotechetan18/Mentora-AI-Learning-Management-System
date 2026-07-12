import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import {
  Container,
  Box,
  Typography,
  Paper,
  Button,
  Chip,
  LinearProgress,
  Accordion,
  AccordionSummary,
  AccordionDetails,
  List,
  ListItem,
  ListItemText,
  ListItemIcon,
  CircularProgress,
  Alert,
} from '@mui/material';
import { ExpandMore, PlayArrow, CheckCircle, Lock } from '@mui/icons-material';
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
    navigate(`/lesson/${lessonId}`);
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
        <Paper elevation={3} sx={{ p: 4, mb: 3 }}>
          <Typography variant="h4" gutterBottom>
            {course.title}
          </Typography>
          {/* ✅ paragraph property काढली */}
          <Typography variant="body1" color="text.secondary" sx={{ mb: 2 }}>
            {course.description}
          </Typography>
          <Box sx={{ display: 'flex', gap: 2, flexWrap: 'wrap', mb: 3 }}>
            <Chip label={`Category: ${course.category}`} variant="outlined" />
            <Chip label={`${course.difficulty}`} color="primary" />
            <Chip label={`${course.duration} hours`} variant="outlined" />
            <Chip label={`₹${course.price}`} variant="outlined" />
          </Box>

          {isEnrolled ? (
            <Button variant="contained" color="success" disabled>
              ✅ Enrolled
            </Button>
          ) : (
            <Button variant="contained" color="primary" onClick={handleEnroll}>
              Enroll Now
            </Button>
          )}
        </Paper>

        {/* Modules */}
        <Typography variant="h5" gutterBottom>
          Course Content
        </Typography>

        {modules.length === 0 ? (
          <Alert severity="info">No modules available for this course yet.</Alert>
        ) : (
          modules.map((module: Module, index: number) => (
            <Accordion key={module.id} defaultExpanded={index === 0}>
              <AccordionSummary expandIcon={<ExpandMore />}>
                <Box sx={{ display: 'flex', alignItems: 'center', gap: 2, width: '100%' }}>
                  <Typography variant="h6">
                    Module {module.order}: {module.title}
                  </Typography>
                  <Chip
                    label={`${module.lessons?.length || 0} lessons`}
                    size="small"
                    variant="outlined"
                  />
                </Box>
              </AccordionSummary>
              <AccordionDetails>
                {/* ✅ paragraph property काढली */}
                <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
                  {module.description}
                </Typography>
                <List>
                  {module.lessons?.map((lesson: Lesson) => (
                    // ✅ button -> component={ListItemButton} वापरा
                    <ListItem
                      key={lesson.id}
                      component="div"
                      onClick={() => handleLessonClick(lesson.id)}
                      sx={{
                        borderRadius: 1,
                        mb: 0.5,
                        cursor: 'pointer',
                        bgcolor: lesson.is_completed ? 'success.light' : 'transparent',
                        '&:hover': {
                          bgcolor: 'action.hover',
                        },
                      }}
                    >
                      <ListItemIcon>
                        {lesson.is_completed ? (
                          <CheckCircle color="success" />
                        ) : (
                          <PlayArrow color="primary" />
                        )}
                      </ListItemIcon>
                      <ListItemText
                        primary={lesson.title}
                        secondary={`${lesson.duration} min`}
                      />
                      {lesson.is_completed && (
                        <Chip label="Completed" size="small" color="success" />
                      )}
                    </ListItem>
                  ))}
                </List>
              </AccordionDetails>
            </Accordion>
          ))
        )}
      </Box>
    </Container>
  );
};

export default CourseDetails;