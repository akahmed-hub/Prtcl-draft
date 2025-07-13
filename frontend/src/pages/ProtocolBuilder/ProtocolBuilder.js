import React, { useState, useEffect } from 'react';
import {
  Box,
  Container,
  Typography,
  Paper,
  TextField,
  Button,
  Grid,
  Card,
  CardContent,
  CardActions,
  Chip,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  List,
  ListItem,
  ListItemText,
  Divider,
  IconButton,
  Tooltip,
  Alert,
  CircularProgress,
} from '@mui/material';
import {
  Add as AddIcon,
  Edit as EditIcon,
  Delete as DeleteIcon,
  ExpandMore as ExpandMoreIcon,
  ExpandLess as ExpandLessIcon,
  Science as ScienceIcon,
  Save as SaveIcon,
  PlayArrow as GenerateIcon,
} from '@mui/icons-material';
import { useSelector, useDispatch } from 'react-redux';
import { generateProtocol, fetchProtocols } from '../../store/slices/protocolSlice';

const ProtocolBuilder = () => {
  const [prompt, setPrompt] = useState('');
  const [expandedSteps, setExpandedSteps] = useState(new Set());
  const [selectedProtocol, setSelectedProtocol] = useState(null);
  const [isGenerating, setIsGenerating] = useState(false);
  const [showSaveDialog, setShowSaveDialog] = useState(false);
  const [protocolName, setProtocolName] = useState('');
  const [protocolDescription, setProtocolDescription] = useState('');

  const dispatch = useDispatch();
  const { protocols, loading, error } = useSelector((state) => state.protocols);

  useEffect(() => {
    dispatch(fetchProtocols());
  }, [dispatch]);

  const handleGenerateProtocol = async () => {
    if (!prompt.trim()) return;

    setIsGenerating(true);
    try {
      const result = await dispatch(generateProtocol({
        prompt: prompt.trim(),
        include_reagents: true,
        include_reasoning: true,
        max_steps: 20,
      })).unwrap();
      
      setSelectedProtocol(result);
      setProtocolName(result.title);
      setProtocolDescription(result.description);
    } catch (error) {
      console.error('Failed to generate protocol:', error);
    } finally {
      setIsGenerating(false);
    }
  };

  const handleStepToggle = (stepId) => {
    const newExpanded = new Set(expandedSteps);
    if (newExpanded.has(stepId)) {
      newExpanded.delete(stepId);
    } else {
      newExpanded.add(stepId);
    }
    setExpandedSteps(newExpanded);
  };

  const handleSaveProtocol = () => {
    // TODO: Implement save functionality
    setShowSaveDialog(false);
  };

  const renderProtocolStep = (step, index) => {
    const isExpanded = expandedSteps.has(step.id);
    
    return (
      <Card key={step.id} sx={{ mb: 2, border: '1px solid #e0e0e0' }}>
        <CardContent sx={{ pb: 1 }}>
          <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
            <Box sx={{ display: 'flex', alignItems: 'center', flex: 1 }}>
              <Chip
                label={`Step ${step.step_number}`}
                size="small"
                color="primary"
                sx={{ mr: 2 }}
              />
              <Typography variant="h6" component="div" sx={{ flex: 1 }}>
                {step.title}
              </Typography>
            </Box>
            <Box>
              <Tooltip title="Edit step">
                <IconButton size="small">
                  <EditIcon />
                </IconButton>
              </Tooltip>
              <Tooltip title="Delete step">
                <IconButton size="small" color="error">
                  <DeleteIcon />
                </IconButton>
              </Tooltip>
              <IconButton
                size="small"
                onClick={() => handleStepToggle(step.id)}
              >
                {isExpanded ? <ExpandLessIcon /> : <ExpandMoreIcon />}
              </IconButton>
            </Box>
          </Box>
          
          <Typography variant="body1" sx={{ mt: 1 }}>
            {step.content}
          </Typography>
          
          {step.duration_minutes && (
            <Chip
              label={`${step.duration_minutes} min`}
              size="small"
              variant="outlined"
              sx={{ mr: 1, mt: 1 }}
            />
          )}
          
          {step.temperature_celsius && (
            <Chip
              label={`${step.temperature_celsius}°C`}
              size="small"
              variant="outlined"
              sx={{ mr: 1, mt: 1 }}
            />
          )}
        </CardContent>
        
        {isExpanded && (
          <CardContent sx={{ pt: 0, backgroundColor: '#f8f9fa' }}>
            <Grid container spacing={2}>
              <Grid item xs={12} md={6}>
                <Typography variant="subtitle2" color="primary" gutterBottom>
                  Reasoning
                </Typography>
                <Typography variant="body2" color="text.secondary">
                  {step.reasoning || 'No reasoning provided for this step.'}
                </Typography>
              </Grid>
              
              <Grid item xs={12} md={6}>
                <Typography variant="subtitle2" color="primary" gutterBottom>
                  Alternative Options
                </Typography>
                {step.alternatives && step.alternatives.length > 0 ? (
                  <List dense>
                    {step.alternatives.map((alt, idx) => (
                      <ListItem key={idx} sx={{ py: 0 }}>
                        <ListItemText
                          primary={`${alt.parameter}: ${alt.value}`}
                          secondary={alt.reason}
                        />
                      </ListItem>
                    ))}
                  </List>
                ) : (
                  <Typography variant="body2" color="text.secondary">
                    No alternatives available.
                  </Typography>
                )}
              </Grid>
            </Grid>
          </CardContent>
        )}
      </Card>
    );
  };

  const renderReagents = () => {
    if (!selectedProtocol?.reagents?.length) return null;
    
    return (
      <Paper sx={{ p: 2, mb: 3 }}>
        <Typography variant="h6" gutterBottom>
          Reagents
        </Typography>
        <Grid container spacing={2}>
          {selectedProtocol.reagents.map((reagent, index) => (
            <Grid item xs={12} sm={6} md={4} key={index}>
              <Card variant="outlined">
                <CardContent>
                  <Typography variant="subtitle1" fontWeight="bold">
                    {reagent.name}
                  </Typography>
                  <Typography variant="body2" color="text.secondary">
                    {reagent.concentration} {reagent.unit}
                  </Typography>
                </CardContent>
              </Card>
            </Grid>
          ))}
        </Grid>
      </Paper>
    );
  };

  return (
    <Container maxWidth="lg">
      <Box sx={{ mb: 4 }}>
        <Typography variant="h4" gutterBottom>
          Protocol Builder
        </Typography>
        <Typography variant="body1" color="text.secondary">
          Generate biological protocols using AI and cross-reference with research papers
        </Typography>
      </Box>

      {/* Protocol Generation */}
      <Paper sx={{ p: 3, mb: 3 }}>
        <Typography variant="h6" gutterBottom>
          Generate New Protocol
        </Typography>
        <TextField
          fullWidth
          multiline
          rows={4}
          variant="outlined"
          label="Describe the protocol you want to generate..."
          value={prompt}
          onChange={(e) => setPrompt(e.target.value)}
          placeholder="e.g., Draft a PCR protocol for human genomic DNA using Taq polymerase"
          sx={{ mb: 2 }}
        />
        <Box sx={{ display: 'flex', gap: 2 }}>
          <Button
            variant="contained"
            startIcon={isGenerating ? <CircularProgress size={20} /> : <GenerateIcon />}
            onClick={handleGenerateProtocol}
            disabled={!prompt.trim() || isGenerating}
          >
            {isGenerating ? 'Generating...' : 'Generate Protocol'}
          </Button>
          <Button
            variant="outlined"
            startIcon={<AddIcon />}
            onClick={() => setSelectedProtocol({ title: 'New Protocol', steps: [], reagents: [] })}
          >
            Start from Scratch
          </Button>
        </Box>
      </Paper>

      {error && (
        <Alert severity="error" sx={{ mb: 3 }}>
          {error}
        </Alert>
      )}

      {/* Generated Protocol */}
      {selectedProtocol && (
        <Paper sx={{ p: 3 }}>
          <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 3 }}>
            <Typography variant="h5">
              {selectedProtocol.title}
            </Typography>
            <Button
              variant="contained"
              startIcon={<SaveIcon />}
              onClick={() => setShowSaveDialog(true)}
            >
              Save Protocol
            </Button>
          </Box>
          
          {selectedProtocol.description && (
            <Typography variant="body1" color="text.secondary" sx={{ mb: 3 }}>
              {selectedProtocol.description}
            </Typography>
          )}

          {/* Reagents Section */}
          {renderReagents()}

          {/* Protocol Steps */}
          <Typography variant="h6" gutterBottom>
            Protocol Steps
          </Typography>
          {selectedProtocol.steps?.map((step, index) => renderProtocolStep(step, index))}
        </Paper>
      )}

      {/* Save Dialog */}
      <Dialog open={showSaveDialog} onClose={() => setShowSaveDialog(false)} maxWidth="sm" fullWidth>
        <DialogTitle>Save Protocol</DialogTitle>
        <DialogContent>
          <TextField
            fullWidth
            label="Protocol Name"
            value={protocolName}
            onChange={(e) => setProtocolName(e.target.value)}
            sx={{ mb: 2, mt: 1 }}
          />
          <TextField
            fullWidth
            multiline
            rows={3}
            label="Description"
            value={protocolDescription}
            onChange={(e) => setProtocolDescription(e.target.value)}
          />
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setShowSaveDialog(false)}>Cancel</Button>
          <Button onClick={handleSaveProtocol} variant="contained">
            Save
          </Button>
        </DialogActions>
      </Dialog>
    </Container>
  );
};

export default ProtocolBuilder; 