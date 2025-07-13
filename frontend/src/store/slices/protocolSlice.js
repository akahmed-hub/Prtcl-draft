import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import axios from 'axios';

// Async thunks
export const fetchProtocols = createAsyncThunk(
  'protocols/fetchProtocols',
  async (_, { rejectWithValue }) => {
    try {
      const response = await axios.get('/api/v1/protocols/');
      return response.data;
    } catch (error) {
      return rejectWithValue(error.response?.data || 'Failed to fetch protocols');
    }
  }
);

export const generateProtocol = createAsyncThunk(
  'protocols/generateProtocol',
  async (protocolData, { rejectWithValue }) => {
    try {
      const response = await axios.post('/api/v1/protocols/generate/', protocolData);
      return response.data;
    } catch (error) {
      return rejectWithValue(error.response?.data || 'Failed to generate protocol');
    }
  }
);

export const createProtocol = createAsyncThunk(
  'protocols/createProtocol',
  async (protocolData, { rejectWithValue }) => {
    try {
      const response = await axios.post('/api/v1/protocols/', protocolData);
      return response.data;
    } catch (error) {
      return rejectWithValue(error.response?.data || 'Failed to create protocol');
    }
  }
);

export const updateProtocol = createAsyncThunk(
  'protocols/updateProtocol',
  async ({ id, data }, { rejectWithValue }) => {
    try {
      const response = await axios.put(`/api/v1/protocols/${id}/`, data);
      return response.data;
    } catch (error) {
      return rejectWithValue(error.response?.data || 'Failed to update protocol');
    }
  }
);

export const deleteProtocol = createAsyncThunk(
  'protocols/deleteProtocol',
  async (id, { rejectWithValue }) => {
    try {
      await axios.delete(`/api/v1/protocols/${id}/`);
      return id;
    } catch (error) {
      return rejectWithValue(error.response?.data || 'Failed to delete protocol');
    }
  }
);

const initialState = {
  protocols: [],
  currentProtocol: null,
  loading: false,
  error: null,
  generating: false,
};

const protocolSlice = createSlice({
  name: 'protocols',
  initialState,
  reducers: {
    clearError: (state) => {
      state.error = null;
    },
    setCurrentProtocol: (state, action) => {
      state.currentProtocol = action.payload;
    },
    clearCurrentProtocol: (state) => {
      state.currentProtocol = null;
    },
  },
  extraReducers: (builder) => {
    builder
      // Fetch protocols
      .addCase(fetchProtocols.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(fetchProtocols.fulfilled, (state, action) => {
        state.loading = false;
        state.protocols = action.payload.results || action.payload;
      })
      .addCase(fetchProtocols.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload;
      })
      
      // Generate protocol
      .addCase(generateProtocol.pending, (state) => {
        state.generating = true;
        state.error = null;
      })
      .addCase(generateProtocol.fulfilled, (state, action) => {
        state.generating = false;
        state.currentProtocol = action.payload;
      })
      .addCase(generateProtocol.rejected, (state, action) => {
        state.generating = false;
        state.error = action.payload;
      })
      
      // Create protocol
      .addCase(createProtocol.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(createProtocol.fulfilled, (state, action) => {
        state.loading = false;
        state.protocols.unshift(action.payload);
        state.currentProtocol = action.payload;
      })
      .addCase(createProtocol.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload;
      })
      
      // Update protocol
      .addCase(updateProtocol.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(updateProtocol.fulfilled, (state, action) => {
        state.loading = false;
        const index = state.protocols.findIndex(p => p.id === action.payload.id);
        if (index !== -1) {
          state.protocols[index] = action.payload;
        }
        state.currentProtocol = action.payload;
      })
      .addCase(updateProtocol.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload;
      })
      
      // Delete protocol
      .addCase(deleteProtocol.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(deleteProtocol.fulfilled, (state, action) => {
        state.loading = false;
        state.protocols = state.protocols.filter(p => p.id !== action.payload);
        if (state.currentProtocol?.id === action.payload) {
          state.currentProtocol = null;
        }
      })
      .addCase(deleteProtocol.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload;
      });
  },
});

export const { clearError, setCurrentProtocol, clearCurrentProtocol } = protocolSlice.actions;
export default protocolSlice.reducer; 