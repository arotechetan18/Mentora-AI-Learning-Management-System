import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import {
  Container,
  Box,
  Typography,
  Paper,
  Button,
  Chip,
  Divider,
  Radio,
  RadioGroup,
  FormControlLabel,
  FormControl,
  CircularProgress,
  Alert,
  Stepper,
  Step,
  StepLabel,
  IconButton,  // ✅ IconButton Add
} from '@mui/material';
import {
  CheckCircle,
  ArrowBack,    // ✅ Back Icon
  ArrowForward,
  Refresh,
} from '@mui/icons-material';
import { getLesson, submitQuiz, markLessonComplete, LessonContent } from '../api/lessons';
import { toast } from 'react-toastify';

interface QuizQuestion {
  id: number;
  question: string;
  options: string[];
  explanation: string;
}

const LessonPage: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const [lesson, setLesson] = useState<LessonContent | null>(null);
  const [loading, setLoading] = useState(true);
  const [activeStep, setActiveStep] = useState(0);
  const [selectedAnswers, setSelectedAnswers] = useState<number[]>([]);
  const [showResults, setShowResults] = useState(false);
  const [quizResult, setQuizResult] = useState<any>(null);

  useEffect(() => {
    fetchLesson();
    }, [id]);

  const fetchLesson = async () => {
    try {
      const data = await getLesson(Number(id));
      setLesson(data);
      setSelectedAnswers(new Array(data.quiz.length).fill(-1));
    } catch (error) {
      console.error('Error fetching lesson:', error);
      toast.error('Failed to load lesson');
    } finally {
      setLoading(false);
    }
  };

  const handleAnswerSelect = (qIndex: number, value: number) => {
    const newAnswers = [...selectedAnswers];
    newAnswers[qIndex] = value;
    setSelectedAnswers(newAnswers);
  };

  const handleSubmitQuiz = async () => {
    if (selectedAnswers.includes(-1)) {
      toast.warning('Please answer all questions before submitting');
      return;
    }

    try {
      const result = await submitQuiz(Number(id), selectedAnswers);
      setQuizResult(result);
      setShowResults(true);

      if (result.passed) {
        await markLessonComplete(Number(id));
        toast.success('🎉 Quiz passed! Lesson completed!');
        await fetchLesson();
      } else {
        toast.error('❌ Need 60% to pass. Please review and try again.');
      }
    } catch (error) {
      console.error('Error submitting quiz:', error);
      toast.error('Failed to submit quiz');
    }
  };

  const handleTryAgain = () => {
    setShowResults(false);
    setSelectedAnswers(new Array(lesson?.quiz?.length || 0).fill(-1));
    toast.info('🔄 Quiz reset. Try again!');
  };

  const handleMarkComplete = async () => {
    try {
      await markLessonComplete(Number(id));
      toast.success('✅ Lesson marked as complete!');
      await fetchLesson();
    } catch (error) {
      console.error('Error marking complete:', error);
      toast.error('Failed to mark complete');
    }
  };

  const goToNext = () => {
    if (lesson?.next_lesson_id) {
      navigate(`/lesson/${lesson.next_lesson_id}`);
    }
  };

  const goToPrev = () => {
    if (lesson?.prev_lesson_id) {
      navigate(`/lesson/${lesson.prev_lesson_id}`);
    }
  };

  const steps = ['📖 Concept', '💡 Example', '📝 Quiz'];

  if (loading) {
    return (
      <Box sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '80vh' }}>
        <CircularProgress />
      </Box>
    );
  }

  if (!lesson) {
    return (
      <Container>
        <Alert severity="error" sx={{ mt: 4 }}>Lesson not found</Alert>
      </Container>
    );
  }

  return (
    <Container maxWidth="lg">
      <Box sx={{ mt: 4, mb: 4 }}>
        <Paper elevation={3} sx={{ p: 4 }}>
          {/*  Header with Back Button */}
          <Box sx={{ display: 'flex', alignItems: 'center', gap: 2, mb: 3 }}>
          
            <IconButton 
              onClick={() => navigate(`/course/${lesson.course_id || 1}`)}
              sx={{ 
                bgcolor: '#f0f0f0', 
                '&:hover': { bgcolor: '#e0e0e0' } 
              }}
            >
              <ArrowBack />
            </IconButton>
            <Typography variant="h4" sx={{ fontWeight: 700, flex: 1 }}>
              {lesson.title}
            </Typography>
            <Chip
              label={lesson.is_completed ? '✅ Completed' : 'In Progress'}
              color={lesson.is_completed ? 'success' : 'warning'}
            />
          </Box>

          <Typography variant="body1" color="text.secondary" sx={{ mb: 3 }}>
            {lesson.description}
          </Typography>

          <Divider sx={{ mb: 3 }} />

          {/* Stepper */}
          <Stepper activeStep={activeStep} sx={{ mb: 4 }}>
            {steps.map((label) => (
              <Step key={label}>
                <StepLabel>{label}</StepLabel>
              </Step>
            ))}
          </Stepper>

          {/* Content */}
          {activeStep === 0 && (
            <Box>
              <Typography variant="h6" sx={{ fontWeight: 600, mb: 2 }}>
                📖 Concept
              </Typography>
              <Box sx={{ p: 3, bgcolor: '#f8f9fa', borderRadius: 2 }}>
                <Typography variant="body1" sx={{ whiteSpace: 'pre-wrap' }}>
                  {lesson.concept}
                </Typography>
              </Box>
              <Box sx={{ mt: 3, display: 'flex', justifyContent: 'flex-end' }}>
                <Button
                  variant="contained"
                  onClick={() => setActiveStep(1)}
                  endIcon={<ArrowForward />}
                >
                  Next: Example
                </Button>
              </Box>
            </Box>
          )}

          {activeStep === 1 && (
            <Box>
              <Typography variant="h6" sx={{ fontWeight: 600, mb: 2 }}>
                💡 Example
              </Typography>
              <Box sx={{ p: 3, bgcolor: '#e3f2fd', borderRadius: 2 }}>
                <Typography variant="body1" sx={{ whiteSpace: 'pre-wrap' }}>
                  {lesson.example}
                </Typography>
              </Box>
              <Box sx={{ mt: 3, display: 'flex', justifyContent: 'space-between' }}>
                <Button
                  variant="outlined"
                  onClick={() => setActiveStep(0)}
                  startIcon={<ArrowBack />}
                >
                  Back
                </Button>
                <Button
                  variant="contained"
                  onClick={() => setActiveStep(2)}
                  endIcon={<ArrowForward />}
                >
                  Next: Quiz
                </Button>
              </Box>
            </Box>
          )}

          {activeStep === 2 && (
            <Box>
              <Typography variant="h6" sx={{ fontWeight: 600, mb: 2 }}>
                📝 Quiz
              </Typography>

              {lesson.quiz.length > 0 && !showResults && (
                <Box>
                  {lesson.quiz.map((q: QuizQuestion, qIndex: number) => (
                    <Box key={q.id} sx={{ mb: 3, p: 2, bgcolor: '#f5f5f5', borderRadius: 2 }}>
                      <Typography variant="subtitle1" sx={{ mb: 1 }}>
                        {qIndex + 1}. {q.question}
                      </Typography>
                      <FormControl component="fieldset" fullWidth>
                        <RadioGroup
                          value={selectedAnswers[qIndex]}
                          onChange={(e) => handleAnswerSelect(qIndex, Number(e.target.value))}
                        >
                          {q.options.map((opt: string, oIndex: number) => (
                            <FormControlLabel
                              key={oIndex}
                              value={oIndex}
                              control={<Radio />}
                              label={opt}
                            />
                          ))}
                        </RadioGroup>
                      </FormControl>
                    </Box>
                  ))}

                  <Box sx={{ display: 'flex', justifyContent: 'space-between', mt: 3 }}>
                    <Button
                      variant="outlined"
                      onClick={() => setActiveStep(1)}
                      startIcon={<ArrowBack />}
                    >
                      Back
                    </Button>
                    <Button
                      variant="contained"
                      color="primary"
                      onClick={handleSubmitQuiz}
                      disabled={selectedAnswers.includes(-1)}
                    >
                      Submit Quiz
                    </Button>
                  </Box>
                </Box>
              )}

              {showResults && quizResult && (
                <Box>
                  <Alert
                    severity={quizResult.passed ? 'success' : 'error'}
                    sx={{ mb: 3 }}
                  >
                    <Typography variant="h6">
                      {quizResult.passed ? '✅ Passed!' : '❌ Need to Review'}
                    </Typography>
                    <Typography>
                      Score: {quizResult.score}/{quizResult.total} ({quizResult.percentage}%)
                    </Typography>
                    {!quizResult.passed && (
                      <Typography variant="body2" sx={{ mt: 1 }}>
                        Minimum passing score is 60%. Please review and try again.
                      </Typography>
                    )}
                  </Alert>

                  {quizResult.results.map((result: any, index: number) => (
                    <Box
                      key={index}
                      sx={{
                        p: 2,
                        mb: 2,
                        bgcolor: result.is_correct ? '#e8f5e9' : '#ffebee',
                        borderRadius: 2,
                      }}
                    >
                      <Typography variant="subtitle2">
                        Q{index + 1}: {result.is_correct ? '✅' : '❌'}
                      </Typography>
                      <Typography variant="body2">
                        {result.explanation || 'No explanation available'}
                      </Typography>
                    </Box>
                  ))}

                  {!quizResult.passed && (
                    <Button
                      variant="contained"
                      color="warning"
                      startIcon={<Refresh />}
                      onClick={handleTryAgain}
                      sx={{ mt: 2 }}
                    >
                      Try Again
                    </Button>
                  )}

                  {quizResult.passed && !lesson.is_completed && (
                    <Button
                      variant="contained"
                      color="success"
                      onClick={handleMarkComplete}
                      startIcon={<CheckCircle />}
                      sx={{ mt: 2 }}
                    >
                      Mark Complete
                    </Button>
                  )}
                </Box>
              )}
            </Box>
          )}

          {/* Navigation */}
          <Box sx={{ display: 'flex', justifyContent: 'space-between', mt: 4 }}>
            <Button
              variant="outlined"
              startIcon={<ArrowBack />}
              onClick={goToPrev}
              disabled={!lesson.prev_lesson_id}
            >
              Previous
            </Button>
            <Button
              variant="outlined"
              endIcon={<ArrowForward />}
              onClick={goToNext}
              disabled={!lesson.next_lesson_id || !lesson.is_completed}
            >
              Next
            </Button>
          </Box>
        </Paper>
      </Box>  
    </Container>
  );
};

export default LessonPage;