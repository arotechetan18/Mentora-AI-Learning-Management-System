import api from './index';

export interface QuizQuestion {
  id: number;
  question: string;
  options: string[];
  explanation: string;
}

export interface LessonContent {
  id: number;
  title: string;
  description: string;
  concept: string;
  example: string;
  interview_questions: string;
  duration: number;
  order: number;
  is_completed: boolean;
  quiz: QuizQuestion[];
  next_lesson_id: number | null;
  prev_lesson_id: number | null;
    course_id: number;
}

export interface QuizResult {
  score: number;
  total: number;
  percentage: number;
  passed: boolean;
  results: {
    question_id: number;
    selected: number;
    correct: number;
    is_correct: boolean;
    explanation: string;
  }[];
}

// ✅ सर्व functions export केले आहेत
export const getLesson = async (lessonId: number): Promise<LessonContent> => {
  const response = await api.get(`/lessons/${lessonId}`);
  return response.data;
};

export const submitQuiz = async (lessonId: number, answers: number[]): Promise<QuizResult> => {
  const response = await api.post(`/lessons/${lessonId}/quiz`, { answers });
  return response.data;
};

export const markLessonComplete = async (lessonId: number): Promise<void> => {
  await api.put(`/lessons/${lessonId}/progress`);
};