import { Alert, Snackbar } from '@mui/material';

const NotificationSystem = ({ notifications, onClose }) => (
  <>
    {notifications.map((notif) => (
      <Snackbar
        key={notif.id}
        open={notif.open}
        autoHideDuration={notif.type === 'error' ? 6000 : 4000}
        onClose={() => onClose(notif.id)}
        anchorOrigin={{ vertical: 'top', horizontal: 'right' }}
      >
        <Alert
          onClose={() => onClose(notif.id)}
          severity={notif.type}
          variant="filled"
          sx={{ width: '100%' }}
        >
          {notif.message}
        </Alert>
      </Snackbar>
    ))}
  </>
);

export default NotificationSystem;
