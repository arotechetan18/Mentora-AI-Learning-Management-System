import api from './index';

export interface CourseProgress {
  course_id: number;
  total_lessons: number;
  completed_lessons: number;
  progress: number;
  is_completed: boolean;
}

export const getCourseProgress = async (courseId: number): Promise<CourseProgress> => {
  const response = await api.get(`/progress/courses/${courseId}`);
  return response.data;
};