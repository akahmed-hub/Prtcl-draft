import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import axios from 'axios';

// Async thunks
export const uploadDataFile = createAsyncThunk(
  'analysis/uploadDataFile',
  async (fileData, { rejectWithValue }) => {
    try {
      const formData = new FormData();
      formData.append('file', fileData.file);
      formData.append('name', fileData.name);
      formData.append('file_type', fileData.fileType);
      formData.append('description', fileData.description || '');
      
      const response = await axios.post('/api/v1/analysis/files/', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
      return response.data;
    } catch (error) {
      return rejectWithValue(error.response?.data || 'Failed to upload file');
    }
  }
);

export const createAnalysisTask = createAsyncThunk(
  'analysis/createAnalysisTask',
  async (taskData, { rejectWithValue }) => {
    try {
      const response = await axios.post('/api/v1/analysis/tasks/', taskData);
      return response.data;
    } catch (error) {
      return rejectWithValue(error.response?.data || 'Failed to create analysis task');
    }
  }
);

export const fetchAnalysisTasks = createAsyncThunk(
  'analysis/fetchAnalysisTasks',
  async (_, { rejectWithValue }) => {
    try {
      const response = await axios.get('/api/v1/analysis/tasks/');
      return response.data;
    } catch (error) {
      return rejectWithValue(error.response?.data || 'Failed to fetch analysis tasks');
    }
  }
);

export const fetchDataFiles = createAsyncThunk(
  'analysis/fetchDataFiles',
  async (_, { rejectWithValue }) => {
    try {
      const response = await axios.get('/api/v1/analysis/files/');
      return response.data;
    } catch (error) {
      return rejectWithValue(error.response?.data || 'Failed to fetch data files');
    }
  }
);

const initialState = {
  dataFiles: [],
  analysisTasks: [],
  currentTask: null,
  loading: false,
  uploading: false,
  error: null,
};

const analysisSlice = createSlice({
  name: 'analysis',
  initialState,
  reducers: {
    clearError: (state) => {
      state.error = null;
    },
    setCurrentTask: (state, action) => {
      state.currentTask = action.payload;
    },
    clearCurrentTask: (state) => {
      state.currentTask = null;
    },
  },
  extraReducers: (builder) => {
    builder
      // Upload data file
      .addCase(uploadDataFile.pending, (state) => {
        state.uploading = true;
        state.error = null;
      })
      .addCase(uploadDataFile.fulfilled, (state, action) => {
        state.uploading = false;
        state.dataFiles.unshift(action.payload);
      })
      .addCase(uploadDataFile.rejected, (state, action) => {
        state.uploading = false;
        state.error = action.payload;
      })
      
      // Create analysis task
      .addCase(createAnalysisTask.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(createAnalysisTask.fulfilled, (state, action) => {
        state.loading = false;
        state.analysisTasks.unshift(action.payload);
        state.currentTask = action.payload;
      })
      .addCase(createAnalysisTask.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload;
      })
      
      // Fetch analysis tasks
      .addCase(fetchAnalysisTasks.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(fetchAnalysisTasks.fulfilled, (state, action) => {
        state.loading = false;
        state.analysisTasks = action.payload.results || action.payload;
      })
      .addCase(fetchAnalysisTasks.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload;
      })
      
      // Fetch data files
      .addCase(fetchDataFiles.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(fetchDataFiles.fulfilled, (state, action) => {
        state.loading = false;
        state.dataFiles = action.payload.results || action.payload;
      })
      .addCase(fetchDataFiles.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload;
      });
  },
});

export const { clearError, setCurrentTask, clearCurrentTask } = analysisSlice.actions;
export default analysisSlice.reducer; 