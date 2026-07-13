import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider, useAuth } from './context/AuthContext';
import { ToastContainer } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css'
import MyCourses from './pages/MyCourses'; 
import Login from './components/auth/Login';
import Register from './components/auth/Register';
import Dashboard from './pages/Dashboard';
import CourseDetails from './pages/CourseDetails';
import LessonPage from './pages/Lesson';
import ProtectedRoute from './components/common/ProtectedRoute';

const AppRoutes = () => {
  const { user, loading } = useAuth();

  if (loading) {
    return <div>Loading...</div>;
  }

  return (
    <>
      <Routes>
        {/*  Dashboard is default page */}
        <Route path="/" element={<Navigate to="/dashboard" />} />
        <Route path="/login" element={!user ? <Login /> : <Navigate to="/dashboard" />} />
        <Route path="/register" element={!user ? <Register /> : <Navigate to="/dashboard" />} />
        <Route path="/dashboard" element={<Dashboard />} />
        <Route path="/course/:id" element={<CourseDetails />} />
        <Route path="/lesson/:id" element={<ProtectedRoute><LessonPage /></ProtectedRoute>} />
        <Route path="/my-courses" element={<ProtectedRoute><MyCourses /></ProtectedRoute>} />
      </Routes>
      <ToastContainer position="top-right" autoClose={3000} />
    </>
  );
};

function App() {
  return (
    <Router>
      <AuthProvider>
        <AppRoutes />
      </AuthProvider>
    </Router>
  );
}

export default App;