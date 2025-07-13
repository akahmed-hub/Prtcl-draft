import React, { useState, useEffect } from 'react';
import {
  Box,
  Container,
  Typography,
  Paper,
  Grid,
  Card,
  CardContent,
  CardActions,
  Button,
  TextField,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  Chip,
  LinearProgress,
  Alert,
  List,
  ListItem,
  ListItemText,
  ListItemIcon,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
} from '@mui/material';
import {
  CloudUpload as UploadIcon,
  Analytics as AnalyticsIcon,
  CheckCircle as CheckCircleIcon,
  Error as ErrorIcon,
  Schedule as ScheduleIcon,
  FileUpload as FileUploadIcon,
} from '@mui/icons-material';
import { useSelector, useDispatch } from 'react-redux';
import { useDropzone } from 'react-dropzone';
import { uploadDataFile, createAnalysisTask, fetchDataFiles, fetchAnalysisTasks } from '../../store/slices/analysisSlice';

const DataAnalysis = () => {
  const [selectedFiles, setSelectedFiles] = useState([]);
  const [analysisType, setAnalysisType] = useState('');
  const [analysisName, setAnalysisName] = useState('');
  const [showAnalysisDialog, setShowAnalysisDialog] = useState(false);
  const [selectedFile, setSelectedFile] = useState(null);

  const dispatch = useDispatch();
  const { dataFiles, analysisTasks, loading, uploading, error } = useSelector((state) => state.analysis);

  useEffect(() => {
    dispatch(fetchDataFiles());
    dispatch(fetchAnalysisTasks());
  }, [dispatch]);

  const onDrop = (acceptedFiles) => {
    setSelectedFiles(acceptedFiles);
  };

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      'text/csv': ['.csv'],
      'image/tiff': ['.tif', '.tiff'],
      'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet': ['.xlsx'],
    },
  });

  const handleFileUpload = async () => {
    for (const file of selectedFiles) {
      const fileType = file.name.endsWith('.csv') ? 'qpc_csv' :
                      file.name.endsWith('.tif') || file.name.endsWith('.tiff') ? 'western_tiff' :
                      file.name.endsWith('.xlsx') ? 'excel' : 'other';

      await dispatch(uploadDataFile({
        file,
        name: file.name,
        fileType,
        description: `Uploaded ${new Date().toLocaleString()}`,
      }));
    }
    setSelectedFiles([]);
  };

  const handleCreateAnalysis = async () => {
    if (!selectedFile || !analysisType || !analysisName) return;

    await dispatch(createAnalysisTask({
      name: analysisName,
      task_type: analysisType,
      data_files: [selectedFile.id],
      parameters: {},
    }));

    setShowAnalysisDialog(false);
    setSelectedFile(null);
    setAnalysisType('');
    setAnalysisName('');
  };

  const getStatusColor = (status) => {
    switch (status) {
      case 'completed': return 'success';
      case 'processing': return 'warning';
      case 'failed': return 'error';
      default: return 'default';
    }
  };

  const getStatusIcon = (status) => {
    switch (status) {
      case 'completed': return <CheckCircleIcon />;
      case 'processing': return <ScheduleIcon />;
      case 'failed': return <ErrorIcon />;
      default: return <ScheduleIcon />;
    }
  };

  return (
    <Container maxWidth="lg">
      <Box sx={{ mb: 4 }}>
        <Typography variant="h4" gutterBottom>
          Data Analysis
        </Typography>
        <Typography variant="body1" color="text.secondary">
          Upload and analyze qPCR and Western Blot data with automated processing
        </Typography>
      </Box>

      {error && (
        <Alert severity="error" sx={{ mb: 3 }}>
          {error}
        </Alert>
      )}

      {/* File Upload Section */}
      <Paper sx={{ p: 3, mb: 3 }}>
        <Typography variant="h6" gutterBottom>
          Upload Data Files
        </Typography>
        
        <Box
          {...getRootProps()}
          sx={{
            border: '2px dashed #ccc',
            borderRadius: 2,
            p: 3,
            textAlign: 'center',
            cursor: 'pointer',
            backgroundColor: isDragActive ? '#f0f8ff' : '#fafafa',
            '&:hover': {
              backgroundColor: '#f0f8ff',
            },
          }}
        >
          <input {...getInputProps()} />
          <FileUploadIcon sx={{ fontSize: 48, color: 'primary.main', mb: 2 }} />
          <Typography variant="h6" gutterBottom>
            {isDragActive ? 'Drop files here' : 'Drag & drop files here, or click to select'}
          </Typography>
          <Typography variant="body2" color="text.secondary">
            Supports CSV (qPCR), TIFF (Western Blot), and Excel files
          </Typography>
        </Box>

        {selectedFiles.length > 0 && (
          <Box sx={{ mt: 2 }}>
            <Typography variant="subtitle1" gutterBottom>
              Selected Files:
            </Typography>
            <List dense>
              {selectedFiles.map((file, index) => (
                <ListItem key={index}>
                  <ListItemIcon>
                    <FileUploadIcon />
                  </ListItemIcon>
                  <ListItemText
                    primary={file.name}
                    secondary={`${(file.size / 1024 / 1024).toFixed(2)} MB`}
                  />
                </ListItem>
              ))}
            </List>
            <Button
              variant="contained"
              startIcon={uploading ? <LinearProgress /> : <UploadIcon />}
              onClick={handleFileUpload}
              disabled={uploading}
              sx={{ mt: 2 }}
            >
              {uploading ? 'Uploading...' : 'Upload Files'}
            </Button>
          </Box>
        )}
      </Paper>

      {/* Data Files */}
      <Paper sx={{ p: 3, mb: 3 }}>
        <Typography variant="h6" gutterBottom>
          Uploaded Files
        </Typography>
        {loading ? (
          <LinearProgress />
        ) : dataFiles.length > 0 ? (
          <Grid container spacing={2}>
            {dataFiles.map((file) => (
              <Grid item xs={12} sm={6} md={4} key={file.id}>
                <Card variant="outlined">
                  <CardContent>
                    <Typography variant="subtitle1" fontWeight="bold">
                      {file.name}
                    </Typography>
                    <Typography variant="body2" color="text.secondary" gutterBottom>
                      {file.get_file_type_display}
                    </Typography>
                    <Chip
                      label={file.is_processed ? 'Processed' : 'Pending'}
                      size="small"
                      color={file.is_processed ? 'success' : 'default'}
                    />
                  </CardContent>
                  <CardActions>
                    <Button
                      size="small"
                      onClick={() => {
                        setSelectedFile(file);
                        setShowAnalysisDialog(true);
                      }}
                    >
                      Analyze
                    </Button>
                  </CardActions>
                </Card>
              </Grid>
            ))}
          </Grid>
        ) : (
          <Typography variant="body2" color="text.secondary" sx={{ textAlign: 'center', py: 2 }}>
            No files uploaded yet. Upload your data files to get started.
          </Typography>
        )}
      </Paper>

      {/* Analysis Tasks */}
      <Paper sx={{ p: 3 }}>
        <Typography variant="h6" gutterBottom>
          Analysis Tasks
        </Typography>
        {loading ? (
          <LinearProgress />
        ) : analysisTasks.length > 0 ? (
          <List>
            {analysisTasks.map((task) => (
              <ListItem key={task.id} divider>
                <ListItemIcon>
                  {getStatusIcon(task.status)}
                </ListItemIcon>
                <ListItemText
                  primary={task.name}
                  secondary={`${task.get_task_type_display} - Created ${new Date(task.created_at).toLocaleDateString()}`}
                />
                <Chip
                  label={task.status}
                  size="small"
                  color={getStatusColor(task.status)}
                />
              </ListItem>
            ))}
          </List>
        ) : (
          <Typography variant="body2" color="text.secondary" sx={{ textAlign: 'center', py: 2 }}>
            No analysis tasks yet. Create your first analysis task.
          </Typography>
        )}
      </Paper>

      {/* Analysis Dialog */}
      <Dialog open={showAnalysisDialog} onClose={() => setShowAnalysisDialog(false)} maxWidth="sm" fullWidth>
        <DialogTitle>Create Analysis Task</DialogTitle>
        <DialogContent>
          <TextField
            fullWidth
            label="Analysis Name"
            value={analysisName}
            onChange={(e) => setAnalysisName(e.target.value)}
            sx={{ mb: 2, mt: 1 }}
          />
          <FormControl fullWidth sx={{ mb: 2 }}>
            <InputLabel>Analysis Type</InputLabel>
            <Select
              value={analysisType}
              onChange={(e) => setAnalysisType(e.target.value)}
              label="Analysis Type"
            >
              <MenuItem value="qpcr_delta_ct">qPCR Delta Ct</MenuItem>
              <MenuItem value="qpcr_delta_delta_ct">qPCR Delta-Delta Ct</MenuItem>
              <MenuItem value="western_quantification">Western Blot Quantification</MenuItem>
              <MenuItem value="western_normalization">Western Blot Normalization</MenuItem>
            </Select>
          </FormControl>
          {selectedFile && (
            <Typography variant="body2" color="text.secondary">
              Selected file: {selectedFile.name}
            </Typography>
          )}
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setShowAnalysisDialog(false)}>Cancel</Button>
          <Button
            onClick={handleCreateAnalysis}
            variant="contained"
            disabled={!analysisName || !analysisType}
          >
            Create Analysis
          </Button>
        </DialogActions>
      </Dialog>
    </Container>
  );
};

export default DataAnalysis; 