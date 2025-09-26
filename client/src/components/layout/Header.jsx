import { useState } from 'react';
import {
  AppBar,
  Toolbar,
  Typography,
  IconButton,
  Button,
  Box,
  Badge,
  Avatar,
  Menu,
  MenuItem,
  Divider,
  Tooltip,
  List,
  ListItem,
  ListItemIcon,
  ListItemText
} from '@mui/material';
import {
  Menu as MenuIcon,
  Dashboard,
  History,
  Person,
  ExitToApp,
  Notifications,
  CheckCircle,
  Info,
  TrendingUp,
  Settings,
  Assessment
} from '@mui/icons-material';

const navItems = [
  { id: 'dashboard', label: 'Dashboard', icon: <Dashboard fontSize="small" /> },
  { id: 'history', label: 'History', icon: <History fontSize="small" /> },
  { id: 'reports', label: 'Reports', icon: <Assessment fontSize="small" /> },
  { id: 'profile', label: 'Profile', icon: <Person fontSize="small" /> }
];

const Header = ({ onMenuToggle, currentPage, onNavigate, user, onLogout }) => {
  const [profileAnchor, setProfileAnchor] = useState(null);
  const [notifAnchor, setNotifAnchor] = useState(null);

  const handleNavigate = (page) => {
    onNavigate(page);
  };

  return (
    <AppBar
      position="sticky"
      elevation={0}
      color="default"
      sx={{ bgcolor: 'background.paper', borderBottom: '1px solid', borderColor: 'divider' }}
    >
      <Toolbar>
        <IconButton edge="start" onClick={onMenuToggle} sx={{ mr: 2, display: { md: 'none' } }}>
          <MenuIcon />
        </IconButton>

        <Assessment sx={{ mr: 2, color: 'text.primary', fontSize: 32 }} />
        <Typography variant="h5" sx={{ flexGrow: 1, color: 'text.primary', fontWeight: 700 }}>
          Resumetric
        </Typography>

        <Box sx={{ display: { xs: 'none', md: 'flex' }, gap: 1.5, mr: 3 }}>
          {navItems.map((item) => (
            <Button
              key={item.id}
              startIcon={item.icon}
              color={currentPage === item.id ? 'primary' : 'inherit'}
              sx={{
                color: currentPage === item.id ? 'primary.main' : 'text.primary',
                fontWeight: currentPage === item.id ? 600 : 500
              }}
              onClick={() => handleNavigate(item.id)}
            >
              {item.label}
            </Button>
          ))}
        </Box>

        <Tooltip title="Notifications">
          <IconButton onClick={(e) => setNotifAnchor(e.currentTarget)} sx={{ mr: 2 }}>
            <Badge badgeContent={3} color="error">
              <Notifications />
            </Badge>
          </IconButton>
        </Tooltip>

        <Menu
          anchorEl={notifAnchor}
          open={Boolean(notifAnchor)}
          onClose={() => setNotifAnchor(null)}
          PaperProps={{ sx: { width: 320, mt: 1 } }}
        >
          <Box sx={{ p: 2 }}>
            <Typography variant="h6" gutterBottom>
              Notifications
            </Typography>
            <Divider sx={{ my: 1 }} />
            <List dense>
              <ListItem>
                <ListItemIcon>
                  <CheckCircle color="success" fontSize="small" />
                </ListItemIcon>
                <ListItemText primary="Resume analyzed successfully" secondary="2 minutes ago" />
              </ListItem>
              <ListItem>
                <ListItemIcon>
                  <Info color="info" fontSize="small" />
                </ListItemIcon>
                <ListItemText primary="New feature: JSON export enabled" secondary="1 hour ago" />
              </ListItem>
              <ListItem>
                <ListItemIcon>
                  <TrendingUp color="primary" fontSize="small" />
                </ListItemIcon>
                <ListItemText primary="Your resume score improved" secondary="Yesterday" />
              </ListItem>
            </List>
          </Box>
        </Menu>

        <IconButton onClick={(e) => setProfileAnchor(e.currentTarget)}>
          <Avatar sx={{ bgcolor: 'grey.900', color: 'common.white', width: 36, height: 36 }}>
            {user?.name?.[0]?.toUpperCase() || 'U'}
          </Avatar>
        </IconButton>

        <Menu anchorEl={profileAnchor} open={Boolean(profileAnchor)} onClose={() => setProfileAnchor(null)}>
          <MenuItem onClick={() => { handleNavigate('profile'); setProfileAnchor(null); }}>
            <ListItemIcon>
              <Person fontSize="small" />
            </ListItemIcon>
            Profile
          </MenuItem>
          <MenuItem onClick={() => { handleNavigate('settings'); setProfileAnchor(null); }}>
            <ListItemIcon>
              <Settings fontSize="small" />
            </ListItemIcon>
            Settings
          </MenuItem>
          <Divider />
          <MenuItem onClick={() => { setProfileAnchor(null); onLogout(); }}>
            <ListItemIcon>
              <ExitToApp fontSize="small" />
            </ListItemIcon>
            Logout
          </MenuItem>
        </Menu>
      </Toolbar>
    </AppBar>
  );
};

export default Header;
