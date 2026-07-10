import React from 'react';
import { CircularProgress, Box } from '@mui/material';

// ✅ export default add करा
const Loader: React.FC = () => {
  return (
    <Box sx={{ display: 'flex', justifyContent: 'center', mt: 4 }}>
      <CircularProgress />
    </Box>
  );
};

export default Loader;