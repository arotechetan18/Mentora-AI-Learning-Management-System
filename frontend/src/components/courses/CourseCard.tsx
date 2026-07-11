import React from 'react';
import { Card, CardContent, Typography, Button, Box, Chip } from '@mui/material';

interface Course {
  id: number;
  title: string;
  description: string;
  category: string;
  difficulty: string;
  duration: number;
  price: number;
}

interface CourseCardProps {
  course: Course;
  onEnroll: (courseId: number) => void;
}

const CourseCard: React.FC<CourseCardProps> = ({ course, onEnroll }) => {
  return (
    <Card sx={{ height: '100%', display: 'flex', flexDirection: 'column' }}>
      <CardContent sx={{ flexGrow: 1 }}>
        <Typography variant="h6" gutterBottom>
          {course.title}
        </Typography>
        <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
          {course.description.substring(0, 100)}...
        </Typography>
        <Box sx={{ display: 'flex', gap: 1, flexWrap: 'wrap', mb: 2 }}>
          <Chip label={course.category} size="small" />
          <Chip label={course.difficulty} size="small" color="primary" />
          <Chip label={`${course.duration}h`} size="small" />
        </Box>
        <Typography variant="h6" color="primary">
          ₹{course.price}
        </Typography>
        <Button
          variant="contained"
          fullWidth
          sx={{ mt: 2 }}
          onClick={() => onEnroll(course.id)}
        >
          Enroll Now
        </Button>
      </CardContent>
    </Card>
  );
};

export default CourseCard;