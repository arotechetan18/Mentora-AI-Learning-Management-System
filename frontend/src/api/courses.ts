import axios from 'axios';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000/api';

export interface Course {
  id: number;
  title: string;
  description: string;
  instructor: string;
  duration: string;
  level: 'Beginner' | 'Intermediate' | 'Advanced';
  enrolled_count: number;
  thumbnail?: string;
}

export interface Module {
  id: number;
  course_id: number;
  title: string;
  description: string;
  order: number;
}

export interface Lesson {
  id: number;
  module_id: number;
  title: string;
  description: string;
  content: string;
  video_url?: string;
  duration: string;
  order: number;
  is_completed: boolean;
}

// Get all courses
export const getCourses = async (): Promise<Course[]> => {
  try {
    const response = await axios.get(`${API_URL}/courses`);
    return response.data;
  } catch (error) {
    console.error('Error fetching courses:', error);
    throw error;
  }
};

// Get single course with modules
export const getCourse = async (id: string): Promise<Course & { modules: Module[] }> => {
  try {
    const response = await axios.get(`${API_URL}/courses/${id}`);
    return response.data;
  } catch (error) {
    console.error('Error fetching course:', error);
    throw error;
  }
};

// Enroll in a course
export const enrollCourse = async (courseId: number): Promise<void> => {
  try {
    await axios.post(`${API_URL}/courses/${courseId}/enroll`);
  } catch (error) {
    console.error('Error enrolling in course:', error);
    throw error;
  }
};