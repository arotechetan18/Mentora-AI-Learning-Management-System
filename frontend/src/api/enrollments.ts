import api from './index';

export const enrollInCourse = async (courseId: number): Promise<any> => {
  const response = await api.post('/enrollments', { course_id: courseId });
  return response.data;
};

export const getMyEnrollments = async (): Promise<number[]> => {
  const response = await api.get('/enrollments/my');
  return response.data;
};