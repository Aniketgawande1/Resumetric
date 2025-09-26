import apiClient, { BASE_URL } from './apiClient.js';

export const analyzeResume = async ({ file, jobDescription, sendEmail }) => {
  const formData = new FormData();
  formData.append('resume', file);
  formData.append('job_description', jobDescription);
  formData.append('send_email', sendEmail ? 'true' : 'false');

  const { data } = await apiClient.post('/api/analyze', formData, {
    headers: { 'Content-Type': 'multipart/form-data' }
  });

  return data;
};

export const listReports = async () => {
  const { data } = await apiClient.get('/api/list-reports');
  return data;
};

export const generateReport = async (payload) => {
  const { data } = await apiClient.post('/api/generate-report', payload);
  return data;
};

export const downloadReportUrl = (relativePath) => {
  if (!relativePath) return null;
  return relativePath.startsWith('http') ? relativePath : `${BASE_URL}${relativePath}`;
};
