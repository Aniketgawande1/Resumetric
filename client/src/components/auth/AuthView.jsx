import { useState } from 'react';
import {
  Alert,
  Box,
  Container,
  Paper,
  Typography,
  TextField,
  Button,
  Divider,
  Stack
} from '@mui/material';
import { Google, GitHub, LinkedIn, Assessment } from '@mui/icons-material';

const AuthView = ({ onAuthenticate, onOAuth, loading = false, error }) => {
  const [isSignup, setIsSignup] = useState(false);
  const [form, setForm] = useState({ name: '', email: '', password: '' });
  const [formError, setFormError] = useState(null);

  const handleSubmit = async (event) => {
    event.preventDefault();
    setFormError(null);

    if (!form.email || !form.password) {
      setFormError('Email and password are required.');
      return;
    }

    if (isSignup && !form.name.trim()) {
      setFormError('Please provide your name to create an account.');
      return;
    }

    try {
      await onAuthenticate?.({
        mode: isSignup ? 'signup' : 'login',
        data: {
          name: form.name.trim(),
          email: form.email.trim(),
          password: form.password
        }
      });
    } catch (submitError) {
      setFormError(submitError.message || 'Authentication failed.');
    }
  };

  const handleOAuth = (provider) => {
    onOAuth?.(provider);
  };

  return (
    <Box
      sx={{
        minHeight: '100vh',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        bgcolor: 'background.default',
        py: 6
      }}
    >
      <Container maxWidth="xs">
        <Paper elevation={2} sx={{ p: 4 }}>
          <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'center', mb: 3 }}>
            <Assessment sx={{ fontSize: 40, color: 'primary.main', mr: 1 }} />
            <Typography variant="h4" color="primary">
              Resumetric
            </Typography>
          </Box>

          <Typography variant="h5" align="center" gutterBottom>
            {isSignup ? 'Create Account' : 'Welcome Back'}
          </Typography>
          <Typography variant="body2" align="center" color="text.secondary" sx={{ mb: 3 }}>
            {isSignup ? 'Sign up to start analyzing your resumes instantly.' : 'Log in to view your reports and analyze new resumes.'}
          </Typography>

          {(formError || error) && (
            <Alert severity="error" sx={{ mb: 2 }}>
              {formError || error}
            </Alert>
          )}

          <form onSubmit={handleSubmit} noValidate>
            {isSignup && (
              <TextField
                fullWidth
                label="Full Name"
                variant="outlined"
                margin="normal"
                value={form.name}
                onChange={(e) => setForm({ ...form, name: e.target.value })}
                disabled={loading}
              />
            )}
            <TextField
              fullWidth
              label="Email"
              type="email"
              variant="outlined"
              required
              margin="normal"
              value={form.email}
              onChange={(e) => setForm({ ...form, email: e.target.value })}
              disabled={loading}
            />
            <TextField
              fullWidth
              label="Password"
              type="password"
              variant="outlined"
              required
              margin="normal"
              value={form.password}
              onChange={(e) => setForm({ ...form, password: e.target.value })}
              disabled={loading}
            />
            <Button type="submit" fullWidth variant="contained" size="large" sx={{ mt: 3 }} disabled={loading}>
              {loading ? 'Please wait…' : isSignup ? 'Sign Up' : 'Login'}
            </Button>
          </form>

          <Divider sx={{ my: 3 }}>OR</Divider>

          <Stack spacing={1.5}>
            <Button variant="outlined" startIcon={<Google />} onClick={() => handleOAuth('Google')} disabled={loading}>
              Continue with Google
            </Button>
            <Button variant="outlined" startIcon={<GitHub />} onClick={() => handleOAuth('GitHub')} disabled={loading}>
              Continue with GitHub
            </Button>
            <Button variant="outlined" startIcon={<LinkedIn />} onClick={() => handleOAuth('LinkedIn')} disabled={loading}>
              Continue with LinkedIn
            </Button>
          </Stack>

          <Box sx={{ mt: 3, textAlign: 'center' }}>
            <Typography variant="body2">
              {isSignup ? 'Already have an account?' : "Don’t have an account?"}
              <Button
                onClick={() => setIsSignup(!isSignup)}
                sx={{ textTransform: 'none', ml: 1 }}
                disabled={loading}
              >
                {isSignup ? 'Login' : 'Sign Up'}
              </Button>
            </Typography>
          </Box>
        </Paper>
      </Container>
    </Box>
  );
};

export default AuthView;
