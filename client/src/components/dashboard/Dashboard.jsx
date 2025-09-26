import {
  Box,
  Container,
  Typography,
  Grid,
  Card,
  CardContent,
  Avatar,
  Chip,
  Divider,
  List,
  ListItem,
  ListItemText,
  Button,
  LinearProgress
} from '@mui/material';
import {
  Description,
  TrendingUp,
  Assessment,
  Code,
  Visibility
} from '@mui/icons-material';
import FileUpload from '../upload/FileUpload';

const formatNumber = (value, suffix = '') => {
  if (value === null || value === undefined) return `--${suffix}`;
  if (typeof value === 'number' && Number.isFinite(value)) {
    return `${Math.round(value)}${suffix}`;
  }
  return `${value}${suffix}`;
};

const Dashboard = ({ user, reports, onUpload, loading, recentReport }) => {
  const totalAnalyzed = reports.length;
  const scores = reports
    .map((report) => Number(report.score ?? report.summary?.score))
    .filter((value) => Number.isFinite(value));
  const averageScore = scores.length ? scores.reduce((acc, curr) => acc + curr, 0) / scores.length : null;
  const skillsIdentified = reports.reduce((acc, report) => {
    const matched = report.summary?.matchedKeywords?.length || report.matchedKeywords?.length || 0;
    return acc + matched;
  }, 0);

  const stats = [
    {
      label: 'Resumes Analyzed',
      value: formatNumber(totalAnalyzed),
      icon: <Description />,
      avatarBg: 'grey.900',
      avatarColor: 'common.white'
    },
    {
      label: 'Average Score',
      value: averageScore !== null ? `${Math.round(averageScore)}%` : '--%',
      icon: <TrendingUp />,
      avatarBg: 'success.light',
      avatarColor: 'success.dark'
    },
    {
      label: 'Reports Generated',
      value: formatNumber(reports.filter((item) => item.downloadUrl).length),
      icon: <Assessment />,
      avatarBg: 'grey.200',
      avatarColor: 'text.primary'
    },
    {
      label: 'Skills Identified',
      value: formatNumber(skillsIdentified),
      icon: <Code />,
      avatarBg: 'secondary.light',
      avatarColor: 'common.white'
    }
  ];

  return (
    <Container maxWidth="lg" sx={{ py: 4 }}>
      <Typography variant="h4" gutterBottom>
        Welcome back, {user?.name || 'User'}!
      </Typography>
      <Typography variant="body1" color="text.secondary" sx={{ mb: 4 }}>
        Here’s what’s happening with your resume analysis.
      </Typography>

      <Grid container spacing={3}>
        {stats.map((stat) => (
          <Grid item xs={12} sm={6} md={3} key={stat.label}>
            <Card sx={{ height: '100%' }}>
              <CardContent>
                <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                  <Avatar sx={{ bgcolor: stat.avatarBg, color: stat.avatarColor, mr: 2 }}>
                    {stat.icon}
                  </Avatar>
                  <Box>
                    <Typography variant="h6" fontWeight={700}>
                      {stat.value}
                    </Typography>
                    <Typography variant="caption" color="text.secondary">
                      {stat.label}
                    </Typography>
                  </Box>
                </Box>
              </CardContent>
            </Card>
          </Grid>
        ))}
      </Grid>

      <Grid container spacing={3} sx={{ mt: 1 }}>
        <Grid item xs={12} md={8}>
          <Card sx={{ p: 3 }}>
            <Typography variant="h6" gutterBottom>
              Upload New Resume
            </Typography>
            <FileUpload onUpload={onUpload} loading={loading} />
          </Card>
        </Grid>
        <Grid item xs={12} md={4}>
          <Card sx={{ p: 3, height: '100%' }}>
            <Typography variant="h6" gutterBottom>
              Recent Analysis
            </Typography>
            {recentReport ? (
              <Box>
                <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 2 }}>
                  <Typography variant="body2" color="text.secondary">
                    Overall Score
                  </Typography>
                  <Chip
                    label={recentReport.score !== undefined && recentReport.score !== null ? `${Math.round(recentReport.score)}%` : '--'}
                    color="success"
                    size="small"
                  />
                </Box>
                {Number.isFinite(recentReport.score) && (
                  <LinearProgress
                    variant="determinate"
                    value={Math.min(Math.max(recentReport.score, 0), 100)}
                    color="success"
                    sx={{ height: 8, borderRadius: 999, mb: 2, bgcolor: 'grey.200' }}
                  />
                )}
                <Divider sx={{ my: 2 }} />
                <Typography variant="subtitle2" gutterBottom>
                  Highlights
                </Typography>
                <List dense>
                  {recentReport.highlights.map((item, idx) => (
                    <ListItem key={idx} disablePadding>
                      <ListItemText primary={item} primaryTypographyProps={{ variant: 'body2' }} />
                    </ListItem>
                  ))}
                </List>
                {recentReport.onView && (
                  <Button
                    fullWidth
                    variant="outlined"
                    startIcon={<Visibility />}
                    sx={{ mt: 2 }}
                    onClick={recentReport.onView}
                  >
                    View Full Report
                  </Button>
                )}
              </Box>
            ) : (
              <Box sx={{ textAlign: 'center', py: 4 }}>
                <Typography variant="body2" color="text.secondary">
                  No recent reports. Upload a resume to get started!
                </Typography>
              </Box>
            )}
          </Card>
        </Grid>
      </Grid>
    </Container>
  );
};

export default Dashboard;
