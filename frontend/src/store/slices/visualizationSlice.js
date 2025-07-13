import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import axios from 'axios';

// Async thunks
export const createVisualization = createAsyncThunk(
  'visualization/createVisualization',
  async (visualizationData, { rejectWithValue }) => {
    try {
      const response = await axios.post('/api/v1/visualization/', visualizationData);
      return response.data;
    } catch (error) {
      return rejectWithValue(error.response?.data || 'Failed to create visualization');
    }
  }
);

export const fetchVisualizations = createAsyncThunk(
  'visualization/fetchVisualizations',
  async (_, { rejectWithValue }) => {
    try {
      const response = await axios.get('/api/v1/visualization/');
      return response.data;
    } catch (error) {
      return rejectWithValue(error.response?.data || 'Failed to fetch visualizations');
    }
  }
);

export const updateVisualization = createAsyncThunk(
  'visualization/updateVisualization',
  async ({ id, data }, { rejectWithValue }) => {
    try {
      const response = await axios.put(`/api/v1/visualization/${id}/`, data);
      return response.data;
    } catch (error) {
      return rejectWithValue(error.response?.data || 'Failed to update visualization');
    }
  }
);

export const deleteVisualization = createAsyncThunk(
  'visualization/deleteVisualization',
  async (id, { rejectWithValue }) => {
    try {
      await axios.delete(`/api/v1/visualization/${id}/`);
      return id;
    } catch (error) {
      return rejectWithValue(error.response?.data || 'Failed to delete visualization');
    }
  }
);

const initialState = {
  visualizations: [],
  currentVisualization: null,
  loading: false,
  error: null,
  chartData: null,
  chartConfig: {
    type: 'bar',
    title: '',
    xAxis: { label: '', data: [] },
    yAxis: { label: '', data: [] },
    colors: ['#1976d2', '#dc004e', '#388e3c', '#f57c00'],
  },
};

const visualizationSlice = createSlice({
  name: 'visualization',
  initialState,
  reducers: {
    clearError: (state) => {
      state.error = null;
    },
    setCurrentVisualization: (state, action) => {
      state.currentVisualization = action.payload;
    },
    clearCurrentVisualization: (state) => {
      state.currentVisualization = null;
    },
    setChartData: (state, action) => {
      state.chartData = action.payload;
    },
    setChartConfig: (state, action) => {
      state.chartConfig = { ...state.chartConfig, ...action.payload };
    },
    updateChartConfig: (state, action) => {
      const { key, value } = action.payload;
      state.chartConfig[key] = value;
    },
  },
  extraReducers: (builder) => {
    builder
      // Create visualization
      .addCase(createVisualization.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(createVisualization.fulfilled, (state, action) => {
        state.loading = false;
        state.visualizations.unshift(action.payload);
        state.currentVisualization = action.payload;
      })
      .addCase(createVisualization.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload;
      })
      
      // Fetch visualizations
      .addCase(fetchVisualizations.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(fetchVisualizations.fulfilled, (state, action) => {
        state.loading = false;
        state.visualizations = action.payload.results || action.payload;
      })
      .addCase(fetchVisualizations.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload;
      })
      
      // Update visualization
      .addCase(updateVisualization.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(updateVisualization.fulfilled, (state, action) => {
        state.loading = false;
        const index = state.visualizations.findIndex(v => v.id === action.payload.id);
        if (index !== -1) {
          state.visualizations[index] = action.payload;
        }
        state.currentVisualization = action.payload;
      })
      .addCase(updateVisualization.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload;
      })
      
      // Delete visualization
      .addCase(deleteVisualization.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(deleteVisualization.fulfilled, (state, action) => {
        state.loading = false;
        state.visualizations = state.visualizations.filter(v => v.id !== action.payload);
        if (state.currentVisualization?.id === action.payload) {
          state.currentVisualization = null;
        }
      })
      .addCase(deleteVisualization.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload;
      });
  },
});

export const {
  clearError,
  setCurrentVisualization,
  clearCurrentVisualization,
  setChartData,
  setChartConfig,
  updateChartConfig,
} = visualizationSlice.actions;

export default visualizationSlice.reducer; 