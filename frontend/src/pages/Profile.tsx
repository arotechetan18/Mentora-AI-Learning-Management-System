// src/pages/Profile.tsx
import React, { useState, useEffect } from 'react';
import {
  Container,
  Box,
  Typography,
  Paper,
  TextField,
  Button,
  Grid,
  Avatar,
  Divider,
  CircularProgress,
  Alert,
  Switch,
  FormControlLabel,
  Chip,
} from '@mui/material';
import { useAuth } from '../context/AuthContext';
import { getMyProfile, updateMyProfile, UserWithProfile } from '../api/profile';

const Profile: React.FC = () => {
  const { user } = useAuth();
  const [profile, setProfile] = useState<UserWithProfile | null>(null);
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');

  useEffect(() => {
    fetchProfile();
  }, []);

  const fetchProfile = async () => {
    try {
      const data = await getMyProfile();
      setProfile(data);
    } catch (err) {
      setError('Failed to load profile');
    } finally {
      setLoading(false);
    }
  };

  const handleSave = async () => {
    if (!profile) return;
    setSaving(true);
    setError('');
    setSuccess('');

    try {
      await updateMyProfile(profile.profile || {});
      setSuccess('Profile updated successfully!');
      await fetchProfile();
    } catch (err) {
      setError('Failed to update profile');
    } finally {
      setSaving(false);
    }
  };

  const handleChange = (field: string, value: any) => {
    if (!profile) return;
    setProfile({
      ...profile,
      profile: {
        ...profile.profile!,
        [field]: value,
      },
    });
  };

  if (loading) {
    return (
      <Box sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '80vh' }}>
        <CircularProgress />
      </Box>
    );
  }

  if (!profile) {
    return (
      <Container>
        <Alert severity="error">Profile not found</Alert>
      </Container>
    );
  }

  return (
    <Container maxWidth="md" sx={{ py: 4 }}>
      <Paper sx={{ p: 4 }}>
        {/* ✅ FIXED: Box with sx prop instead of display directly */}
        <Box sx={{ display: 'flex', alignItems: 'center', gap: 3, mb: 3 }}>
          <Avatar sx={{ width: 80, height: 80, bgcolor: '#6C63FF' }}>
            {profile.full_name?.charAt(0) || 'U'}
          </Avatar>
          <Box>
            <Typography variant="h4">{profile.full_name}</Typography>
            <Typography variant="body2" color="text.secondary">
              {profile.email} • {profile.role}
            </Typography>
            <Chip label={profile.role} size="small" sx={{ mt: 1 }} />
          </Box>
        </Box>

        <Divider sx={{ my: 3 }} />

        {error && <Alert severity="error" sx={{ mb: 2 }}>{error}</Alert>}
        {success && <Alert severity="success" sx={{ mb: 2 }}>{success}</Alert>}

        <Grid container spacing={3}>
          <Grid size={{ xs: 12 }}>
            <TextField
              fullWidth
              label="Bio"
              multiline
              rows={3}
              value={profile.profile?.bio || ''}
              onChange={(e) => handleChange('bio', e.target.value)}
            />
          </Grid>

          <Grid size={{ xs: 12, md: 6 }}>
            <TextField
              fullWidth
              label="Phone"
              value={profile.profile?.phone || ''}
              onChange={(e) => handleChange('phone', e.target.value)}
            />
          </Grid>

          <Grid size={{ xs: 12, md: 6 }}>
            <TextField
              fullWidth
              label="Location"
              value={profile.profile?.location || ''}
              onChange={(e) => handleChange('location', e.target.value)}
            />
          </Grid>

          <Grid size={{ xs: 12 }}>
            <TextField
              fullWidth
              label="Education"
              multiline
              rows={2}
              value={profile.profile?.education || ''}
              onChange={(e) => handleChange('education', e.target.value)}
            />
          </Grid>

          <Grid size={{ xs: 12 }}>
            <TextField
              fullWidth
              label="Experience"
              multiline
              rows={2}
              value={profile.profile?.experience || ''}
              onChange={(e) => handleChange('experience', e.target.value)}
            />
          </Grid>

          <Grid size={{ xs: 12 }}>
            <TextField
              fullWidth
              label="Skills (comma separated)"
              value={profile.profile?.skills || ''}
              onChange={(e) => handleChange('skills', e.target.value)}
              helperText="e.g. Python, React, SQL"
            />
          </Grid>

          <Grid size={{ xs: 12 }}>
            <Divider sx={{ my: 2 }} />
            <Typography variant="h6" gutterBottom>Social Links</Typography>
          </Grid>

          <Grid size={{ xs: 12, md: 6 }}>
            <TextField
              fullWidth
              label="GitHub"
              value={profile.profile?.github || ''}
              onChange={(e) => handleChange('github', e.target.value)}
            />
          </Grid>

          <Grid size={{ xs: 12, md: 6 }}>
            <TextField
              fullWidth
              label="LinkedIn"
              value={profile.profile?.linkedin || ''}
              onChange={(e) => handleChange('linkedin', e.target.value)}
            />
          </Grid>

          <Grid size={{ xs: 12, md: 6 }}>
            <TextField
              fullWidth
              label="Twitter"
              value={profile.profile?.twitter || ''}
              onChange={(e) => handleChange('twitter', e.target.value)}
            />
          </Grid>

          <Grid size={{ xs: 12, md: 6 }}>
            <TextField
              fullWidth
              label="YouTube"
              value={profile.profile?.youtube || ''}
              onChange={(e) => handleChange('youtube', e.target.value)}
            />
          </Grid>

          <Grid size={{ xs: 12 }}>
            <Divider sx={{ my: 2 }} />
            <Typography variant="h6" gutterBottom>Preferences</Typography>
            
            <FormControlLabel
              control={
                <Switch
                  checked={profile.profile?.email_notifications ?? true}
                  onChange={(e) => handleChange('email_notifications', e.target.checked)}
                />
              }
              label="Email Notifications"
            />
            
            <FormControlLabel
              control={
                <Switch
                  checked={profile.profile?.course_updates ?? true}
                  onChange={(e) => handleChange('course_updates', e.target.checked)}
                />
              }
              label="Course Updates"
            />
          </Grid>
        </Grid>

        <Box sx={{ mt: 3, display: 'flex', gap: 2 }}>
          <Button
            variant="contained"
            onClick={handleSave}
            disabled={saving}
            sx={{ bgcolor: '#6C63FF' }}
          >
            {saving ? <CircularProgress size={24} /> : 'Save Profile'}
          </Button>
        </Box>
      </Paper>
    </Container>
  );
};

export default Profile;