// src/pages/Profile.tsx
import React, { useState, useEffect, useRef } from 'react';
import { useNavigate } from 'react-router-dom';
import { motion, AnimatePresence } from 'framer-motion';
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
  IconButton,
  Card,
  CardContent,
  Stack,
  Badge,
  Tooltip,
  Snackbar,
} from '@mui/material';
import {
  Edit as EditIcon,
  Save as SaveIcon,
  Cancel as CancelIcon,
  PhotoCamera as PhotoCameraIcon,
  GitHub as GitHubIcon,
  LinkedIn as LinkedInIcon,
  Twitter as TwitterIcon,
  YouTube as YouTubeIcon,
  Person as PersonIcon,
  Email as EmailIcon,
  LocationOn as LocationIcon,
  School as SchoolIcon,
  Work as WorkIcon,
  Code as CodeIcon,
} from '@mui/icons-material';
import { useAuth } from '../context/AuthContext';
import { getMyProfile, updateMyProfile, UserWithProfile } from '../api/profile';

const Profile: React.FC = () => {
  const { user, logout } = useAuth();
  const navigate = useNavigate();
  const fileInputRef = useRef<HTMLInputElement>(null);
  
  const [profile, setProfile] = useState<UserWithProfile | null>(null);
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [editMode, setEditMode] = useState(false);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  const [avatarFile, setAvatarFile] = useState<File | null>(null);
  const [avatarPreview, setAvatarPreview] = useState<string | null>(null);
  
  // Form state
  const [formData, setFormData] = useState({
    bio: '',
    phone: '',
    location: '',
    website: '',
    education: '',
    experience: '',
    skills: '',
    github: '',
    linkedin: '',
    twitter: '',
    youtube: '',
    email_notifications: true,
    course_updates: true,
  });

  useEffect(() => {
    fetchProfile();
  }, []);

  const fetchProfile = async () => {
    try {
      const data = await getMyProfile();
      setProfile(data);
      // Populate form data
      if (data.profile) {
        setFormData({
          bio: data.profile.bio || '',
          phone: data.profile.phone || '',
          location: data.profile.location || '',
          website: data.profile.website || '',
          education: data.profile.education || '',
          experience: data.profile.experience || '',
          skills: data.profile.skills || '',
          github: data.profile.github || '',
          linkedin: data.profile.linkedin || '',
          twitter: data.profile.twitter || '',
          youtube: data.profile.youtube || '',
          email_notifications: data.profile.email_notifications ?? true,
          course_updates: data.profile.course_updates ?? true,
        });
      }
    } catch (err: any) {
      if (err.response?.status === 401) {
        setError('Please login again');
        setTimeout(() => { logout(); navigate('/login'); }, 2000);
      } else {
        setError('Failed to load profile');
      }
    } finally {
      setLoading(false);
    }
  };

  const handleSave = async () => {
    setSaving(true);
    setError('');
    setSuccess('');

    try {
      // If avatar file selected, upload it first
      let avatarUrl = profile?.profile?.avatar_url;
      if (avatarFile) {
        // You can implement avatar upload here
        // For now, we'll just use the preview
        avatarUrl = avatarPreview || undefined;
      }

      await updateMyProfile({ ...formData, avatar_url: avatarUrl });
      setSuccess('Profile updated successfully!');
      setEditMode(false);
      await fetchProfile();
    } catch (err) {
      setError('Failed to update profile');
    } finally {
      setSaving(false);
    }
  };

  const handleCancel = () => {
    setEditMode(false);
    setAvatarFile(null);
    setAvatarPreview(null);
    // Reset form data
    if (profile?.profile) {
      setFormData({
        bio: profile.profile.bio || '',
        phone: profile.profile.phone || '',
        location: profile.profile.location || '',
        website: profile.profile.website || '',
        education: profile.profile.education || '',
        experience: profile.profile.experience || '',
        skills: profile.profile.skills || '',
        github: profile.profile.github || '',
        linkedin: profile.profile.linkedin || '',
        twitter: profile.profile.twitter || '',
        youtube: profile.profile.youtube || '',
        email_notifications: profile.profile.email_notifications ?? true,
        course_updates: profile.profile.course_updates ?? true,
      });
    }
  };

  const handleAvatarClick = () => {
    fileInputRef.current?.click();
  };

  const handleAvatarChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) {
      setAvatarFile(file);
      const reader = new FileReader();
      reader.onloadend = () => {
        setAvatarPreview(reader.result as string);
      };
      reader.readAsDataURL(file);
    }
  };

  const handleChange = (field: string, value: any) => {
    setFormData({ ...formData, [field]: value });
  };

  // Stats
  const stats = [
    { icon: <SchoolIcon />, label: 'Courses', value: profile?.profile?.education ? '5' : '0' },
    { icon: <WorkIcon />, label: 'Experience', value: profile?.profile?.experience ? '3+ yrs' : '0 yrs' },
    { icon: <CodeIcon />, label: 'Skills', value: profile?.profile?.skills?.split(',').length || 0 },
  ];

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
    <Container maxWidth="lg" sx={{ py: 4 }}>
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5 }}
      >
        {/* Error/Success Snackbar */}
        <Snackbar
          open={!!error || !!success}
          autoHideDuration={3000}
          onClose={() => { setError(''); setSuccess(''); }}
          anchorOrigin={{ vertical: 'top', horizontal: 'center' }}
        >
          <Alert severity={error ? 'error' : 'success'}>
            {error || success}
          </Alert>
        </Snackbar>

        <Grid container spacing={4}>
          {/* Left Panel - Profile Card */}
          <Grid size={{ xs: 12, md: 4 }}>
            <motion.div
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ duration: 0.5, delay: 0.2 }}
            >
              <Paper sx={{ p: 3, textAlign: 'center', position: 'relative' }}>
                {/* Avatar with Upload */}
                <Badge
                  overlap="circular"
                  anchorOrigin={{ vertical: 'bottom', horizontal: 'right' }}
                  badgeContent={
                    <IconButton
                      onClick={handleAvatarClick}
                      sx={{
                        bgcolor: '#6C63FF',
                        color: 'white',
                        '&:hover': { bgcolor: '#5A52D9' },
                        width: 40,
                        height: 40,
                      }}
                    >
                      <PhotoCameraIcon fontSize="small" />
                    </IconButton>
                  }
                >
                  <Avatar
                    src={avatarPreview || profile?.profile?.avatar_url || undefined}
                    sx={{
                      width: 150,
                      height: 150,
                      margin: '0 auto',
                      bgcolor: '#6C63FF',
                      fontSize: 60,
                      border: '4px solid #6C63FF',
                      transition: 'all 0.3s ease',
                      '&:hover': { transform: 'scale(1.05)' },
                    }}
                  >
                    {profile.full_name?.charAt(0) || 'U'}
                  </Avatar>
                </Badge>
                <input
                  type="file"
                  ref={fileInputRef}
                  accept="image/*"
                  style={{ display: 'none' }}
                  onChange={handleAvatarChange}
                />

                <Typography variant="h5" sx={{ mt: 2, fontWeight: 700 }}>
                  {profile.full_name}
                </Typography>
                <Chip
                  label={profile.role.toUpperCase()}
                  size="small"
                  sx={{ bgcolor: '#6C63FF', color: 'white', mt: 1 }}
                />
                <Typography variant="body2" color="text.secondary" sx={{ mt: 1, display: 'flex', alignItems: 'center', justifyContent: 'center', gap: 0.5 }}>
                  <EmailIcon fontSize="small" /> {profile.email}
                </Typography>
                {profile.profile?.location && (
                  <Typography variant="body2" color="text.secondary" sx={{ display: 'flex', alignItems: 'center', justifyContent: 'center', gap: 0.5 }}>
                    <LocationIcon fontSize="small" /> {profile.profile.location}
                  </Typography>
                )}

                <Divider sx={{ my: 2 }} />

                {/* Social Links */}
              {/* Social Links */}
<Stack 
  direction="row" 
  spacing={1} 
  sx={{ justifyContent: 'center' }}
>
  {profile.profile?.github && (
    <IconButton 
      href={profile.profile.github} 
      target="_blank" 
      sx={{ color: '#333' }}
    >
      <GitHubIcon />
    </IconButton>
  )}
  {profile.profile?.linkedin && (
    <IconButton 
      href={profile.profile.linkedin} 
      target="_blank" 
      sx={{ color: '#0077B5' }}
    >
      <LinkedInIcon />
    </IconButton>
  )}
  {profile.profile?.twitter && (
    <IconButton 
      href={profile.profile.twitter} 
      target="_blank" 
      sx={{ color: '#1DA1F2' }}
    >
      <TwitterIcon />
    </IconButton>
  )}
  {profile.profile?.youtube && (
    <IconButton 
      href={profile.profile.youtube} 
      target="_blank" 
      sx={{ color: '#FF0000' }}
    >
      <YouTubeIcon />
    </IconButton>
  )}
</Stack>
                <Divider sx={{ my: 2 }} />

                {/* Stats */}
                <Grid container spacing={1}>
                  {stats.map((stat, index) => (
                    <Grid size={{ xs: 4 }} key={index}>
                      <Box sx={{ textAlign: 'center' }}>
                        <Typography variant="h6" sx={{ fontWeight: 700, color: '#6C63FF' }}>
                          {stat.value}
                        </Typography>
                        <Typography variant="caption" color="text.secondary">
                          {stat.label}
                        </Typography>
                      </Box>
                    </Grid>
                  ))}
                </Grid>

                <Divider sx={{ my: 2 }} />

                {!editMode && (
                  <Button
                    fullWidth
                    variant="contained"
                    startIcon={<EditIcon />}
                    onClick={() => setEditMode(true)}
                    sx={{ bgcolor: '#6C63FF', '&:hover': { bgcolor: '#5A52D9' } }}
                  >
                    Edit Profile
                  </Button>
                )}
              </Paper>
            </motion.div>
          </Grid>

          {/* Right Panel - Profile Details */}
          <Grid size={{ xs: 12, md: 8 }}>
            <motion.div
              initial={{ opacity: 0, x: 20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ duration: 0.5, delay: 0.3 }}
            >
              <Paper sx={{ p: 3 }}>
                {/* Header */}
                <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 3 }}>
                  <Typography variant="h5" sx={{ fontWeight: 700 }}>
                    {editMode ? '✏️ Edit Profile' : '📋 Profile Details'}
                  </Typography>
                  {editMode && (
                    <Box sx={{ display: 'flex', gap: 1 }}>
                      <Button
                        variant="outlined"
                        startIcon={<CancelIcon />}
                        onClick={handleCancel}
                        sx={{ color: '#666', borderColor: '#ddd' }}
                      >
                        Cancel
                      </Button>
                      <Button
                        variant="contained"
                        startIcon={saving ? <CircularProgress size={20} /> : <SaveIcon />}
                        onClick={handleSave}
                        disabled={saving}
                        sx={{ bgcolor: '#6C63FF', '&:hover': { bgcolor: '#5A52D9' } }}
                      >
                        {saving ? 'Saving...' : 'Save Changes'}
                      </Button>
                    </Box>
                  )}
                </Box>

                {/* Bio */}
                {profile.profile?.bio && !editMode && (
                  <Card sx={{ mb: 3, bgcolor: '#F8F9FE' }}>
                    <CardContent>
                      <Typography variant="body1">{profile.profile.bio}</Typography>
                    </CardContent>
                  </Card>
                )}

                <Grid container spacing={3}>
                  {/* Bio - Edit Mode */}
                  {editMode && (
                    <Grid size={{ xs: 12 }}>
                      <TextField
                        fullWidth
                        label="Bio"
                        multiline
                        rows={3}
                        value={formData.bio}
                        onChange={(e) => handleChange('bio', e.target.value)}
                        placeholder="Tell us about yourself..."
                      />
                    </Grid>
                  )}

                  {/* Personal Info */}
                  <Grid size={{ xs: 12 }}>
                    <Typography variant="subtitle1" sx={{ fontWeight: 600, color: '#6C63FF', mb: 2 }}>
                      <PersonIcon sx={{ mr: 1, verticalAlign: 'middle' }} />
                      Personal Information
                    </Typography>
                  </Grid>

                  <Grid size={{ xs: 12, md: 6 }}>
                    {editMode ? (
                      <TextField
                        fullWidth
                        label="Phone"
                        value={formData.phone}
                        onChange={(e) => handleChange('phone', e.target.value)}
                        placeholder="+91 98765 43210"
                      />
                    ) : (
                      <Box>
                        <Typography variant="caption" color="text.secondary">Phone</Typography>
                        <Typography variant="body1">{profile.profile?.phone || 'Not set'}</Typography>
                      </Box>
                    )}
                  </Grid>

                  <Grid size={{ xs: 12, md: 6 }}>
                    {editMode ? (
                      <TextField
                        fullWidth
                        label="Location"
                        value={formData.location}
                        onChange={(e) => handleChange('location', e.target.value)}
                        placeholder="City, Country"
                      />
                    ) : (
                      <Box>
                        <Typography variant="caption" color="text.secondary">Location</Typography>
                        <Typography variant="body1">{profile.profile?.location || 'Not set'}</Typography>
                      </Box>
                    )}
                  </Grid>

                  <Grid size={{ xs: 12 }}>
                    {editMode ? (
                      <TextField
                        fullWidth
                        label="Website"
                        value={formData.website}
                        onChange={(e) => handleChange('website', e.target.value)}
                        placeholder="https://yourwebsite.com"
                      />
                    ) : (
                      <Box>
                        <Typography variant="caption" color="text.secondary">Website</Typography>
                        <Typography variant="body1">
                          {profile.profile?.website ? (
                            <a href={profile.profile.website} target="_blank" rel="noopener noreferrer">
                              {profile.profile.website}
                            </a>
                          ) : 'Not set'}
                        </Typography>
                      </Box>
                    )}
                  </Grid>

                  {/* Education & Experience */}
                  <Grid size={{ xs: 12 }}>
                    <Divider sx={{ my: 2 }} />
                    <Typography variant="subtitle1" sx={{ fontWeight: 600, color: '#6C63FF', mb: 2 }}>
                      <SchoolIcon sx={{ mr: 1, verticalAlign: 'middle' }} />
                      Education & Experience
                    </Typography>
                  </Grid>

                  <Grid size={{ xs: 12 }}>
                    {editMode ? (
                      <TextField
                        fullWidth
                        label="Education"
                        multiline
                        rows={2}
                        value={formData.education}
                        onChange={(e) => handleChange('education', e.target.value)}
                        placeholder="B.S. Computer Science, MIT"
                      />
                    ) : (
                      <Box>
                        <Typography variant="caption" color="text.secondary">Education</Typography>
                        <Typography variant="body1">{profile.profile?.education || 'Not set'}</Typography>
                      </Box>
                    )}
                  </Grid>

                  <Grid size={{ xs: 12 }}>
                    {editMode ? (
                      <TextField
                        fullWidth
                        label="Experience"
                        multiline
                        rows={2}
                        value={formData.experience}
                        onChange={(e) => handleChange('experience', e.target.value)}
                        placeholder="Senior Developer at Google (2018-2023)"
                      />
                    ) : (
                      <Box>
                        <Typography variant="caption" color="text.secondary">Experience</Typography>
                        <Typography variant="body1">{profile.profile?.experience || 'Not set'}</Typography>
                      </Box>
                    )}
                  </Grid>

                  <Grid size={{ xs: 12 }}>
                    {editMode ? (
                      <TextField
                        fullWidth
                        label="Skills (comma separated)"
                        value={formData.skills}
                        onChange={(e) => handleChange('skills', e.target.value)}
                        placeholder="Python, React, SQL, Docker"
                        helperText="Separate skills with commas"
                      />
                    ) : (
                      <Box>
                        <Typography variant="caption" color="text.secondary">Skills</Typography>
                        <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 0.5, mt: 1 }}>
                          {profile.profile?.skills ? (
                            profile.profile.skills.split(',').map((skill, i) => (
                              <Chip key={i} label={skill.trim()} size="small" sx={{ bgcolor: '#6C63FF', color: 'white' }} />
                            ))
                          ) : (
                            <Typography variant="body1">No skills added</Typography>
                          )}
                        </Box>
                      </Box>
                    )}
                  </Grid>

                  {/* Social Links */}
                  <Grid size={{ xs: 12 }}>
                    <Divider sx={{ my: 2 }} />
                    <Typography variant="subtitle1" sx={{ fontWeight: 600, color: '#6C63FF', mb: 2 }}>
                      🌐 Social Links
                    </Typography>
                  </Grid>

                  {['github', 'linkedin', 'twitter', 'youtube'].map((social) => (
                    <Grid size={{ xs: 12, md: 6 }} key={social}>
                      {editMode ? (
                        <TextField
                          fullWidth
                          label={social.charAt(0).toUpperCase() + social.slice(1)}
                          value={formData[social as keyof typeof formData] as string}
                          onChange={(e) => handleChange(social, e.target.value)}
                          placeholder={`https://${social}.com/yourusername`}
                        />
                      ) : (
                        <Box>
                          <Typography variant="caption" color="text.secondary">
                            {social.charAt(0).toUpperCase() + social.slice(1)}
                          </Typography>
                          <Typography variant="body1">
                            {profile.profile?.[social as keyof typeof profile.profile] ? (
                              <a href={profile.profile?.[social as keyof typeof profile.profile] as string} target="_blank" rel="noopener noreferrer">
                                {profile.profile?.[social as keyof typeof profile.profile] as string}
                              </a>
                            ) : 'Not set'}
                          </Typography>
                        </Box>
                      )}
                    </Grid>
                  ))}

                  {/* Preferences */}
                  <Grid size={{ xs: 12 }}>
                    <Divider sx={{ my: 2 }} />
                    <Typography variant="subtitle1" sx={{ fontWeight: 600, color: '#6C63FF', mb: 2 }}>
                      ⚙️ Preferences
                    </Typography>
                  </Grid>

                  <Grid size={{ xs: 12, md: 6 }}>
                    {editMode ? (
                      <FormControlLabel
                        control={
                          <Switch
                            checked={formData.email_notifications}
                            onChange={(e) => handleChange('email_notifications', e.target.checked)}
                          />
                        }
                        label="Email Notifications"
                      />
                    ) : (
                      <Box>
                        <Typography variant="body1">
                          Email Notifications: {profile.profile?.email_notifications ? '✅ Enabled' : '❌ Disabled'}
                        </Typography>
                      </Box>
                    )}
                  </Grid>

                  <Grid size={{ xs: 12, md: 6 }}>
                    {editMode ? (
                      <FormControlLabel
                        control={
                          <Switch
                            checked={formData.course_updates}
                            onChange={(e) => handleChange('course_updates', e.target.checked)}
                          />
                        }
                        label="Course Updates"
                      />
                    ) : (
                      <Box>
                        <Typography variant="body1">
                          Course Updates: {profile.profile?.course_updates ? '✅ Enabled' : '❌ Disabled'}
                        </Typography>
                      </Box>
                    )}
                  </Grid>
                </Grid>

                {/* Edit Mode - Bottom Actions */}
                {editMode && (
                  <Box sx={{ mt: 4, display: 'flex', justifyContent: 'flex-end', gap: 2 }}>
                    <Button
                      variant="outlined"
                      onClick={handleCancel}
                      sx={{ color: '#666', borderColor: '#ddd' }}
                    >
                      Cancel
                    </Button>
                    <Button
                      variant="contained"
                      onClick={handleSave}
                      disabled={saving}
                      sx={{ bgcolor: '#6C63FF', '&:hover': { bgcolor: '#5A52D9' } }}
                    >
                      {saving ? <CircularProgress size={24} /> : 'Save Profile'}
                    </Button>
                  </Box>
                )}
              </Paper>
            </motion.div>
          </Grid>
        </Grid>
      </motion.div>
    </Container>
  );
};

export default Profile;