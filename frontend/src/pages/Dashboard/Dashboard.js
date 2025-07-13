import React, { useEffect } from 'react';
import {
  Box,
  Container,
  Typography,
  Grid,
  Card,
  CardContent,
  CardActions,
  Button,
  Paper,
  List,
  ListItem,
  ListItemText,
  ListItemIcon,
  Chip,
  LinearProgress,
} from '@mui/material';
import {
  Science as ScienceIcon,
  Analytics as AnalyticsIcon,
  BarChart as BarChartIcon,
  TrendingUp as TrendingUpIcon,
  Schedule as ScheduleIcon,
  CheckCircle as CheckCircleIcon,
} from '@mui/icons-material';
import { useSelector, useDispatch } from 'react-redux';
import { useNavigate } from 'react-router-dom';
import { fetchProtocols } from '../../store/slices/protocolSlice';
import { fetchAnalysisTasks } from '../../store/slices/analysisSlice';
import { fetchVisualizations } from '../../store/slices/visualizationSlice';

const Dashboard = () => {
  const dispatch = useDispatch();
  const navigate = useNavigate();
  const { user } = useSelector((state) => state.auth);
  const { protocols, loading: protocolsLoading } = useSelector((state) => state.protocols);
  const { analysisTasks, loading: analysisLoading } = useSelector((state) => state.analysis);
  const { visualizations, loading: vizLoading } = useSelector((state) => state.visualization);

  useEffect(() => {
    dispatch(fetchProtocols());
    dispatch(fetchAnalysisTasks());
    dispatch(fetchVisualizations());
  }, [dispatch]);

  const featureCards = [
    {
      title: 'Protocol Builder',
      description: 'Generate biological protocols using AI and cross-reference with research papers',
      icon: <ScienceIcon sx={{ fontSize: 40 }} />,
      color: '#1976d2',
      path: '/protocols',
      stats: `${protocols.length} protocols`,
    },
    {
      title: 'Data Analysis',
      description: 'Analyze qPCR and Western Blot data with automated processing',
      icon: <AnalyticsIcon sx={{ fontSize: 40 }} />,
      color: '#dc004e',
      path: '/analysis',
      stats: `${analysisTasks.length} tasks`,
    },
    {
      title: 'Visualization',
      description: 'Create interactive charts and graphs from your analyzed data',
      icon: <BarChartIcon sx={{ fontSize: 40 }} />,
      color: '#388e3c',
      path: '/visualization',
      stats: `${visualizations.length} charts`,
    },
  ];

  const recentProtocols = protocols.slice(0, 5);
  const recentTasks = analysisTasks.slice(0, 5);

  return (
    <Container maxWidth="lg">
      <Box sx={{ mb: 4 }}>
        <Typography variant="h4" gutterBottom>
          Welcome back, {user?.username || 'User'}!
        </Typography>
        <Typography variant="body1" color="text.secondary">
          Your biological research assistant is ready to help you build protocols, analyze data, and create visualizations.
        </Typography>
      </Box>

      {/* Feature Cards */}
      <Grid container spacing={3} sx={{ mb: 4 }}>
        {featureCards.map((card) => (
          <Grid item xs={12} md={4} key={card.title}>
            <Card
              sx={{
                height: '100%',
                display: 'flex',
                flexDirection: 'column',
                cursor: 'pointer',
                transition: 'transform 0.2s, box-shadow 0.2s',
                '&:hover': {
                  transform: 'translateY(-4px)',
                  boxShadow: '0 8px 25px rgba(0,0,0,0.15)',
                },
              }}
              onClick={() => navigate(card.path)}
            >
              <CardContent sx={{ flexGrow: 1, textAlign: 'center' }}>
                <Box sx={{ color: card.color, mb: 2 }}>
                  {card.icon}
                </Box>
                <Typography variant="h6" gutterBottom>
                  {card.title}
                </Typography>
                <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
                  {card.description}
                </Typography>
                <Chip label={card.stats} size="small" variant="outlined" />
              </CardContent>
              <CardActions sx={{ justifyContent: 'center', pb: 2 }}>
                <Button size="small" color="primary">
                  Get Started
                </Button>
              </CardActions>
            </Card>
          </Grid>
        ))}
      </Grid>

      {/* Recent Activity */}
      <Grid container spacing={3}>
        {/* Recent Protocols */}
        <Grid item xs={12} md={6}>
          <Paper sx={{ p: 2 }}>
            <Typography variant="h6" gutterBottom>
              Recent Protocols
            </Typography>
            {protocolsLoading ? (
              <LinearProgress />
            ) : recentProtocols.length > 0 ? (
              <List>
                {recentProtocols.map((protocol) => (
                  <ListItem key={protocol.id} divider>
                    <ListItemIcon>
                      <ScienceIcon color="primary" />
                    </ListItemIcon>
                    <ListItemText
                      primary={protocol.title}
                      secondary={`Created ${new Date(protocol.created_at).toLocaleDateString()}`}
                    />
                    <Chip
                      label={protocol.is_public ? 'Public' : 'Private'}
                      size="small"
                      color={protocol.is_public ? 'success' : 'default'}
                    />
                  </ListItem>
                ))}
              </List>
            ) : (
              <Typography variant="body2" color="text.secondary" sx={{ textAlign: 'center', py: 2 }}>
                No protocols yet. Create your first protocol!
              </Typography>
            )}
            <Box sx={{ mt: 2 }}>
              <Button
                variant="outlined"
                size="small"
                onClick={() => navigate('/protocols')}
              >
                View All Protocols
              </Button>
            </Box>
          </Paper>
        </Grid>

        {/* Recent Analysis Tasks */}
        <Grid item xs={12} md={6}>
          <Paper sx={{ p: 2 }}>
            <Typography variant="h6" gutterBottom>
              Recent Analysis Tasks
            </Typography>
            {analysisLoading ? (
              <LinearProgress />
            ) : recentTasks.length > 0 ? (
              <List>
                {recentTasks.map((task) => (
                  <ListItem key={task.id} divider>
                    <ListItemIcon>
                      <AnalyticsIcon color="primary" />
                    </ListItemIcon>
                    <ListItemText
                      primary={task.name}
                      secondary={`${task.task_type} - ${task.status}`}
                    />
                    <Chip
                      label={task.status}
                      size="small"
                      color={
                        task.status === 'completed' ? 'success' :
                        task.status === 'processing' ? 'warning' :
                        task.status === 'failed' ? 'error' : 'default'
                      }
                    />
                  </ListItem>
                ))}
              </List>
            ) : (
              <Typography variant="body2" color="text.secondary" sx={{ textAlign: 'center', py: 2 }}>
                No analysis tasks yet. Upload data to get started!
              </Typography>
            )}
            <Box sx={{ mt: 2 }}>
              <Button
                variant="outlined"
                size="small"
                onClick={() => navigate('/analysis')}
              >
                View All Tasks
              </Button>
            </Box>
          </Paper>
        </Grid>
      </Grid>

      {/* Quick Actions */}
      <Paper sx={{ p: 3, mt: 3 }}>
        <Typography variant="h6" gutterBottom>
          Quick Actions
        </Typography>
        <Grid container spacing={2}>
          <Grid item xs={12} sm={6} md={3}>
            <Button
              variant="contained"
              fullWidth
              startIcon={<ScienceIcon />}
              onClick={() => navigate('/protocols')}
            >
              New Protocol
            </Button>
          </Grid>
          <Grid item xs={12} sm={6} md={3}>
            <Button
              variant="contained"
              fullWidth
              startIcon={<AnalyticsIcon />}
              onClick={() => navigate('/analysis')}
            >
              Upload Data
            </Button>
          </Grid>
          <Grid item xs={12} sm={6} md={3}>
            <Button
              variant="contained"
              fullWidth
              startIcon={<BarChartIcon />}
              onClick={() => navigate('/visualization')}
            >
              Create Chart
            </Button>
          </Grid>
          <Grid item xs={12} sm={6} md={3}>
            <Button
              variant="outlined"
              fullWidth
              startIcon={<TrendingUpIcon />}
              onClick={() => navigate('/analysis')}
            >
              View Results
            </Button>
          </Grid>
        </Grid>
      </Paper>
    </Container>
  );
};

export default Dashboard; 