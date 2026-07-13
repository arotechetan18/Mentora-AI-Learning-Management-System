import api from './index';

// ✅ Complete Course interface with progress
export interface Course {
  id: number;
  title: string;
  description: string;
  category: string;
  difficulty: string;
  duration: number;
  price: number;
  instructor_id: number;
  is_published: boolean;
  cover_image?: string;
  created_at: string;
  updated_at?: string;
  progress?: number;  // ✅ Optional progress property
}

// ✅ Module Interface
export interface Module {
  id: number;
  course_id: number;
  title: string;
  description: string;
  order: number;
  lessons?: Lesson[];
  created_at: string;
  updated_at: string;
}

// ✅ Lesson Interface
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

export interface CourseCreate {
  title: string;
  description: string;
  category: string;
  difficulty: 'beginner' | 'intermediate' | 'advanced';
  duration: number;
  price: number;
}

export const getCourses = async (params?: {
  skip?: number;
  limit?: number;
  category?: string;
  difficulty?: string;
  search?: string;
}): Promise<Course[]> => {
  const response = await api.get<Course[]>('/courses', { params });
  return response.data;
};

export const getCourse = async (id: number): Promise<Course> => {
  const response = await api.get<Course>(`/courses/${id}`);
  return response.data;
};

export const getCourseModules = async (courseId: number): Promise<Module[]> => {
  const response = await api.get<Module[]>(`/courses/${courseId}/modules`);
  return response.data;
};

export const createCourse = async (data: CourseCreate): Promise<Course> => {
  const response = await api.post<Course>('/courses', data);
  return response.data;
};

export const updateCourse = async (id: number, data: Partial<CourseCreate>): Promise<Course> => {
  const response = await api.put<Course>(`/courses/${id}`, data);
  return response.data;
};

export const deleteCourse = async (id: number): Promise<void> => {
  await api.delete(`/courses/${id}`);
};