import React from 'react';
import {
  Card,
  CardContent,
  Typography,
  Button,
  Box,
  Chip,
  LinearProgress,
} from '@mui/material';
import { School, Timer } from '@mui/icons-material';

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
  isEnrolled: boolean;
  progress?: number;  
  onEnroll: () => void;
  onClick?: () => void;
}

const CourseCard: React.FC<CourseCardProps> = ({
  course,
  isEnrolled,
  progress = 0,
  onEnroll,
  onClick,
}) => {
  const getDifficultyColor = (level: string) => {
    switch (level.toLowerCase()) {
      case 'beginner':
        return { bg: '#E8F5E9', color: '#2E7D32', label: 'Beginner' };
      case 'intermediate':
        return { bg: '#FFF3E0', color: '#E65100', label: 'Intermediate' };
      case 'advanced':
        return { bg: '#FCE4EC', color: '#C62828', label: 'Advanced' };
      default:
        return { bg: '#F5F5F5', color: '#616161', label: level };
    }
  };

  const difficulty = getDifficultyColor(course.difficulty);

  return (
    <Card
      sx={{
        height: '100%',
        display: 'flex',
        flexDirection: 'column',
        cursor: onClick ? 'pointer' : 'default',
        transition: 'all 0.3s ease',
        '&:hover': {
          transform: 'translateY(-6px)',
          boxShadow: '0 12px 48px rgba(108, 99, 255, 0.15)',
        },
      }}
      onClick={onClick}
    >
      {/* Card Header */}
      <Box
        sx={{
          p: 2,
          background: 'linear-gradient(135deg, #F8F9FE 0%, #EEF1FA 100%)',
          borderBottom: '1px solid rgba(108, 99, 255, 0.06)',
        }}
      >
        <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start' }}>
          <Chip
            label={course.category}
            size="small"
            sx={{
              bgcolor: 'rgba(108, 99, 255, 0.08)',
              color: '#6C63FF',
              fontWeight: 500,
            }}
          />
          <Chip
            label={difficulty.label}
            size="small"
            sx={{
              bgcolor: difficulty.bg,
              color: difficulty.color,
              fontWeight: 500,
            }}
          />
        </Box>
        <Typography
          variant="h6"
          sx={{
            mt: 1.5,
            fontWeight: 700,
            color: '#1A1A2E',
            display: '-webkit-box',
            WebkitLineClamp: 2,
            WebkitBoxOrient: 'vertical',
            overflow: 'hidden',
          }}
        >
          {course.title}
        </Typography>
      </Box>

      {/* Content */}
      <CardContent sx={{ flexGrow: 1, display: 'flex', flexDirection: 'column' }}>
        <Typography
          variant="body2"
          color="text.secondary"
          sx={{
            display: '-webkit-box',
            WebkitLineClamp: 2,
            WebkitBoxOrient: 'vertical',
            overflow: 'hidden',
            mb: 2,
          }}
        >
          {course.description?.substring(0, 120)}...
        </Typography>

        <Box sx={{ display: 'flex', gap: 2, mb: 2 }}>
          <Box sx={{ display: 'flex', alignItems: 'center', gap: 0.5 }}>
            <Timer sx={{ fontSize: 16, color: '#6B7280' }} />
            <Typography variant="caption" color="text.secondary">
              {course.duration}h
            </Typography>
          </Box>
          <Box sx={{ display: 'flex', alignItems: 'center', gap: 0.5 }}>
            <School sx={{ fontSize: 16, color: '#6B7280' }} />
            <Typography variant="caption" color="text.secondary">
              {course.difficulty}
            </Typography>
          </Box>
        </Box>

        {/* Progress Section - Fixed */}
        {isEnrolled ? (
          <Box sx={{ mt: 'auto' }}>
            <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 1 }}>
              <Typography variant="caption" sx={{ fontWeight: 600, color: '#6C63FF' }}>
                Progress
              </Typography>
              <Typography variant="caption" sx={{ fontWeight: 600, color: '#1A1A2E' }}>
                {progress}%
              </Typography>
            </Box>
            <LinearProgress
              variant="determinate"
              value={progress}
              sx={{
                height: 6,
                borderRadius: 4,
                bgcolor: 'rgba(108, 99, 255, 0.1)',
                '& .MuiLinearProgress-bar': {
                  background: 'linear-gradient(90deg, #6C63FF 0%, #4A42D9 100%)',
                  borderRadius: 4,
                },
              }}
            />
            <Button
              variant="outlined"
              fullWidth
              size="small"
              sx={{
                mt: 1.5,
                borderColor: '#6C63FF',
                color: '#6C63FF',
                '&:hover': { borderColor: '#4A42D9', bgcolor: 'rgba(108, 99, 255, 0.05)' },
              }}
            >
              Continue Learning
            </Button>
          </Box>
        ) : (
          <Button
            variant="contained"
            fullWidth
            size="large"
            onClick={(e) => { e.stopPropagation(); onEnroll(); }}
            sx={{ mt: 'auto' }}
          >
            Enroll Now
          </Button>
        )}
      </CardContent>
    </Card>
  );
};

export default CourseCard;