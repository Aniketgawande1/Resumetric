import { useCallback, useEffect, useMemo, useState } from 'react';
import { ThemeProvider } from '@mui/material/styles';
import {
  CssBaseline,
  Box,
  Container,
  Typography
} from '@mui/material';
import { AnimatePresence, motion } from 'framer-motion';
import theme from './theme';
import { AppProvider, useAppContext } from './context/AppContext.jsx';
import Header from './components/layout/Header.jsx';
import Sidebar from './components/layout/Sidebar.jsx';
import NotificationSystem from './components/common/NotificationSystem.jsx';
import GlobalLoader from './components/common/GlobalLoader.jsx';
import Dashboard from './components/dashboard/Dashboard.jsx';
import ReportViewer from './components/report/ReportViewer.jsx';
import HistoryList from './components/history/HistoryList.jsx';
import AuthView from './components/auth/AuthView.jsx';
import ProfileSettings from './components/profile/ProfileSettings.jsx';
import { registerUser, loginUser, fetchProfile } from './services/auth.js';
import { analyzeResume, listReports, generateReport, downloadReportUrl } from './services/resume.js';

const clampScore = (value) => {
  const numeric = Number(value);
  if (!Number.isFinite(numeric)) return 0;
  if (numeric < 0) return 0;
  if (numeric > 100) return 100;
  return Math.round(numeric);
};

const sanitizeMessages = (items = []) => {
  if (!Array.isArray(items)) return [];
  return items
    .filter((message) => message && typeof message === 'string')
    .map((message) => message.trim())
    .filter((message) => message.length > 0 && !message.toLowerCase().includes('gemini feedback generation failed'));
};

const buildSummaryFromAnalysis = (analysis) => {
  const suggestions = sanitizeMessages(analysis?.suggestions);
  const generatedLines = sanitizeMessages(analysis?.generated_lines);
  const overallScore = clampScore(analysis?.score);
  const matchPercentage = clampScore(analysis?.analysis_details?.match_percentage ?? analysis?.score);
  const matchedSkills = analysis?.matched_skills ?? [];
  const missingSkills = analysis?.missing_skills ?? [];
  const totalFound = analysis?.analysis_details?.total_keywords_found ?? matchedSkills.length;
  const totalMissing = analysis?.analysis_details?.total_missing_keywords ?? missingSkills.length;
  const keywordsDenominator = totalFound + totalMissing;
  const skillsScore = clampScore(keywordsDenominator > 0 ? (totalFound / keywordsDenominator) * 100 : overallScore);

  const overviewSummary = `Your resume currently aligns ${matchPercentage}% with the target role based on AI analysis.`;
  const experienceSummary = suggestions[0] || generatedLines[0] || 'Highlight measurable achievements tied to the job description to improve alignment.';
  const skillsSummary = keywordsDenominator
    ? `Matched ${totalFound} relevant skills${totalMissing ? `, with ${totalMissing} key gaps remaining.` : '.'}`
    : 'No skills detected yet—double-check the resume text for recognizable keywords.';
  const educationSummary = suggestions[1] || generatedLines[1] || 'Include relevant coursework, certifications, or training to strengthen this section.';

  return {
    score: overallScore,
    sections: {
      overview: { score: matchPercentage, summary: overviewSummary },
      experience: { score: clampScore(overallScore - 5), summary: experienceSummary },
      skills: { score: skillsScore, summary: skillsSummary },
      education: { score: clampScore(overallScore - 10), summary: educationSummary }
    },
    suggestions,
    matchedKeywords: matchedSkills,
    missingKeywords: missingSkills,
    rawJson: analysis
  };
};

const createReportFromAnalysis = (analysis, metadata = {}) => {
  const timestamp = metadata.date || new Date().toISOString();
  const filename = metadata.filename || 'uploaded_resume.pdf';
  const suggestions = sanitizeMessages(analysis?.suggestions);
  const generatedLines = sanitizeMessages(analysis?.generated_lines);
  const highlights = [...suggestions.slice(0, 2), ...generatedLines.slice(0, 1)].filter(Boolean).slice(0, 3);

  return {
    id: metadata.id || `${timestamp}-${filename}`,
    filename,
    date: timestamp,
    score: clampScore(analysis?.score),
    summary: buildSummaryFromAnalysis(analysis),
    suggestions,
    generatedLines,
    highlights,
    downloadUrl: metadata.downloadUrl ?? null,
    source: metadata.source || 'analysis'
  };
};

const normalizeHistoryReports = (items = []) =>
  items.map((item) => ({
    id: item.download_url || `${item.filename}-${item.created}`,
    filename: item.filename,
    date: item.created,
    score: item.score ?? null,
    summary: null,
    suggestions: [],
    generatedLines: [],
    highlights: [],
    downloadUrl: downloadReportUrl(item.download_url),
    size: item.size,
    source: 'history'
  }));

const mergeReportCollections = (existing = [], incoming = []) => {
  const map = new Map();

  [...incoming, ...existing].forEach((item) => {
    if (!item) return;
    const key = item.id || `${item.filename}-${item.date || ''}`;
    const current = map.get(key);
    if (current) {
      map.set(key, {
        ...current,
        ...item,
        summary: current.summary ?? item.summary ?? null,
        suggestions: current.suggestions?.length ? current.suggestions : item.suggestions ?? [],
        generatedLines: current.generatedLines?.length ? current.generatedLines : item.generatedLines ?? [],
        highlights: current.highlights?.length ? current.highlights : item.highlights ?? [],
        downloadUrl: current.downloadUrl || item.downloadUrl || null
      });
    } else {
      map.set(key, item);
    }
  });

  return Array.from(map.values()).sort((a, b) => new Date(b.date || 0) - new Date(a.date || 0));
};

const AppContent = () => {
  const {
    token,
    user,
    setUser,
    currentPage,
    setCurrentPage,
    notifications,
    addNotification,
    closeNotification,
    isLoading,
    showLoader,
    hideLoader,
    reports,
    setReports,
    activeReport,
    setActiveReport,
    saveSession,
    clearSession
  } = useAppContext();

  const [sidebarOpen, setSidebarOpen] = useState(false);
  const [authError, setAuthError] = useState(null);

  const bootstrapSession = useCallback(async ({ showLoader: shouldShowLoader = true } = {}) => {
    if (!token) return;
    if (shouldShowLoader) {
      showLoader();
    }

    try {
      const profileResponse = await fetchProfile();
      if (profileResponse?.user) {
        setUser(profileResponse.user);
      }

      const reportsResponse = await listReports();
      const normalizedHistory = normalizeHistoryReports(reportsResponse?.reports ?? []);
      setReports((prev) => mergeReportCollections(prev, normalizedHistory));
    } catch (error) {
      const status = error?.response?.status;
      const message = error?.response?.data?.error || 'Unable to sync your account. Please sign in again.';

      if (status === 401) {
        clearSession();
        setAuthError('Your session expired. Please log in again.');
        addNotification('Your session expired. Please log in again.', 'warning');
      } else {
        addNotification(message, 'error');
      }
    } finally {
      if (shouldShowLoader) {
        hideLoader();
      }
    }
  }, [token, showLoader, hideLoader, setUser, setReports, clearSession, addNotification, setAuthError]);

  const handleAuthenticate = async ({ mode, data }) => {
    setAuthError(null);
    showLoader();

    try {
      const response = mode === 'signup' ? await registerUser(data) : await loginUser(data);
      if (!response?.access_token) {
        throw new Error(response?.error || 'Authentication failed. No access token returned.');
      }

      saveSession(response.access_token, response.user);
      addNotification(mode === 'signup' ? 'Account created! Welcome to Resumetric.' : 'Welcome back! 🎉', 'success');
      await bootstrapSession({ showLoader: false });
    } catch (error) {
      const message = error?.response?.data?.error || error.message || 'Authentication failed.';
      setAuthError(message);
      addNotification(message, 'error');
      throw new Error(message);
    } finally {
      hideLoader();
    }
  };

  const handleLogout = () => {
    clearSession();
    setAuthError(null);
    addNotification('You have logged out safely.', 'info');
  };

  const handleUpload = async ({ file, jobDescription, sendEmail }) => {
    if (!file) {
      addNotification('Please select a resume file to upload.', 'warning');
      return;
    }

    showLoader();
    addNotification(`Uploading ${file.name} for analysis…`, 'info');

    try {
      const analysis = await analyzeResume({ file, jobDescription, sendEmail });
      const newReport = createReportFromAnalysis(analysis, { filename: file.name });

      setReports((prev) => mergeReportCollections(prev, [newReport]));
      setActiveReport(newReport);
      setCurrentPage('reports');
      addNotification('Resume analyzed successfully!', 'success');

      if (sendEmail && analysis?.email_sent) {
        addNotification('Analysis results were emailed to you.', 'success');
      }

      try {
        const reportsResponse = await listReports();
        const normalizedHistory = normalizeHistoryReports(reportsResponse?.reports ?? []);
        setReports((prev) => mergeReportCollections(prev, normalizedHistory));
      } catch (historyError) {
        const message = historyError?.response?.data?.error || 'Analysis succeeded, but we could not refresh your report history.';
        addNotification(message, 'warning');
      }
    } catch (error) {
      const message = error?.response?.data?.error || error.message || 'Failed to analyze resume. Please try again.';
      addNotification(message, 'error');
    } finally {
      hideLoader();
    }
  };

  const handleViewReport = useCallback((report) => {
    if (!report?.summary) {
      addNotification('Preview is not available for this report yet. Try downloading it instead.', 'info');
      return;
    }

    setActiveReport(report);
    setCurrentPage('reports');
  }, [addNotification, setActiveReport, setCurrentPage]);

  const handleDownloadReport = useCallback(async (report = activeReport) => {
    if (!report) {
      addNotification('No report selected to download.', 'warning');
      return;
    }

    if (report.downloadUrl && typeof window !== 'undefined') {
      window.open(report.downloadUrl, '_blank', 'noopener,noreferrer');
      return;
    }

    if (!report.summary) {
      addNotification('We could not find enough data to regenerate this report. Try re-analyzing the resume to create a fresh download.', 'info');
      return;
    }

    try {
      showLoader();
      const payload = {
        score: report.summary?.score ?? report.score ?? 0,
        missing_skills: report.summary?.missingKeywords ?? report.missingKeywords ?? [],
        matched_skills: report.summary?.matchedKeywords ?? report.matchedKeywords ?? [],
        suggestions: report.suggestions ?? report.summary?.suggestions ?? [],
        generated_lines: report.generatedLines ?? []
      };

      const response = await generateReport(payload);
      const htmlFilePath = response?.files?.html_report;
      const htmlFileName = htmlFilePath ? htmlFilePath.split('/').pop() : null;
      const resolvedUrl = downloadReportUrl(response?.download_links?.html || (htmlFileName ? `/api/download-report/${htmlFileName}` : null));

      if (!resolvedUrl) {
        throw new Error('Report generated but no download link was provided.');
      }

      setReports((prev) =>
        prev.map((item) => (item.id === report.id ? { ...item, downloadUrl: resolvedUrl } : item))
      );

      if (activeReport?.id === report.id) {
        setActiveReport((prev) => (prev ? { ...prev, downloadUrl: resolvedUrl } : prev));
      }

      if (typeof window !== 'undefined') {
        window.open(resolvedUrl, '_blank', 'noopener,noreferrer');
      }

      addNotification('Report generated and download started.', 'success');
    } catch (error) {
      const message = error?.response?.data?.error || error.message || 'Failed to generate report download.';
      addNotification(message, 'error');
    } finally {
      hideLoader();
    }
  }, [activeReport, addNotification, hideLoader, setActiveReport, setReports, showLoader]);

  const handlePrintReport = useCallback(() => {
    if (typeof window !== 'undefined') {
      window.print();
    }
  }, []);

  useEffect(() => {
    if (!token) return;
    bootstrapSession({ showLoader: false });
  }, [token, bootstrapSession]);

  const recentReport = useMemo(() => {
    const latest = reports.find((item) => item.summary);
    if (!latest) return null;

    const derivedHighlights = latest.highlights?.length
      ? latest.highlights
      : (latest.suggestions ?? latest.summary?.suggestions ?? []).slice(0, 3);
    const highlights = derivedHighlights.length
      ? derivedHighlights
      : ['Open the full report to explore tailored recommendations.'];

    return {
      score: latest.summary?.score ?? latest.score,
      highlights,
      onView: () => handleViewReport(latest)
    };
  }, [reports, handleViewReport]);

  if (!user) {
    return <AuthView onAuthenticate={handleAuthenticate} loading={isLoading} error={authError} />;
  }

  return (
    <Box
      sx={{
        minHeight: '100vh',
        position: 'relative',
        overflowX: 'hidden',
        bgcolor: 'background.default'
      }}
    >
      <Box sx={{ position: 'relative', zIndex: 2 }}>
        <Header
          onMenuToggle={() => setSidebarOpen(true)}
          currentPage={currentPage}
          onNavigate={setCurrentPage}
          user={user}
          onLogout={handleLogout}
        />

        <Sidebar open={sidebarOpen} onClose={() => setSidebarOpen(false)} currentPage={currentPage} onNavigate={setCurrentPage} />

        <NotificationSystem notifications={notifications} onClose={closeNotification} />
        <GlobalLoader open={isLoading} />

        <Box component="main" sx={{ py: 2 }}>
          <AnimatePresence mode="wait">
            {currentPage === 'dashboard' && (
              <motion.div
                key="dashboard"
                initial={{ opacity: 0, y: 24 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: -24 }}
                transition={{ duration: 0.45, ease: 'easeOut' }}
              >
                <Dashboard user={user} reports={reports} onUpload={handleUpload} loading={isLoading} recentReport={recentReport} />
              </motion.div>
            )}

            {currentPage === 'history' && (
              <motion.div
                key="history"
                initial={{ opacity: 0, y: 24 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: -24 }}
                transition={{ duration: 0.4, ease: 'easeOut' }}
              >
                <HistoryList items={reports} onView={handleViewReport} onDownload={handleDownloadReport} />
              </motion.div>
            )}

            {currentPage === 'reports' && (
              <motion.div
                key="reports"
                initial={{ opacity: 0, y: 24 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: -24 }}
                transition={{ duration: 0.45, ease: 'easeOut' }}
              >
                <Container maxWidth="lg" sx={{ py: 4 }}>
                  {activeReport ? (
                    <ReportViewer
                      report={activeReport.summary
                        ? {
                            score: activeReport.summary.score,
                            sections: activeReport.summary.sections,
                            suggestions: activeReport.summary.suggestions,
                            matchedKeywords: activeReport.summary.matchedKeywords,
                            missingKeywords: activeReport.summary.missingKeywords,
                            rawJson: activeReport.summary.rawJson
                          }
                        : undefined}
                      onDownload={() => handleDownloadReport(activeReport)}
                      onPrint={handlePrintReport}
                    />
                  ) : (
                    <Box textAlign="center" py={6}>
                      <Typography variant="h6" gutterBottom>
                        Select a report from your history to view details.
                      </Typography>
                      <Typography variant="body2" color="text.secondary">
                        Upload a resume or choose from your history to start analyzing.
                      </Typography>
                    </Box>
                  )}
                </Container>
              </motion.div>
            )}

            {(currentPage === 'profile' || currentPage === 'settings') && (
              <motion.div
                key="profile"
                initial={{ opacity: 0, y: 24 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: -24 }}
                transition={{ duration: 0.45, ease: 'easeOut' }}
              >
                <ProfileSettings user={user} />
              </motion.div>
            )}
          </AnimatePresence>
        </Box>
      </Box>
    </Box>
  );
};

const App = () => (
  <ThemeProvider theme={theme}>
    <CssBaseline />
    <AppProvider>
      <AppContent />
    </AppProvider>
  </ThemeProvider>
);

export default App;
