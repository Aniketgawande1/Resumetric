import { useState } from 'react';
import {
  Container,
  Typography,
  Grid,
  Paper,
  Avatar,
  Button,
  TextField,
  List,
  ListItem,
  ListItemText,
  Switch,
  Divider
} from '@mui/material';

const ProfileSettings = ({ user }) => {
  const [preferences, setPreferences] = useState({
    emailNotifications: true,
    autoSaveReports: true,
    darkMode: false,
    shareAnalytics: true
  });

  const togglePreference = (key) => {
    setPreferences((prev) => ({ ...prev, [key]: !prev[key] }));
  };

  return (
    <Container maxWidth="md" sx={{ py: 4 }}>
      <Typography variant="h4" gutterBottom>
        Profile & Settings
      </Typography>

      <Grid container spacing={3}>
        <Grid item xs={12} md={4}>
          <Paper sx={{ p: 3, textAlign: 'center' }}>
            <Avatar sx={{ width: 96, height: 96, mx: 'auto', mb: 2, bgcolor: 'primary.main' }}>
              {user?.name?.[0]?.toUpperCase() || 'U'}
            </Avatar>
            <Typography variant="h6">{user?.name || 'Resumetric User'}</Typography>
            <Typography variant="body2" color="text.secondary">
              {user?.email || 'user@example.com'}
            </Typography>
            <Button variant="outlined" fullWidth sx={{ mt: 2 }}>
              Change Avatar
            </Button>
          </Paper>
        </Grid>

        <Grid item xs={12} md={8}>
          <Paper sx={{ p: 3, mb: 3 }}>
            <Typography variant="h6" gutterBottom>
              Account Information
            </Typography>
            <Grid container spacing={2}>
              <Grid item xs={12}>
                <TextField fullWidth label="Full Name" defaultValue={user?.name} variant="outlined" />
              </Grid>
              <Grid item xs={12}>
                <TextField fullWidth label="Email" defaultValue={user?.email} variant="outlined" />
              </Grid>
              <Grid item xs={12}>
                <TextField fullWidth label="Phone" defaultValue="+1 (555) 123-4567" variant="outlined" />
              </Grid>
              <Grid item xs={12}>
                <Button variant="contained">Update Profile</Button>
              </Grid>
            </Grid>
          </Paper>

          <Paper sx={{ p: 3 }}>
            <Typography variant="h6" gutterBottom>
              Preferences
            </Typography>
            <List>
              <ListItem>
                <ListItemText primary="Email Notifications" secondary="Receive updates about your resume analysis" />
                <Switch checked={preferences.emailNotifications} onChange={() => togglePreference('emailNotifications')} />
              </ListItem>
              <Divider />
              <ListItem>
                <ListItemText primary="Auto-save Reports" secondary="Automatically keep your report history up to date" />
                <Switch checked={preferences.autoSaveReports} onChange={() => togglePreference('autoSaveReports')} />
              </ListItem>
              <Divider />
              <ListItem>
                <ListItemText primary="Dark Mode" secondary="Toggle dark theme (coming soon)" />
                <Switch checked={preferences.darkMode} onChange={() => togglePreference('darkMode')} />
              </ListItem>
              <Divider />
              <ListItem>
                <ListItemText primary="Share Analytics" secondary="Help improve Resumetric with anonymous usage data" />
                <Switch checked={preferences.shareAnalytics} onChange={() => togglePreference('shareAnalytics')} />
              </ListItem>
            </List>
          </Paper>
        </Grid>
      </Grid>
    </Container>
  );
};

export default ProfileSettings;
