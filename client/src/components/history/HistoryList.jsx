import { Fragment } from 'react';
import {
  Container,
  Typography,
  Paper,
  List,
  ListItem,
  ListItemIcon,
  ListItemText,
  IconButton,
  Chip,
  Divider,
  Tooltip
} from '@mui/material';
import { FilePresent, Visibility, Download } from '@mui/icons-material';

const formatDate = (value) => {
  if (!value) return 'Unknown date';
  const parsed = new Date(value);
  if (Number.isNaN(parsed.getTime())) return value;
  return parsed.toLocaleString();
};

const getChipColor = (score) => {
  if (!Number.isFinite(score)) return 'default';
  return score >= 80 ? 'success' : 'warning';
};

const HistoryList = ({ items, onView, onDownload }) => (
  <Container maxWidth="lg" sx={{ py: 4 }}>
    <Typography variant="h4" gutterBottom>
      Upload History
    </Typography>
    <Paper>
      <List>
        {items.map((item, index) => (
          <Fragment key={item.id}>
            <ListItem
              sx={{ py: 2, '&:hover': { bgcolor: 'grey.50' } }}
              secondaryAction={
                <>
                  <Chip
                    label={`Score: ${Number.isFinite(item.score) ? Math.round(item.score) : '--'}%`}
                    color={getChipColor(item.score)}
                    sx={{ mr: 2 }}
                  />
                  <Tooltip title={item.summary ? 'View in app' : 'No preview available'}>
                    <span>
                      <IconButton
                        edge="end"
                        color="primary"
                        disabled={!onView || !item.summary}
                        onClick={() => onView?.(item)}
                      >
                        <Visibility />
                      </IconButton>
                    </span>
                  </Tooltip>
                  {item.downloadUrl && (
                    <Tooltip title="Download report">
                      <IconButton edge="end" color="secondary" onClick={() => onDownload?.(item)}>
                        <Download />
                      </IconButton>
                    </Tooltip>
                  )}
                </>
              }
            >
              <ListItemIcon>
                <FilePresent color="primary" />
              </ListItemIcon>
              <ListItemText
                primary={item.filename}
                secondary={`Uploaded on ${formatDate(item.date)}`}
              />
            </ListItem>
            {index < items.length - 1 && <Divider component="li" />}
          </Fragment>
        ))}
      </List>
    </Paper>
  </Container>
);

export default HistoryList;
