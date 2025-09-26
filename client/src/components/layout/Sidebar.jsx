import {
  Drawer,
  Box,
  Typography,
  Divider,
  List,
  ListItemButton,
  ListItemIcon,
  ListItemText
} from '@mui/material';
import {
  Dashboard,
  History,
  Person,
  Settings,
  Assessment
} from '@mui/icons-material';

const menuItems = [
  { id: 'dashboard', label: 'Dashboard', icon: <Dashboard /> },
  { id: 'history', label: 'History', icon: <History /> },
  { id: 'reports', label: 'Reports', icon: <Assessment /> },
  { id: 'profile', label: 'Profile', icon: <Person /> },
  { id: 'settings', label: 'Settings', icon: <Settings /> }
];

const Sidebar = ({ open, onClose, currentPage, onNavigate }) => (
  <Drawer
    variant="temporary"
    open={open}
    onClose={onClose}
    ModalProps={{ keepMounted: true }}
    sx={{
      display: { xs: 'block', md: 'none' },
      '& .MuiDrawer-paper': { width: 260, bgcolor: 'background.paper' }
    }}
  >
    <Box sx={{ p: 3 }}>
      <Typography variant="h6" color="text.primary">
        Resumetric Menu
      </Typography>
    </Box>
    <Divider />
    <List>
      {menuItems.map((item) => (
        <ListItemButton
          key={item.id}
          selected={currentPage === item.id}
          sx={{
            '&.Mui-selected': {
              bgcolor: 'grey.100',
              '&:hover': { bgcolor: 'grey.200' }
            }
          }}
          onClick={() => {
            onNavigate(item.id);
            onClose();
          }}
        >
          <ListItemIcon>{item.icon}</ListItemIcon>
          <ListItemText primary={item.label} />
        </ListItemButton>
      ))}
    </List>
  </Drawer>
);

export default Sidebar;
