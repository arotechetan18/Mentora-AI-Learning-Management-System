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
} from '@mui/material';
import { CheckCircle, ArrowBack, ArrowForward } from '@mui/icons-material';
import { getLesson, submitQuiz, markLessonComplete, LessonContent, QuizResult } from '../api/lessons';

const LessonPage: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const [lesson, setLesson] = useState<LessonContent | null>(null);
  const [selectedAnswers, setSelectedAnswers] = useState<number[]>([]);
  const [quizSubmitted, setQuizSubmitted] = useState(false);
  const [quizResult, setQuizResult] = useState<QuizResult | null>(null);
  const [loading, setLoading] = useState(true);

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
    try {
      const result = await submitQuiz(Number(id), selectedAnswers);
      setQuizResult(result);
      setQuizSubmitted(true);
      if (result.passed) {
        await markLessonComplete(Number(id));
        await fetchLesson();
      }
    } catch (error) {
      console.error('Error submitting quiz:', error);
    }
  };

  const handleMarkComplete = async () => {
    try {
      await markLessonComplete(Number(id));
      await fetchLesson();
    } catch (error) {
      console.error('Error marking complete:', error);
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

  if (loading) return <Box sx={{ p: 4 }}><Typography>Loading lesson...</Typography></Box>;
  if (!lesson) return <Box sx={{ p: 4 }}><Typography>Lesson not found</Typography></Box>;

  return (
    <Container maxWidth="lg">
      <Box sx={{ mt: 4, mb: 4 }}>
        <Paper elevation={3} sx={{ p: 4 }}>
          {/* Header */}
          <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 3 }}>
            <Typography variant="h4">{lesson.title}</Typography>
            <Chip
              label={lesson.is_completed ? '✅ Completed' : 'In Progress'}
              color={lesson.is_completed ? 'success' : 'warning'}
            />
          </Box>

          <Typography variant="body1" color="text.secondary" sx={{ mb: 3 }}>
            {lesson.description}
          </Typography>

          <Divider sx={{ my: 3 }} />

          {/* 📖 Concept */}
          <Typography variant="h6" sx={{ mb: 2 }}>
            📖 Concept
          </Typography>
          <Box sx={{ p: 3, bgcolor: '#f8f9fa', borderRadius: 2, mb: 3, whiteSpace: 'pre-wrap' }}>
            <Typography variant="body1">{lesson.concept}</Typography>
          </Box>

          {/* 💡 Example */}
          <Typography variant="h6" sx={{ mb: 2 }}>
            💡 Example
          </Typography>
          <Box sx={{ p: 3, bgcolor: '#e3f2fd', borderRadius: 2, mb: 3, whiteSpace: 'pre-wrap', fontFamily: 'monospace' }}>
            <Typography variant="body1">{lesson.example}</Typography>
          </Box>

          {/* 🎯 Interview Questions */}
          {lesson.interview_questions && (
            <>
              <Typography variant="h6" sx={{ mb: 2 }}>
                🎯 Interview Questions
              </Typography>
              <Box sx={{ p: 3, bgcolor: '#fce4ec', borderRadius: 2, mb: 3, whiteSpace: 'pre-wrap' }}>
                <Typography variant="body1">{lesson.interview_questions}</Typography>
              </Box>
            </>
          )}

          <Divider sx={{ my: 3 }} />

          {/* 📝 Quiz */}
          {lesson.quiz.length > 0 && !quizSubmitted && (
            <Box>
              <Typography variant="h6" sx={{ mb: 2 }}>
                📝 Quiz ({lesson.quiz.length} Questions)
              </Typography>
              {lesson.quiz.map((q: any, qIndex: number) => (
                <Box key={q.id} sx={{ mb: 3, p: 2, bgcolor: '#f5f5f5', borderRadius: 2 }}>
                  <Typography variant="subtitle1" sx={{ mb: 1 }}>
                    {qIndex + 1}. {q.question}
                  </Typography>
                  <FormControl component="fieldset">
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
              <Button
                variant="contained"
                color="primary"
                onClick={handleSubmitQuiz}
                disabled={selectedAnswers.includes(-1)}
              >
                Submit Quiz
              </Button>
            </Box>
          )}

          {/* Quiz Results */}
          {quizSubmitted && quizResult && (
            <Box sx={{ mt: 3, p: 3, bgcolor: quizResult.passed ? '#e8f5e9' : '#ffebee', borderRadius: 2 }}>
              <Typography variant="h6">
                {quizResult.passed ? '✅ Passed!' : '❌ Need to Review'}
              </Typography>
              <Typography>
                Score: {quizResult.score}/{quizResult.total} ({quizResult.percentage}%)
              </Typography>
              <Typography>
                {quizResult.percentage >= 60 ? 'You can proceed to next lesson.' : 'Please review the content and try again.'}
              </Typography>
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
            <Box sx={{ display: 'flex', gap: 2 }}>
              {!lesson.is_completed && quizSubmitted && quizResult?.passed && (
                <Button
                  variant="contained"
                  color="success"
                  onClick={handleMarkComplete}
                  startIcon={<CheckCircle />}
                >
                  Mark Complete
                </Button>
              )}
              {lesson.is_completed && (
                <Button variant="contained" color="warning" disabled>
                  ✅ Completed
                </Button>
              )}
            </Box>
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