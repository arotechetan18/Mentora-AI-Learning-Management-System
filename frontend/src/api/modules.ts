import api from './index';

export interface Module {
  id: number;
  course_id: number;
  title: string;
  description: string;
  order: number;
  created_at: string;
  updated_at: string;
}

export interface Lesson {
  id: number;
  module_id: number;
  title: string;
  description: string;
  concept: string;
  example: string;
  interview_questions: string;
  duration: number;
  order: number;
  is_completed?: boolean;
  created_at: string;
  updated_at: string;
}

export const getModules = async (courseId: number): Promise<Module[]> => {
  const response = await api.get(`/courses/${courseId}/modules`);
  return response.data;
};

export const getModuleLessons = async (moduleId: number): Promise<Lesson[]> => {
  const response = await api.get(`/modules/${moduleId}/lessons`);
  return response.data;
};