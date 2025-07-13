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
  ColorPicker,
} from '@mui/material';
import {
  BarChart as BarChartIcon,
  ShowChart as LineChartIcon,
  ScatterPlot as ScatterPlotIcon,
  Add as AddIcon,
  Edit as EditIcon,
  Delete as DeleteIcon,
  Save as SaveIcon,
} from '@mui/icons-material';
import { useSelector, useDispatch } from 'react-redux';
import { useDropzone } from 'react-dropzone';
import { createVisualization, fetchVisualizations, updateVisualization, deleteVisualization } from '../../store/slices/visualizationSlice';

const Visualization = () => {
  const [showCreateDialog, setShowCreateDialog] = useState(false);
  const [selectedFiles, setSelectedFiles] = useState([]);
  const [chartType, setChartType] = useState('bar');
  const [chartTitle, setChartTitle] = useState('');
  const [xAxisLabel, setXAxisLabel] = useState('');
  const [yAxisLabel, setYAxisLabel] = useState('');
  const [selectedVisualization, setSelectedVisualization] = useState(null);

  const dispatch = useDispatch();
  const { visualizations, loading, error } = useSelector((state) => state.visualization);

  useEffect(() => {
    dispatch(fetchVisualizations());
  }, [dispatch]);

  const onDrop = (acceptedFiles) => {
    setSelectedFiles(acceptedFiles);
  };

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet': ['.xlsx'],
      'text/csv': ['.csv'],
      'application/json': ['.json'],
    },
  });

  const handleCreateVisualization = async () => {
    if (!chartTitle || selectedFiles.length === 0) return;

    const formData = new FormData();
    formData.append('title', chartTitle);
    formData.append('chart_type', chartType);
    formData.append('x_axis_label', xAxisLabel);
    formData.append('y_axis_label', yAxisLabel);
    
    selectedFiles.forEach((file) => {
      formData.append('data_files', file);
    });

    await dispatch(createVisualization(formData));
    setShowCreateDialog(false);
    setSelectedFiles([]);
    setChartTitle('');
    setChartType('bar');
    setXAxisLabel('');
    setYAxisLabel('');
  };

  const handleDeleteVisualization = async (id) => {
    if (window.confirm('Are you sure you want to delete this visualization?')) {
      await dispatch(deleteVisualization(id));
    }
  };

  const chartTypes = [
    { value: 'bar', label: 'Bar Chart', icon: <BarChartIcon /> },
    { value: 'line', label: 'Line Chart', icon: <LineChartIcon /> },
    { value: 'scatter', label: 'Scatter Plot', icon: <ScatterPlotIcon /> },
  ];

  return (
    <Container maxWidth="lg">
      <Box sx={{ mb: 4 }}>
        <Typography variant="h4" gutterBottom>
          Data Visualization
        </Typography>
        <Typography variant="body1" color="text.secondary">
          Create interactive charts and graphs from your analyzed data
        </Typography>
      </Box>

      {error && (
        <Alert severity="error" sx={{ mb: 3 }}>
          {error}
        </Alert>
      )}

      {/* Create New Visualization */}
      <Paper sx={{ p: 3, mb: 3 }}>
        <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 2 }}>
          <Typography variant="h6">
            Create New Visualization
          </Typography>
          <Button
            variant="contained"
            startIcon={<AddIcon />}
            onClick={() => setShowCreateDialog(true)}
          >
            New Chart
          </Button>
        </Box>
        
        <Typography variant="body2" color="text.secondary">
          Upload Excel, CSV, or JSON files to create custom visualizations with extensive customization options.
        </Typography>
      </Paper>

      {/* Visualizations Grid */}
      <Paper sx={{ p: 3 }}>
        <Typography variant="h6" gutterBottom>
          Your Visualizations
        </Typography>
        {loading ? (
          <LinearProgress />
        ) : visualizations.length > 0 ? (
          <Grid container spacing={3}>
            {visualizations.map((viz) => (
              <Grid item xs={12} sm={6} md={4} key={viz.id}>
                <Card>
                  <CardContent>
                    <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 2 }}>
                      <Typography variant="h6" component="div">
                        {viz.title}
                      </Typography>
                      <Chip
                        label={viz.chart_type}
                        size="small"
                        variant="outlined"
                      />
                    </Box>
                    <Typography variant="body2" color="text.secondary" gutterBottom>
                      {viz.description || 'No description'}
                    </Typography>
                    <Typography variant="caption" color="text.secondary">
                      Created {new Date(viz.created_at).toLocaleDateString()}
                    </Typography>
                  </CardContent>
                  <CardActions>
                    <Button
                      size="small"
                      startIcon={<EditIcon />}
                      onClick={() => setSelectedVisualization(viz)}
                    >
                      Edit
                    </Button>
                    <Button
                      size="small"
                      color="error"
                      startIcon={<DeleteIcon />}
                      onClick={() => handleDeleteVisualization(viz.id)}
                    >
                      Delete
                    </Button>
                  </CardActions>
                </Card>
              </Grid>
            ))}
          </Grid>
        ) : (
          <Typography variant="body2" color="text.secondary" sx={{ textAlign: 'center', py: 4 }}>
            No visualizations yet. Create your first chart to get started.
          </Typography>
        )}
      </Paper>

      {/* Create Visualization Dialog */}
      <Dialog open={showCreateDialog} onClose={() => setShowCreateDialog(false)} maxWidth="md" fullWidth>
        <DialogTitle>Create New Visualization</DialogTitle>
        <DialogContent>
          <Grid container spacing={2} sx={{ mt: 1 }}>
            <Grid item xs={12}>
              <TextField
                fullWidth
                label="Chart Title"
                value={chartTitle}
                onChange={(e) => setChartTitle(e.target.value)}
              />
            </Grid>
            
            <Grid item xs={12} sm={6}>
              <FormControl fullWidth>
                <InputLabel>Chart Type</InputLabel>
                <Select
                  value={chartType}
                  onChange={(e) => setChartType(e.target.value)}
                  label="Chart Type"
                >
                  {chartTypes.map((type) => (
                    <MenuItem key={type.value} value={type.value}>
                      <Box sx={{ display: 'flex', alignItems: 'center' }}>
                        {type.icon}
                        <Typography sx={{ ml: 1 }}>{type.label}</Typography>
                      </Box>
                    </MenuItem>
                  ))}
                </Select>
              </FormControl>
            </Grid>
            
            <Grid item xs={12} sm={6}>
              <TextField
                fullWidth
                label="X-Axis Label"
                value={xAxisLabel}
                onChange={(e) => setXAxisLabel(e.target.value)}
              />
            </Grid>
            
            <Grid item xs={12} sm={6}>
              <TextField
                fullWidth
                label="Y-Axis Label"
                value={yAxisLabel}
                onChange={(e) => setYAxisLabel(e.target.value)}
              />
            </Grid>
            
            <Grid item xs={12}>
              <Typography variant="subtitle2" gutterBottom>
                Upload Data Files
              </Typography>
              <Box
                {...getRootProps()}
                sx={{
                  border: '2px dashed #ccc',
                  borderRadius: 2,
                  p: 2,
                  textAlign: 'center',
                  cursor: 'pointer',
                  backgroundColor: isDragActive ? '#f0f8ff' : '#fafafa',
                  '&:hover': {
                    backgroundColor: '#f0f8ff',
                  },
                }}
              >
                <input {...getInputProps()} />
                <Typography variant="body2">
                  {isDragActive ? 'Drop files here' : 'Drag & drop files here, or click to select'}
                </Typography>
                <Typography variant="caption" color="text.secondary">
                  Supports Excel, CSV, and JSON files
                </Typography>
              </Box>
              
              {selectedFiles.length > 0 && (
                <List dense sx={{ mt: 1 }}>
                  {selectedFiles.map((file, index) => (
                    <ListItem key={index}>
                      <ListItemText
                        primary={file.name}
                        secondary={`${(file.size / 1024 / 1024).toFixed(2)} MB`}
                      />
                    </ListItem>
                  ))}
                </List>
              )}
            </Grid>
          </Grid>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setShowCreateDialog(false)}>Cancel</Button>
          <Button
            onClick={handleCreateVisualization}
            variant="contained"
            disabled={!chartTitle || selectedFiles.length === 0}
          >
            Create Visualization
          </Button>
        </DialogActions>
      </Dialog>

      {/* Edit Visualization Dialog */}
      {selectedVisualization && (
        <Dialog open={!!selectedVisualization} onClose={() => setSelectedVisualization(null)} maxWidth="md" fullWidth>
          <DialogTitle>Edit Visualization</DialogTitle>
          <DialogContent>
            <Typography variant="body1">
              Edit functionality will be implemented in future versions.
            </Typography>
          </DialogContent>
          <DialogActions>
            <Button onClick={() => setSelectedVisualization(null)}>Close</Button>
          </DialogActions>
        </Dialog>
      )}
    </Container>
  );
};

export default Visualization; 