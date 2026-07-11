import api from './index';

export interface Module {
  id: number;
  title: string;
  description: string;
  order: number;
  course_id: number;
  created_at: string;
  updated_at: string;
}

export interface Lesson {
  id: number;
  title: string;
  description: string;
  concept: string;
  example: string;
  interview_questions: string;
  duration: number;
  order: number;
  is_completed?: boolean;
}

export interface ModuleWithLessons extends Module {
  lessons: Lesson[];
}

export const getModules = async (courseId: number): Promise<Module[]> => {
  const response = await api.get(`/courses/${courseId}/modules`);
  return response.data;
};

export const getModuleLessons = async (moduleId: number): Promise<Lesson[]> => {
  const response = await api.get(`/modules/${moduleId}/lessons`);
  return response.data;
};