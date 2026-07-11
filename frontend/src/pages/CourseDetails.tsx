import React, { useState, useEffect } from 'react';
import {
  Container,
  Typography,
  Box,
  Button,
  Chip,
  Accordion,
  AccordionSummary,
  AccordionDetails,
  List,
  ListItem,
  ListItemIcon,
  ListItemText,
  CircularProgress,
  Alert,
  Paper,
} from '@mui/material';
import ExpandMoreIcon from '@mui/icons-material/ExpandMore';
import CheckCircleIcon from '@mui/icons-material/CheckCircle';
import LockIcon from '@mui/icons-material/Lock';
import PlayArrowIcon from '@mui/icons-material/PlayArrow';
import { useParams, useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { getCourse, Course, Module, Lesson } from '../api/courses';

const CourseDetails: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const [course, setCourse] = useState<(Course & { modules: Module[] }) | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const { user } = useAuth();
  const navigate = useNavigate();

  useEffect(() => {
    if (id) {
      fetchCourse(id);
    }
  }, [id]);

  const fetchCourse = async (courseId: string) => {
    try {
      const data = await getCourse(courseId);
      setCourse(data);
    } catch (err) {
      setError('Failed to load course details');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleLessonClick = (lessonId: number) => {
    navigate(`/lesson/${lessonId}`);
  };

  if (loading) {
    return (
      <Box sx={{ display: 'flex', justifyContent: 'center', mt: 8 }}>
        <CircularProgress />
      </Box>
    );
  }

  if (error || !course) {
    return (
      <Container sx={{ mt: 4 }}>
        <Alert severity="error">{error || 'Course not found'}</Alert>
      </Container>
    );
  }

  return (
    <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
      <Paper elevation={0} sx={{ p: 3, bgcolor: 'background.paper', borderRadius: 2 }}>
        <Typography variant="h4" gutterBottom>
          {course.title}
        </Typography>
        <Typography variant="body1" color="text.secondary" sx={{ mb: 2 }}>
          {course.description}
        </Typography>
        <Box sx={{ display: 'flex', gap: 2, flexWrap: 'wrap', mb: 3 }}>
          <Chip label={`Instructor: ${course.instructor}`} variant="outlined" />
          <Chip label={course.level} color="primary" />
          <Chip label={`${course.enrolled_count} students`} variant="outlined" />
        </Box>

        <Typography variant="h5" sx={{ mt: 4, mb: 2 }}>
          Course Modules
        </Typography>

        {course.modules.map((module) => (
          <Accordion key={module.id}>
            <AccordionSummary expandIcon={<ExpandMoreIcon />}>
              <Typography variant="subtitle1">
                {module.order}. {module.title}
              </Typography>
            </AccordionSummary>
            <AccordionDetails>
              <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
                {module.description}
              </Typography>
              <List>
                {/* Remove lessons if not available, or use empty array */}
                {(module as any).lessons?.map((lesson: Lesson) => (
                  <ListItem
                    key={lesson.id}
                    onClick={() => handleLessonClick(lesson.id)}
                    sx={{
                      borderRadius: 1,
                      mb: 0.5,
                      bgcolor: lesson.is_completed ? 'success.light' : 'transparent',
                      cursor: 'pointer',
                      '&:hover': {
                        bgcolor: 'action.hover',
                      },
                    }}
                  >
                    <ListItemIcon>
                      {lesson.is_completed ? (
                        <CheckCircleIcon color="success" />
                      ) : (
                        <PlayArrowIcon color="primary" />
                      )}
                    </ListItemIcon>
                    <ListItemText
                      primary={lesson.title}
                      secondary={`Duration: ${lesson.duration}`}
                    />
                  </ListItem>
                ))}
              </List>
            </AccordionDetails>
          </Accordion>
        ))}
      </Paper>
    </Container>
  );
};

export default CourseDetails;