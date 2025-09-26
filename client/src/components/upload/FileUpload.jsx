import { useState } from 'react';
import {
  Alert,
  Paper,
  Box,
  Typography,
  Button,
  Chip,
  LinearProgress,
  TextField,
  FormControlLabel,
  Switch,
  Stack
} from '@mui/material';
import { CloudUpload, FilePresent } from '@mui/icons-material';

const FileUpload = ({ onUpload, loading }) => {
  const [file, setFile] = useState(null);
  const [dragActive, setDragActive] = useState(false);
  const [jobDescription, setJobDescription] = useState('');
  const [sendEmail, setSendEmail] = useState(false);
  const [error, setError] = useState(null);
  const [isUploading, setIsUploading] = useState(false);

  const handleDrag = (event) => {
    event.preventDefault();
    event.stopPropagation();

    if (event.type === 'dragenter' || event.type === 'dragover') {
      setDragActive(true);
    } else if (event.type === 'dragleave') {
      setDragActive(false);
    }
  };

  const handleDrop = (event) => {
    event.preventDefault();
    event.stopPropagation();
    setDragActive(false);

    const droppedFile = event.dataTransfer?.files?.[0];
    if (droppedFile && droppedFile.type === 'application/pdf') {
      setFile(droppedFile);
      setError(null);
    } else if (droppedFile) {
      setError('Please upload a PDF file.');
    }
  };

  const handleFileSelect = (event) => {
    const selectedFile = event.target.files?.[0];
    if (selectedFile && selectedFile.type === 'application/pdf') {
      setFile(selectedFile);
      setError(null);
    } else if (selectedFile) {
      setError('Please upload a PDF file.');
    }
  };

  const handleUpload = async () => {
    if (!file) {
      setError('Please select a PDF resume to analyze.');
      return;
    }

    if (!jobDescription.trim()) {
      setError('Add the job description or summary so we can compare it with your resume.');
      return;
    }
    setError(null);
    setIsUploading(true);

    try {
      await onUpload?.({ file, jobDescription, sendEmail });
      setFile(null);
      setJobDescription('');
      setSendEmail(false);
    } catch (uploadError) {
      setError(uploadError.message || 'Failed to analyze the resume. Please try again.');
    } finally {
      setIsUploading(false);
    }
  };

  const isBusy = loading || isUploading;

  return (
    <Paper
      sx={{
        p: 4,
        border: dragActive ? '2px dashed #2563eb' : '2px dashed #e5e7eb',
        bgcolor: dragActive ? 'primary.light' : 'background.paper',
        transition: 'all 0.3s ease-in-out'
      }}
      onDragEnter={handleDrag}
      onDragLeave={handleDrag}
      onDragOver={handleDrag}
      onDrop={handleDrop}
    >
      <Box sx={{ textAlign: 'center' }}>
        <CloudUpload sx={{ fontSize: 48, color: 'primary.main', mb: 2 }} />
        <Typography variant="h6" gutterBottom>
          Upload your resume for AI-powered analysis
        </Typography>
        <Typography variant="body2" color="text.secondary" sx={{ mb: 3 }}>
          Supported format: PDF • Max size 10MB
        </Typography>

        <input
          id="resume-input"
          type="file"
          accept=".pdf"
          style={{ display: 'none' }}
          onChange={handleFileSelect}
        />
        <label htmlFor="resume-input">
          <Button variant="outlined" component="span" startIcon={<FilePresent />} disabled={isBusy}>
            Select File
          </Button>
        </label>

        {file && (
          <Stack spacing={2} sx={{ mt: 3 }} alignItems="center">
            <Chip
              color="primary"
              variant="outlined"
              icon={<FilePresent />}
              label={file.name}
              onDelete={isBusy ? undefined : () => setFile(null)}
            />

            <TextField
              label="Job Description / Role Summary"
              placeholder="Paste the job description or key requirements here..."
              multiline
              minRows={4}
              fullWidth
              value={jobDescription}
              onChange={(event) => setJobDescription(event.target.value)}
              disabled={isBusy}
            />

            <FormControlLabel
              control={
                <Switch
                  checked={sendEmail}
                  onChange={(event) => setSendEmail(event.target.checked)}
                  disabled={isBusy}
                />
              }
              label="Email me the detailed analysis"
            />

            <Button
              variant="contained"
              onClick={handleUpload}
              disabled={isBusy}
              startIcon={<CloudUpload />}
            >
              {isBusy ? 'Analyzing…' : 'Upload & Analyze'}
            </Button>
          </Stack>
        )}

        {error && (
          <Alert severity="error" sx={{ mt: 3, textAlign: 'left' }}>
            {error}
          </Alert>
        )}

        {isBusy && (
          <Box sx={{ mt: 3 }}>
            <LinearProgress />
            <Typography variant="caption" sx={{ mt: 1, display: 'block' }}>
              This can take a few moments while we analyze your resume…
            </Typography>
          </Box>
        )}
      </Box>
    </Paper>
  );
};

export default FileUpload;
