import { useMemo, useState } from 'react';
import {
  Paper,
  Box,
  Typography,
  IconButton,
  Tabs,
  Tab,
  Grid,
  Card,
  CardContent,
  Chip,
  List,
  ListItem,
  ListItemIcon,
  ListItemText,
  Tooltip,
  Stack,
  Button
} from '@mui/material';
import {
  Print,
  Download,
  CheckCircle,
  Error as ErrorIcon,
  Info
} from '@mui/icons-material';

const sanitizeMessages = (items = []) =>
  items
    .filter((message) => message && typeof message === 'string')
    .map((message) => message.trim())
    .filter((message) => message.length > 0 && !message.toLowerCase().includes('gemini feedback generation failed'));

const cleanText = (text) => {
  if (!text || typeof text !== 'string') return text;
  if (text.toLowerCase().includes('gemini feedback generation failed')) {
    return 'We could not retrieve AI feedback for this section. Please try again after verifying your Gemini access.';
  }
  return text;
};

const ReportViewer = ({ report, onDownload, onPrint }) => {
  const [viewMode, setViewMode] = useState(0);

  const data = report || {
    score: 86,
    sections: {
      overview: {
        score: 88,
        summary: 'Strong overall alignment with job requirements and keyword coverage.'
      },
      experience: {
        score: 82,
        summary: 'Relevant experience but lacks quantifiable results in several roles.'
      },
      skills: {
        score: 90,
        summary: 'Excellent technical skill coverage with only a few gaps.'
      },
      education: {
        score: 84,
        summary: 'Well-structured education section with relevant coursework.'
      }
    },
    suggestions: [
      'Add measurable outcomes to your recent role to strengthen impact.',
      'Include hands-on experience with Docker and Kubernetes.',
      'Consider adding a brief professional summary at the top of the resume.'
    ],
    matchedKeywords: ['React', 'Node.js', 'REST APIs', 'MongoDB', 'AWS'],
    missingKeywords: ['Docker', 'Kubernetes'],
    rawJson: {
      similarity_score: 0.86,
      matched_keywords: ['React', 'Node.js', 'REST APIs', 'MongoDB', 'AWS'],
      missing_keywords: ['Docker', 'Kubernetes'],
      match_percentage: 86,
      recommendations: ['Add quantifiable metrics', 'Highlight DevOps tooling']
    }
  };

  const filteredSuggestions = useMemo(() => sanitizeMessages(data.suggestions), [data.suggestions]);
  const filteredMatchedKeywords = useMemo(
    () => (data.matchedKeywords || []).filter(Boolean),
    [data.matchedKeywords]
  );
  const filteredMissingKeywords = useMemo(
    () => (data.missingKeywords || []).filter(Boolean),
    [data.missingKeywords]
  );

  const scoreMessage = useMemo(() => {
    const scoreValue = Number(data.score);
    if (!Number.isFinite(scoreValue)) {
      return 'Upload a resume to see your overall alignment score.';
    }
    if (scoreValue >= 80) {
      return 'Outstanding alignment—fine-tune a few areas to push beyond 90%.';
    }
    if (scoreValue >= 50) {
      return 'Solid foundation. Address the highlighted gaps to raise your score.';
    }
    return 'Focus on the recommendations and missing keywords to strengthen alignment quickly.';
  }, [data.score]);

  return (
    <Paper sx={{ p: 3 }}>
      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 3 }}>
        <Box>
          <Typography variant="h5">Analysis Report</Typography>
          <Typography variant="body2" color="text.secondary">
            Comprehensive insights based on your latest upload
          </Typography>
        </Box>
        <Stack direction="row" spacing={1}>
          <Tooltip title="Print report">
            <span>
              <IconButton color="primary" onClick={onPrint}>
                <Print />
              </IconButton>
            </span>
          </Tooltip>
          <Tooltip title="Download report">
            <span>
              <IconButton color="primary" onClick={onDownload}>
                <Download />
              </IconButton>
            </span>
          </Tooltip>
        </Stack>
      </Box>

      <Tabs value={viewMode} onChange={(event, value) => setViewMode(value)} sx={{ mb: 3 }}>
        <Tab label="Visual Summary" />
        <Tab label="JSON Output" />
      </Tabs>

      {viewMode === 0 ? (
        <Box>
          <Card sx={{ mb: 3, bgcolor: 'success.light', color: 'success.dark', border: '1px solid', borderColor: 'success.main' }}>
            <CardContent>
              <Typography variant="subtitle2" gutterBottom>
                Overall Score
              </Typography>
              <Typography variant="h3" fontWeight={700}>
                {data.score}%
              </Typography>
              <Typography variant="body2">
                {scoreMessage}
              </Typography>
            </CardContent>
          </Card>

          <Grid container spacing={2}>
            {Object.entries(data.sections).map(([key, value]) => (
              <Grid item xs={12} md={6} key={key}>
                <Card>
                  <CardContent>
                    <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 1 }}>
                      <Typography variant="subtitle1" sx={{ textTransform: 'capitalize' }}>
                        {key}
                      </Typography>
                      <Chip label={`${value.score}%`} color={value.score >= 80 ? 'success' : 'warning'} size="small" />
                    </Box>
                    <Typography variant="body2" color="text.secondary">
                      {cleanText(value.summary)}
                    </Typography>
                  </CardContent>
                </Card>
              </Grid>
            ))}
          </Grid>

          <Card sx={{ mt: 3 }}>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Recommendations
              </Typography>
              {filteredSuggestions.length ? (
                <List>
                  {filteredSuggestions.map((suggestion, index) => (
                    <ListItem key={index}>
                      <ListItemIcon>
                        <CheckCircle color="success" />
                      </ListItemIcon>
                      <ListItemText primary={suggestion} />
                    </ListItem>
                  ))}
                </List>
              ) : (
                <Typography variant="body2" color="text.secondary">
                  No AI-generated recommendations are available right now. Try re-running the analysis after verifying your AI integration.
                </Typography>
              )}
            </CardContent>
          </Card>

          <Grid container spacing={2} sx={{ mt: 1 }}>
            <Grid item xs={12} md={6}>
              <Card>
                <CardContent>
                  <Typography variant="subtitle1" gutterBottom>
                    Matched Keywords
                  </Typography>
                  <Stack direction="row" spacing={1} flexWrap="wrap" useFlexGap>
                    {filteredMatchedKeywords.map((keyword) => (
                      <Chip key={keyword} label={keyword} color="success" variant="outlined" />
                    ))}
                  </Stack>
                </CardContent>
              </Card>
            </Grid>
            <Grid item xs={12} md={6}>
              <Card>
                <CardContent>
                  <Typography variant="subtitle1" gutterBottom>
                    Missing Keywords
                  </Typography>
                  {filteredMissingKeywords.length ? (
                    <Stack direction="row" spacing={1} flexWrap="wrap" useFlexGap>
                      {filteredMissingKeywords.map((keyword) => (
                        <Chip key={keyword} label={keyword} color="warning" icon={<ErrorIcon />} />
                      ))}
                    </Stack>
                  ) : (
                    <Chip label="No gaps detected" color="success" icon={<CheckCircle />} />
                  )}
                </CardContent>
              </Card>
            </Grid>
          </Grid>
        </Box>
      ) : (
        <Paper sx={{ p: 2, bgcolor: 'grey.100' }}>
          <Typography variant="subtitle2" gutterBottom>
            Raw Analysis Output
          </Typography>
          <pre style={{ overflow: 'auto', fontSize: '0.875rem', margin: 0 }}>
            {JSON.stringify(data.rawJson, null, 2)}
          </pre>
          <Box sx={{ mt: 2, display: 'flex', alignItems: 'center', gap: 1 }}>
            <Info color="info" fontSize="small" />
            <Typography variant="caption" color="text.secondary">
              Export the JSON for custom dashboards or ATS integrations.
            </Typography>
          </Box>
        </Paper>
      )}
    </Paper>
  );
};

export default ReportViewer;
