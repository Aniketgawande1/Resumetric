import { Backdrop, CircularProgress, Typography, Box } from '@mui/material';

const GlobalLoader = ({ open, message = 'Processing your request...' }) => (
  <Backdrop
    sx={{ color: '#fff', zIndex: (theme) => theme.zIndex.drawer + 1, display: 'flex', flexDirection: 'column', gap: 2 }}
    open={open}
  >
    <CircularProgress color="inherit" size={48} thickness={4} />
    <Box textAlign="center">
      <Typography variant="body1" fontWeight={600}>
        {message}
      </Typography>
      <Typography variant="body2" sx={{ opacity: 0.75 }}>
        This usually takes just a moment.
      </Typography>
    </Box>
  </Backdrop>
);

export default GlobalLoader;
